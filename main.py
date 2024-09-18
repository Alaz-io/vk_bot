import os
import sys
import subprocess
import vk_api
from vk_api.longpoll import VkLongPoll, VkEventType
from vk_api.keyboard import VkKeyboard, VkKeyboardColor
from config import VK_TOKEN, GROUP_ID, OPERATOR_IDS
# Константы команд
COMMANDS = {
    'hello': 'привет',
    'order': 'заказать',
    'faq': 'FAQ: ответы на вопросы',
    'contact_operator': 'связь со специалистом',
    'free_chat': 'выключить бота',
    'operator_commands': 'админка',
    'back_to_bot': 'перейти к боту',
    'back': 'назад',
    'design': 'дизайн',
    'development': 'видео',
    'copywriting': 'кодинг',
    'logo': 'логотип',
    'banner': 'баннер',
    'web_design': 'веб-дизайн',
    'animation': 'анимация',
    'videography': 'видеография',
    'post_production': 'пост-продакшн',
    'front_end': 'фронтенд',
    'back_end': 'бэкенд',
    'mobile_dev': 'мобильная разработка',
    'change_status': 'изменить статус',
    'check_status': 'Просмотреть статусы',
    'start_chat': 'начать чат со специалистом',
    'leave_message': 'отправить сообщение'
}

# Константы сообщений
RESPONSE_MESSAGES = {
    'greeting': 'Здравствуйте! Чем могу помочь?',
    'order_prompt': 'Выберите сферу услуги:',
    'faq_prompt': 'Выберите интересующий вопрос:',
    'contact_operator_prompt': 'Как хотите установить связь со специалистом:',
    'free_chat_entered': 'Вы вошли в режим свободного общения. Нажмите или напишите "перейти к боту", чтобы вернуться обратно.',
    'return_to_bot': 'Вы вернулись к общению с ботом. Давайте помогу Вам?)',
    'order_received': 'Ваш заказ принят. Специалисты уведомлены.',
    'message_received': 'Ваше сообщение отправлено. Специалисты уже получили сообщение.',
    'status_updated': 'Ваш статус обновлен на "{status}".',
    'faq_answer': 'Пожалуйста, выберите корректный вопрос из FAQ или вернитесь в главное меню.',
    'operator_only': 'Эта команда доступна только для операторов.',
    'all_operators_busy': 'Просим прощения, в данный момент все специалисты заняты. Пожалуйста, попробуйте позже или просто оставьте сообщение!',
    'invalid_option': 'Пожалуйста, выберите из предложенных кнопок',
    'admin_commands': 'Выберите команду:',
    'invalid_command': 'Пожалуйста, выберите из предложенных команд.',
    'faq_back': 'Возвращаемся в главное меню.',
    'back_to_main': 'Возвращаемся в главное меню.',
    'select_type': 'Выберите тип услуги:',
    'enter_description': 'Введите описание проекта:',
    'empty': ''\
}

# Инициализация API
vk_session = vk_api.VkApi(token=VK_TOKEN)
vk = vk_session.get_api()
longpoll = VkLongPoll(vk_session)

is_contact_operator = False

# Функция для перезапуска скрипта
def restart_script():
    """Перезапускает текущий скрипт."""
    print("Перезапуск скрипта...")
    python = sys.executable
    os.execl(python, python, *sys.argv)

# Функция для обновления из GitHub
def update_from_github():
    """Обновляет код из репозитория GitHub и перезапускает скрипт."""
    print("Обновление из GitHub...")
    try:
        subprocess.run(["git", "pull"], check=True)
        restart_script()
    except subprocess.CalledProcessError as e:
        print(f"Ошибка при обновлении из GitHub: {e}")

# Состояния пользователей
user_states = {}
operator_status = {op_id: True for op_id in OPERATOR_IDS}  # Изначально все операторы доступны

# Краткая информация для FAQ
faq = {
    "1. Что такое AlazAlm?": "AlazAlm - фриланс-студия, которая выполняет много разных услуг, каждый из которых выполняется разными людьми.",
    "2. Политика правок": "В случае, если у Вас слишком много правок, специалист вправе отказать Вам в дальнейших изменениях работы.",
    "3. Возврат средств": "Если Вам работа не понравилась, мы можем вернуть денежные средства до 50%. Но если Вы будете использовать отказанную работу, то мы с Вами больше не будем работать.",
    "4. Оплата рекламой": "Вместо оплаты деньгами, Вы можете прорекламировать нас.",
    "5. Платежные системы": "Платежные системы удобные для нас: Сбербанк, Тинькофф, Qiwi, Donationalerts, DonatPay и др. (уточнить)",
    "6. Сотрудничество": "Мы готовы выполнить работу за бесплатно или с постоянной скидкой, если Вы будете сотрудничать с нами и рекламировать нас по специальному выданному промокоду! Промокод дает скидку на любой из товаров для Ваших подписчиков.",
    "7. Контакты": "Благодарим за заказ и соблюдение условий, по любым вопросам обращайтесь в личные сообщения сообщества."
}

def send_message(user_id, message, keyboard=None):
    """
    Отправляет сообщение пользователю.

    :param user_id: ID пользователя, которому отправляется сообщение.
    :param message: Текст сообщения.
    :param keyboard: (Необязательно) Клавиатура для сообщения.
    """
    try:
        vk.messages.send(
            user_id=user_id,
            message=message,
            random_id=vk_api.utils.get_random_id(),
            keyboard=keyboard.get_keyboard() if keyboard else None
        )
    except vk_api.exceptions.ApiError as e:
        print(f"Ошибка при отправке сообщения пользователю {user_id}: {e}")

def notify_operators(message):
    """
    Отправляет уведомление всем операторам.

    :param message: Текст уведомления.
    """
    for operator_id in OPERATOR_IDS:
        try:
            vk.messages.send(
                user_id=operator_id,
                message=message,
                random_id=vk_api.utils.get_random_id()
            )
        except vk_api.exceptions.ApiError as e:
            print(f"Ошибка при отправке уведомления оператору {operator_id}: {e}")

def main_menu_keyboard():
    """
    Создает клавиатуру для главного меню.

    :return: Объект VkKeyboard с кнопками главного меню.
    """
    keyboard = VkKeyboard(one_time=True)
    keyboard.add_button(COMMANDS['order'], color=VkKeyboardColor.POSITIVE)
    keyboard.add_button(COMMANDS['faq'], color=VkKeyboardColor.PRIMARY)
    keyboard.add_button(COMMANDS['contact_operator'], color=VkKeyboardColor.NEGATIVE)
    keyboard.add_line()
    keyboard.add_button(COMMANDS['free_chat'], color=VkKeyboardColor.SECONDARY)
    return keyboard

def order_services_keyboard():
    """
    Создает клавиатуру для выбора типа услуги.

    :return: Объект VkKeyboard с кнопками для выбора услуги.
    """
    keyboard = VkKeyboard(one_time=True)
    keyboard.add_button(COMMANDS['design'], color=VkKeyboardColor.POSITIVE)
    keyboard.add_button(COMMANDS['development'], color=VkKeyboardColor.PRIMARY)
    keyboard.add_button(COMMANDS['copywriting'], color=VkKeyboardColor.NEGATIVE)
    keyboard.add_line()
    keyboard.add_button(COMMANDS['back'], color=VkKeyboardColor.SECONDARY)
    return keyboard

def design_types_keyboard():
    """
    Создает клавиатуру для выбора типа дизайна.

    :return: Объект VkKeyboard с кнопками для выбора типа дизайна.
    """
    keyboard = VkKeyboard(one_time=True)
    keyboard.add_button(COMMANDS['logo'], color=VkKeyboardColor.POSITIVE)
    keyboard.add_button(COMMANDS['banner'], color=VkKeyboardColor.PRIMARY)
    keyboard.add_button(COMMANDS['web_design'], color=VkKeyboardColor.NEGATIVE)
    keyboard.add_line()
    keyboard.add_button(COMMANDS['back'], color=VkKeyboardColor.SECONDARY)
    return keyboard

def video_types_keyboard():
    """
    Создает клавиатуру для выбора типа видео услуг.

    :return: Объект VkKeyboard с кнопками для выбора типа видео услуг.
    """
    keyboard = VkKeyboard(one_time=True)
    keyboard.add_button(COMMANDS['animation'], color=VkKeyboardColor.POSITIVE)
    keyboard.add_button(COMMANDS['videography'], color=VkKeyboardColor.PRIMARY)
    keyboard.add_button(COMMANDS['post_production'], color=VkKeyboardColor.NEGATIVE)
    keyboard.add_line()
    keyboard.add_button(COMMANDS['back'], color=VkKeyboardColor.SECONDARY)
    return keyboard

def coding_types_keyboard():
    """
    Создает клавиатуру для выбора типа кодинга.

    :return: Объект VkKeyboard с кнопками для выбора типа кодинга.
    """
    keyboard = VkKeyboard(one_time=True)
    keyboard.add_button(COMMANDS['front_end'], color=VkKeyboardColor.POSITIVE)
    keyboard.add_button(COMMANDS['back_end'], color=VkKeyboardColor.PRIMARY)
    keyboard.add_button(COMMANDS['mobile_dev'], color=VkKeyboardColor.NEGATIVE)
    keyboard.add_line()
    keyboard.add_button(COMMANDS['back'], color=VkKeyboardColor.SECONDARY)
    return keyboard

def contact_operator_keyboard():
    """
    Создает клавиатуру для связи с оператором.

    :return: Объект VkKeyboard с кнопками для связи с оператором.
    """
    keyboard = VkKeyboard(one_time=True)
    keyboard.add_button(COMMANDS['leave_message'], color=VkKeyboardColor.POSITIVE)
    keyboard.add_button(COMMANDS['start_chat'], color=VkKeyboardColor.PRIMARY)
    keyboard.add_line()
    keyboard.add_button(COMMANDS['back'], color=VkKeyboardColor.SECONDARY)
    return keyboard

def operator_commands_keyboard():
    """
    Создает клавиатуру для операторов/специалистов.

    :return: Объект VkKeyboard с кнопками операторов.
    """
    keyboard = VkKeyboard(one_time=True)
    keyboard.add_button(COMMANDS['change_status'], color=VkKeyboardColor.POSITIVE)
    keyboard.add_button(COMMANDS['check_status'], color=VkKeyboardColor.PRIMARY)
    keyboard.add_line()
    keyboard.add_button(COMMANDS['back'], color=VkKeyboardColor.SECONDARY)
    return keyboard

def free_chat_keyboard():
    """
    Создает клавиатуру для режима свободного чата.

    :return: Объект VkKeyboard с кнопками для возврата к боту.
    """
    keyboard = VkKeyboard(one_time=True)
    keyboard.add_button(COMMANDS['back_to_bot'], color=VkKeyboardColor.SECONDARY)
    return keyboard

def faq_keyboard():
    """
    Создает клавиатуру для раздела FAQ.

    :return: Объект VkKeyboard с кнопками для выбора FAQ.
    """
    keyboard = VkKeyboard(one_time=False)
    for key in faq.keys():
        keyboard.add_button(key, color=VkKeyboardColor.PRIMARY)
        keyboard.add_line()
    keyboard.add_button(COMMANDS['back'], color=VkKeyboardColor.SECONDARY)
    return keyboard

def handle_operator_message(event):
    global is_contact_operator
    user_id = event.user_id
    message = event.text

    if is_contact_operator:
        # Проверяем, не ввел ли оператор команду для завершения общения
        if message.lower() == "/end":
            # Выходим из режима "Contact operator"
            is_contact_operator = False
            send_message(user_id, "Контакт с оператором завершен.")
        else:
            # Продолжаем отправлять сообщения оператору
            send_message_to_operator(user_id, message)
    else:
        # Обычная логика обработки сообщений
        handle_normal_user_message(event)

def handle_message(user_id, text):
    """
    Обрабатывает сообщения пользователей и управляет состоянием диалога.

    :param user_id: ID пользователя, отправившего сообщение.
    :param text: Текст сообщения.
    """
    text = text.strip().lower()

    state = user_states.get(user_id, {'step': 'start'})
# Шаг - меню/старт
    if state['step'] == 'start':
        command = next((cmd for cmd, alias in COMMANDS.items() if alias.lower() in text), None)
    #привет
        if command == 'hello':
            send_message(user_id, RESPONSE_MESSAGES['greeting'], keyboard=main_menu_keyboard())
    #заказать
        elif command == 'order':
            send_message(user_id, RESPONSE_MESSAGES['order_prompt'], keyboard=order_services_keyboard())
            user_states[user_id] = {'step': 'select_service'}
    #faq
        elif command == 'faq':
            send_message(user_id, RESPONSE_MESSAGES['faq_prompt'], keyboard=faq_keyboard())
            user_states[user_id] = {'step': 'faq'}
    #связаться со спец
        elif command == 'contact_operator':
            send_message(user_id, RESPONSE_MESSAGES['contact_operator_prompt'], keyboard=contact_operator_keyboard())
            user_states[user_id] = {'step': 'contact_operator'}
    #свободный чат
        elif command == 'free_chat':
            user_states[user_id] = {'step': 'free_chat'}
            send_message(user_id, RESPONSE_MESSAGES['free_chat_entered'], keyboard=free_chat_keyboard())
    #админка
        elif command == 'operator_commands':
            if user_id in OPERATOR_IDS:
                send_message(user_id, RESPONSE_MESSAGES['admin_commands'], keyboard=operator_commands_keyboard())
                user_states[user_id] = {'step': 'operator_commands'}
            else:
                send_message(user_id, RESPONSE_MESSAGES['operator_only'], keyboard=main_menu_keyboard())
    #неверно написал
        else:
            send_message(user_id, RESPONSE_MESSAGES['invalid_option'], keyboard=main_menu_keyboard())
#Шаг - выбор сферы
    elif state['step'] == 'select_service':
        if text == COMMANDS['back']:
            send_message(user_id, RESPONSE_MESSAGES['back_to_main'], keyboard=main_menu_keyboard())
            user_states[user_id] = {'step': 'start'}
    #дизайн
        elif text == COMMANDS['design']:
            send_message(user_id, RESPONSE_MESSAGES['select_type'], keyboard=design_types_keyboard())
            user_states[user_id] = {'step': 'select_type'}
    #видео
        elif text == COMMANDS['development']:
            send_message(user_id, RESPONSE_MESSAGES['select_type'], keyboard=video_types_keyboard())
            user_states[user_id] = {'step': 'select_video_type'}
    #кодинг
        elif text == COMMANDS['copywriting']:
            send_message(user_id, RESPONSE_MESSAGES['select_type'], keyboard=coding_types_keyboard())
            user_states[user_id] = {'step': 'select_coding_type'}
    #неверно написал
        else:
            send_message(user_id, RESPONSE_MESSAGES['invalid_option'], keyboard=order_services_keyboard())

    elif state['step'] == 'select_type':
        if text == COMMANDS['back']:
            send_message(user_id, RESPONSE_MESSAGES['back_to_main'], keyboard=order_services_keyboard())
            user_states[user_id] = {'step': 'select_service'}
        elif text in [COMMANDS['logo'], COMMANDS['banner'], COMMANDS['web_design']]:
            send_message(user_id, RESPONSE_MESSAGES['enter_description'], keyboard=None)
            user_states[user_id] = {'step': 'wait_description', 'type': text}
        else:
            send_message(user_id, RESPONSE_MESSAGES['invalid_option'], keyboard=design_types_keyboard())

    elif state['step'] == 'select_video_type':
        if text == COMMANDS['back']:
            send_message(user_id, RESPONSE_MESSAGES['back_to_main'], keyboard=order_services_keyboard())
            user_states[user_id] = {'step': 'select_service'}
        elif text in [COMMANDS['animation'], COMMANDS['videography'], COMMANDS['post_production']]:
            send_message(user_id, RESPONSE_MESSAGES['enter_description'], keyboard=None)
            user_states[user_id] = {'step': 'wait_description', 'type': text}
        else:
            send_message(user_id, RESPONSE_MESSAGES['invalid_option'], keyboard=video_types_keyboard())

    elif state['step'] == 'select_coding_type':
        if text == COMMANDS['back']:
            send_message(user_id, RESPONSE_MESSAGES['back_to_main'], keyboard=order_services_keyboard())
            user_states[user_id] = {'step': 'select_service'}
        elif text in [COMMANDS['front_end'], COMMANDS['back_end'], COMMANDS['mobile_dev']]:
            send_message(user_id, RESPONSE_MESSAGES['enter_description'], keyboard=None)
            user_states[user_id] = {'step': 'wait_description', 'type': text}
        else:
            send_message(user_id, RESPONSE_MESSAGES['invalid_option'], keyboard=coding_types_keyboard())

    elif state['step'] == 'faq':
        if text == COMMANDS['back']:
            send_message(user_id, RESPONSE_MESSAGES['faq_back'], keyboard=main_menu_keyboard())
            user_states[user_id] = {'step': 'start'}
        elif text in faq:
            send_message(user_id, faq[text], keyboard=faq_keyboard())
        else:
            send_message(user_id, RESPONSE_MESSAGES['invalid_option'], keyboard=faq_keyboard())

    elif state['step'] == 'free_chat':
        if text == COMMANDS['back_to_bot']:
            send_message(user_id, RESPONSE_MESSAGES['return_to_bot'], keyboard=main_menu_keyboard())
            user_states[user_id] = {'step': 'start'}

    elif state['step'] == 'contact_operator':
        if text == COMMANDS['back']:
            send_message(user_id, RESPONSE_MESSAGES['back_to_main'], keyboard=main_menu_keyboard())
            user_states[user_id] = {'step': 'start'}
        elif text == COMMANDS['leave_message']:
            send_message(user_id, RESPONSE_MESSAGES['enter_description'], keyboard=None)
            user_states[user_id] = {'step': 'leave_message'}
        elif text == COMMANDS['start_chat']:
            available_operator = next((op_id for op_id, status in operator_status.items() if status), None)
            if available_operator:
                operator_status[available_operator] = False
                send_message(user_id, f"Вы подключены к оператору {available_operator}.", keyboard=free_chat_keyboard())
                send_message(available_operator, f"Пользователь {user_id} подключен к вам.", keyboard=None)
                user_states[user_id] = {'step': 'chatting', 'operator_id': available_operator}
            else:
                send_message(user_id, RESPONSE_MESSAGES['all_operators_busy'], keyboard=contact_operator_keyboard())
        else:
            send_message(user_id, RESPONSE_MESSAGES['invalid_option'], keyboard=contact_operator_keyboard())

    elif state['step'] == 'wait_description':
        service_type = state.get('type')
        send_message(user_id, RESPONSE_MESSAGES['order_received'], keyboard=main_menu_keyboard())
        notify_operators(f"Новый заказ на {service_type} от пользователя {user_id}: {text}")
        user_states[user_id] = {'step': 'start'}

    elif state['step'] == 'operator_commands':
        if text == COMMANDS['change_status']:
            if user_id in OPERATOR_IDS:
                send_message(user_id, RESPONSE_MESSAGES['status_updated'], keyboard=operator_commands_keyboard())
                notify_operators(f"Один из админов сменил статус. {operator_status}")
                user_states[user_id] = {'step': 'change_status'}
        elif text == COMMANDS['back']:
            send_message(user_id, RESPONSE_MESSAGES['back_to_main'], keyboard=main_menu_keyboard())
            user_states[user_id] = {'step': 'start'}

    elif state['step'] == 'leave_message':
        send_message(user_id, RESPONSE_MESSAGES['message_received'], keyboard=main_menu_keyboard())
        notify_operators(f"Новое сообщение от пользователя {user_id}: {text}")
        user_states[user_id] = {'step': 'start'}

    elif state['step'] == 'chatting':
        operator_id = state.get('operator_id')
        if operator_id:
            send_message(operator_id, f"Сообщение от пользователя {user_id}: {text}", keyboard=None)
        else:
            send_message(user_id, RESPONSE_MESSAGES['invalid_option'], keyboard=free_chat_keyboard())


    elif state['step'] == 'wait_description':
        service_type = state.get('type')
        send_message(user_id, RESPONSE_MESSAGES['order_received'], keyboard=main_menu_keyboard())
        notify_operators(f"Новый заказ на {service_type} от пользователя {user_id}: {text}")
        user_states[user_id] = {'step': 'start'}

    elif state['step'] == 'leave_message':
        send_message(user_id, RESPONSE_MESSAGES['message_received'], keyboard=main_menu_keyboard())
        notify_operators(f"Новое сообщение от пользователя {user_id}: {text}")
        user_states[user_id] = {'step': 'start'}

    elif state['step'] == 'chatting':
        operator_id = state.get('operator_id')
        if operator_id:
            send_message(operator_id, f"Сообщение от пользователя {user_id}: {text}", keyboard=None)
        else:
            send_message(user_id, RESPONSE_MESSAGES['invalid_option'], keyboard=free_chat_keyboard())

# Основной цикл прослушивания сообщений
while True:
    try:
        for event in longpoll.listen():
            if event.type == VkEventType.MESSAGE_NEW and event.to_me and event.text:
                handle_message(event.user_id, event.text)
    except Exception as e:
        print(f"Произошла ошибка: {e}")
        restart_script()
