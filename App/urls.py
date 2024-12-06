from django.urls import path
from .views import RegisterView, LoginView, login_view, register_view, student_records_view, teacher_records_view, enter_marks
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
]