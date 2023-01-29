from datetime import date
from django.db import models
from django.utils import timezone
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _

from django.contrib.auth.models import AbstractUser
from django.contrib.auth.hashers import make_password
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
    tg_id = models.IntegerField(default=0,
                                verbose_name='Telegram ID'
                                )
    is_bot = models.BooleanField(default=False, )
    tg_first_name = models.CharField(max_length=150,
                                     verbose_name='Telegram first name'
                                     )
    tg_last_name = models.CharField(max_length=150,
                                    verbose_name='Telegram last name'
                                    )
    tg_username = models.CharField(max_length=150,
                                   verbose_name='Telegram username'
                                   )
    language_code = models.CharField(max_length=3,
                                     choices=Language.choices,
                                     default=Language.RUSSIAN,
                                     )
    can_join_groups = models.BooleanField(default=False, )
    can_read_all_group_messages = models.BooleanField(default=False, )
    supports_inline_queries = models.BooleanField(default=False, )
    is_premium = models.BooleanField(default=False, )
    added_to_attachment_menu = models.BooleanField(default=False, )
    last_button_pressed = models.CharField(default="rootButton",
                                           max_length=150,
                                           verbose_name='Last pressed button'
                                           )

    class Meta:
        verbose_name = 'User'
        verbose_name_plural = 'Users'
        ordering = ('username',)

    def __str__(self):
        return self.username

    def save(self, *args, **kwargs):
        if not self.password:
            self.password = make_password(
                self.username, salt=None, hasher='default')
        if not self.tg_first_name:
            self.tg_first_name = self.first_name
        if not self.tg_last_name:
            self.tg_last_name = self.last_name
        if not self.tg_username:
            self.tg_username = self.username
        super(User, self).save(*args, **kwargs)


class Sessions(models.Model):

    class Session_types(models.TextChoices):
        INDIVIDUAL = 'IND', 'Individual'
        GROUP = 'GRP', 'Group'
        WEBINAR = 'WEB', 'Webinar'

    def validate_date_time(date_time):
        if date_time < timezone.now():
            raise ValidationError(_('The date cannot be in the past!'),
                                  params={'Date': date_time},
                                  )

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
    date_time = models.DateTimeField(default=timezone.now(),
                                     blank=True, null=True,
                                     validators=[validate_date_time])
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
    experienced = models.BooleanField(default=False)
    patient_info_flag = models.BooleanField(default=False)

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
    tg_authorized = models.BooleanField(default=False)

    class Meta:
        verbose_name = 'Psychologist'
        verbose_name_plural = 'Psychologists'
        ordering = ('username',)

    def __str__(self):
        return self.username
