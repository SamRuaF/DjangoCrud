from django.contrib import admin
from django.urls import path
from tasks import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.home, name='home'),
    path('/signup/', views.signup, name='Sesion'),
    path('tasks/', views.tasks, name='tasks'),
    path('tasks/completed', views.tasks_completed, name='tasks_completed'),
    path('logout/', views.signout, name='logout'),
    path('/signin/', views.signin, name='signin'),
    path('tasks/create/', views.create_tasks, name='create_task'),
    path('tasks/<int:task_id>/', views.task_detail, name='task_detail'),
    path('tasks/<int:task_id>/completed', views.completed_task, name='completed_task'),
    path('tasks/<int:task_id>/completed', views.completed_task, name='completed_task'),
    path('tasks/<int:task_id>/delete', views.delete_task, name='delete_task')


]

handler404 = 'tasks.views.handling_404'