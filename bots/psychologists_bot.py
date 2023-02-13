import json
import telebot
from bot_definitions import KeyboardButton, Psychologist

from bot_configs.config import PSYCHOLOGISTS_BOT_TOKEN as TOKEN
bot = telebot.TeleBot(TOKEN)

rootButton = KeyboardButton(
    name='rootButton',
    root_button=True,
    downward_buttons={
        '🆘SOS': None,
        '👤Заявки': None,
        '📅Расписание': None,
        '❓Техподдержка': None
    },
    message='Привет! Я бот "Ковчега". Я нужен для того, чтобы упростить запись на личный прием, группу или вебинары.',
    markup=telebot.types.ReplyKeyboardMarkup(resize_keyboard=True)
)
rootButton.markup.add('🆘SOS', '👤Заявки', '📅Расписание', '❓Техподдержка', row_width=2)

supportButton = KeyboardButton(
    name='supportButton',
    button_text='❓Техподдержка',
    upward_button=rootButton,
    downward_buttons=None,
    message="Если Вам нужно уточнить какой-то вопрос, напишите его в чат и наши специалисты ответят в ближайшее время.",
    markup=telebot.types.ReplyKeyboardMarkup(resize_keyboard=True)
)
supportButton.markup.add('⏪Назад')
supportButton.supportRequests = []
supportButton.support_request_accepted_message = "Заявка принята"

scheduleButton = KeyboardButton(
    name='scheduleButton',
    button_text='📅Расписание',
    upward_button=rootButton,
    downward_buttons=None,
    message="Ваше расписание доступно по ссылке. Там можно посмотреть, что назначено на ближайшее время, а также перенести или отменить консультации: link",
    markup=telebot.types.ReplyKeyboardMarkup(resize_keyboard=True)
)
scheduleButton.markup.add('⏪Назад')

applicationsButton = KeyboardButton(
    name='applicationsButton',
    button_text='👤Заявки',
    upward_button=rootButton,
    downward_buttons={
        '✅Взять в работу': None
    },
    message="На данный момент нет необработанных заявок.",
    markup=telebot.types.ReplyKeyboardMarkup(resize_keyboard=True)
)
applicationsButton.markup.add('⏪Назад')
# applicationsButton.application_message = (
#     'Имя: ' + telebot_defenitions.examplePatient.first_name + '\n' +
#     'Фамилия: ' + telebot_defenitions.examplePatient.last_name + '\n' +
#     'Телефон: ' + telebot_defenitions.examplePatient.telephone_number + '\n' +
#     'Телеграм: ' + telebot_defenitions.examplePatient.telegram + '\n' +
#     'E-mail: ' + telebot_defenitions.examplePatient.email + '\n' +
#     'Тип: ' + telebot_defenitions.examplePatient.appointment_type + '\n' +
#     'Что хотелось бы обсудть в первую очередь: ' + telebot_defenitions.examplePatient.problem + '\n' +
#     'Есть ли опыт психотерапии: ' + telebot_defenitions.examplePatient.experience + '\n' +
#     'Заявка зарегистрирована: ' + telebot_defenitions.examplePatient.application_date + '\n'
# )
applicationsButton.applications_quantity = 0
applicationsButton.application_markup = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True)
applicationsButton.application_markup.add('✅Взять в работу', '⏪Назад')

acceptApplicationButton = KeyboardButton(
    name='acceptApplicationButton',
    button_text='✅Взять в работу',
    upward_button=applicationsButton,
    downward_buttons=None,
    message="Закрепил заявку за Вами. Уведомлю Вас, когда Мария выберет время консультации.", # TODO name shouldn't be hardcoded
    markup=telebot.types.ReplyKeyboardMarkup(resize_keyboard=True)
)
acceptApplicationButton.markup.add('⏮Меню')

emergencyButton = KeyboardButton(
    name='emergencyButton',
    button_text='🆘SOS',
    upward_button=rootButton,
    downward_buttons=None,
    message="На данный момент нет необработанных заявок на экстренную психологическую помощь.",
    markup=telebot.types.ReplyKeyboardMarkup(resize_keyboard=True)
)
emergencyButton.markup.add('⏪Назад')

psychologists = {}
try:
    with open("psychologists.json", 'r') as json_file:
        for user in json.load(json_file).values():
            psychologists[user['id']] = Psychologist.de_json(user, locals()[user["lastButtonPressed"]])
except IOError:
   pass


@bot.message_handler(commands=['help', 'start'])
def send_welcome(message):

    psychologists[message.from_user.id] = Psychologist(message.from_user, rootButton)
    with open("psychologists.json", 'w') as json_file:
        json.dump(psychologists, json_file, indent=4)

    bot.reply_to(message, rootButton.message, reply_markup=rootButton.markup)

    if psychologists[message.from_user.id].authorized is False:
        bot.send_message(
            message.from_user.id, 
            'У вас нет доступа к системе\nВаш id:\n{}'.format(message.from_user.id)
            )


@bot.message_handler(content_types=["text"])
def handle_text(message):

    if message.from_user.id not in psychologists.keys():
        return None
    if not psychologists[message.from_user.id].authorized:
        return None

    if message.text == '⏪Назад':
        psychologists[message.from_user.id].lastButtonPressed = psychologists[message.from_user.id].lastButtonPressed.upward_button
        bot.send_message(
            message.from_user.id, 
            psychologists[message.from_user.id].lastButtonPressed.message, 
            reply_markup=psychologists[message.from_user.id].lastButtonPressed.markup
            )
    elif message.text == '⏮Меню':
        psychologists[message.from_user.id].lastButtonPressed = rootButton
        bot.send_message(
            message.from_user.id, 
            psychologists[message.from_user.id].lastButtonPressed.message, 
            reply_markup=psychologists[message.from_user.id].lastButtonPressed.markup
            )
    elif psychologists[message.from_user.id].lastButtonPressed.button_text == '❓Техподдержка':
        supportButton.supportRequests.append(message.text) # TODO save info
        bot.send_message(
            message.from_user.id, 
            supportButton.support_request_accepted_message
            )
        psychologists[message.from_user.id].lastButtonPressed = rootButton
        bot.send_message(
            message.from_user.id, 
            psychologists[message.from_user.id].lastButtonPressed.message, 
            reply_markup=psychologists[message.from_user.id].lastButtonPressed.markup
            )
    elif message.text in psychologists[message.from_user.id].lastButtonPressed.downward_buttons.keys():
        psychologists[message.from_user.id].lastButtonPressed = psychologists[message.from_user.id].lastButtonPressed.downward_buttons[message.text]
        match psychologists[message.from_user.id].lastButtonPressed.button_text:
            case '👤Заявки':
                if applicationsButton.applications_quantity > 0:
                    bot.send_message(
                        message.from_user.id, 
                        psychologists[message.from_user.id].lastButtonPressed.application_message, 
                        reply_markup=psychologists[message.from_user.id].lastButtonPressed.application_markup
                        )
                else:
                    bot.send_message(
                        message.from_user.id, 
                        psychologists[message.from_user.id].lastButtonPressed.message, 
                        reply_markup=psychologists[message.from_user.id].lastButtonPressed.markup
                        )
            case '✅Взять в работу':
                bot.send_message(
                    message.from_user.id, psychologists[message.from_user.id].lastButtonPressed.message, 
                    reply_markup=psychologists[message.from_user.id].lastButtonPressed.markup
                    )
                psychologists[message.from_user.id].lastButtonPressed = rootButton
                bot.send_message(
                    message.from_user.id, 
                    psychologists[message.from_user.id].lastButtonPressed.message, 
                    reply_markup=psychologists[message.from_user.id].lastButtonPressed.markup
                    )
            case _:
                bot.send_message(
                    message.from_user.id, 
                    psychologists[message.from_user.id].lastButtonPressed.message, 
                    reply_markup=psychologists[message.from_user.id].lastButtonPressed.markup
                    )
    else:
        bot.send_message(message.from_user.id, "Не могу распознать команду")
    
    with open("psychologists.json", 'w') as json_file:
        json.dump(psychologists, json_file, indent=4)


bot.polling(none_stop=True, interval=0)