# Generated by Django 5.1.4 on 2024-12-07 05:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('App', '0006_remove_student_name_remove_teacher_name'),
    ]

    operations = [
        migrations.AddField(
            model_name='student',
            name='name',
            field=models.CharField(default='Default Name', max_length=100),
        ),
        migrations.AddField(
            model_name='teacher',
            name='name',
            field=models.CharField(default='Default Name', max_length=100),
            preserve_default=False,
        ),
        migrations.DeleteModel(
            name='CustomUser',
        ),
    ]