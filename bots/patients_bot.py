import json
import telebot
from bot_definitions import KeyboardButton, Patient

from bot_configs.config import PATIENTS_BOT_TOKEN as TOKEN
bot = telebot.TeleBot(TOKEN)

rootButton = KeyboardButton(
    name='rootButton',
    root_button=True,
    message=('Привет! Я бот "Ковчега". Если из-за войны Вы были вынуждены эмигрировать из России и чувствуете, '
    'что вам нужна профессиональная психологическая помощь, я помогу записаться на личную консультацию специалиста (онлайн), '
    'в психотерапевтическую группу, на вебинары. Выберите, что Вас интересует. Если что-то не ясно, нажмите на кнопку "FAQ".'),
    markup=telebot.types.ReplyKeyboardMarkup(resize_keyboard=True)
)
rootButton.markup.add('👤Личный прием', '👥Группа', '💻Вебинары', '❓FAQ', row_width=2)
rootButton.markup.add(telebot.types.KeyboardButton('🆘SOS'))

psychological_problems_markup = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True)
psychological_problems_markup.add(
    '🥺Моё состояние',
    '❤️Отношения',
    '👨🏻‍💻Работа, учёба',
    '🌪События в жизни',
    '❓Поиск себя',
    row_width=2
)
psychological_problems_markup.add('⏮Меню')
psychological_problems_message = ('Давайте определим суть проблемы, а потом я соберу контактные данные, '
                    'по которым с Вами свяжется специалист. Что Вы хотели бы обсудить в первую очередь?')

personalAppointmentButton = KeyboardButton(
    name='personalAppointmentButton',
    button_text='👤Личный прием',
    upward_button=rootButton,
    message=psychological_problems_message,
    markup=psychological_problems_markup
)

groupAppointmentButton = KeyboardButton(
    name='groupAppointmentButton',
    button_text='👥Группа',
    upward_button=rootButton,
    message=psychological_problems_message,
    markup=psychological_problems_markup
)

webinarsButton = KeyboardButton(
    name='webinarsButton',
    button_text='💻Вебинары',
    upward_button=rootButton,
    message=psychological_problems_message,
    markup=psychological_problems_markup
)

sosButton = KeyboardButton(
    name='sosButton',
    button_text='🆘SOS',
    upward_button=rootButton,
    message="Вы обратились за экстренной помощью. Связать Вас со специалистом?",
    markup=telebot.types.ReplyKeyboardMarkup(resize_keyboard=True)
)
sosButton.markup.add('✅Да', '⏪Назад')

sosConfirmedButton = KeyboardButton(
    name='sosConfirmedButton',
    button_text='✅Да',
    upward_button=sosButton,
    message=psychological_problems_message,
    markup=psychological_problems_markup
)

faqButton = KeyboardButton(
    name='faqButton',
    button_text='❓FAQ',
    upward_button=rootButton,
    message="Что вас интересует?",
    markup=telebot.types.ReplyKeyboardMarkup(resize_keyboard=True)
)
faqButton.markup.add('Про "Ковчег"', 'Как помочь "Ковчегу"?', 'Чем мы можем помочь', '⏪Назад', row_width=1)

aboutKovchegButton = KeyboardButton(
    name='aboutKovchegButton',
    button_text='Про "Ковчег"',
    upward_button=faqButton,
    message=('«Ковчег» — это группа помощи российским эмигрантам, '
    'которые осудили военную агрессию путинского правительства и покинули страну, '
    'не найдя для себя возможностей жить в нынешней России.\n'
    'Волонтёры «Ковчега» — это сообщество неравнодушных людей по всему миру, '
    'готовых помочь тем, кто вынужден покинуть страну и искать новый дом и новые возможности. '
    'Наши волонтёры предоставляют помощь релокантам в десятках стран мира как онлайн, так и офлайн.'),
    markup=None
)

giveHelpButton = KeyboardButton(
    name='giveHelpButton',
    button_text='Как помочь "Ковчегу"?',
    upward_button=faqButton,
    message=('Вы можете стать волонтером. Если вы юрист, психолог или переводчик, '
    'вы можете давать консультации релокантам в рамках своих знаний. '
    'Часто нам нужны и другие профессиональные волонтёры — всё зависит от конкретной заявки.  '
    'Или поддержать нас. Если вы хотите стать волонтёром «Ковчега», нажмите на кнопку и заполните форму по ссылке.\n'
    'Поддержать проект деньгами можно на нашем сайте.'),
    markup=telebot.types.InlineKeyboardMarkup()
)

giveHelpButton.markup.add(
    telebot.types.InlineKeyboardButton(
        text='🤝🏻Стать волонтером',
        url='https://docs.google.com/forms/d/e/1FAIpQLSdjCMhg543q6jmavwIHKFbJ9PqXGqkknb4IZm-W0dG5-0_Evw/viewform?usp=send_form'
        )
)

giveHelpButton.markup.add(
    telebot.types.InlineKeyboardButton(
        text='🙌🏼Поддержать деньгами',
        url='https://antiwarcommittee.info/kovcheg/'
        )
)

getHelpButton = KeyboardButton(
    name='getHelpButton',
    button_text='Чем мы можем помочь',
    upward_button=faqButton,
    message=('Многие эмигранты сталкиваются с психологическими проблемами: '
    'неприятие антивоенной позиции родственниками, чувства вины и стыда, неопределенность будущего.\n'
    'Мы предлагаем индивидуальные и групповые консультации со специалистами, а также вебинары.'),
    markup=telebot.types.ReplyKeyboardMarkup(resize_keyboard=True)
)
getHelpButton.markup.add('👤Личный прием', '👥Группа', '💻Вебинары', '🙌🏼Другое', row_width=2)
getHelpButton.markup.add('⏮Меню', '⏪Назад', row_width=2)

aboutPersonalAppointmentButton = KeyboardButton(
    name='aboutPersonalAppointmentButton',
    button_text='👤Личный прием',
    upward_button=getHelpButton,
    downward_buttons={
        '✅Записаться на личный прием': personalAppointmentButton
    },
    message=('Если Вам нужна индивидуальная помощь специалиста, запишитесь в боте. '
    'Личные консультации помогают найти в себе ресурсы, осознать переживания, '
    'понять причины трудностей и справиться с ними'),
    markup=telebot.types.ReplyKeyboardMarkup(resize_keyboard=True)
)
aboutPersonalAppointmentButton.markup.add('✅Записаться на личный прием', '⏪Назад')

aboutGroupAppointmentButton = KeyboardButton(
    name='aboutGroupAppointmentButton',
    button_text='👥Группа',
    upward_button=getHelpButton,
    downward_buttons={
        '✅Записаться в группу': groupAppointmentButton
    },
    message=('Если Вам нужна поддержка, можете записаться в этом боте на групповые консультации. '
    'Около 15 человек в группе, быстрое снижение психологического напряжения, облечение острых состояний'),
    markup=telebot.types.ReplyKeyboardMarkup(resize_keyboard=True)
)
aboutGroupAppointmentButton.markup.add('✅Записаться в группу', '⏪Назад')

aboutWebinarsButton = KeyboardButton(
    name='aboutWebinarsButton',
    button_text='💻Вебинары',
    upward_button=getHelpButton,
    downward_buttons={
        '✅Записаться на вебинар': webinarsButton
    },
    message=('В боте можно зарегистрироваться на наши вебинары. Волонтёры «Ковчега», '
    'обладающие уникальными знаниями и опытом, регулярно проводят полезные вебинары. '
    'На них можно узнать о том, как переехать в ту или иную страну, '
    'какие возможности образования за рубежом есть для россиян, '
    'а также получить психологическую поддержку и справиться со стрессом.'),
    markup=telebot.types.ReplyKeyboardMarkup(resize_keyboard=True)
)
aboutWebinarsButton.markup.add('✅Записаться на вебинар', '⏪Назад')

aboutOtherButton = KeyboardButton(
    name='aboutOtherButton',
    button_text='🙌🏼Другое',
    upward_button=getHelpButton,
    message=('🙌🏼 Если Вам нужно жилье в Ереване или Стамбуле, '
    'заполните форму: https://clck.ru/eMmPL. '
    'Мы свяжемся с Вами в ближайшее время.\n'
    '🙌🏼 Если Вам нужна консультация по юридическим и бытовым вопросам, '
    'воспользуйтесь ботом в Telegram: '
    'https://t.me/EmigrantHelpBot.\n🙌🏼 '
    'Если Вы хотите стать волонтером: '
    'предоставить жилье эмигранту или помочь с правовыми консультациями, '
    'напишите нам в Telegram: https://t.me/kovcheghelp'),
    markup=None
)


markup_patient_info = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True)
markup_patient_info.add('⏮Меню')

markup_patient_info_email = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True)
markup_patient_info_email.add('⏩Пропустить', '⏮Меню', row_width=1)

markup_patient_info_experience = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True)
markup_patient_info_experience.add('❌Нет', '✅Да', row_width=2)
markup_patient_info_experience.add('⏮Меню')

patients = {}
try:
    with open("patients.json", 'r') as json_file:
        for user in json.load(json_file).values():
            patients[user['id']] = Patient.de_json(user, locals()[user["lastButtonPressed"]])
except IOError:
   pass

@bot.message_handler(commands=['help', 'start'])
def send_welcome(message):

    patients[message.from_user.id] = Patient(message.from_user, rootButton)
    with open("patients.json", 'w') as json_file:
        json.dump(
            patients, #{k:v.to_dict() for k, v in patients.items()},
            json_file,
            indent=4,
            #cls=UserEncoder
            )
    bot.reply_to(message, rootButton.message, reply_markup=rootButton.markup)

@bot.message_handler(content_types=["text"])
def handle_text(message):

    if message.from_user.id not in patients.keys():
        return None
    
    if message.text == '⏪Назад':
        patients[message.from_user.id].lastButtonPressed = patients[message.from_user.id].lastButtonPressed.upward_button
        bot.send_message(
            message.from_user.id,
            patients[message.from_user.id].lastButtonPressed.message,
            reply_markup=patients[message.from_user.id].lastButtonPressed.markup
            )
    elif message.text == '⏮Меню':
        patients[message.from_user.id].lastButtonPressed = rootButton
        bot.send_message(
            message.from_user.id,
            patients[message.from_user.id].lastButtonPressed.message,
            reply_markup=patients[message.from_user.id].lastButtonPressed.markup
            )
        patients[message.from_user.id].patient_info_flag = False
        patients[message.from_user.id].patient_info = {
                'appointment type': None,
                'problem': None,
                'first name': None,
                'last name': None,
                'telephone number': None,
                'email': None,
                'experience': None
                }
    elif patients[message.from_user.id].patient_info_flag is True:
        if patients[message.from_user.id].patient_info['problem'] is None:
            patients[message.from_user.id].patient_info['problem'] = message.text
            bot.send_message(
                message.from_user.id,
                "Введите, пожалуйста, Ваше имя",
                reply_markup=markup_patient_info
                )
        elif patients[message.from_user.id].patient_info['first name'] is None:
            patients[message.from_user.id].patient_info['first name'] = message.text
            bot.send_message(
                message.from_user.id,
                "Введите, пожалуйста, Вашу фамилию",
                reply_markup=markup_patient_info
                )
        elif patients[message.from_user.id].patient_info['last name'] is None:
            patients[message.from_user.id].patient_info['last name'] = message.text
            bot.send_message(
                message.from_user.id,
                "Введите, пожалуйста, актуальный номер Вашего телефона",
                reply_markup=markup_patient_info
                )
        elif patients[message.from_user.id].patient_info['telephone number'] is None:
            patients[message.from_user.id].patient_info['telephone number'] = message.text
            bot.send_message(
                message.from_user.id,
                "Введите, пожалуйста, Ваш e-mail. Этот шаг можно пропустить",
                reply_markup=markup_patient_info_email
                )
        elif patients[message.from_user.id].patient_info['email'] is None:
            if message.text == '⏩Пропустить':
                patients[message.from_user.id].patient_info['email'] = False
            else:
                patients[message.from_user.id].patient_info['email'] = message.text
            bot.send_message(
                message.from_user.id,
                "Был ли у вас опыт в психотерапии?",
                reply_markup=markup_patient_info_experience
                )
        elif patients[message.from_user.id].patient_info['experience'] is None:
            patients[message.from_user.id].patient_info['experience'] = message.text
            # TODO save info
            bot.send_message(
                message.from_user.id,
                "Спасибо! Сохранил Ваши ответы. В ближайшее время направлю информацию о возможности записи.",
                reply_markup=markup_patient_info
                )

    elif message.text in patients[message.from_user.id].lastButtonPressed.downward_buttons.keys():
        patients[message.from_user.id].lastButtonPressed = patients[message.from_user.id].lastButtonPressed.downward_buttons[message.text]
        if patients[message.from_user.id].lastButtonPressed.markup is None:
            bot.send_message(message.from_user.id, patients[message.from_user.id].lastButtonPressed.message)
        else:
            bot.send_message(
                message.from_user.id,
                patients[message.from_user.id].lastButtonPressed.message,
                reply_markup=patients[message.from_user.id].lastButtonPressed.markup
                )
        if patients[message.from_user.id].lastButtonPressed in [personalAppointmentButton, groupAppointmentButton, webinarsButton, sosConfirmedButton]:
            patients[message.from_user.id].patient_info['appointment type'] = patients[message.from_user.id].lastButtonPressed.button_text
            patients[message.from_user.id].patient_info_flag = True
        elif patients[message.from_user.id].lastButtonPressed.downward_buttons == {}:
            patients[message.from_user.id].lastButtonPressed = patients[message.from_user.id].lastButtonPressed.upward_button
    else:
        bot.send_message(message.from_user.id, "Не могу распознать команду")

    with open("patients.json", 'w') as json_file:
        json.dump(patients, json_file, indent=4)

bot.polling(non_stop=True, interval=0)
