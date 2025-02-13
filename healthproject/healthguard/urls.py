from django.urls import path
from . import views


urlpatterns =[
    path('', views.home, name='home'),
    path('diagnosis/', views.diagnosis, name='diagnosis' ),
   path('patient/<int:patient_id>/',views.patient_detail, name='patient_detail'),
   path('voice-diagnosis/', views.voice_sti_prediction, name='voice_sti_prediction'),
   path("patient/<int:patient_id>/update/", views.update_patient_symptoms, name="update_patient_symptoms"),
]