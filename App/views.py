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
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('view-marksheet')
        else:
            return render(request, 'login.html', {'error': 'Invalid credentials'})
    return render(request, 'login.html')

def register_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']
        user = User.objects.create_user(username, email, password)
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

@login_required
def view_marksheet(request):
    student = Student.objects.get(user=request.user)
    if request.method == 'POST':
        semester = request.POST.get('semester')
        marks = Marks.objects.filter(student=student, subject__semester__number=semester)

        total_grade_points = 0
        total_subjects = 0
        for mark in marks:
            total_grade_points += calculate_grade_point(mark.grade)
            total_subjects += 1

        sgpa = total_grade_points / total_subjects if total_subjects > 0 else 0

        # Calculate CGPA
        all_marks = Marks.objects.filter(student=student, subject__semester__number__lte=semester)
        total_cumulative_grade_points = 0
        total_cumulative_subjects = 0
        for mark in all_marks:
            total_cumulative_grade_points += calculate_grade_point(mark.grade)
            total_cumulative_subjects += 1

        cgpa = total_cumulative_grade_points / total_cumulative_subjects if total_cumulative_subjects > 0 else 0

        return render(request, 'view_marksheet.html', {'marks': marks, 'student': student, 'semester': semester, 'sgpa': sgpa, 'cgpa': cgpa})
    else:
        semesters = Semester.objects.filter(course=student.course)
        return render(request, 'select_semester.html', {'semesters': semesters})

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