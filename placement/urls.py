from django.urls import path
from django.contrib.auth import views as auth_views
from . import views
 

urlpatterns = [
    path('register/', views.register, name='register'),
    path('login/', views.user_login, name='login'),
    path('logout/', views.user_logout, name='logout'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('upload-report/', views.upload_report, name='upload_report'),
    path('student-info/', views.student_info_view, name='student_info'),
    path('', views.homepage, name='homepage'),
    path('submit-evaluation/', views.submit_evaluation, name='submit_evaluation'),
    path('get-students-by-company/', views.get_students_by_company, name='get_students_by_company'),
    
    path('eval-login/', views.company_login, name='company_login'),

    


    path('password_reset/', auth_views.PasswordResetView.as_view(template_name='registration/password_reset_form.html'), name='password_reset'),
    path('password_reset/done/', auth_views.PasswordResetDoneView.as_view(template_name='registration/password_reset_done.html'), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(template_name='registration/password_reset_confirm.html'), name='password_reset_confirm'),
    path('reset/done/', auth_views.PasswordResetCompleteView.as_view(template_name='registration/password_reset_complete.html'), name='password_reset_complete'),


]