import vk_api
from vk_api.longpoll import VkLongPoll, VkEventType
from vk_api.keyboard import VkKeyboard, VkKeyboardColor
from config import VK_TOKEN, GROUP_ID, OPERATOR_IDS

# Константы команд
COMMANDS = {
    'hello':'привет',
    'order':'заказать',
    'faq':'FAQ: ответы на вопросы',
    'contact_operator':'связь со специалистом',
    'free_chat':'выключить бота',
    'operator_commands': 'админка',
    'back': 'назад',
    'design': 'дизайн',
    'development': 'видео',
    'copywriting': 'кодинг',
    'logo': 'логотип',
    'banner': 'баннер',
    'web_design': 'веб-дизайн',
    'change_status': 'изменить статус',
    'start_chat': 'начать чат со специалистом',
    'leave_message': 'отправить собщение'
}

# Инициализация API
vk_session = vk_api.VkApi(token=VK_TOKEN)
vk = vk_session.get_api()
longpoll = VkLongPoll(vk_session)

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

def status_keyboard():
    """
    Создает клавиатуру для изменения статуса оператора.

    :return: Объект VkKeyboard с кнопками для выбора статуса.
    """
    keyboard = VkKeyboard(one_time=True)
    keyboard.add_button('Доступен', color=VkKeyboardColor.POSITIVE)
    keyboard.add_button('Недоступен', color=VkKeyboardColor.NEGATIVE)
    keyboard.add_line()
    keyboard.add_button(COMMANDS['back'], color=VkKeyboardColor.SECONDARY)
    return keyboard

def operator_commands_keyboard():
    """
    Создает клавиатуру для команд оператора.

    :return: Объект VkKeyboard с кнопками для операторских команд.
    """
    keyboard = VkKeyboard(one_time=True)
    keyboard.add_button('Сменить статус активности', color=VkKeyboardColor.POSITIVE)
    keyboard.add_button('Показать статусы активности операторов', color=VkKeyboardColor.PRIMARY)
    keyboard.add_line()
    keyboard.add_button(COMMANDS['back'], color=VkKeyboardColor.NEGATIVE)
    return keyboard

def free_chat_keyboard():
    """
    Создает клавиатуру для режима свободного общения.

    :return: Объект VkKeyboard с кнопкой для возврата к боту.
    """
    keyboard = VkKeyboard(one_time=True)
    keyboard.add_button(COMMANDS['back'], color=VkKeyboardColor.POSITIVE)
    return keyboard

def faq_keyboard():
    """
    Создает клавиатуру для выбора вопросов из FAQ.

    :return: Объект VkKeyboard с кнопками для вопросов FAQ.
    """
    keyboard = VkKeyboard(one_time=False)
    for question in faq.keys():
        keyboard.add_button(question, color=VkKeyboardColor.PRIMARY)
        keyboard.add_line()
    keyboard.add_button(COMMANDS['back'], color=VkKeyboardColor.NEGATIVE)
    return keyboard

def handle_message(user_id, text):
    """
    Обрабатывает сообщения пользователей и управляет состоянием диалога.

    :param user_id: ID пользователя, отправившего сообщение.
    :param text: Текст сообщения.
    """
    text = text.strip().lower()  # Приводим текст к нижнему регистру и убираем пробелы по краям

    # Обработка состояния свободного общения
    if user_states.get(user_id, {}).get('step') == 'free_chat':
        if text == COMMANDS['back']:
            user_states[user_id]['step'] = 'start'
            send_message(user_id, 'Вы вернулись к общению с ботом. Выберите опцию:', keyboard=main_menu_keyboard())
        else:
            send_message(user_id, 'Вы находитесь в режиме свободного общения. Нажмите "Перейти к боту", чтобы вернуться.', keyboard=free_chat_keyboard())
        return

    # Получаем текущее состояние пользователя
    state = user_states.get(user_id, {'step': 'start'})

    # Основная обработка команд
    if state['step'] == 'start':
        command = next((cmd for cmd, alias in COMMANDS.items() if alias.lower() in text), None)
        
        if command == 'hello':
            send_message(user_id, 'Здравствуйте! Выберите опцию:', keyboard=main_menu_keyboard())
        elif command == 'order':
            send_message(user_id, 'Выберите услугу:', keyboard=order_services_keyboard())
            user_states[user_id] = {'step': 'select_service'}
        elif command == 'faq':
            send_message(user_id, 'Выберите вопрос:', keyboard=faq_keyboard())
            user_states[user_id] = {'step': 'faq'}
        elif command == 'contact_operator':
            send_message(user_id, 'Выберите действие:\n1. Оставить сообщение\n2. Начать чат с оператором', keyboard=contact_operator_keyboard())
            user_states[user_id] = {'step': 'contact_operator'}
        elif command == 'change_status':
            if user_id in OPERATOR_IDS:
                send_message(user_id, 'Выберите новый статус:', keyboard=status_keyboard())
                user_states[user_id] = {'step': 'change_status'}
            else:
                send_message(user_id, 'Вы не имеете прав для изменения статуса.', keyboard=main_menu_keyboard())
        elif command == 'free_chat':
            user_states[user_id] = {'step': 'free_chat'}
            send_message(user_id, 'Вы вошли в режим свободного общения. Нажмите "Перейти к боту", чтобы вернуться.', keyboard=free_chat_keyboard())
        elif command == 'operator_commands':
            if user_id in OPERATOR_IDS:
                send_message(user_id, 'Выберите команду:', keyboard=operator_commands_keyboard())
                user_states[user_id] = {'step': 'operator_commands'}
            else:
                send_message(user_id, 'Эта команда доступна только для операторов.', keyboard=main_menu_keyboard())
        else:
            send_message(user_id, 'Пожалуйста, выберите корректную опцию.', keyboard=main_menu_keyboard())
    elif state['step'] == 'select_service':
        if text == COMMANDS['back']:
            send_message(user_id, 'Возвращаемся в главное меню.', keyboard=main_menu_keyboard())
            user_states[user_id] = {'step': 'start'}
        elif text in [COMMANDS['design'], COMMANDS['development'], COMMANDS['copywriting']]:
            send_message(user_id, 'Выберите тип услуги:', keyboard=design_types_keyboard())
            user_states[user_id] = {'step': 'select_type'}
        else:
            send_message(user_id, 'Пожалуйста, выберите корректную услугу.', keyboard=order_services_keyboard())
    elif state['step'] == 'select_type':
        if text == COMMANDS['back']:
            send_message(user_id, 'Выберите услугу:', keyboard=order_services_keyboard())
            user_states[user_id] = {'step': 'select_service'}
        elif text in [COMMANDS['logo'], COMMANDS['banner'], COMMANDS['web_design']]:
            send_message(user_id, 'Введите описание проекта:', keyboard=None)
            user_states[user_id] = {'step': 'wait_description', 'type': text}
        else:
            send_message(user_id, 'Пожалуйста, выберите корректный тип услуги.', keyboard=design_types_keyboard())
    elif state['step'] == 'wait_description':
        description = text.strip()
        service_type = state.get('type', 'Неизвестно')
        chat_link = f'https://vk.com/gim209325953?sel={user_id}'
        notify_operators(f'Новый заказ от пользователя {user_id}. Тип услуги: {service_type}. Описание проекта: {description}. Ссылка на чат: {chat_link}')
        send_message(user_id, 'Ваш заказ принят. Операторы уведомлены.', keyboard=main_menu_keyboard())
        user_states[user_id] = {'step': 'start'}
    elif state['step'] == 'contact_operator':
        if text == COMMANDS['back']:
            send_message(user_id, 'Выберите опцию:', keyboard=main_menu_keyboard())
            user_states[user_id] = {'step': 'start'}
        elif text == COMMANDS['leave_message']:
            send_message(user_id, 'Введите ваше сообщение:', keyboard=None)
            user_states[user_id] = {'step': 'wait_message'}
        elif text == COMMANDS['start_chat']:
            if any(operator_status.get(op_id, False) for op_id in OPERATOR_IDS):
                notify_operators(f'Пользователь {user_id} хочет начать чат. Ссылка на чат: https://vk.com/gim209325953?sel={user_id}')
                send_message(user_id, 'Операторы уведомлены. Пожалуйста, ожидайте ответа.', keyboard=main_menu_keyboard())
            else:
                send_message(user_id, 'В данный момент все операторы заняты. Пожалуйста, попробуйте позже.', keyboard=main_menu_keyboard())
            user_states[user_id] = {'step': 'start'}
        else:
            send_message(user_id, 'Пожалуйста, выберите корректное действие.', keyboard=contact_operator_keyboard())
    elif state['step'] == 'wait_message':
        message = text.strip()
        chat_link = f'https://vk.com/gim209325953?sel={user_id}'
        notify_operators(f'Сообщение от пользователя {user_id}: {message}. Ссылка на чат: {chat_link}')
        send_message(user_id, 'Ваше сообщение отправлено. Операторы уведомлены.', keyboard=main_menu_keyboard())
        user_states[user_id] = {'step': 'start'}
    elif state['step'] == 'change_status':
        if text == COMMANDS['back']:
            send_message(user_id, 'Выберите опцию:', keyboard=main_menu_keyboard())
            user_states[user_id] = {'step': 'start'}
        elif text == 'доступен':
            operator_status[user_id] = True
            send_message(user_id, 'Ваш статус обновлен на "Доступен".', keyboard=main_menu_keyboard())
        elif text == 'недоступен':
            operator_status[user_id] = False
            send_message(user_id, 'Ваш статус обновлен на "Недоступен".', keyboard=main_menu_keyboard())
        else:
            send_message(user_id, 'Пожалуйста, выберите корректный статус.', keyboard=status_keyboard())
        user_states[user_id] = {'step': 'start'}
    elif state['step'] == 'faq':
        if text == COMMANDS['back']:
            send_message(user_id, 'Возвращаемся в главное меню.', keyboard=main_menu_keyboard())
            user_states[user_id] = {'step': 'start'}
        elif any(question.lower() in text for question in faq):
            # Находим наиболее подходящий вопрос и отправляем ответ
            matched_question = next((question for question in faq if question.lower() in text), None)
            if matched_question:
                send_message(user_id, faq[matched_question], keyboard=faq_keyboard())
            else:
                send_message(user_id, 'Пожалуйста, выберите корректный вопрос из FAQ или вернитесь в главное меню.', keyboard=faq_keyboard())
        else:
            send_message(user_id, 'Пожалуйста, выберите корректный вопрос или вернитесь в главное меню.', keyboard=faq_keyboard())
    elif state['step'] == 'operator_commands':
        if text == COMMANDS['back']:
            send_message(user_id, 'Возвращаемся в главное меню.', keyboard=main_menu_keyboard())
            user_states[user_id] = {'step': 'start'}
        elif text == 'сменить статус активности':
            send_message(user_id, 'Выберите новый статус:', keyboard=status_keyboard())
            user_states[user_id] = {'step': 'change_status'}
        elif text == 'показать статусы активности операторов':
            statuses = "\n".join(f"Оператор {op_id}: {'Доступен' if status else 'Недоступен'}" for op_id, status in operator_status.items())
            send_message(user_id, f"Статусы активности операторов:\n{statuses}", keyboard=operator_commands_keyboard())
        else:
            send_message(user_id, 'Пожалуйста, выберите корректное действие.', keyboard=operator_commands_keyboard())

def main():
    """
    Основная функция для прослушивания и обработки событий.
    """
    for event in longpoll.listen():
        if event.type == VkEventType.MESSAGE_NEW and event.to_me and event.text:
            handle_message(event.user_id, event.text)

if __name__ == '__main__':
    main()
