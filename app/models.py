from django.db import models
from django.contrib.auth.models import User

class TgUser(models.Model):
    tg = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
    first_name = models.CharField(max_length=20, null=True, blank=True)
    last_name = models.CharField(max_length=20, null=True, blank=True)
    username = models.CharField(max_length=20, null=True, blank=True)
    language_code = models.CharField(max_length=2, null=True, blank=True)

    def __str__(self):
        return self.first_name

class PsychologistBotUIState(models.Model):
    tg = models.OneToOneField(TgUser, on_delete=models.CASCADE, primary_key=True)
    authorized = models.BooleanField(default=False)
    last_button_pressed = models.CharField(max_length=30)

    def __str__(self):
        return self.last_button_pressed

class PatientsBotUIState(models.Model):
    tg = models.OneToOneField(TgUser, on_delete=models.CASCADE, primary_key=True)
    patient_info_flag = models.BooleanField(default=False)
    appointment_type = models.CharField(max_length=20, null=True, blank=True)
    problem = models.CharField(max_length=80, null=True, blank=True)
    first_name = models.CharField(max_length=20, null=True, blank=True)
    last_name = models.CharField(max_length=20, null=True, blank=True)
    telephone_number = models.CharField(max_length=20, null=True, blank=True)
    email = models.CharField(max_length=20, null=True, blank=True)
    experience = models.CharField(max_length=20, null=True, blank=True)
    last_button_pressed = models.CharField(max_length=30)

    def __str__(self):
        return self.last_button_pressed

class Session(models.Model):

    session_id = models.AutoField(primary_key=True, default=0)
    patient_id = models.ForeignKey('TgUser', on_delete=models.CASCADE, related_name='+', null=True, blank=True)
    psychologist_id = models.ForeignKey('TgUser', on_delete=models.CASCADE, null=True, blank=True, related_name='+')
    time = models.DateField( null=True, blank=True)

    appointment_type = models.CharField(max_length=20, null=True, blank=True)
    problem = models.CharField(max_length=80, null=True, blank=True)
    first_name = models.CharField(max_length=20, null=True, blank=True)
    last_name = models.CharField(max_length=20, null=True, blank=True)
    telephone_number = models.CharField(max_length=20, null=True, blank=True)
    email = models.CharField(max_length=20, null=True, blank=True)
    experience = models.CharField(max_length=20, null=True, blank=True)
