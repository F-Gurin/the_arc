# import datetime
from datetime import date
from django.db import models

from django.contrib.auth.models import AbstractUser
# from django.core.validators import MinValueValidator
from django.db import models

class Language(models.TextChoices):
    ENGLISH = 'ENG', 'English'
    RUSSIAN = 'RUS', 'Russian'
    UKRAINIAN = 'UKR', 'Ukrainian'

class User(AbstractUser):

    password = models.CharField(max_length=150,
                                verbose_name='Password'
                                )
    username = models.CharField(max_length=150,
                                verbose_name='Login',
                                unique=True
                                )
    first_name = models.CharField(max_length=150,
                                  verbose_name='First name'
                                  )
    last_name = models.CharField(max_length=150,
                                 verbose_name='Last name',
                                 )
    date_of_birth = models.DateField(default=date.today().strftime("%Y-%m-%d"))
    language = models.CharField(
        max_length=3,
        choices=Language.choices,
        default=Language.RUSSIAN,)
    telegram_nickname = models.CharField(max_length=50,
                                         verbose_name='Telegram nickname',
                                         )
    phone = models.CharField(max_length=150,
                             verbose_name='Phone number',
                             )
    email = models.EmailField(max_length=254,
                              verbose_name='Email',
                              )

    class Meta:
        verbose_name = 'User'
        verbose_name_plural = 'Users'
        ordering = ('username',)

    def __str__(self):
        return self.username


class Sessions(models.Model):

    class Session_types(models.TextChoices):
        INDIVIDUAL = 'IND', 'Individual'
        GROUP = 'GRP', 'Group'
        WEBINAR = 'WEB', 'Webinar'

    psychologists = models.ForeignKey(
        'Psychologist',
        on_delete=models.CASCADE,
        verbose_name='psychologist',)
    patient = models.ForeignKey(
        'Patient',
        on_delete=models.CASCADE,
        related_name='session',
        verbose_name='patient',
        blank=True,
        null=True,)
    date_time = models.DateTimeField(blank=True, null=True,)
    session_type = models.CharField(
        max_length=3,
        choices=Session_types.choices,
        default=Session_types.INDIVIDUAL,
        blank=True,
        null=True,)
    language = models.CharField(
        max_length=3,
        choices=Language.choices,
        default=Language.RUSSIAN,)

    class Meta:
        verbose_name = 'Session'
        verbose_name_plural = 'Sessions'


class Patient(User):

    class Problems(models.TextChoices):
        RELATIONSHIPS = 'REL', 'Relationships'
        INTERNAL_STATE = 'INT', 'Internal_state'
        WORK_STUDY = 'W&S', 'Work_study'
        LIFE = 'LIF', 'Life'
        FINDING_YOURSELF = 'FND', 'Finding_yourself'

    problem_type = models.CharField(
        max_length=3,
        choices=Problems.choices,
        default=Problems.INTERNAL_STATE,)
    assigned_id = models.IntegerField(blank=True, null=True,)
    registration_time = models.DateTimeField(verbose_name='Registration time',
                                             auto_now=True)
    priority = models.IntegerField(blank=True, null=True,)
    processed = models.BooleanField(default=False)
    processed_time = models.DateTimeField(verbose_name='Processed time',
                                          blank=True, null=True,)
    approved_time = models.DateTimeField(verbose_name='Approved time',
                                         blank=True, null=True,)

    class Meta:
        verbose_name = 'Patient'
        verbose_name_plural = 'Patients'
        ordering = ('username',)

    def __str__(self):
        return self.username


class Psychologist(User):
    added_by = models.CharField(max_length=50,
                                verbose_name='Added by',
                                blank=True,)
    time_table_id = models.ForeignKey(
        Sessions,
        on_delete=models.CASCADE,
        verbose_name='time_table_id',
        related_name='psychologist',
        blank=True,
        null=True,)

    class Meta:
        verbose_name = 'Psychologist'
        verbose_name_plural = 'Psychologists'
        ordering = ('username',)

    def __str__(self):
        return self.username
