from datetime import date
from peewee import *

con = SqliteDatabase(
    "./Admin/Admin_part/db.sqlite3")


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

    class Meta:
        table_name = 'Web_admin_user'


class Patient(User):
    problem_type = CharField(choices=PROBLEMS)
    assigned_id = IntegerField(null=True,)
    registration_time = DateTimeField(default=date.today())
    priority = IntegerField(null=True,)
    processed = BooleanField(default=False)
    processed_time = DateTimeField(null=True,)
    approved_time = DateTimeField(null=True,)

    class Meta:
        table_name = 'Web_admin_patient'


class Psychologist(User):
    added_by = CharField(null=True,)
    time_table_id = DeferredForeignKey(
        'Sessions',
        null=True,)

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
# print(Patient.get(Patient.first_name == 'Ivan').username)

patient = Patient.create(
    username='Maria',
    password='Maria',
    first_name='Мария',
    last_name='Иванова',
    date_of_birth='2000-10-20',
    language='ENG',
    telegram_nickname='@test',
    phone='+79991111111',
    email='test@example.com',
    problem_type='REL',
    assigned_id='',
    priority=10,
    processed=False,
    processed_time='',
    approved_time='',)
