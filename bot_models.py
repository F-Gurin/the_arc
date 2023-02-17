from datetime import date, datetime
from peewee import *

con = SqliteDatabase("db.sqlite3")


class BaseModel(Model):
    class Meta:
        database = con


LANGUAGES = [('ENG', 'RUS', 'UKR'),
             ('English', 'Russian', 'Ukrainian')]


SESSION_TYPES = [('IND', 'GRP', 'WEB'),
                 ('Individual', 'Group', 'Webinar')]


PROBLEMS = [('REL', 'INT', 'W&S', 'LIF', 'FND'),
            ('Relationships', 'Internal_state',
            'Work_study', 'Life', 'Finding_yourself')]


class User(BaseModel):
    password = CharField(max_length=150)
    username = CharField(max_length=150, unique=True)
    first_name = CharField(max_length=150)
    last_name = CharField(max_length=150, verbose_name='Last name')
    date_of_birth = DateField(default=date.today().strftime("%Y-%m-%d"))
    language = CharField(choices=LANGUAGES)
    telegram_nickname = CharField(max_length=50)
    phone = CharField(max_length=150)
    email = CharField(max_length=254)
    is_superuser = BooleanField(default=False)
    is_staff = BooleanField(default=False)
    is_active = BooleanField(default=True)
    date_joined = DateTimeField(default=datetime.now())
    tg_id = IntegerField(default=0)
    is_bot = BooleanField(default=False, )
    tg_first_name = CharField(max_length=150)
    tg_last_name = CharField(max_length=150)
    tg_username = CharField(max_length=150)
    language_code = CharField(choices=LANGUAGES, default='RUS')
    can_join_groups = BooleanField(default=False, )
    can_read_all_group_messages = BooleanField(default=False, )
    supports_inline_queries = BooleanField(default=False, )
    is_premium = BooleanField(default=False, )
    added_to_attachment_menu = BooleanField(default=False, )
    last_button_pressed = CharField(default="rootButton")

    class Meta:
        table_name = 'Web_admin_user'

    def save(self, *args, **kwargs):
        if not self.password:
            self.password = self.username
        if not self.tg_first_name:
            self.tg_first_name = self.first_name
        if not self.tg_last_name:
            self.tg_last_name = self.last_name
        if not self.tg_username:
            self.tg_username = self.username
        super(User, self).save(*args, **kwargs)


class Patient(BaseModel):
    user_ptr_id = IntegerField()
    problem_type = CharField(choices=PROBLEMS)
    assigned_id = IntegerField(null=True,)
    registration_time = DateTimeField(default=datetime.now())
    priority = IntegerField(null=True,)
    processed = BooleanField(default=False)
    processed_time = DateTimeField(null=True,)
    approved_time = DateTimeField(null=True,)
    experienced = BooleanField(default=False)
    patient_info_flag = BooleanField(default=False)

    class Meta:
        table_name = 'Web_admin_patient'


class Psychologist(BaseModel):
    user_ptr_id = IntegerField()
    added_by = CharField(null=True,)
    time_table_id = DeferredForeignKey(
        'Sessions',
        null=True,)
    tg_authorized = BooleanField(default=False)
    

    class Meta:
        table_name = 'Web_admin_psychologist'


class Sessions(BaseModel):
    psychologists = ForeignKeyField(
        Psychologist,
        backref='sessions')
    patient = ForeignKeyField(
        Patient,
        backref='sessions',
        null=True,)
    date_time = DateTimeField(null=True,)
    session_type = CharField(
        choices=SESSION_TYPES,
        null=True,)
    language = CharField(choices=LANGUAGES)

    class Meta:
        table_name = 'Web_admin_sessions'


# q = con.cursor()

# print(Patient.select().execute())
# print(Patient.get(User.id == 1))
# print(User.get(User.first_name == 'Мария').id)
# print(Patient.get(Patient.user_ptr_id = (User.get(User.first_name == 'Мария').id)))

user = User.create(
    username='Maria',
    password='Maria',
    first_name='Мария',
    last_name='Иванова',
    date_of_birth='2000-10-20',
    language='ENG',
    telegram_nickname='@test',
    phone='+79991111111',
    email='test@example.com',
    )


patient = Patient.create(
    user_ptr_id=user,
    problem_type='REL',
    assigned_id='',
    priority=10,
    processed=False,
    processed_time='',
    approved_time='',)
