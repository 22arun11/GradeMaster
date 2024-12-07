from rest_framework import generics, permissions
from django.contrib.auth.models import User
from .serializers import UserSerializer, RegisterSerializer
from rest_framework.permissions import AllowAny
from rest_framework_simplejwt.views import TokenObtainPairView
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from .models import Marks, Student, Subject, Semester
from .serializers import MarksSerializer
from django.contrib.auth.decorators import login_required
from .forms import MarksFormSet, StudentSelectForm
from django.http import JsonResponse
from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse
from django.template.loader import get_template
from xhtml2pdf import pisa
from django.utils import timezone
from io import BytesIO
import google.generativeai as genai
import os
import requests
import re

@login_required
def teacher_dashboard(request):
    # if not hasattr(request.user, 'teacher'):
    #     return redirect('login')
    students = Student.objects.all()
    return render(request, 'teacher_dashboard.html', {'students': students})

def view_student_marksheet(request, student_id):
    
    student = get_object_or_404(Student, id=student_id)
    marks = Marks.objects.filter(student=student)
    total_grade_points = 0
    total_credits = 0
    for mark in marks:
        grade_point = calculate_grade_point(mark.grade)
        total_grade_points += grade_point * mark.subject.credits
        total_credits += mark.subject.credits

    sgpa = total_grade_points / total_credits if total_credits > 0 else 0

    all_marks = Marks.objects.filter(student=student)
    total_cumulative_grade_points = 0
    total_cumulative_credits = 0
    for mark in all_marks:
        grade_point = calculate_grade_point(mark.grade)
        total_cumulative_grade_points += grade_point * mark.subject.credits
        total_cumulative_credits += mark.subject.credits

    cgpa = total_cumulative_grade_points / total_cumulative_credits if total_cumulative_credits > 0 else 0

    context = {
        'student': student,
        'marks': marks,
        'sgpa': sgpa,
        'cgpa': cgpa,
        'total_credits': total_cumulative_credits,
        'semester': marks.first().subject.semester.number if marks.exists() else None,
    }
    return render(request, 'view_marksheet.html', context)
    

def view_strengths_weaknesses(request):
    student = get_object_or_404(Student, user=request.user)
    marks = Marks.objects.filter(student=student)

    # Calculate strengths and weaknesses
    subject_scores = {}
    for mark in marks:
        if mark.subject.name not in subject_scores:
            subject_scores[mark.subject.name] = []
        subject_scores[mark.subject.name].append(mark.marks)

    strengths = sorted(subject_scores.items(), key=lambda x: sum(x[1]) / len(x[1]), reverse=True)[:3]
    weaknesses = sorted(subject_scores.items(), key=lambda x: sum(x[1]) / len(x[1]))[:3]

    # Configure the Google Generative AI API
    gemini_api_key = os.getenv('GEMINI_API_KEY')
    genai.configure(api_key=gemini_api_key)
    model = genai.GenerativeModel("gemini-1.5-flash")

    # Generate recommendations using the Google Generative AI API
    recommendations = []
    for subject, _ in strengths:
        prompt = f"Provide career and higher study recommendations for a student excelling in {subject}."
        try:
            response = model.generate_content(prompt)
            formatted_response = response.text.replace('\n', '<br>')
            # Replace **text** with <strong>text</strong>
            formatted_response = re.sub(r'\*\*(.*?)\*\*', r'<strong>\1</strong>', formatted_response)
            # Replace *text* with <em>text</em>
            formatted_response = re.sub(r'\*(.*?)\*', r'<em>\1</em>', formatted_response)
            recommendations.append(formatted_response)
        except Exception as e:
            print(f"Exception occurred while fetching recommendations for {subject}: {e}")  # Debugging step
            recommendations.append(f"Consider exploring career opportunities in {subject} related fields.")

    context = {
        'student': student,
        'strengths': strengths,
        'weaknesses': weaknesses,
        'recommendations': recommendations,
    }
    return render(request, 'view_strengths_weaknesses.html', context)

def render_to_pdf(template_src, context_dict):
    template = get_template(template_src)
    html = template.render(context_dict)
    result = BytesIO()
    pdf = pisa.pisaDocument(BytesIO(html.encode("UTF-8")), result)
    if not pdf.err:
        return HttpResponse(result.getvalue(), content_type='application/pdf')
    return None

def download_marksheet_pdf(request, student_id, semester_number):
    student = get_object_or_404(Student, id=student_id)
    semester = get_object_or_404(Semester, number=semester_number, course=student.course)
    marks = Marks.objects.filter(student=student, subject__semester=semester)

    total_grade_points = 0
    total_subjects = 0
    for mark in marks:
        total_grade_points += calculate_grade_point(mark.grade)
        total_subjects += 1

    sgpa = total_grade_points / total_subjects if total_subjects > 0 else 0

    all_marks = Marks.objects.filter(student=student, subject__semester__number__lte=semester.number)
    total_cumulative_grade_points = 0
    total_cumulative_subjects = 0
    for mark in all_marks:
        total_cumulative_grade_points += calculate_grade_point(mark.grade)
        total_cumulative_subjects += 1

    cgpa = total_cumulative_grade_points / total_cumulative_subjects if total_cumulative_subjects > 0 else 0

    context = {
        'student': student,
        'semester': semester.number,
        'marks': marks,
        'sgpa': sgpa,
        'cgpa': cgpa,
        'date': timezone.now().strftime('%Y-%m-%d'),
    }
    pdf = render_to_pdf('view_marksheet.html', context)
    return HttpResponse(pdf, content_type='application/pdf')

def download_consolidated_marksheet_pdf(request, student_id):
    student = get_object_or_404(Student, id=student_id)
    all_marks = Marks.objects.filter(student=student)

    total_cumulative_grade_points = 0
    total_cumulative_credits = 0
    for mark in all_marks:
        grade_point = calculate_grade_point(mark.grade)
        total_cumulative_grade_points += grade_point * mark.subject.credits
        total_cumulative_credits += mark.subject.credits

    cgpa = total_cumulative_grade_points / total_cumulative_credits if total_cumulative_credits > 0 else 0

    context = {
        'student': student,
        'marks': all_marks,
        'cgpa': cgpa,
        'date': timezone.now().strftime('%Y-%m-%d'),
    }
    pdf = render_to_pdf('view_consolidated_marksheet.html', context)
    return HttpResponse(pdf, content_type='application/pdf')

class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    permission_classes = (AllowAny,)
    serializer_class = RegisterSerializer

class LoginView(TokenObtainPairView):
    permission_classes = (AllowAny,)


def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        role = request.POST['role']
        if role == "teacher":
            role = True 
        else: role = False
        user = authenticate(request, username=username, password=password, is_staff=role)
        if user is not None and not role:
            login(request, user)
            return redirect('view-marksheet')
        elif role:
            return redirect('teacher_dashboard')
        else:
            return render(request, 'login.html', {'error': 'Invalid credentials'})
    return render(request, 'login.html')

def register_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        email = request.POST['email']
        password1 = request.POST['password1']
        password2 = request.POST['password2']
        role = request.POST['role']
        if password1 == password2:
            password = password1
        if role == "teacher":
            role = True 
        else: role = False
        user = User.objects.create_user(username, email, password, is_staff=role)
        return redirect('login')
    return render(request, 'register.html')

class StudentRecordsView(generics.ListAPIView):
    serializer_class = MarksSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Marks.objects.filter(student__user=self.request.user)

class TeacherRecordsView(generics.ListAPIView):
    serializer_class = MarksSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Marks.objects.all()

@login_required
def student_records_view(request):
    records = Marks.objects.filter(student__user=request.user)
    return render(request, 'student_records.html', {'records': records})

@login_required
def teacher_records_view(request):
    records = Marks.objects.all()
    return render(request, 'teacher_records.html', {'records': records})

# from django.shortcuts import render, redirect
# from django.forms.models import modelformset_factory
# from .forms import MarksForm, SectionSelectForm, SubjectSelectForm
# from .models import Student, Marks, Subject, Semester, Course

# def enter_marks(request):
#     if request.method == 'POST':
#         section_form = SectionSelectForm(request.POST)
#         subject_form = SubjectSelectForm(request.POST)
#         if section_form.is_valid() and subject_form.is_valid():
#             course = section_form.cleaned_data['course']
#             semester = section_form.cleaned_data['semester']
#             subject = subject_form.cleaned_data['subject']
#             students = Student.objects.filter(course=course)
            
#             # Create a formset with all students for the selected subject
#             initial_data = []
#             for student in students:
#                 marks = Marks.objects.filter(student=student, subject=subject).first()
#                 if marks:
#                     initial_data.append({'student': student, 'marks': marks.marks, 'grade': marks.grade})
#                 else:
#                     initial_data.append({'student': student})

#             MarksFormSet = modelformset_factory(Marks, form=MarksForm, extra=len(students))
#             formset = MarksFormSet(queryset=Marks.objects.none(), initial=initial_data)

#             if 'save' in request.POST:
#                 formset = MarksFormSet(request.POST)
#                 if formset.is_valid():
#                     for form in formset:
#                         marks = form.save(commit=True)
#                         marks.subject = subject
#                         marks.student = Student.objects.get(id=form.cleaned_data['student'])
#                         marks.save()
#                     return redirect('enter-marks')
#         else:
#             formset = None
#     else:
#         section_form = SectionSelectForm()
#         subject_form = SubjectSelectForm()
#         formset = None

#     return render(request, 'enter_marks.html', {'section_form': section_form, 'subject_form': subject_form, 'formset': formset})

# def calculate_grade_point(grade):
#     if grade == 'O':
#         return 10
#     elif grade == 'A+':
#         return 9.5
#     elif grade == 'A':
#         return 9
#     elif grade == 'B+':
#         return 8
#     elif grade == 'B':
#         return 7
#     elif grade == 'C':
#         return 6
#     elif grade == 'P':
#         return 5
#     else:
#         return 0

# def view_marksheet(request):
#     if request.method == 'POST':
#         student_form = StudentSelectForm(request.POST)
#         if student_form.is_valid():
#             student = student_form.cleaned_data['student']
#             semester = student_form.cleaned_data['semester']
#             marks = Marks.objects.filter(student=student, subject__semester=semester)

#             total_grade_points = 0
#             total_subjects = 0
#             for mark in marks:
#                 total_grade_points += calculate_grade_point(mark.grade)
#                 total_subjects += 1

#             sgpa = total_grade_points / total_subjects if total_subjects > 0 else 0

#             # Calculate CGPA
#             all_marks = Marks.objects.filter(student=student, subject__semester__number__lte=semester.number)
#             total_cumulative_grade_points = 0
#             total_cumulative_subjects = 0
#             for mark in all_marks:
#                 total_cumulative_grade_points += calculate_grade_point(mark.grade)
#                 total_cumulative_subjects += 1

#             cgpa = total_cumulative_grade_points / total_cumulative_subjects if total_cumulative_subjects > 0 else 0

#             return render(request, 'view_marksheet.html', {'marks': marks, 'student': student, 'semester': semester, 'sgpa': sgpa, 'cgpa': cgpa})
#     else:
#         student_form = StudentSelectForm()

#     return render(request, 'select_student.html', {'student_form': student_form})


from django.shortcuts import render, redirect
from django.forms.models import modelformset_factory
from .forms import MarksForm, SectionSelectForm, SubjectSelectForm, StudentSelectForm
from .models import Student, Marks, Subject, Semester, Course
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User

def get_semesters(request):
    course_id = request.GET.get('course_id')
    semesters = Semester.objects.filter(course_id=course_id).values('id', 'number')
    return JsonResponse({'semesters': list(semesters)})


from django.shortcuts import render, get_object_or_404
from django.utils import timezone
from .models import Student, Semester, Marks

def calculate_grade_point(grade):
    if grade == 'O':
        return 10
    elif grade == 'A+':
        return 9.5
    elif grade == 'A':
        return 9
    elif grade == 'B+':
        return 8
    elif grade == 'B':
        return 7
    elif grade == 'C':
        return 6
    elif grade == 'P':
        return 5
    else:
        return 0

def view_marksheet(request):
    student = Student.objects.get(user=request.user)
    if request.method == 'POST':
        semester = request.POST.get('semester')
        marks = Marks.objects.filter(student=student, subject__semester__number=semester)

        total_grade_points = 0
        total_credits = 0
        for mark in marks:
            grade_point = calculate_grade_point(mark.grade)
            total_grade_points += grade_point * mark.subject.credits
            total_credits += mark.subject.credits

        sgpa = total_grade_points / total_credits if total_credits > 0 else 0

        # Calculate CGPA and total credits
        all_marks = Marks.objects.filter(student=student, subject__semester__number__lte=semester)
        total_cumulative_grade_points = 0
        total_cumulative_credits = 0
        for mark in all_marks:
            grade_point = calculate_grade_point(mark.grade)
            total_cumulative_grade_points += grade_point * mark.subject.credits
            total_cumulative_credits += mark.subject.credits

        cgpa = total_cumulative_grade_points / total_cumulative_credits if total_cumulative_credits > 0 else 0

        context = {
            'marks': marks,
            'student': student,
            'semester': semester,
            'sgpa': sgpa,
            'cgpa': cgpa,
            'semester_credits': total_credits,
            'total_credits': total_cumulative_credits,
            'date': timezone.now().strftime('%Y-%m-%d'),
        }
        return render(request, 'view_marksheet.html', context)
    else:
        semesters = Semester.objects.filter(course=student.course)
        return render(request, 'select_semester.html', {'semesters': semesters})
    
def view_consolidated_marksheet(request):
    student = get_object_or_404(Student, user=request.user)
    semesters = Semester.objects.filter(course=student.course)

    consolidated_data = []
    total_cumulative_grade_points = 0
    total_cumulative_credits = 0

    for semester in semesters:
        marks = Marks.objects.filter(student=student, subject__semester=semester)
        total_grade_points = 0
        total_credits = 0
        for mark in marks:
            grade_point = calculate_grade_point(mark.grade)
            total_grade_points += grade_point * mark.subject.credits
            total_credits += mark.subject.credits

        if total_credits > 0:
            sgpa = total_grade_points / total_credits
            total_cumulative_grade_points += total_grade_points
            total_cumulative_credits += total_credits

            consolidated_data.append({
                'semester': semester.number,
                'total_credits': total_credits,
                'sgpa': sgpa,
            })

    cgpa = total_cumulative_grade_points / total_cumulative_credits if total_cumulative_credits > 0 else 0

    context = {
        'student': student,
        'consolidated_data': consolidated_data,
        'cgpa': cgpa,
        'date': timezone.now().strftime('%Y-%m-%d'),
        'total_cumulative_credits': total_cumulative_credits,
    }
    return render(request, 'view_consolidated_marksheet.html', context)

def download_consolidated_marksheet_pdf(request, student_id):
    student = get_object_or_404(Student, id=student_id)
    semesters = Semester.objects.filter(course=student.course)

    consolidated_data = []
    total_cumulative_grade_points = 0
    total_cumulative_credits = 0

    for semester in semesters:
        marks = Marks.objects.filter(student=student, subject__semester=semester)
        total_grade_points = 0
        total_credits = 0
        for mark in marks:
            grade_point = calculate_grade_point(mark.grade)
            total_grade_points += grade_point * mark.subject.credits
            total_credits += mark.subject.credits

        sgpa = total_grade_points / total_credits if total_credits > 0 else 0
        total_cumulative_grade_points += total_grade_points
        total_cumulative_credits += total_credits

        consolidated_data.append({
            'semester': semester.number,
            'total_credits': total_credits,
            'sgpa': sgpa,
        })

    cgpa = total_cumulative_grade_points / total_cumulative_credits if total_cumulative_credits > 0 else 0

    context = {
        'student': student,
        'consolidated_data': consolidated_data,
        'cgpa': cgpa,
        'date': timezone.now().strftime('%Y-%m-%d'),
    }
    pdf = render_to_pdf('view_consolidated_marksheet_pdf.html', context)
    return HttpResponse(pdf, content_type='application/pdf')

@login_required
def enter_marks(request):
    if not request.user.is_staff:
        return redirect('view-marksheet')

    if request.method == 'POST':
        section_form = SectionSelectForm(request.POST)
        subject_form = SubjectSelectForm(request.POST)
        if section_form.is_valid() and subject_form.is_valid():
            course = section_form.cleaned_data['course']
            semester = section_form.cleaned_data['semester']
            subject = subject_form.cleaned_data['subject']
            students = Student.objects.filter(course=course)
            
            # Create a formset with all students for the selected subject
            initial_data = []
            for student in students:
                marks = Marks.objects.filter(student=student, subject=subject).first()
                if marks:
                    initial_data.append({'student': student.id, 'marks': marks.marks, 'grade': marks.grade})
                else:
                    initial_data.append({'student': student.id})

            MarksFormSet = modelformset_factory(Marks, form=MarksForm, extra=len(students))
            formset = MarksFormSet(queryset=Marks.objects.none(), initial=initial_data)

            if 'save' in request.POST:
                formset = MarksFormSet(request.POST)
                if formset.is_valid():
                    for form in formset:
                        marks = form.save(commit=False)
                        marks.subject = subject
                        marks.student = Student.objects.get(id=form.cleaned_data['student'])
                        marks.save()
                    return redirect('enter-marks')
        else:
            formset = None
    else:
        section_form = SectionSelectForm()
        subject_form = SubjectSelectForm()
        formset = None

    return render(request, 'enter_marks.html', {'section_form': section_form, 'subject_form': subject_form, 'formset': formset})


def view_cumulative_marksheet(request):
    if request.method == 'POST':
        student_form = StudentSelectForm(request.POST)
        if student_form.is_valid():
            student = student_form.cleaned_data['student']
            semester = student_form.cleaned_data['semester']
            marks = Marks.objects.filter(student=student, subject__semester__number__lte=semester.number)
            return render(request, 'view_cumulative_marksheet.html', {'marks': marks, 'student': student, 'semester': semester})
    else:
        student_form = StudentSelectForm()

    return render(request, 'select_student.html', {'student_form': student_form})