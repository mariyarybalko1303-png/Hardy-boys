#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import time
import sys

def print_slow(text, delay=0.015):
    """Prints text slowly for a vintage text adventure feel."""
    for char in text:
        sys.stdout.write(char)
        sys.stdout.flush()
        time.sleep(delay)
    print()

def display_header(lang):
    title_text = {
        'uk': "          НЕНСІ ДРЮ ТА БРАТИ ХАРДІ: ВЕЛИКА ЗМОВА В РІВЕР-ГАЙТС          ",
        'en': "      NANCY DREW & THE HARDY BOYS: THE RIVER HEIGHTS CONSPIRACY        ",
        'ru': "          НЭНСИ ДРЮ И БРАТЬЯ ХАРДИ: ВЕЛИКИЙ ЗАГОВОР В РИВЕР-ХАЙТС      "
    }
    subtitle_text = {
        'uk': "             Ювілейний Кросовер — Інтерактивний Текстовий Квест         ",
        'en': "             Anniversary Crossover — Interactive Text Quest            ",
        'ru': "             Юбилейный Кроссовер — Интерактивный Текстовый Квест       "
    }
    print("=" * 80)
    print(title_text[lang])
    print(subtitle_text[lang])
    print("=" * 80)
    print()

class GameState:
    def __init__(self):
        self.lang = 'uk'
        self.inventory = []
        self.route_taken = None  # 'nancy_frank' (logic/office) or 'joe_george' (action/docks)
        self.trap_solved_with = None
        self.score = 0

LOCALIZATION = {
    'uk': {
        'select_lang': "Оберіть мову / Select Language / Выберите язык:\n1. Українська\n2. English\n3. Русский",
        'lang_choice_prompt': "Ваш вибір (1-3): ",
        'press_enter': "Натисніть ENTER, щоб розпочати ювілейну пригоду...",
        'invalid_input': "Будь ласка, введіть 1 або 2.",
        'intro_text': (
            "Ласкаво просимо до 10-ї, ювілейної частини нашої детективної саги!\n"
            "Вперше в історії легендарна детективка Ненсі Дрю об'єднує зусилля з братами Френком та Джо Харді.\n"
            "Дія розгортається у затишному містечку Рівер-Гайтс, де дві команди розслідувачів зіткнуться\n"
            "із наймасштабнішою змовою міжнародного синдикату, яка загрожує репутації Карсона Дрю!"
        ),
        'act1_title': "\n--- АКТ I: ВЕЛИКИЙ БЕНКЕТ ТА ТАЄМНИЧИЙ ШИФР ---",
        'act1_text': (
            "У затишній вітальні будинку Дрю панує справжнє кулінарне протистояння!\n"
            "На столі красується легендарний теплий лимонний пиріг Ганни Груен із повітряною меренгою.\n"
            "Поруч Чет Мортон, який приїхав з хлопцями з Бейпорта, викладає коробку фірмової піци з пепероні\n"
            "та м'які булочки з корицею, що створює неймовірне поєднання ароматів.\n\n"
            "— Оце я розумію — детективний саміт! — радісно вигукує Чет, відкушуючи шматочок пирога і запиваючи його піцою.\n"
            "Бесс Марвін погоджується: — Ганно, ваш пиріг — це шедевр! Я готова розслідувати що завгодно, якщо у нас буде така вечеря!\n"
            "Джесс (Джордж) Фейн лише хитає головою: — Hypers! Бесс, ми приїхали сюди за серйозною справою!\n\n"
            "Ненсі Дрю викладає на стіл мідний циліндр та мікрочип синдикату «Восьминіг», знайдений братами.\n"
            "Френк Харді підключає чип до свого ноутбука: дані вказують на те, що корумпований прокурор Рівер-Гайтс\n"
            "намагається підставити батька Ненсі — адвоката Карсона Дрю, сфабрикувавши докази фінансових махінацій."
        ),
        'act1_q': "Хто очолить перший етап розслідування?",
        'act1_opt1': "1. [Група логіки: Ненсі та Френк] Вирушити до офісу Карсона Дрю, щоб знайти оригінали судових паперів та розгадати комп'ютерний пароль.",
        'act1_opt2': "2. [Група дії: Джо та Джордж] Вирушити на річковий причал, щоб простежити за таємничим кур'єром синдикату.",
        'act1_out1': (
            "\nНенсі та Френк діють методично. Вони пробираються до офісу Карсона Дрю.\n"
            "Френк підключає дешифратор до сейфа, а Ненсі аналізує робочий стіл батька.\n"
            "Тут вони виявляють, що комп'ютер заблоковано складною системою захисту синдикату.\n"
            "Щоб розкрити файли, їм необхідно розгадати пароль, заснований на латинському написі над каміном:\n"
            "«JUSTITIA VINCIT» (Справедливість перемагає)."
        ),
        'act1_out2': (
            "\nРевіння двигунів синього родстера Ненсі та мотоцикла Джо розриває нічну тишу Рівер-Гайтс!\n"
            "Джо Харді та Джордж Фейн мчать до туманного річкового причалу.\n"
            "Там вони помічають підозрілого чоловіка в темному плащі, який передає металевий кейс охоронцю.\n"
            "Джо та Джордж вирішують діяти без зайвих розмов і влаштувати засідку."
        ),
        'act2_title': "\n--- АКТ II: РОЗГАДКИ ТА ЗАСІДКИ ---",
        'act2_q_logic': "Введіть пароль для розблокування комп'ютера синдикату (підказка: латинський напис з офісу великими літерами):",
        'act2_logic_success': (
            "\nВітаємо! Пароль правильний! Файли розблоковано.\n"
            "Ненсі та Френк знаходять копії фальшивих контрактів і дізнаються, що головний доказ синдикату —\n"
            "оригінальна печатка — схована у сейфі старого закинутого театру 'Глобус' на околиці міста."
        ),
        'act2_logic_fail': (
            "\nПароль невірний! Спрацьовує безшумна сигналізація синдикату.\n"
            "Ненсі та Френк встигають скопіювати лише частину даних про закинутий театр 'Глобус',\n"
            "але тепер охорона синдикату знає про їхній інтерес!"
        ),
        'act2_action_q': "Як Джо та Джордж атакуватимуть кур'єра?",
        'act2_action_opt1': "1. Стрімкий лобовий удар: Джо збиває охоронця з ніг, а Джордж перехоплює кейс.",
        'act2_action_opt2': "2. Тактичний маневр: виманити кур'єра під прожектор та засліпити його спалахом ліхтаря.",
        'act2_action_out1': (
            "\nДжо блискавично кидається вперед! Охоронець падає, але кур'єр встигає кинути кейс у багажник машини\n"
            "і дає по газах. Починається шалена погоня! Джо та Джордж переслідують авто до закинутого театру 'Глобус'."
        ),
        'act2_action_out2': (
            "\nДжордж спритно кидає залізну банку, привертаючи увагу, а Джо засліплює кур'єра потужним променем ліхтаря!\n"
            "Злочинець кидає кейс і тікає. Всередині кейса хлопці знаходять карту підземель театру 'Глобус'.\n"
            "Вони негайно вирушають туди, щоб випередити синдикат."
        ),
        'act3_title': "\n--- АКТ III: ПАСТКА ПІД СЦЕНОЮ ТА МІЦНА ГОЛОВА ---",
        'act3_text': (
            "Обидві групи детективів зустрічаються біля закинутого вікторіанського театру 'Глобус'.\n"
            "Разом із Недом Нікерсоном та Четом Мортоном вони заходять усередину.\n"
            "Навколо панує похмура атмосфера: старі оксамитові завіси, пил та тіні на стінах.\n"
            "Раптом з-під стелі зривається важкий металевий софіт!\n\n"
            "Джо Харді блискавично відштовхує Ненсі в бік, але сам отримує сильний удар металевою рамою по голові!\n"
            "Він падає на підлогу без свідомості. Злочинці зачиняють важкі сталеві двері за лаштунками, затискаючи героїв у пастці.\n\n"
            "За кілька хвилин Джо приходить до тями, потираючи потилицю:\n"
            "— Ох... Здається, на мене впав цілий рояль. Але голова ціла, продовжуємо роботу! (Легендарна міцна голова Джо!)\n"
            "Наші герої замкнені в кімнаті під сценою. Потрібно негайно вибиратися!"
        ),
        'act3_q': "Як ви виберетесь із пастки театру?",
        'act3_opt1': "1. [Дія Джордж та Джо] Використати стару декоративну театральну гармату як таран, щоб вибити двері.",
        'act3_opt2': "2. [Декітка Ненсі] Використати металеву шпильку для волосся Ненсі та інженерний мультитул Френка, щоб зламати замок дверей.",
        'act3_out1': (
            "\nДжо та Джордж беруться за важку бутафорську гармату. Джесс вигукує свій фірмовий бойовий клич:\n"
            "— Hypers! Розігріємо цю старість!\n"
            "З гучним тріском важкі дерев'яні двері розлітаються на друзки! Ви вільні, хоча шум почули всі навколо."
        ),
        'act3_out2': (
            "\nКласичний дует детективів! Ненсі вставляє свою шпильку в механізм, а Френк акуратно підкручує шестерні.\n"
            "Кілька секунд ювелірної точності... Клац! Важкий замок тихо відчиняється. Ви виходите абсолютно безшумно!"
        ),
        'act4_title': "\n--- АКТ IV: ФІНАЛЬНИЙ ТРІУМФ В РІВЕР-ГАЙТС ---",
        'act4_text': (
            "Детективи прокрадаються до головної сцени. Там корумпований прокурор і ватажок синдикату\n"
            "намагаються спалити документи, які повністю виправдовують Карсона Дрю.\n"
            "У цей момент Бесс Марвін, яка ховалася в ложі, з переляку зачіпає важкий канат,\n"
            "і на голови злочинців падає величезна пильна завіса, повністю заплутавши їх!\n\n"
            "Нед Нікерсон та Чет Мортон миттєво кидаються вперед, блокуючи виходи.\n"
            "Ненсі вириває з вогню вцілілі документи синдикату, що містять оригінальну печатку та підписи!"
        ),
        'act4_sheriff': (
            "\nЧерез кілька хвилин до театру забігає Карсон Дрю разом із шерифом МакГіннісом та поліцією!\n"
            "Злочинців заарештовано на гарячому.\n"
            "— Чудова робота, діти! — каже Карсон Дрю, обіймаючи Ненсі. — Ви врятували не лише мою репутацію, а й закон у місті!\n"
            "Шериф МакГінніс лише посміхається: — Ну що ж, з такою командою з Бейпорта та Рівер-Гайтс поліція може йти на пенсію."
        ),
        'final_header': "                 ЮВІЛЕЙНИЙ ФІНАЛ                       ",
        'final_high': (
            "Вітаємо! Ви блискуче пройшли 10-ту ювілейну частину кросоверу! Рахунок: {score} очок.\n"
            "Синдикат повністю знищено! Увечері в домі Дрю Ганна Груен влаштовує грандіозний святковий бенкет.\n"
            "Бесс Марвін та Чет Мортон мирно ділять останній шматочок лимонного пирога,\n"
            "Джесс і Джо обговорюють спільні заїзди на мотоциклах, Нед і Ненсі посміхаються одне одному,\n"
            "а Френк робить запис у спільному щоденнику пригод. Рівер-Гайтс та Бейпорт святкують перемогу!"
        ),
        'final_normal': (
            "Справу успішно розкрито! Ваш рахунок: {score} очок.\n"
            "Хоча деякі пастки змусили вас понервувати, а голова Джо все ще гуде від софіта,\n"
            "спільна команда Ненсі Дрю та Братів Харді довела свою абсолютну непереможність!\n"
            "Попереду на героїв чекають нові неймовірні розслідування!"
        ),
        'final_thanks': "\nДякуємо, що були з нами протягом усіх 10 частин! Справжні Carolyn Keene та Franklin W. Dixon пишалися б вами."
    },
    'en': {
        'select_lang': "Select Language / Оберіть мову / Выберите язык:\n1. Українська\n2. English\n3. Русский",
        'lang_choice_prompt': "Your choice (1-3): ",
        'press_enter': "Press ENTER to start the anniversary adventure...",
        'invalid_input': "Please enter 1 or 2.",
        'intro_text': (
            "Welcome to the 10th anniversary part of our detective saga!\n"
            "For the first time in history, the legendary detective Nancy Drew joins forces with Frank and Joe Hardy.\n"
            "The story takes place in the cozy town of River Heights, where two sleuthing teams face\n"
            "a massive conspiracy by an international syndicate threatening the reputation of Carson Drew!"
        ),
        'act1_title': "\n--- ACT I: A GREAT FEAST & THE MYSTERIOUS CIPHER ---",
        'act1_text': (
            "A culinary battle of epic proportions is taking place in the Drews' cozy living room!\n"
            "On the table is Hannah Gruen's legendary warm lemon meringue pie.\n"
            "Right next to it, Chet Morton, who arrived with the boys from Bayport, lays out a box of pepperoni pizza\n"
            "and soft cinnamon rolls, creating an incredible blend of aromas.\n\n"
            "— Now this is what I call a detective summit! — Chet exclaims happily, taking a bite of pie and washing it down with pizza.\n"
            "Bess Marvin agrees: — Hannah, your pie is a masterpiece! I'm ready to investigate anything if we have a dinner like this!\n"
            "George Fayne just shakes her head: — Hypers! Bess, we are here on serious business!\n\n"
            "Nancy Drew places the copper cylinder and the 'Octopus' syndicate microchip found by the boys on the table.\n"
            "Frank Hardy plugs the chip into his laptop: the data reveals that a corrupt River Heights prosecutor\n"
            "is trying to frame Nancy's father, attorney Carson Drew, by fabricating financial fraud evidence."
        ),
        'act1_q': "Who will lead the first stage of the investigation?",
        'act1_opt1': "1. [Logic Group: Nancy & Frank] Go to Carson Drew's office to find the original court documents and crack the computer password.",
        'act1_opt2': "2. [Action Group: Joe & George] Go to the river docks to tail the mysterious syndicate courier.",
        'act1_out1': (
            "\nNancy and Frank act methodically. They sneak into Carson Drew's office.\n"
            "Frank connects his decoder to the safe, while Nancy analyzes her father's desk.\n"
            "They discover that the computer is locked by the syndicate's complex security system.\n"
            "To unlock the files, they need to guess the password based on the Latin inscription above the fireplace:\n"
            "'JUSTITIA VINCIT' (Justice Prevails)."
        ),
        'act1_out2': (
            "\nThe roar of Nancy's blue roadster and Joe's motorcycle shatters the quiet River Heights night!\n"
            "Joe Hardy and George Fayne rush to the foggy river docks.\n"
            "There, they spot a suspicious man in a dark coat handing over a metal case to a guard.\n"
            "Joe and George decide to act without hesitation and set up an ambush."
        ),
        'act2_title': "\n--- ACT II: CLUES & AMBUSHES ---",
        'act2_q_logic': "Enter the password to unlock the syndicate's computer (hint: the Latin inscription in the office in UPPERCASE):",
        'act2_logic_success': (
            "\nCongratulations! The password is correct! Files unlocked.\n"
            "Nancy and Frank find copies of the fake contracts and learn that the syndicate's main piece of evidence —\n"
            "the original stamp — is hidden in the safe of the old abandoned 'Globe' theater on the edge of town."
        ),
        'act2_logic_fail': (
            "\nIncorrect password! The syndicate's silent alarm is triggered.\n"
            "Nancy and Frank only manage to copy some of the data about the abandoned 'Globe' theater,\n"
            "but now the syndicate's guards know about their interest!"
        ),
        'act2_action_q': "How will Joe and George attack the courier?",
        'act2_action_opt1': "1. Direct head-on strike: Joe tackles the guard while George grabs the case.",
        'act2_action_opt2': "2. Tactical maneuver: lure the courier under the spotlight and blind him with a flashlight.",
        'act2_action_out1': (
            "\nJoe rushes forward lightning-fast! The guard falls, but the courier manages to throw the case in the trunk\n"
            "and speeds away. A wild chase begins! Joe and George pursue the car to the abandoned 'Globe' theater."
        ),
        'act2_action_out2': (
            "\nGeorge tosses a metal can to distract him, and Joe blinds the courier with a powerful flashlight beam!\n"
            "The criminal drops the case and flees. Inside, the boys find a map of the 'Globe' theater's basement.\n"
            "They set off immediately to beat the syndicate there."
        ),
        'act3_title': "\n--- ACT III: THE TRAP UNDER THE STAGE & THE HARD HEAD ---",
        'act3_text': (
            "Both groups of detectives meet outside the abandoned Victorian 'Globe' theater.\n"
            "Together with Ned Nickerson and Chet Morton, they step inside.\n"
            "The atmosphere is gloomy: old velvet curtains, dust, and long shadows on the walls.\n"
            "Suddenly, a heavy metal stage light breaks loose from the ceiling!\n\n"
            "Joe Hardy shoves Nancy out of the way just in time, but takes the full force of the falling metal frame on his head!\n"
            "He falls to the floor unconscious. The criminals lock the heavy steel doors behind the stage, trapping our heroes.\n\n"
            "A few minutes later, Joe wakes up, rubbing the back of his head:\n"
            "— Ouch... Feels like a grand piano fell on me. But my head is intact, let's get back to work! (Joe's legendary hard head!)\n"
            "We are locked in the room under the stage. We need to escape immediately!"
        ),
        'act3_q': "How will you escape the theater trap?",
        'act3_opt1': "1. [George & Joe's Action] Use an old decorative theater cannon as a ram to break down the door.",
        'act3_opt2': "2. [Nancy's Classic] Use Nancy's hairpin and Frank's engineering multitool to pick the lock.",
        'act3_out1': (
            "\nJoe and George grab the heavy prop cannon. George yells her signature battle cry:\n"
            "— Hypers! Let's heat things up!\n"
            "With a loud crash, the heavy wooden door splinters into pieces! You are free, though everyone nearby heard the noise."
        ),
        'act3_out2': (
            "\nA classic detective duo! Nancy inserts her hairpin into the mechanism while Frank carefully adjusts the gears.\n"
            "A few seconds of absolute precision... Click! The heavy lock opens quietly. You slip out completely silent!"
        ),
        'act4_title': "\n--- ACT IV: FINAL TRIUMPH IN RIVER HEIGHTS ---",
        'act4_text': (
            "The detectives slip onto the main stage. There, the corrupt prosecutor and the syndicate leader\n"
            "are trying to burn the documents that fully exonerate Carson Drew.\n"
            "At that moment, Bess Marvin, who was hiding in the balcony box, accidentally trips a heavy rope in fear,\n"
            "dropping a massive dusty velvet curtain right on the villains, completely tangling them up!\n\n"
            "Ned Nickerson and Chet Morton instantly rush forward, blocking the exits.\n"
            "Nancy pulls the surviving syndicate documents, complete with the original stamp and signatures, from the fire!"
        ),
        'act4_sheriff': (
            "\nA few minutes later, Carson Drew rushes into the theater along with Sheriff McGinnis and the police!\n"
            "The criminals are caught red-handed.\n"
            "— Magnificent work, kids! — Carson Drew says, hugging Nancy. — You saved not only my reputation, but justice in this town!\n"
            "Sheriff McGinnis just smiles: — Well, with a team like this from Bayport and River Heights, the police can retire."
        ),
        'final_header': "                 ANNIVERSARY END                       ",
        'final_high': (
            "Congratulations! You solved the 10th anniversary crossover case brilliantly! Score: {score} points.\n"
            "The syndicate is completely destroyed! In the evening at the Drew home, Hannah Gruen hosts a grand feast.\n"
            "Bess Marvin and Chet Morton peacefully share the last piece of lemon meringue pie,\n"
            "George and Joe talk about riding motorcycles, Ned and Nancy smile at each other,\n"
            "and Frank makes an entry in their shared adventure journal. River Heights and Bayport celebrate victory!"
        ),
        'final_normal': (
            "The case is successfully solved! Your score: {score} points.\n"
            "Although some traps made you sweat, and Joe's head is still ringing from the stage light,\n"
            "the combined force of Nancy Drew and the Hardy Boys has proven absolutely unstoppable!\n"
            "New incredible mysteries lie ahead for our heroes!"
        ),
        'final_thanks': "\nThank you for being with us through all 10 parts! The real Carolyn Keene and Franklin W. Dixon would be proud of you."
    },
    'ru': {
        'select_lang': "Выберите язык / Oберіть мову / Select Language:\n1. Українська\n2. English\n3. Русский",
        'lang_choice_prompt': "Ваш выбор (1-3): ",
        'press_enter': "Нажмите ENTER, чтобы начать юбилейное приключение...",
        'invalid_input': "Пожалуйста, введите 1 или 2.",
        'intro_text': (
            "Добро пожаловать в 10-ю, юбилейную часть нашей детективной саги!\n"
            "Впервые в истории легендарная детективка Нэнси Дрю объединяет усилия с братьями Фрэнком и Джо Харди.\n"
            "Действие разворачивается в уютном городке Ривер-Хайтс, где две команды сыщиков столкнутся\n"
            "с масштабным заговором международного синдиката, угрожающим репутации Карсона Дрю!"
        ),
        'act1_title': "\n--- АКТ I: ВЕЛИКИЙ ПИР И ТАИНСТВЕННЫЙ ШИФР ---",
        'act1_text': (
            "В уютной гостиной дома Дрю разворачивается настоящее кулинарное противостояние!\n"
            "На столе красуется легендарный теплый лимонный пирог Анны Груэн с воздушной меренгой.\n"
            "Рядом Чет Мортон, приехавший с парнями из Бейпорта, выкладывает коробку фирменной пиццы с пепперони\n"
            "и мягкие булочки с корицей, что создает невероятное сочетание ароматов.\n\n"
            "— Вот это я понимаю — детективный саммит! — радостно восклицает Чет, откусывая пирог и запивая его пиццей.\n"
            "Бесс Марвин соглашается: — Анна, ваш пирог — это шедевр! Я готова расследовать что угодно, если у нас будет такой ужин!\n"
            "Джесс (Джордж) Фейн лишь качает головой: — Hypers! Бесс, мы приехали сюда по серьезному делу!\n\n"
            "Нэнси Дрю выкладывает на стол медный цилиндр и микрочип синдиката «Осьминог», найденный братьями.\n"
            "Фрэнк Харди подключает чип к своему ноутбуку: данные указывают на то, что коррумпированный прокурор Ривер-Хайтс\n"
            "пытается подставить отца Нэнси — адвоката Карсона Дрю, сфабриковав улики о финансовых махинациях."
        ),
        'act1_q': "Кто возглавит первый этап расследования?",
        'act1_opt1': "1. [Группа логики: Нэнси и Фрэнк] Отправиться в офис Карсона Дрю, чтобы найти оригиналы судебных бумаг и разгадать компьютерный пароль.",
        'act1_opt2': "2. [Группа действия: Джо и Джордж] Отправиться на речной причал, чтобы проследить за таинственным курьером синдиката.",
        'act1_out1': (
            "\nНэнси и Фрэнк действуют методично. Они пробираются в офис Карсона Дрю.\n"
            "Фрэнк подключает дешифратор к сейфу, а Нэнси анализирует рабочий стол отца.\n"
            "Они обнаруживают, что компьютер заблокирован сложной системой защиты синдиката.\n"
            "Чтобы раскрыть файлы, им необходимо разгадать пароль, основанный на латинской надписи над камином:\n"
            "«JUSTITIA VINCIT» (Справедливость побеждает)."
        ),
        'act1_out2': (
            "\nРев двигателей синего родстера Нэнси и мотоцикла Джо разрывает ночную тишину Ривер-Хайтс!\n"
            "Джо Харди и Джордж Фейн мчатся к туманному речному причалу.\n"
            "Там они замечают подозрительного человека в темном плаще, передающего металлический кейс охраннику.\n"
            "Джо и Джордж решают действовать без лишних разговоров и устроить засаду."
        ),
        'act2_title': "\n--- АКТ II: РАЗГАДКИ И ЗАСАДЫ ---",
        'act2_q_logic': "Введите пароль для разблокировки компьютера синдиката (подсказка: латинская надпись из офиса ЗАГЛАВНЫМИ БУКВАМИ):",
        'act2_logic_success': (
            "\nПоздравляем! Пароль верный! Файлы разблокированы.\n"
            "Нэнси и Фрэнк находят копии фальшивых контрактов и узнают, что главная улика синдиката —\n"
            "оригинальная печать — спрятана в сейфе старого заброшенного театра 'Глобус' на окраине города."
        ),
        'act2_logic_fail': (
            "\nПароль неверный! Срабатывает бесшумная сигнализация синдиката.\n"
            "Нэнси и Фрэнк успевают скопировать лишь часть данных о заброшенном театре 'Глобус',\n"
            "но теперь охрана синдиката знает об их интересе!"
        ),
        'act2_action_q': "Как Джо и Джордж атакуют курьера?",
        'act2_action_opt1': "1. Стремительный лобовой удар: Джо сбивает охранника с ног, а Джордж перехватывает кейс.",
        'act2_action_opt2': "2. Тактический маневр: выманить курьера под прожектор и ослепить его вспышкой фонаря.",
        'act2_action_out1': (
            "\nДжо молниеносно бросается вперед! Охранник падает, но курьер успевает бросить кейс в багажник машины\n"
            "и дает по газам. Начинается бешеная погоня! Джо и Джордж преследуют авто до заброшенного театра 'Глобус'."
        ),
        'act2_action_out2': (
            "\nДжордж ловко бросает железную банку, привлекая внимание, а Джо ослепляет курьера мощным лучом фонаря!\n"
            "Преступник бросает кейс и убегает. Внутри кейса парни находят карту подземелий театра 'Глобус'.\n"
            "Они немедленно отправляются туда, чтобы опередить синдикат."
        ),
        'act3_title': "\n--- АКТ III: ЛОВУШКА ПОД СЦЕНОЙ И КРЕПКАЯ ГОЛОВА ---",
        'act3_text': (
            "Обе группы детективов встречаются у заброшенного викторианского театра 'Глобус'.\n"
            "Вместе с Недом Никерсоном и Четом Мортоном они заходят внутрь.\n"
            "Вокруг царит мрачная атмосфера: старые бархатные занавеси, пыль и длинные тени на стенах.\n"
            "Вдруг из-под потолка срывается тяжелый металлический софит!\n\n"
            "Джо Харди молниеносно отталкивает Нэнси в сторону, но сам получает сильный удар металлической рамой по голове!\n"
            "Он падает на пол без сознания. Преступники закрывают тяжелую стальную дверь за кулисами, зажимая героев в ловушке.\n\n"
            "Через несколько минут Джо приходит в себя, потирая затылок:\n"
            "— Ох... Кажется, на меня упал целый рояль. Но голова цела, продолжаем работу! (Легендарная крепкая голова Джо!)\n"
            "Наши герои заперты в комнате под сценой. Нужно немедленно выбираться!"
        ),
        'act3_q': "Как вы выберетесь из ловушки театра?",
        'act3_opt1': "1. [Действие Джордж и Джо] Использовать старую декоративную театральную пушку как таран, чтобы выбить дверь.",
        'act3_opt2': "2. [Классика Нэнси] Использовать металлическую шпильку для волос Нэнси и инженерный мультитул Фрэнка, чтобы вскрыть замок.",
        'act3_out1': (
            "\nДжо и Джордж берутся за тяжелую бутафорскую пушку. Джордж выкрикивает свой фирменный боевой клич:\n"
            "— Hypers! Разогреем эту старость!\n"
            "С громким треском тяжелая деревянная дверь разлетается в щепки! Вы свободны, хотя шум услышали все вокруг."
        ),
        'act3_out2': (
            "\nКлассический дуэт детективов! Нэнси вставляет шпильку в механизм, а Фрэнк аккуратно подкручивает шестеренки.\n"
            "Несколько секунд ювелирной точности... Щелк! Тяжелый замок тихо открывается. Вы выходите абсолютно бесшумно!"
        ),
        'act4_title': "\n--- АКТ IV: ФИНАЛЬНЫЙ ТРИУМФ В РИВЕР-ХАЙТС ---",
        'act4_text': (
            "Детективы прокрадываются к главной сцене. Там коррумпированный прокурор и главарь синдиката\n"
            "пытаются сжечь документы, полностью оправдывающие Карсона Дрю.\n"
            "В этот момент Бесс Марвин, прятавшаяся в ложе, со страху задевает тяжелый канат,\n"
            "и на головы злодеев падает огромный пыльный занавес, полностью запутав их!\n\n"
            "Нед Никерсон и Чет Мортон мгновенно бросаются вперед, блокируя выходы.\n"
            "Нэнси вырывает из огня уцелевшие документы синдиката, содержащие оригинальную печать и подписи!"
        ),
        'act4_sheriff': (
            "\nЧерез несколько минут в театр вбегает Карсон Дрю вместе с шерифом МакГиннисом и полицией!\n"
            "Преступники арестованы с поличным.\n"
            "— Великолепная работа, дети! — говорит Карсон Дрю, обнимая Нэнси. — Вы спасли не только мою репутацию, но и закон в городе!\n"
            "Шериф МакГинніс улыбается: — Ну что ж, с такой командой из Бейпорта и Ривер-Хайтс полиция может уходить на пенсию."
        ),
        'final_header': "                 ЮБИЛЕЙНЫЙ ФИНАЛ                       ",
        'final_high': (
            "Поздравляем! Вы блестяще прошли 10-ю юбилейную часть кроссовера! Счет: {score} очков.\n"
            "Синдикат полностью уничтожен! Вечером в доме Дрю Анна Груэн устраивает грандиозный праздничный пир.\n"
            "Бесс Марвин и Чет Мортон мирно делят последний кусочек лимонного пирога,\n"
            "Джесс и Джо обсуждают совместные поездки на мотоциклах, Нед и Нэнси улыбаются друг другу,\n"
            "а Фрэнк делает запись в совместном дневнике приключений. Ривер-Хайтс и Бейпорт празднуют победу!"
        ),
        'final_normal': (
            "Дело успешно раскрыто! Ваш счет: {score} очок.\n"
            "Хотя некоторые ловушки заставили вас понервничать, а голова Джо все еще гудит от софита,\n"
            "совместная команда Нэнси Дрю и Братьев Харди доказала свою абсолютную непобедимость!\n"
            "Впереди героев ждут новые невероятные расследования!"
        ),
        'final_thanks': "\nСпасибо, что были с нами на протяжении всех 10 частей! Настоящие Carolyn Keene и Franklin W. Dixon гордились бы вами."
    }
}

def intro(state):
    display_header(state.lang)
    print_slow(LOCALIZATION[state.lang]['intro_text'])
    print_slow("\n" + LOCALIZATION[state.lang]['press_enter'])
    input()
    act_1(state)

def act_1(state):
    loc = LOCALIZATION[state.lang]
    print_slow(loc['act1_title'])
    print_slow(loc['act1_text'])
    
    while True:
        print("\n" + loc['act1_q'])
        print(loc['act1_opt1'])
        print(loc['act1_opt2'])
        choice = input("\n-> ").strip()
        
        if choice == '1':
            state.route_taken = 'nancy_frank'
            state.score += 20
            print_slow(loc['act1_out1'])
            act_2_logic(state)
            break
        elif choice == '2':
            state.route_taken = 'joe_george'
            state.score += 15
            print_slow(loc['act1_out2'])
            act_2_action(state)
            break
        else:
            print(loc['invalid_input'])

def act_2_logic(state):
    loc = LOCALIZATION[state.lang]
    print_slow(loc['act2_title'])
    
    while True:
        print("\n" + loc['act2_q_logic'])
        password = input("-> ").strip().upper()
        
        if password == "JUSTITIA VINCIT":
            state.score += 30
            print_slow(loc['act2_logic_success'])
            break
        else:
            state.score += 10
            print_slow(loc['act2_logic_fail'])
            break
            
    act_3(state)

def act_2_action(state):
    loc = LOCALIZATION[state.lang]
    print_slow(loc['act2_title'])
    
    while True:
        print("\n" + loc['act2_action_q'])
        print(loc['act2_action_opt1'])
        print(loc['act2_action_opt2'])
        choice = input("\n-> ").strip()
        
        if choice == '1':
            state.score += 15
            print_slow(loc['act2_action_out1'])
            break
        elif choice == '2':
            state.score += 25
            print_slow(loc['act2_action_out2'])
            break
        else:
            print(loc['invalid_input'])
            
    act_3(state)

def act_3(state):
    loc = LOCALIZATION[state.lang]
    print_slow(loc['act3_title'])
    print_slow(loc['act3_text'])
    
    while True:
        print("\n" + loc['act3_q'])
        print(loc['act3_opt1'])
        print(loc['act3_opt2'])
        choice = input("\n-> ").strip()
        
        if choice == '1':
            state.trap_solved_with = 'force'
            state.score += 15
            print_slow(loc['act3_out1'])
            break
        elif choice == '2':
            state.trap_solved_with = 'lockpick'
            state.score += 25
            print_slow(loc['act3_out2'])
            break
        else:
            print(loc['invalid_input'])
            
    act_4(state)

def act_4(state):
    loc = LOCALIZATION[state.lang]
    print_slow(loc['act4_title'])
    print_slow(loc['act4_text'])
    print_slow(loc['act4_sheriff'])
    
    print_slow("\n=============================================")
    print_slow(loc['final_header'])
    print_slow("=============================================\n")
    
    if state.score >= 70:
        print_slow(loc['final_high'].format(score=state.score))
    else:
        print_slow(loc['final_normal'].format(score=state.score))
        
    print_slow(loc['final_thanks'])

def main():
    state = GameState()
    print(LOCALIZATION['uk']['select_lang'])
    while True:
        choice = input(LOCALIZATION['uk']['lang_choice_prompt']).strip()
        if choice == '1':
            state.lang = 'uk'
            break
        elif choice == '2':
            state.lang = 'en'
            break
        elif choice == '3':
            state.lang = 'ru'
            break
        else:
            print("1, 2, 3?")
            
    intro(state)

if __name__ == "__main__":
    main()
