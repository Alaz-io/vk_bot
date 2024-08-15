import vk_api
from vk_api import VkUpload
from vk_api.longpoll import VkLongPoll, VkEventType
from vk_api.utils import get_random_id
from vk_api.keyboard import VkKeyboard, VkKeyboardColor
keyboard = VkKeyboard(one_time=True)
keyboard.add_button('Привет', color=VkKeyboardColor.SECONDARY)
keyboard.add_line()
keyboard.add_button('Привет', color=VkKeyboardColor.PRIMARY)
keyboard.add_line()
keyboard.add_button('Пока', color=VkKeyboardColor.POSITIVE)
keyboard.add_line()
keyboard.add_button('Третья кнопка', color=VkKeyboardColor.NEGATIVE)
keyboard.add_line()
keyboard.add_openlink_button('Ссылка', link='https://vk.com/AlazAlm')
def write_message(sender, message):
    authorize.method('messages.send', {'user_id': sender, 'message': message, 'random_id': get_random_id(), 'attachment': ','.join(attachments), 'keyboard': keyboard.get_keyboard()})
token = 'vk1.a.fBog8piwgA_Wgsg4RNjbFJNmeec9euqY4D50r4OwGHQrsEB1iBDnsww6seIeHwXa0eACFO617i8bDIwaKgpKyy4ndBv-_Wpu0ITY2B3oERLbcjX5tj7n0U_pxeeSt4vupEYzBHUXWYFXhXE8GX05IJ4-_dI-6x9PB1WqdqSlMA2Rkie8LV-WPs_8zQCI31p6T4v9ba_ORsv_REGwNiYV4g'
image = 'c:/Users/AlazAlm/Downloads/Локальный диск (D)/AlazAlm Studio/ALAZALM STUDIO/Пост6.png'
authorize = vk_api.VkApi(token = token)
longpoll = VkLongPoll(authorize)    
upload = VkUpload(authorize)
for event in longpoll.listen():
    if event.type == VkEventType.MESSAGE_NEW and event.to_me and event.text:
        reseived_message = event.text
        sender = event.user_id
        attachments =  []
        upload_image = upload.photo_messages(photos = image)[0]
        attachments.append('photo{}_{}'.format(upload_image['owner_id'], upload_image['id']))
        if reseived_message == 'Привет':
            write_message(sender, 'Добрый день! &#128142;')
        elif reseived_message == 'Пока':
            write_message(sender, 'Досвидания!')
        else:
            write_message(sender, 'Прямо сейчас ведётся разработка бота, приносим извинения, но Вы можете написать - мы прочтём!')