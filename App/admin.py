from django.contrib import admin
from django.shortcuts import render, redirect
from django.urls import path
from .models import Course, Semester, Subject, Student, Marks, Teacher
from .forms import SubjectBulkCreateForm, SubjectAdminForm
   

class SubjectAdmin(admin.ModelAdmin):
    
    # actions = ['bulk_create_subjects']
    list_display = ('name', 'course', 'semester', 'credits')
    fields = ('name', 'course', 'semester', 'credits')
    form = SubjectAdminForm
    class Media:
        js = ('admin/subject_admin.js',)
    # def bulk_create_subjects(self, request, queryset):
    #     if 'apply' in request.POST:
    #         form = SubjectBulkCreateForm(request.POST)
    #         if form.is_valid():
    #             semester = form.cleaned_data['semester']
    #             subject_names = form.cleaned_data['subject_names'].split(',')
    #             for name in subject_names:
    #                 Subject.objects.create(course=semester.course, semester=semester, name=name.strip())
    #             self.message_user(request, "Subjects created successfully")
    #             return redirect(request.get_full_path())
    #     else:
    #         form = SubjectBulkCreateForm()

    #     return render(request, 'admin/subject_bulk_create.html', {'form': form})

    # bulk_create_subjects.short_description = "Bulk create subjects"

admin.site.register(Subject, SubjectAdmin)
admin.site.register(Course)
admin.site.register(Semester)
admin.site.register(Student)
admin.site.register(Marks)
admin.site.register(Teacher)