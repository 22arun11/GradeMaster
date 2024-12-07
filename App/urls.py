from django.urls import path
from .views import RegisterView, LoginView, login_view, register_view, student_records_view, teacher_records_view, enter_marks, view_consolidated_marksheet, view_marksheet, get_semesters, download_marksheet_pdf, download_consolidated_marksheet_pdf, view_cumulative_marksheet,view_strengths_weaknesses
from rest_framework_simplejwt.views import TokenRefreshView
from .views import teacher_dashboard, view_student_marksheet
urlpatterns = [
    path('api/register/', RegisterView.as_view(), name='register'),
    path('api/login/', LoginView.as_view(), name='login'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('login/', login_view, name='login'),
    path('register/', register_view, name='register'),
    path('student-records/', student_records_view, name='student-records'),
    path('teacher-records/', teacher_records_view, name='teacher-records'),
    path('enter-marks/', enter_marks, name='enter-marks'),
    path('view-marksheet/', view_marksheet, name='view-marksheet'),
    path('view-cumulative-marksheet/', view_cumulative_marksheet, name='view-cumulative-marksheet'),
    path('admin/get_semesters/', get_semesters, name='get_semesters'),
    path('download_marksheet_pdf/<int:student_id>/<int:semester_number>/', download_marksheet_pdf, name='download_marksheet_pdf'),
    path('download_consolidated_marksheet_pdf/<int:student_id>/', download_consolidated_marksheet_pdf, name='download_consolidated_marksheet_pdf'),
    path('view_marksheet/', view_marksheet, name='view_marksheet'),
    path('view_consolidated_marksheet/', view_consolidated_marksheet, name='view_consolidated_marksheet'),
    path('view_strengths_weaknesses/', view_strengths_weaknesses, name='view_strengths_weaknesses'),
    path('teacher_dashboard/', teacher_dashboard, name='teacher_dashboard'),
    path('view_student_marksheet/<int:student_id>/', view_student_marksheet, name='view_student_marksheet'),
]