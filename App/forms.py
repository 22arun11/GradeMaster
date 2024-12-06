from django.forms import modelformset_factory
from django import forms
from .models import Marks, Student, Semester

class MarksForm(forms.ModelForm):
    class Meta:
        model = Marks
        fields = ['subject', 'marks', 'grade']

class StudentSelectForm(forms.Form):
    student = forms.ModelChoiceField(queryset=Student.objects.all(), label="Select Student")
    semester = forms.ModelChoiceField(queryset=Semester.objects.all(), label="Select Semester")
MarksFormSet = modelformset_factory(Marks, form=MarksForm, extra=0)