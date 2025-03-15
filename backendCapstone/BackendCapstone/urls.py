from django.contrib import admin
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from Capstone import views

urlpatterns = [
    path('logout/', views.logout, name='logout'),
    path('admin/', admin.site.urls),
    path('undo_student/<int:student_id>/', views.undo_student, name='undo_student'),
    path('adminPanel/', views.adminPanel, name='adminPanel'),
    path('teacherPanel/', views.teacherPanel, name='teacherPanel'),
    path('course/', views.course, name='course'),
    path('teacherCourses/', views.teacherCourses, name='teacherCourses'),
    path('feedback/', views.feedback, name='feedback'),
    path('', views.loginForm, name='loginForm'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('dashboardAdmin/', views.dashboardAdmin, name='dashboardAdmin'),
    path('dashboardTeacher/', views.dashboardTeacher, name='dashboardTeacher'),
    path('result/', views.result, name='result'),
    path('add_to_list/', views.add_to_list, name='add_to_list'),
    path('exploreCourses/', views.exploreCourses, name='exploreCourses'),
    path('generate-student-id/', views.generate_student_id, name='generate_student_id'),
    path('update_student_status/', views.update_student_status, name='update_student_status'),
    path('approved_students/', views.approved_students, name='approved_students'),
    path('approved_studentsDeclined/', views.approved_studentsDeclined, name='approved_studentsDeclined'),
    path('fetch-students/', views.fetch_students, name='fetch_students'),
    path('fetch-studentsDeclined/', views.fetch_studentsDeclined, name='fetch_studentsDeclined'),
    path('recommend_courses/<int:student_id>/', views.recommend_courses, name='recommend_courses'),
    path('setting/', views.setting, name='setting'),
    path('adminSetting/', views.adminSetting, name='adminSetting'),
    path('delete_teacher/', views.delete_teacher, name='delete_teacher'),
    path('send-otp/', views.send_otp, name='send_otp'),
    path('reset-password/', views.reset_password, name='reset_password'),
    path('delete_student/', views.delete_student, name='delete_student'),
    path('get-courses/', views.get_courses_by_college, name='get_courses'),
]

# ✅ Serve media files during development
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
