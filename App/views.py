from rest_framework import generics, permissions
from django.contrib.auth.models import User
from .serializers import UserSerializer, RegisterSerializer
from rest_framework.permissions import AllowAny
from rest_framework_simplejwt.views import TokenObtainPairView
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from .models import Marks, Student, Subject
from .serializers import MarksSerializer
from django.contrib.auth.decorators import login_required
from .forms import MarksFormSet, StudentSelectForm

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
            return redirect('student-records')
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

from django.shortcuts import render, redirect
from django.forms.models import modelformset_factory
from .forms import MarksForm, StudentSelectForm
from .models import Student, Marks, Subject, Semester

def enter_marks(request):
    MarksFormSet = modelformset_factory(Marks, form=MarksForm, extra=0)

    if request.method == 'POST':
        student_form = StudentSelectForm(request.POST)
        if student_form.is_valid():
            student = student_form.cleaned_data['student']
            semester = student_form.cleaned_data['semester']
            subjects = Subject.objects.filter(course=student.course, semester=semester)

            # Create a formset with all subjects for the selected semester
            MarksFormSet = modelformset_factory(Marks, form=MarksForm, extra=subjects.count())
            formset = MarksFormSet(queryset=Marks.objects.filter(student=student, subject__in=subjects))

            if 'save' in request.POST:
                formset = MarksFormSet(request.POST, queryset=Marks.objects.filter(student=student, subject__in=subjects))
                if formset.is_valid():
                    for form in formset:
                        marks = form.save(commit=False)
                        marks.student = student
                        marks.save()
                    return redirect('enter-marks')  # Redirect to the same page or another existing URL pattern
        else:
            formset = MarksFormSet(queryset=Marks.objects.none())
    else:
        student_form = StudentSelectForm()
        formset = None

    return render(request, 'enter_marks.html', {'student_form': student_form, 'formset': formset})