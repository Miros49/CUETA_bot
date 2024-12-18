LEXICON: dict[str, str | list[str]] = {
    'dev': '⚙️ В разработке...',
    'error_occurred': 'Что-то пошло не так... 🤕\n'
                      'Пожалуйста, обратитесь к администрации: @Miros49\n'
                      'Приносим свои извинения.',
    'start': '<b>Привет! 👋\n\n'
             'Ты в <code>CUETA</code> – месте, где тусовки и турниры становятся незабываемыми! 😎</b>',
    'ref_error': 'Вы не можете играть с собой же в команде.\nВам нужно скинуть ссылку другу 😉',
    'ref_abuse': 'Так нельзя! 🙂‍↔️\nВы не можете участвовать в нескольких командах одновременно',
    'help': 'Пожалуйста, дайте нам знать, если у вас появились:\n'
            '- Организационные вопросы: @ShIN_66\n'
            '- Технические вопросы: @Miros49\n\n'
            'Мы всегда рады помочь вам!',
    'no_upcoming_events': '<b>Похоже, что на данный момент нет запланированных мероприятий 😴</b>',
    'events_list': '<b>📋 Список ближайших мероприятий:</b>',
    'new_event_notification': '<b>🏷 Название: <code>{}</code>\n'
                              '📝 Описание: {}\n'
                              '📆 Дата: <i>{}</i></b>',
    'event_info': '<b>🏷 Название: <code>{}</code>\n'
                  '📝 Описание: {}\n'
                #  '📆 Дата: <i>{}</i>'
                  '{}</b>',
    'you_need_to_sign_in': '<b>Похоже, вы ещё не зарегистрировались в системе.\n'
                           'Введите, пожалуйста, Ваше <u>ФИО</u>:</b>',
    'sign_in_enter_date_of_birth': '<b>Приятно познакомиться, {}! 😊\n'
                                   'Теперь укажи, пожалуйста, дату твоего рождения </b>',
    'sign_in_enter_date_of_birth_again': '<b>{} 🤕\n'
                                         'Попробуй ещё раз:</b>',
    'sign_in_enter_status': '<b>Хорошо!\nТеперь укажи свой статус:</b>\n',
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
                            '🔹 Статус: {}\n'
                            '📱 Номер телефона: <code>{}</code></b>',
    'registration_to_event_confirmed': '<b>✅ Вы зарегистрированы на мероприятие <u>{}</u>, '
                                       'которое состоится <code>{}</code></b>',
    'profile_message': '<b>🪪 ФИО: <i>{}</i>\n'
                       '📆 Дата рождения: <code>{}</code>\n'
                       '🔹 Статус: {}\n'
                       '📱 Номер телефона: <code>{}</code></b>',
    'change_profile_message': 'Что вы хотите поменять?',

    'beer_pong_registration_player': 'Скажите текст\nЕсть команда?',
    'beer_pong_registrate_team': '<b>Отлично! 😎\n'
                                 'Отправь <a href="{}">эту ссылку</a> своему напарнику для регистрации команды</b>',
    'beer_pong_solo': '<b>✅ Ты успешно зарегистрирован!\n'
                      '👀 Уже ищем для тебя напарника!\n'
                      'Совсем скоро свяжем вас</b>',
    'beer_pong_team_registered': '<b>✅ Регистрация команды завершена!\n\n'
                                 'Напарник: @{}\n'
                                 'Номер команды: <code>{}</code>.\n\n'
                                 'До встречи на мероприятии! 🤗</b>',
    'beer_pong_team_just_created': '<b>✅ Мы подобрали для тебя напарника для участия в мероприятии '
                                   '<u>{}</u> - @{}.\nКоманда зарегистрирована под номером <code>{}</code>.\n'
                                   'До встречи на мероприятии! 😉</b>',
    'beer_pong_registration_team_errored': '<b>Кажется, что-то пошло не так... 🤕\n'
                                           'Пожалуйста, свяжитесь с администрацией для '
                                           'регистрации команды вручную: @Miros49.\n'
                                           'Приносим извинения за неудобства</b>',

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
    'profile': '👤 Профиль',
    'help': 'ℹ️ Помощь',
    'menu': 'Меню',
    'back_to_menu': 'В меню',
    'event_registration_standard': '📝 Зарегистрироваться',
    'event_registration_fast': '⚡️ Фаст-регистрация',
    'confirm_registration': '✅ Всё верно',
    'cancel_registration': '❌ Отмена',
    'registration_status_bachelor-cu': 'Бакалавр ЦУ',
    'registration_status_master-cu': 'Магистрант ЦУ',
    'registration_status_other': 'Другое',
    'back': '⏪ Назад',
    'change_profile_info': 'Изменить информацию о себе',
    'change_name': 'Изменить ФИО',
    'change_date_of_birth': 'Изменить дату рождения',
    'change_status': 'Изменить свой статус',
    'change_phone_number': 'Изменить номер телефона',


    'beer_pong_registration_visitor': '👀 Приду посмотреть (бесплатно)',
    'beer_pong_registration_player': '🍺 Буду играть! (1000₽)',
    'beer_pong_player_team_registration': '🤝 У меня есть напарник',
    'beer_pong_player_team_creation': '🤚 У меня нет напарника',

    'admin_mailing': '📢 Рассылка',
    'admin_events': '📋 Мероприятия',
    'admin_back_to_menu': '⏪ В меню',
    'admin_create_event': '➕ Добавить мероприятие',
    'admin_creation_of_event_confirm': '✅ Подтвердить',
    'admin_creation_of_event_cancel': '❌ Отменить',
    'admin_edit_event': '✏️ Изменить мероприятие',
}

callbacks: dict[str, str] = {
    buttons['upcoming_events']: 'events_button',
    buttons['profile']: 'profile_button',
    buttons['help']: 'help_button',
    buttons['event_registration_standard']: 'register_for_the_event_standard_{}',
    buttons['event_registration_fast']: 'register_for_the_event_fast_{}',
    buttons['confirm_registration']: 'registration_confirmed',
    buttons['cancel_registration']: 'registration_canceled',
    buttons['registration_status_bachelor-cu']: 'registration_status_bachelor-cu',
    buttons['registration_status_master-cu']: 'registration_status_master-cu',
    buttons['registration_status_other']: 'registration_status_other',
    buttons['change_profile_info']: 'change_profile_info_button',
    buttons['change_name']: 'change_name_button',
    buttons['change_date_of_birth']: 'change_date_of_birth_button',
    buttons['change_status']: 'change_status_button',
    buttons['change_phone_number']: 'change_phone_number_button',
    buttons['back']: 'back_button',

    buttons['beer_pong_registration_visitor']: 'beer_pong_registration_visitor',
    buttons['beer_pong_registration_player']: 'beer_pong_registration_player',
    buttons['beer_pong_player_team_registration']: 'beer_pong_player_team_registration',
    buttons['beer_pong_player_team_creation']: 'beer_pong_player_team_creation',
    'cancel_registration_on_beer_pong': 'cancel_registration_beer_pong_{}',

    buttons['admin_mailing']: 'admin_mailing',
    buttons['admin_events']: 'admin_events',
    buttons['admin_back_to_menu']: 'admin_main_menu',
    buttons['admin_create_event']: 'admin_create_event',
    buttons['admin_creation_of_event_confirm']: 'admin_creation_of_event_confirm',
    buttons['admin_creation_of_event_cancel']: 'admin_creation_of_event_cancel',
    buttons['admin_edit_event']: 'admin_edit_event_{}',
}

status_callback_to_string: dict[str, str] = {
    'registration_status_bachelor-cu': buttons['registration_status_bachelor-cu'],
    'registration_status_master-cu': buttons['registration_status_master-cu'],
    'registration_status_other': buttons['registration_status_other']
}
