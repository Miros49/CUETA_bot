LEXICON: dict[str, str | list[str]] = {
    # -----------------------------   USER   ----------------------------- #
    'dev': '⚙️ В разработке...',
    'error_occurred': 'Что-то пошло не так... 🤕\n'
                      'Пожалуйста, обратитесь к администрации: @ShIN_66 | @Miros49\n'
                      'Приносим свои извинения.',
    'start': '<b>Привет! 👋\n\n'
             'Ты в <a href="">CUETA</a> – месте, где тусовки и турниры становятся незабываемыми! 😎</b>',
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
    # 'event_info': '<b>🏷 Название: <code>{}</code>\n'
    #               '📝 Описание: {}\n'
    #               '📆 Дата: <i>{}</i>'
    #               '{}</b>',
    'event_info': '{}'
                  '<b>{}</b>',
    'you_need_to_sign_in': '<b>Похоже, вы ещё не зарегистрировались в системе.\n'
                           'Введите, пожалуйста, Ваше <u>ФИО</u>:</b>',
    'sign_in_enter_name': '<b>Введите, пожалуйста, Ваше <u>ФИО</u>:</b>',
    'sign_in_enter_name_again': "<b>Неверный формат ввода 🤕\n"
                                "Пожалуйста, попробуйте ещё раз (в формате 'Фамилия Имя Отчество'):</b>",
    'sign_in_enter_date_of_birth': '<b>Приятно познакомиться, {}! 😊\n'
                                   'Теперь укажи, пожалуйста, дату твоего рождения '
                                   '(в формате <code>ДД.ММ.ГГГГ</code>):\n\n'
                                   'Пожалуйста, указывайте реальную дату рождения.\n'
                                   'На входе мы будем проверять паспорт</b>',
    'sign_in_enter_date_of_birth_again': '<b>{}\n'
                                         'Попробуй ещё раз:</b>',
    'sign_in_enter_status': '<b>Хорошо!\nТеперь укажи свой статус:</b>\n',
    'sign_in_enter_phone_number': '<b>Отлично! Осталось только указать номер телефона 😉</b>',
    'sign_in_enter_phone_number_additional': '<b>Можешь <i>нажать на кнопку снизу 👇</i>, либо написать его вручную</b>',
    'sign_in_enter_phone_number_again': '<b>{} 🤕\n'
                                        'Попробуй ещё раз:</b>',
    'sign_in_confirmation': '<b><u>Всё верно?</u>\n\n'
                            '🪪 ФИО: {}\n'
                            '📆 Дата рождения: <code>{}</code>\n'
                            '🔹 Статус: {}\n'
                            '📱 Номер телефона: <code>{}</code></b>',
    'pre-registration_to_event_confirmed': '\n\n✅ Оформлена предрегистрация на мероприятие.\nСкоро свяжемся с тобой 😎',
    'pre-registration_mailing': '<b>¡Amigos!</b>\n'
                                'Спасибо за предрегистрацию на <b>MEXICAN PARTY</b>.\n'
                                'У вас есть <u>3 дня</u>, чтобы выкупить билет по стартовой '
                                'цене — 2500 ₽., затем цена повысится.\n\n'
                                'Что входит в билет?\n'
                                '• Безлимитные мексиканские закуски\n'
                                '• FREE bar (алко/безалко)\n'
                                '• Тир, лимбо, дартс\n'
                                '• Грим, фотозона и фотограф\n\n'
                                'Когда и где?\n'
                                '<b>1 февраля, с 22:00 до 5:00</b>, в <a href="https://yandex.ru/maps/org/'
                                '161816133691">HAWAI HOUSE LOFT</a>.\n\n'
                                '<b>Как купить билет?</b>\n'
                                '1. <b>Оплатите</b> переводом по номеру: <code>{}</code> (<b>{}</b>).\n'
                                '2. <b>Подтвердите оплату</b>: нажми на кнопку снизу и пришли чек в чат.\n\n'
                                'Остались вопросы?\n'
                                'Свяжитесь с организатором: @{}\n\n'
                                'Ждём вас на самой жаркой вечеринке февраля!\n'
                                '<b>¡Hasta pronto!</b>',
    'pre-registration_mailing_underage': '<b>¡Amigos!</b>\n'
                                         'Спасибо за предрегистрацию на <b>MEXICAN PARTY</b>.\n'
                                         'У вас есть <u>3 дня</u>, чтобы выкупить билет по стартовой '
                                         'цене — 2500 ₽., затем цена повысится.\n\n'
                                         'Поскольку тебе нет 18 лет, пусть <u>родители обязательно заполнят</u> '
                                         '<a href="https://docs.google.com/document/d/153ABy5ZqApFK3TKiH7Eh_7IHS2m_'
                                         'EsAA/edit?usp=sharing&ouid=100133804037697762729&rtpof=true&sd=true">этот '
                                         'документ</a>. Пожалуйста, пришли фото или скан согласия родителей '
                                         'организатору (контакты указаны ниже). Не забудь, что оригинал '
                                         'необходимо будет взять с собой на мероприятие.\n\n'
                                         'Что входит в билет?\n'
                                         '• Безлимитные мексиканские закуски\n'
                                         '• FREE bar (алко/безалко)\n'
                                         '• Тир, лимбо, дартс\n'
                                         '• Грим, фотозона и фотограф\n\n'
                                         'Когда и где?\n'
                                         '<b>1 февраля, с 22:00 до 5:00</b>, в <a href="https://yandex.ru/maps/org/'
                                         '161816133691">HAWAI HOUSE LOFT</a>.\n\n'
                                         '<b>Как купить билет?</b>\n'
                                         '1. Пришлите фото или скан согласия родителей организатору (@{})\n'
                                         '2. <b>Оплатите</b> переводом по номеру: <code>{}</code> (<b>{}</b>).\n'
                                         '3. <b>Подтвердите оплату</b>: нажми на кнопку снизу и пришли чек в чат.\n\n'
                                         'Остались вопросы?\n'
                                         'Свяжитесь с организатором: @{}\n\n'
                                         'Ждём вас на самой жаркой вечеринке февраля!\n'
                                         '<b>¡Hasta pronto!</b>',
    'seems_like_your_profile_unfilled': '<b>Для начала давайте заполним твой профиль 😉\n'
                                        'Введите, пожалуйста, Ваше <u>ФИО</u>:</b>',
    'pre-registration_mailing_no_profile': '<b>¡Amigos!</b>\n'
                                           'Спасибо за предрегистрацию на <b>MEXICAN PARTY</b>.\n'
                                           'У вас есть <u>3 дня</u>, чтобы выкупить билет по стартовой '
                                           'цене — 2500 ₽., затем цена повысится.\n\n'
                                           'Что входит в билет?\n'
                                           '• Безлимитные мексиканские закуски\n'
                                           '• FREE bar (алко/безалко)\n'
                                           '• Тир, лимбо, дартс\n'
                                           '• Грим, фотозона и фотограф\n\n'
                                           'Когда и где?\n'
                                           '<b>1 февраля, с 22:00 до 5:00</b>, в <a href="https://yandex.ru/maps/org/'
                                           '161816133691">HAWAI HOUSE LOFT</a>.\n\n'
                                           'Но для начала давай заполним твой профиль 😉',
    'enter_your_name': '<u>Введи, пожалуйста, своё ФИО:</u>\n'
                       'Без этого мы не сможем подтвердить твою регистрацию',
    'pre-registration_profile_filled': '<b>Отлично! Теперь можем вернуться к оплате 😊</b>',
    'mailing_for_others_mexican': '<b>MEXICAN PARTY | 01.02</b>\n'
                                  'ПРОДАЖИ ОТКРЫТЫ\n\n'
                                  '<i>Пиньяты, которые разлетаются конфетами, яркий грим в стиле Ла Катрины, '
                                  'зажигательные танцы и конкурс лимбо, где смех не прекращается.</i>\n\n'
                                  '1 февраля, 22:00 — 5:00\n'
                                  '<a href="https://yandex.ru/maps/org/161816133691">HAWAI HOUSE LOFT</a>\n\n'
                                  'Мы открываем продажу билетов по начальным ценам, в ограниченном количестве, '
                                  'так что не прозевай. 😉\n\n'
                                  'Информация и регистрация — по кнопке «📋 Список ближайших мероприятий»',
    'see_payment_instructions_below': '\nДля подтверждения регистрации необходимо осуществить оплату 👇',
    'payment_instructions': '<b>Как купить билет?</b>\n{}'
                            '{}. <b>Оплатите</b> переводом по номеру: <code>{}</code> ({}).\n'
                            '{}. <b>Подтвердите оплату</b>: нажми на кнопку снизу и пришли чек в чат.\n\n'
                            '<b>Остались вопросы?</b>\n'
                            'Свяжитесь с организатором: @{}\n'
                            'Ждём вас на самой жаркой вечеринке февраля!\n',
    'underage_instruction': '1. Пришлите фото или скан <a href="https://docs.google.com/document/'
                            'd/153ABy5ZqApFK3TKiH7Eh_7IHS2m_EsAA/edit?usp=sharing&ouid=100133804037697762729&'
                            'rtpof=true&sd=true">согласия родителей</a> организатору ({})\n',
    'profile_message': '<b>🪪 <u>Профиль</u>:\n'
                       '🔹 ФИО: <i>{name}</i>\n'
                       '🎂 Дата рождения: <code>{date_of_birth}</code>\n'
                       '📱 Телефон: <code>{phone_number}</code>\n'
                       '🔖 Статус: {status}\n\n'
                       '💰 Баланс: <code>{balance}</code> CUETA Coin{s}</b>',
    'change_profile_message': '<b>Выбери, что хочешь поменять:</b>',
    'change_name_message': '<b>Введи свои ФИО</b>',
    'change_status_message': '<b>Выбери новый статус 👇</b>',
    'change_phone_number_message': '<b>Введи новый номер телефона\n'
                                   'Можешь <i>нажать на кнопку снизу 👇</i>, либо написать его вручную</b>',

    'profile_change_successful': '✅ Успешная смена данных профиля!',
    'profile_change_failed': '🤕 Произошла ошибка, но мы над ней уже работаем!\n'
                             'Попробуй ещё раз или обратись за помощью к нам',
    
    'contact_your_fundraiser': 'Что-то пошло не так. '
                               'Пожалуйста, свяжись с назначенным тебе менеджером, если оплата всё ещё не завершена',

    'payment_confirmation_text': '<b>Хорошо! Пришлите, пожалуйста, файл или фото подтверждения оплаты:</b>',
    'payment_confirmation_text_again': '<b>Вам необходимо прислать файл или фото подтверждения оплаты.\n'
                                       'Попробуйте ещё раз:</b>',
    'top_up_balance_menu': '<b>Сколько CUETA Coins хочешь приобрести?</b> 💰\n'
                           '<blockquote>💵 100₽ = 1 CUETA Coin 🪙</blockquote>',
    'top_up_balance_manual_input': '<blockquote>💵 100₽ = 1 CUETA Coin 🪙</blockquote>\n\n'
                                   '<b>Введи нужное количество коинов</b> (только целое число):',
    'top_up_balance_manual_input_again': '<blockquote>💵 100₽ = 1 CUETA Coin 🪙</blockquote>\n\n'
                                         '<b>Вам необходимо ввести целое число монет, '
                                         'которое вы хотите приобрести:</b>',
    'top_up_balance_instructions': '<b>Для начисления <code>{}</code> CUETA Coin{}, следуйте инструкции:</b>\n\n'
                                   '1. <b>Переведите</b> <code>{}₽</code> по номеру: <code>{}</code> <u>{}</u>\n'
                                   '2. <b>Подтвердите оплату</b>: нажмите на кнопку снизу, '
                                   'а затем пришлите чек в этот чат.\n\n'
                                   'При возникновении трудностей, свяжитесь с организатором: @{}\n\n',
    'transaction_confirmed_contact_administrator': 'Эта транзакция уже подтверждена.\n'
                                                   'Для возврата обратитесь к администратору: @{}',

    # -----------------------------   ADMIN   ----------------------------- #
    'admin_menu': '<b>Здравствуйте, {}! 🤗</b>',
    'admin_add_event_name': '<b>Добавление мероприятия</b>\n\n'
                            '<i>🏷  Введите название мероприятия:</i>',
    'admin_add_event_description': '<b>Добавление мероприятия\n\n'
                                   '🏷 Название: <code>{}</code>\n'
                                   '📝 Введите описание мероприятия:</b>',
    'admin_add_event_date': '<b>Добавление мероприятия\n\n'
                            '🏷 Название: <code>{}</code>\n'
                            '📝 Описание: {}\n'
                            '📆 Введите дату мероприятия (в формате <code>ДД.ММ.ГГГГ ММ:ЧЧ</code>):</b>',
    'admin_add_event_card': '<b>Добавление мероприятия\n\n'
                            '🏷 Название: <code>{}</code>\n'
                            '📝 Описание: {}\n'
                            '📆 Дата: <i>{}</i>\n\n'
                            'Последний шаг: прикрепите карточку мероприятия (фото)</b>',
    'admin_create_event': '<b>🏷 Название: <code>{}</code>\n'
                          '📝 Описание: {}\n'
                          '📆 Дата: <i>{}</i>\n\n'
                          '<u>Подтвердите создание мероприятия</u></b>',
    'admin_event_created': '<b>🏷 Название: <code>{}</code>\n'
                           '📝 Описание: {}\n'
                           '📆 Дата: <i>{}</i></b>\n\n'
                           '✅ Мероприятие создано',
    'admin_event_creation_canceled': '<b>🗑 Создание мероприятия отменено</b>',
    'admin_mailing_options': '<b>Для кого сделать рассылку?</b>',
    'admin_enter_mailing_message': '<b>Введите сообщение для рассылки (не будет отправлено без подтверждения)</b>',
    'admin_overall_statistics': "📝 <u><b>Всего регистраций</b>: <code>{total}</code></u>\n"
                                "✅ <i><b>Подтверждённых:</b> <code>{confirmed}</code></i>\n"
                                "⏳ <b>Ожидает подтверждения:</b> <code>{waiting_for_confirmation}</code>\n"
                                "💸 <b>Производит оплату:</b> <code>{waiting_for_payment}</code>\n"
                                "☑️ <b>Готовы оплатить:</b> <code>{ready_to_pay}</code>\n"
                                "🔄 <b>Остальные:</b> <code>{processing}</code>",
    'admin_fundraiser_statistics': "<b>@{fundraiser_username}</b>\n"
                                   "💰 <u><b>Собрано денег:</b> <code>{collected_money}₽</code></u>\n"
                                   "📝 <b>Всего регистраций:</b> <code>{total}</code>\n"
                                   "✅ <i><b>Подтверждённых:</b> <code>{confirmed}</code></i>\n"
                                   "⏳ <b>Ожидает подтверждения:</b> <code>{waiting_for_confirmation}</code>\n"
                                   "💸 <b>Производит оплату:</b> <code>{waiting_for_payment}</code>\n"
                                   "☑️ <b>Готовы оплатить:</b> <code>{ready_to_pay}</code>\n\n",

    'temp_mailing_mexican_party': '<b>¡Amigo!</b>\n\n'
                                  'Напоминаем, что твой билет на <code>Mexican Party | 01.02</code> '
                                  'скоро будет аннулирован! 😱\n'
                                  'Из-за большого интереса к событию цена скоро повысится, но'
                                  'вы ещё можете оплатить билет <b>до конца дня</b> по старой цене.\n\n'
                                  'Не упустите шанс попасть на самую жаркую вечеринку этой зимы! 🌶\n\n'
                                  'Напоминаем, что для совершения оплаты вам необходимо:\n'
                                  '1. <b>Оплатить</b> переводом по номеру: <code>{}</code> (<b>{}</b>).\n'
                                  '2. <b>Подтвердить оплату</b>: нажми на кнопку снизу и пришли чек в чат.\n\n'
                                  'Остались вопросы?\n'
                                  'Свяжитесь с организатором: @{}\n\n',
    'temp_mailing_mexican_party_underage': '<b>¡Amigo!</b>\n\n'
                                           'Напоминаем, что твой билет на <code>Mexican Party | 01.02</code> '
                                           'скоро будет аннулирован! 😱\n'
                                           'Из-за большого интереса к событию цена скоро повысится, но'
                                           'вы ещё можете оплатить билет <b>до конца дня</b> по старой цене.\n\n'
                                           'Не упустите шанс попасть на самую жаркую вечеринку этой зимы! 🌶\n\n'
                                           'Напоминаем, что для совершения оплаты вам необходимо:\n'
                                           '1. Прислать фото или скан <a href="https://docs.google.com/document/'
                                           'd/153ABy5ZqApFK3TKiH7Eh_7IHS2m_EsAA/edit?usp=sharing&ouid=1001338040376'
                                           '97762729&rtpof=true&sd=true">согласия родителей</a> организатору (@{})\n'
                                           '2. <b>Оплатить</b> переводом по номеру: <code>{}</code> (<b>{}</b>).\n'
                                           '3. <b>Подтвердить оплату</b>: нажми на кнопку снизу и пришли чек в чат.\n\n'
                                           'Остались вопросы?\n'
                                           'Свяжитесь с организатором: @{}\n\n',

    # -----------------------------   FUNDRAISER   ----------------------------- #
    'fundraiser_transaction_confirmation_caption': '<b>Оплата на сумму <code>{}₽</code> от {}</b>\n'
                                                   '(Покупка {} CUETA Coins 🪙)',
}

buttons: dict[str, str] = {
    # ---------------------   USER   --------------------- #
    'upcoming_events': '📋 Список ближайших мероприятий',
    'profile': '👤 Профиль',
    'change_profile': '️✏️ Изменить информацию профиля',
    'change_name': 'Изменить ФИО',
    'change_date_of_birth': 'Изменить дату рождения',
    'change_phone_number': 'Изменить номер телефона',
    'change_status': 'Изменить статус',
    'help': 'ℹ️ Помощь',
    'back_button': '🔙 Назад',
    'menu': 'Меню',
    'back_to_menu': 'В меню',
    'event_registration_pre-registration': 'Предрегистрация',
    'event_registration_standard': '📝 Зарегистрироваться',
    'event_registration_premium': 'Премиум',
    'event_registration_fast': '⚡️ Фаст-регистрация',
    'confirm_registration': '✅ Всё верно',
    'cancel_registration': '❌ Отмена',
    'registration_status_bachelor-cu': 'Бакалавр ЦУ',
    'registration_status_master-cu': 'Магистрант ЦУ',
    'registration_status_t-bank': 'Сотрудник Т-Банка',
    'registration_status_other': 'Другое',

    # ---------------------   PAYMENT   --------------------- #
    'payment_confirmation_button': '✅ Скинуть подтверждении оплаты',
    'top_up_balance': '➕💰 Пополнить баланс',

    # ---------------------   ADMIN   --------------------- #
    'admin_mailing': '📢 Рассылка',
    'admin_events': '📋 Мероприятия',
    'admin_back_to_menu': '⏪ В меню',
    'admin_create_event': '➕ Добавить мероприятие',
    'admin_creation_of_event_confirm': '✅ Подтвердить',
    'admin_creation_of_event_cancel': '❌ Отменить',
    'admin_edit_event': '✏️ Изменить мероприятие',
    'admin_mailing_options_all': 'Для всех (пока не работает)',
    'admin_mailing_options_event-participants': 'Для посетителей Бир-Понга',
    'initiate_mailing': '📤 Начать рассылку',
}

callbacks: dict[str, str] = {
    # ---------------------   USER   --------------------- #
    buttons['upcoming_events']: 'events_button',
    buttons['profile']: 'profile_button',
    buttons['change_profile']: 'change_profile_button',
    buttons['change_name']: 'change_name_button',
    buttons['change_date_of_birth']: 'change_date_of_birth_button',
    buttons['change_phone_number']: 'change_phone_number_button',
    buttons['change_status']: 'change_status_button',
    buttons['help']: 'help_button',
    buttons['event_registration_pre-registration']: 'register_for_the_event_pre-registration_{}',
    buttons['event_registration_standard']: 'register_for_the_event_standard_{}',
    buttons['event_registration_premium']: 'register_for_the_event_premium_{}',
    buttons['event_registration_fast']: 'register_for_the_event_fast_{}',
    buttons['confirm_registration']: 'registration_confirmed',
    buttons['cancel_registration']: 'registration_canceled',
    buttons['registration_status_bachelor-cu']: 'registration_status_bachelor-cu',
    buttons['registration_status_master-cu']: 'registration_status_master-cu',
    buttons['registration_status_t-bank']: 'registration_status_t-bank',
    buttons['registration_status_other']: 'registration_status_other',

    # ---------------------   USER   --------------------- #
    buttons['payment_confirmation_button']: 'send_payment_confirmation_{}',
    'cancel_payment_confirmation_button': 'cancel_payment_confirmation_{}',
    buttons['top_up_balance']: 'top_up_balance_coins',
    'enter_coins_amount': 'top_up_balance_enter_coins_amount_{}',
    'confirm_transaction': 'transaction_confirmation_confirm_{}',
    'cancel_transaction': 'transaction_confirmation_cancel_{}',

    # ---------------------   Back   --------------------- #
    'profile_registration_back_to_name': 'profile_registration_back_to_name',
    'profile_registration_back_to_date_of_birth': 'profile_registration_back_to_date-of-birth',
    'profile_registration_back_to_status': 'profile_registration_back_to_status',
    'profile_registration_back_to_phone_number': 'profile_registration_back_to_phone-number',
    'back_to_profile': 'back_to_profile_button',

    # ---------------------   ADMIN   --------------------- #
    buttons['admin_mailing']: 'admin_mailing',
    buttons['admin_events']: 'admin_events',
    buttons['admin_back_to_menu']: 'admin_main_menu',
    buttons['admin_create_event']: 'admin_create_event',
    buttons['admin_creation_of_event_confirm']: 'admin_creation_of_event_confirm',
    buttons['admin_creation_of_event_cancel']: 'admin_creation_of_event_cancel',
    buttons['admin_edit_event']: 'admin_edit_event_{}',
    buttons['admin_mailing_options_all']: 'admin_mailing_options_all',
    buttons['admin_mailing_options_event-participants']: 'admin_mailing_options_event-participants',
    buttons['initiate_mailing']: 'admin_initiate_mailing',
}

status_callback_to_string: dict[str, str] = {
    'registration_status_bachelor-cu': buttons['registration_status_bachelor-cu'],
    'registration_status_master-cu': buttons['registration_status_master-cu'],
    'registration_status_other': buttons['registration_status_other'],
    'registration_status_t-bank': buttons['registration_status_t-bank']
}
