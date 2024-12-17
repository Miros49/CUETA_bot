LEXICON: dict[str, str | list[str]] = {
    'dev': '⚙️ В разработке...',
    'error_occurred': 'Упс... Произошла ошибка, приносим свои извинения',
    'start': '<b>Привет! 👋\n\n'
             'Ты в <code>CUETA</code> – месте, где тусовки и турниры становятся незабываемыми! 😎</b>',
    'notifications': '<b>🔔 Хотите получать уведомления о новых тусовках и турнирах?</b>',
    'notifications_turned_on': '<b>Отлично, теперь ты не пропустишь ни одной движухи! 😎</b>',
    'notifications_turned_off': '<b>Мы не будем присылать тебе анонсы новых мероприятий</b>',
    'no_upcoming_events': '<b>Похоже, что на данный момент нет запланированных мероприятий 😴\n\n'
                          'Чтобы не пропустить анонс новых мероприятий, советуем <u>включить уведомления</u></b>',
    'events_list': '<b>📋 Список ближайших мероприятий:</b>',
    'new_event_notification': '<b>Тут уже сами текст поправите:\n\n'
                              '🏷 Название: <code>{}</code>\n'
                              '📝 Описание: {}\n'
                              '📆 Дата: <i>{}</i></b>',
    'event_info': '<b>Тут уже сами текст поправите:\n\n'
                  '🏷 Название: <code>{}</code>\n'
                  '📝 Описание: {}\n'
                  '📆 Дата: <i>{}</i></b>',
    'you_need_to_sign_in': '<b>Похоже, вы ещё не зарегистрировались в системе.\n'
                           'Введите, пожалуйста, Ваше <u>ФИО</u>:</b>',
    'sign_in_enter_date_of_birth': '<b>Приятно познакомиться, {}! 😊\n'
                                   'Теперь укажи, пожалуйста, дату твоего рождения </b>',
    'sign_in_enter_status': '<b>Хорошо! Теперь укажи свой статус:\n'
                            '🔹 <code>Бакалавр ЦУ</code>\n🔹 <code>Магистрант ЦУ</code>\n🔹<code>Другое</code></b>',
    'sign_in_enter_status_again': '<b>Статус введён некорректно 🤕\n Пожалуйста, выбери один из этих вариантов:\n'
                                  '🔹 <code>Бакалавр ЦУ</code>\n🔹 <code>Магистрант ЦУ</code>\n '
                                  '🔹<code>Другое</code></b>',
    'sign_in_enter_phone_number': '<b>Отлично! Осталось только указать номер телефона 😉</b>',
    'sign_in_enter_phone_number_additional': '<b>Можешь <i>нажать на кнопку снизу 👇</i>, либо написать его вручную</b>',
    'sign_in_enter_phone_number_again': '<b>{} 🤕\n'
                                        'Попробуй ещё раз:</b>',
    'sign_in_confirmation': '<b><u>Всё верно?</u>\n\n'
                            '🪪 ФИО: {}\n'
                            '📆 Дата рождения: <code>{}</code>\n'
                            '👤 Статус: {}\n'
                            '📱 Номер телефона: <code>{}</code></b>',
    'registration_to_event_confirmed': '<b>Вы зарегистрированы на мероприятие <u>{}</u>, '
                                       'которое состоится <code>{}</code></b>',

    'admin_menu': '<b>Здравствуйте, {}!</b>',
    'admin_add_event_name': '<b>Добавление мероприятия</b>\n\n'
                            '<i>🏷  Введите название мероприятия:</i>',
    'admin_add_event_description': '<b>Добавление мероприятия\n\n'
                                   '🏷 Название: <code>{}</code>\n'
                                   '📝 Введите описание мероприятия:</b>',
    'admin_add_event_date': '<b>Добавление мероприятия\n\n'
                            '🏷 Название: <code>{}</code>\n'
                            '📝 Описание: {}\n'
                            '📆 Введите дату мероприятия (в формате <code>ДД.ММ.ГГГГ ММ:ЧЧ</code>):</b>',
    'admin_create_event': '<b>Подтвердите создание мероприятия:\n\n'
                          '🏷 Название: <code>{}</code>\n'
                          '📝 Описание: {}\n'
                          '📆 Дата: <i>{}</i></b>',
    'admin_event_created': '<b>✅ Создано мероприятие:\n\n'
                           '🏷 Название: <code>{}</code>\n'
                           '📝 Описание: {}\n'
                           '📆 Дата: <i>{}</i></b>',
    'admin_event_creation_canceled': '<b>🗑 Создание мероприятия отменено</b>',
}

buttons: dict[str, str] = {
    'upcoming_events': '📋 Список ближайших мероприятий',
    'notifications': '📨 Уведомления',
    'help': 'ℹ️ Помощь',
    'turn_notifications_on': '✅ Да',
    'turn_notifications_off': '❌ Нет',
    'register': '📝 Зарегистрироваться',
    'confirm_registration': '✅ Всё верно',
    'cancel_registration': '❌ Отмена',

    'admin_mailing': '📢 Рассылка',
    'admin_events': '📋 Мероприятия',
    'admin_back_to_menu': '⏪ В меню',
    'admin_create_event': '➕ Добавить мероприятие',
    'admin_creation_of_event_confirm': '✅ Подтвердить',
    'admin_creation_of_event_cancel': '❌ Отменить',
    'admin_edit_event': '✏️ Изменить мероприятие',

}

callbacks: dict[str, str] = {
    buttons['notifications']: 'notifications_button',
    buttons['upcoming_events']: 'events_button',
    buttons['help']: 'help_button',
    buttons['turn_notifications_on']: 'turn_notifications_on',
    buttons['turn_notifications_off']: 'turn_notifications_off',
    buttons['register']: 'register_for_the_event_{}',
    buttons['confirm_registration']: 'registration_confirmed',
    buttons['cancel_registration']: 'registration_canceled',

    buttons['admin_mailing']: 'admin_mailing',
    buttons['admin_events']: 'admin_events',
    buttons['admin_back_to_menu']: 'admin_main_menu',
    buttons['admin_create_event']: 'admin_create_event',
    buttons['admin_creation_of_event_confirm']: 'admin_creation_of_event_confirm',
    buttons['admin_creation_of_event_cancel']: 'admin_creation_of_event_cancel',
    buttons['admin_edit_event']: 'admin_edit_event_{}',
}

other: dict[str, str | list[str]] = {
    'statuses': ['Бакалавр ЦУ', 'Магистрант ЦУ', 'Другое']
}
