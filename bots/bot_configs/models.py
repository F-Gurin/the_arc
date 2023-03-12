import json
import telebot

import bot_configs.config
from app import models
from django.contrib.auth.models import User

json.JSONEncoder.default = lambda self, obj: getattr(obj.__class__, "to_dict")(obj)

# class UserEncoder(json.JSONEncoder):
#     def default(self, obj):
#         return getattr(obj.__class__, "to_dict")(obj)

# def _default(self, obj):
#      return getattr(obj.__class__, "to_json", _default.default)(obj)
# _default.default = json.JSONEncoder().default
# json.JSONEncoder.default = _default

class KeyboardButton():

    def __init__(self, name=None, root_button=False, button_text='noButtonText', upward_button=None, downward_buttons=None, message='noButtonMessage', markup=None):
        self.name = name
        if self.name is None:
            raise Exception("You should pass a name of the button to KeyboardButton constructor")
        self.root_button = root_button
        self.button_text = button_text
        if self.root_button:
            self.upward_button = None
            self.button_text = None
        elif upward_button is not None:
            self.upward_button = upward_button
            self.upward_button.downward_buttons[self.button_text] = self
        else:
            raise Exception("You should pass either 'upward_button' or 'root_button=True' arguments to KeyboardButton constructor")
        if downward_buttons is None:
            self.downward_buttons = {}
        else:
            self.downward_buttons = downward_buttons
        self.message = message
        self.markup = markup

class AuthorizedUser(telebot.types.User):

    def __init__(self, telebot_user):
        super().__init__(
            telebot_user.id,
            telebot_user.is_bot,
            telebot_user.first_name,
            last_name=telebot_user.last_name,
            username=telebot_user.username,
            language_code=telebot_user.language_code,
            can_join_groups=telebot_user.can_join_groups,
            can_read_all_group_messages=telebot_user.can_read_all_group_messages,
            supports_inline_queries=telebot_user.supports_inline_queries,
            is_premium=telebot_user.is_premium,
            added_to_attachment_menu=telebot_user.added_to_attachment_menu
            )
        AuthorizedUser.save(self)

    def save(self):
        models.TgUser(
            tg_id=self.id,
            first_name=self.first_name,
            last_name=self.last_name,
            username=self.username,
            language_code=self.language_code,
            ).save()

    def register_user(self):

        try:
            models.TgUser.objects.get(tg_id=self.id)
            return None
        except models.TgUser.DoesNotExist:
            if self.username != '':
                username = self.username
            else:
                username = self.first_name # TODO deal with duplicates
                while(models.TgUser(username).exists()):
                    username += '_' + str(000) # TODO generate a random password and return it to the user
            user = User.objects.create_user(username, password='testpass', id=self.id)
            return user

    def get_model(self):
        return models.TgUser(
                tg_id=self.id,
                first_name=self.first_name,
                last_name=self.last_name,
                username=self.username,
                language_code=self.language_code,
                )
    
    # def to_dict(self):
    #     return super().to_dict()

    # def to_json(self):
    #     return super().to_json()

    # def de_json(self, json_string):
    #     return super().de_json(json_string)
        
class Patient(AuthorizedUser):

    def __init__(self, telebot_user, last_button_pressed, patient_info=None, patient_info_flag=False):
        super().__init__(telebot_user)
        if patient_info is None:
            self.patient_info = {
                'appointment type': None,
                'problem': None,
                'first name': None,
                'last name': None,
                'telephone number': None,
                'email': None,
                'experience': None
            }
        else:
            self.patient_info = patient_info
        self.patient_info_flag = patient_info_flag
        self.lastButtonPressed = last_button_pressed
        self.save()

    def save(self):
        super().save()
        models.PatientsBotUIState(
            tg=super().get_model(),
            patient_info_flag=self.patient_info_flag,
            appointment_type=self.patient_info['appointment type'],
            problem=self.patient_info['problem'],
            first_name=self.patient_info['first name'],
            last_name=self.patient_info['last name'],
            telephone_number=self.patient_info['telephone number'],
            email=self.patient_info['email'],
            experience=self.patient_info['experience'],
            last_button_pressed=self.lastButtonPressed.name,
            ).save()

    def to_dict(self):
        to_return = super().to_dict()
        to_return["patient_info"] = self.patient_info
        to_return["patient_info_flag"] = self.patient_info_flag
        to_return["lastButtonPressed"] = self.lastButtonPressed.name
        return to_return

    # def to_json(self):
    #     return super().to_json()

    @classmethod
    def de_json(cls, json_string, last_button_pressed):
        return cls(
            telebot.types.User.de_json(json_string),
            last_button_pressed,
            patient_info=json_string["patient_info"],
            patient_info_flag=json_string["patient_info_flag"]
            )

class Psychologist(AuthorizedUser):

    authorized_users = []

    def __init__(self, telebot_user, last_button_pressed):
        super().__init__(telebot_user)
        self.lastButtonPressed = last_button_pressed
        self.authorized = self.id in self.authorized_users # AUTHORIZED_USERS
        self.save()

    def save(self):
        super().save()
        models.PsychologistBotUIState(
            tg=self.id,
            authorized=self.authorized,
            last_button_pressed=self.last_button_pressed.name,
            ).save()

    def to_dict(self):
        to_return = super().to_dict()
        to_return["lastButtonPressed"] = self.lastButtonPressed.name
        to_return["authorized"] = self.authorized
        return to_return

    # def to_json(self):
    #     return super().to_json()

    @classmethod
    def de_json(cls, json_string, last_button_pressed):
        return cls(
            telebot.types.User.de_json(json_string),
            last_button_pressed
            )

        
# examplePatient = Patient(
#     first_name='Мария',
#     last_name='Иванова',
#     telephone_number='+79991111111',
#     telegram='@test',
#     email='test@example.com',
#     appointment_type='Личный приём',
#     problem='❤️Отношения',
#     experience='Нет',
#     application_date='2022-11-20 12:00'
# )
