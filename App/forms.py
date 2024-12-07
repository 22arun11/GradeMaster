from django.forms import modelformset_factory
from django import forms
from .models import Marks, Student, Subject, Semester, Course
from django import forms
from .models import Subject, Semester
from django import forms
from .models import Subject, Semester

class SubjectAdminForm(forms.ModelForm):
    class Meta:
        model = Subject
        fields = ['course', 'semester', 'name']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if 'course' in self.data:
            try:
                course_id = int(self.data.get('course'))
                self.fields['semester'].queryset = Semester.objects.filter(course_id=course_id).order_by('number')
            except (ValueError, TypeError):
                pass  # invalid input from the client; ignore and fallback to empty Semester queryset
        elif self.instance.pk:
            self.fields['semester'].queryset = self.instance.course.semester_set.order_by('number')
            
class SubjectBulkCreateForm(forms.Form):
    semester = forms.ModelChoiceField(queryset=Semester.objects.all(), label="Select Semester")
    subject_count = forms.IntegerField(label="Number of Subjects", min_value=1)
    subject_names = forms.CharField(widget=forms.Textarea, help_text="Enter subject names separated by commas")
    
class MarksForm(forms.ModelForm):
    # student = forms.ModelChoiceField(queryset=Student.objects.all(), widget=forms.HiddenInput())

    class Meta:
        model = Marks
        fields = [ 'marks', 'grade']

class SectionSelectForm(forms.Form):
    course = forms.ModelChoiceField(queryset=Course.objects.all(), label="Select Course")
    semester = forms.ModelChoiceField(queryset=Semester.objects.all(), label="Select Semester")

class SubjectSelectForm(forms.Form):
    subject = forms.ModelChoiceField(queryset=Subject.objects.all(), label="Select Subject")

class StudentSelectForm(forms.Form):
    student = forms.ModelChoiceField(queryset=Student.objects.all(), label="Select Student")
    semester = forms.ModelChoiceField(queryset=Semester.objects.all(), label="Select Semester")
MarksFormSet = modelformset_factory(Marks, form=MarksForm, extra=0)