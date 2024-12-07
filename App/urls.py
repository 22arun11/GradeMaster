from django.urls import path
from .views import RegisterView, LoginView, login_view, register_view, student_records_view, teacher_records_view, enter_marks, view_cumulative_marksheet, view_marksheet, get_semesters, download_marksheet_pdf, download_consolidated_marksheet_pdf
from rest_framework_simplejwt.views import TokenRefreshView

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
]