from django.urls import path

from . import views

app_name = 'web_admin'

urlpatterns = [
    path('', views.index, name='index'),
    path('sessions/', views.sessions_list, name='sessions_list'),
    path('detail/<int:session_id>/', views.session_detail, name='session_detail'),
    path('create/', views.session_create, name='session_create'),
    path('patient/<int:patient_id>/', views.patient, name='patient'),
    path('session/<int:pk>/edit', views.session_edit, name='session_edit'),
]
