#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import time
import sys

def print_slow(text, delay=0.02):
    """Prints text slowly for a vintage text adventure feel."""
    for char in text:
        sys.stdout.write(char)
        sys.stdout.flush()
        time.sleep(delay)
    print()

def display_header(lang):
    title_text = {
        'uk': "          БРАТИ ХАРДІ ТА ТАЄМНИЦЯ КАРНАВАЛУ ТІНЕЙ          ",
        'en': "      THE HARDY BOYS AND THE MYSTERY OF THE SHADOW CARNIVAL     ",
        'ru': "          БРАТЬЯ ХАРДИ И ТАЙНА КАРНАВАЛА ТЕНЕЙ            "
    }
    subtitle_text = {
        'uk': "                 Частина 8: Інтерактивний квест                ",
        'en': "                 Part 8: Interactive Text-Based Quest          ",
        'ru': "                 Часть 8: Интерактивный текстовый квест         "
    }
    print("=" * 70)
    print(title_text[lang])
    print(subtitle_text[lang])
    print("=" * 70)
    print()

class GameState:
    def __init__(self):
        self.lang = 'uk'
        self.inventory = []
        self.route_taken = None  # 'frank' (booth/cameras) or 'joe' (mirrors/dash)
        self.found_microchip = False
        self.freed_with_logic = False
        self.score = 0

# Localization dictionary for Part 8
LOCALIZATION = {
    'uk': {
        'select_lang': "Оберіть мову / Select Language / Выберите язык:\n1. Українська\n2. English\n3. Русский",
        'lang_choice_prompt': "Ваш вибір (1-3): ",
        'press_enter': "Натисніть ENTER, щоб розпочати нову пригоду...",
        'invalid_input': "Будь ласка, введіть 1 або 2.",
        'intro_text': (
            "Ви граєте за відважних братів-детективів Френка та Джо Харді з Бейпорта.\n"
            "Після розгрому синдикату «Диригент» на маяку, ви вирішили влаштувати собі відпочинок.\n"
            "Проте таємниці переслідують вас всюди, куди б ви не попрямували!"
        ),
        'act1_title': "\n--- АКТ I: КАРНАВАЛЬНІ СМАКОЛИКИ ТА ЗНИКНЕННЯ ЗОЛТАРА ---",
        'act1_text': (
            "Вечірній Бейпорт наповнений яскравими вогнями мандрівного «Карнавалу Тіней».\n"
            "Ви відпочиваєте разом із Четом Мортоном, і повітря навколо просочене неймовірними ароматами:\n"
            "гарячими, пишними карнавальними пончиками, густо присипаними цукровою пудрою,\n"
            "яблуками у товстій янтарній карамелі, що виблискує у світлі гірлянд, великими відрами\n"
            "солоного попкорну з маслом та крижаними вишневими слейшами. (Класичний гастрономічний троп!)\n\n"
            "Раптом до вас підбігає схвильований власник карнавалу, містер Дженкінс:\n"
            "— Хлопці Харді! Сталася біда! Хтось викрав наш головний атракціон — механічного віщуна Золтара!\n"
            "Але річ не в атракціоні... Всередині Золтара був захований секретний мікрочип синдикату «Диригент»,\n"
            "який мій покійний брат-інженер намагався врятувати. Злодій у масці міма втік у бік Лабіринту Дзеркал!"
        ),
        'act1_q': "Як ви почнете переслідування?",
        'act1_opt1': "1. [Вибір Френка] Побігти до будки охорони, зламати систему камер та відстежити рух міма по моніторах.",
        'act1_opt2': "2. [Вибір Джо] Не роздумуючи, кинутися в Лабіринт Дзеркал наввипередки, щоб перехопити злодія на гарячому.",
        'act1_out1': (
            "\nФренк діє раціонально. Ви вриваєтесь до будки охорони. Використовуючи знання електроніки,\n"
            "Френк перепідключає кабелі моніторів і бачить на екрані міма, який ховає чип у кишеню біля виходу з дзеркал.\n"
            "Ви берете карту карнавалу, ліхтарик та прямуєте на випередження до покинутого шатра Freak Show.\n"
            "У вашому інвентарі з'являється: КАРТА та ЛІХТАРИК."
        ),
        'act1_out2': (
            "\nДжо мчить вперед! Ревіння натовпу згасає, коли ви забігаєте під скляні арки лабіринту.\n"
            "Навколо тисячі ваших відображень. Раптом одна з тіней різко повертає за ріг.\n"
            "Ви біжите наосліп крізь скляні коридори, орієнтуючись лише на звук кроків.\n"
            "У вашому інвентарі є лише ЛІХТАРИК."
        ),
        'act2_title': "\n--- АКТ II: ЛАБІРИНТ ВІДДЗЕРКАЛЕНЬ ---",
        'act2_text': (
            "Лабіринт Дзеркал виглядає моторошно в нічному освітленні. Світло заломлюється під дивними кутами.\n"
            "Раптом попереду лунає знущальний сміх міма, який манить вас углиб пастки."
        ),
        'act2_frank_branch': (
            "\nЗавдяки перегляду камер охорони Френк точно знає розташування фальшивих дзеркал.\n"
            "Ви бачите, що мім намагається заманити вас у тупик із хиткою підлогою."
        ),
        'act2_joe_branch': (
            "\nДжо біжить наосліп. Раптом дзеркала навколо починають обертатися, створюючи дезорієнтуючу ілюзію.\n"
            "Справжній мім зникає, а перед вами з'являється зачинена дзеркальна панель із кодовим замком."
        ),
        'act2_q': "Ваша дія для подолання перешкоди?",
        'act2_opt1': "1. Спробувати розгадати закономірність лазерних променів на дзеркалах (логічний шлях).",
        'act2_opt2': "2. Використати фізичну силу, щоб вибити хитку панель плечем (шлях дії).",
        'act2_out1': (
            "\nВи уважно аналізуєте заломлення світла ліхтарика. Френк вираховує кут падіння\n"
            "і знаходить секретну кнопку, яка відчиняє панель без жодного шуму. Ви прокрадаєтесь далі!"
        ),
        'act2_out2': (
            "\nДжо розбігається і з силою б'є плечем по стику панелей! З гуркотом рама піддається,\n"
            "відкриваючи прохід до старого шатра Freak Show. Але гучний звук привернув увагу!"
        ),
        'act3_title': "\n--- АКТ III: ПАСТКА ПІД КУПОЛОМ ТА МІЦНА ГОЛОВА ---",
        'act3_text': (
            "Ви опиняєтесь у напівтемному, занедбаному шатрі Freak Show серед старих кліток та реквізиту.\n"
            "Раптом зверху лунає скрип. Важка залізна трапеція зривається з купола і летить прямо на вас!\n"
            "Джо встигає відштовхнути Френка, але сам отримує сильний удар металевою штангою по голові!\n"
            "Джо падає на арену непритомним, а мім зачиняє за вами важку сталеву клітку для тигрів!\n\n"
            "За хвилину Джо приходить до тями, потираючи велику гулю на потилиці:\n"
            "— Ох... Моя бідна голова. Здається, по мені проїхав товарний поїзд Бейпорта! (Класичний троп!)\n"
            "— Але нічого, бувало й гірше, розберемося з цим клоуном пізніше. Як нам вибратися?"
        ),
        'act3_q': "Клітка заблокована магнітним замком. Що ви зробите?",
        'act3_opt1': "1. [Дія Джо] Використати старий залізний покажчик як важіль, щоб розігнути прути силою.",
        'act3_opt2': "2. [Дія Френка] Використати знання електроніки, щоб розкрити пульт замка та замкнути дроти напряму.",
        'act3_out1_success': (
            "\nДжо вставляє важкий металевий покажчик між прутами клітки. Напруживши всі сили,\n"
            "ви розсуваєте старі іржаві прути настільки, що Френк і Джо ледве пролазять на волю!"
        ),
        'act3_out1_fail': (
            "\nВи намагаєтесь розігнути прути, але залізо надто міцне. Ви лише марно втомлюєтеся.\n"
            "Потрібно шукати розумніший підхід!"
        ),
        'act3_out2_success': (
            "\nФренк розбирає захисну кришку електронного пульта. Знайшовши потрібні контакти,\n"
            "він замикає їх батарейкою від ліхтарика. Іскри летять врізнобіч — і магнітний замок відкривається!"
        ),
        'act4_title': "\n--- АКТ IV: ФІНАЛ НА ЧОРТОВОМУ КОЛЕСІ ---",
        'act4_text': (
            "Ви вибігаєте на площу карнавалу. Мім уже намагається запустити Чортове колесо,\n"
            "щоб піднятися на платформу технічного обслуговування, де його чекає спільник на гелікоптері!\n"
            "Кабіни колеса починають стрімко обертатися. Мікрочип у його руках!"
        ),
        'act4_q': "Як зупинити втікача?",
        'act4_opt1': "1. [Дія Джо] Стрибнути на металеву конструкцію колеса і заблокувати механізм ручним гальмом.",
        'act4_opt2': "2. [Дія Френка] Підбігти до пульта керування атракціоном та перевантажити генератор, вимкнувши живлення.",
        'act4_out1': (
            "\nДжо здійснює відчайдушний стрибок на сталеві опори колеса! Чіпляючись за балки,\n"
            "він дістається важеля екстреного гальмування та тисне на нього всією вагою.\n"
            "Колесо зупиняється з гучним скреготом! Мім втрачає рівновагу, падає на сітку, де його в'яже Френк!"
        ),
        'act4_out2': (
            "\nФренк підбігає до головного генератора карнавалу. Швидко зорієнтувавшись у тумблерах,\n"
            "він переводить подачу струму в режим максимального навантаження. Запобіжники вибухають,\n"
            "колесо плавно зупиняється, блокуючи міма в кабіні на висоті трьох метрів до приїзду поліції!"
        ),
        'final_header': "                 ФІНАЛ                       ",
        'final_high': (
            "Вітаємо! Справу розкрито блискуче! Ваш рахунок: {score} очок.\n"
            "Секретний мікрочип повернуто, а міма та його спільників заарештував шериф Колліг.\n"
            "Містер Дженкінс безмежно вдячний вам і безкоштовно пригощає гарячими бельгійськими вафлями\n"
            "та карамельним морозивом. Чет Мортон запевняє, що це найкращий карнавал у його житті,\n"
            "а Бейпорт знову може спати спокійно!"
        ),
        'final_normal': (
            "Справу успішно завершено! Ваш рахунок: {score} очок.\n"
            "Хоча Джо отримав ще одну міцну гулю на голові, а Френку довелося неабияк поламати мозок,\n"
            "ви знову довели, що для братів Харді немає нерозв'язних загадок!"
        ),
        'final_thanks': "\nДякуємо за гру! Брати Харді пишалися б вашим вибором."
    },
    'en': {
        'select_lang': "Select Language / Оберіть мову / Выберите язык:\n1. Українська\n2. English\n3. Русский",
        'lang_choice_prompt': "Your choice (1-3): ",
        'press_enter': "Press ENTER to start the new adventure...",
        'invalid_input': "Please enter 1 or 2.",
        'intro_text': (
            "You play as the brave detective brothers, Frank and Joe Hardy from Bayport.\n"
            "After smashing the 'Conductor' syndicate at the lighthouse, you decided to take a break.\n"
            "However, mysteries follow you wherever you go!"
        ),
        'act1_title': "\n--- ACT I: CARNIVAL TREATS & ZOLTAR'S DISAPPEARANCE ---",
        'act1_text': (
            "Evening Bayport is filled with the bright lights of the traveling 'Shadow Carnival'.\n"
            "You are relaxing with Chet Morton, and the air around is filled with incredible aromas:\n"
            "hot, fluffy funnel cakes heavily dusted with powdered sugar, apples dipped in thick\n"
            "amber caramel shining in the lights of garlands, huge buckets of salted butter popcorn,\n"
            "and icy cherry slushies. (Classic food porn trope!)\n\n"
            "Suddenly, the excited owner of the carnival, Mr. Jenkins, runs up to you:\n"
            "— Hardy boys! Disaster has struck! Someone stole our main attraction — Zoltar the mechanical fortune teller!\n"
            "But it's not about the machine... Inside Zoltar, a secret microchip of the 'Conductor' syndicate was hidden,\n"
            "which my late engineer brother tried to save. The thief dressed as a mime fled towards the Mirror Maze!"
        ),
        'act1_q': "How will you begin the chase?",
        'act1_opt1': "1. [Frank's Choice] Run to the security booth, hack the camera system and track the mime on the monitors.",
        'act1_opt2': "2. [Joe's Choice] Without hesitation, rush into the Mirror Maze to catch the thief red-handed.",
        'act1_out1': (
            "\nFrank acts rationally. You burst into the security booth. Using electronics knowledge,\n"
            "Frank reconnects the monitor cables and sees the mime on screen hiding the chip in his pocket near the mirror exit.\n"
            "You take a map of the carnival, a flashlight, and head ahead of him to the abandoned Freak Show tent.\n"
            "In your inventory appears: MAP and FLASHLIGHT."
        ),
        'act1_out2': (
            "\nJoe rushes forward! The roar of the crowd fades as you run under the glass arches of the maze.\n"
            "Around you are thousands of your reflections. Suddenly, one of the shadows turns sharply around the corner.\n"
            "You run blindly through the glass corridors, guided only by the sound of footsteps.\n"
            "Your inventory contains only a FLASHLIGHT."
        ),
        'act2_title': "\n--- ACT II: THE MIRROR LABYRINTH ---",
        'act2_text': (
            "The Mirror Labyrinth looks eerie in the night lighting. The light refracts at strange angles.\n"
            "Suddenly, the mocking laughter of the mime echoes ahead, baiting you deeper into the trap."
        ),
        'act2_frank_branch': (
            "\nThanks to viewing the security cameras, Frank knows exactly where the fake mirrors are.\n"
            "You see that the mime is trying to lure you into a dead end with a shaky floor."
        ),
        'act2_joe_branch': (
            "\nJoe runs blindly. Suddenly, the mirrors around begin to rotate, creating a disorienting illusion.\n"
            "The real mime disappears, and a locked mirror panel with a combination lock appears before you."
        ),
        'act2_q': "Your action to overcome the obstacle?",
        'act2_opt1': "1. Try to figure out the pattern of laser beams on the mirrors (logical path).",
        'act2_opt2': "2. Use physical force to knock out the shaky panel with your shoulder (action path).",
        'act2_out1': (
            "\nYou carefully analyze the refraction of the flashlight light. Frank calculates the angle of incidence\n"
            "and finds a secret button that opens the panel without any noise. You slip further!"
        ),
        'act2_out2': (
            "\nJoe runs and hits the panel joint hard with his shoulder! With a crash, the frame gives way,\n"
            "opening a passage to the old Freak Show tent. But the loud sound attracted attention!"
        ),
        'act3_title': "\n--- ACT III: THE TRAP UNDER THE DOME & THE HARD HEAD ---",
        'act3_text': (
            "You find yourself in a dim, abandoned Freak Show tent among old cages and props.\n"
            "Suddenly, a creak sounds from above. A heavy iron trapeze breaks from the dome and flies straight at you!\n"
            "Joe manages to push Frank away, but gets hit hard on the head by the metal bar himself!\n"
            "Joe falls onto the arena unconscious, and the mime locks the heavy steel tiger cage behind you!\n\n"
            "A minute later, Joe wakes up, rubbing a big lump on the back of his head:\n"
            "— Ouch... My poor head. Feels like a Bayport freight train ran over me! (Classic trope!)\n"
            "— But hey, I've had worse, we'll deal with this clown later. How do we get out?"
        ),
        'act3_q': "The cage is locked with a magnetic lock. What will you do?",
        'act3_opt1': "1. [Joe's Action] Use an old iron sign as a lever to bend the bars by force.",
        'act3_opt2': "2. [Frank's Action] Use electronics knowledge to open the lock panel and hotwire the wires.",
        'act3_out1_success': (
            "\nJoe inserts the heavy metal sign between the cage bars. Straining all your strength,\n"
            "you push the old rusty bars apart enough so that Frank and Joe barely squeeze out to freedom!"
        ),
        'act3_out1_fail': (
            "\nYou try to bend the bars, but the iron is too strong. You only tire yourself out in vain.\n"
            "Must look for a smarter approach!"
        ),
        'act3_out2_success': (
            "\nFrank disassembles the protective cover of the electronic panel. Finding the right contacts,\n"
            "he hotwires them with a flashlight battery. Sparks fly — and the magnetic lock clicks open!"
        ),
        'act4_title': "\n--- ACT IV: THE FINALE ON THE FERRIS WHEEL ---",
        'act4_text': (
            "You run out into the carnival square. The mime is already trying to start the Ferris Wheel\n"
            "to climb to the maintenance platform, where his accomplice on a helicopter is waiting!\n"
            "The wheel cabins begin to rotate rapidly. The microchip is in his hands!"
        ),
        'act4_q': "How to stop the fugitive?",
        'act4_opt1': "1. [Joe's Action] Jump onto the metal frame of the wheel and block the mechanism with the manual brake.",
        'act4_opt2': "2. [Frank's Action] Run to the ride's control panel and overload the generator, turning off the power.",
        'act4_out1': (
            "\nJoe makes a desperate leap onto the steel support beams of the wheel! Clinging to the bars,\n"
            "he reaches the emergency brake lever and presses on it with all his weight.\n"
            "The wheel stops with a loud screech! The mime loses his balance, falls onto the safety net, where Frank ties him up!"
        ),
        'act4_out2': (
            "\nFrank runs to the main generator of the carnival. Quickly orienting himself in the switches,\n"
            "he turns the current supply to maximum load mode. The fuses explode,\n"
            "the wheel stops smoothly, trapping the mime in the cabin at a height of three meters until the police arrive!"
        ),
        'final_header': "                THE END                      ",
        'final_high': (
            "Congratulations! The case is solved brilliantly! Your score: {score} points.\n"
            "The secret microchip is returned, and the mime and his accomplices are arrested by Sheriff Collig.\n"
            "Mr. Jenkins is extremely grateful to you and treats you to hot Belgian waffles\n"
            "and caramel ice cream for free. Chet Morton assures that this is the best carnival of his life,\n"
            "and Bayport can sleep soundly again!"
        ),
        'final_normal': (
            "The case is successfully completed! Your score: {score} points.\n"
            "Although Joe got another solid lump on his head, and Frank had to rack his brain quite a bit,\n"
            "you proved once again that there are no insolvable riddles for the Hardy Boys!"
        ),
        'final_thanks': "\nThanks for playing! The Hardy Boys would be proud of your choice."
    },
    'ru': {
        'select_lang': "Выберите язык / Oберіть мову / Select Language:\n1. Українська\n2. English\n3. Русский",
        'lang_choice_prompt': "Ваш выбор (1-3): ",
        'press_enter': "Нажмите ENTER, чтобы начать новое приключение...",
        'invalid_input': "Пожалуйста, введите 1 или 2.",
        'intro_text': (
            "Вы играете за отважных братьев-детективов Фрэнка и Джо Харди из Бейпорта.\n"
            "После разгрома синдиката «Дирижер» на маяке, вы решили устроить себе отдых.\n"
            "Однако тайны преследуют вас повсюду, куда бы вы ни направились!"
        ),
        'act1_title': "\n--- АКТ I: КАРНАВАЛЬНЫЕ УГОЩЕНИЯ И ИСЧЕЗНОВЕНИЕ ЗОЛТАРА ---",
        'act1_text': (
            "Вечерний Бейпорт наводнен яркими огнями бродячего «Карнавала Теней».\n"
            "Вы отдыхаете вместе с Четом Мортоном, и воздух вокруг пропитан невероятными ароматами:\n"
            "горячими, пышными карнавальными пончиками, густо присыпанными сахарной пудрой,\n"
            "яблоками в густой янтарной карамели, блестящей в свете гирлянд, большими ведрами\n"
            "соленого попкорна с маслом и ледяными вишневыми слейшами. (Классический гастрономический троп!)\n\n"
            "Вдруг к вам подбегает взволнованный владелец карнавала, мистер Дженкинс:\n"
            "— Ребята Харди! Случилась беда! Кто-то похитил наш главный аттракцион — механического предсказателя Золтара!\n"
            "Но дело не в аттракционе... Внутри Золтара был спрятан секретный микрочип синдиката «Дирижер»,\n"
            "который мой покойный брат-инженер пытался спасти. Вор в маске мима скрылся в сторону Лабиринта Зеркал!"
        ),
        'act1_q': "Как вы начнете преследование?",
        'act1_opt1': "1. [Выбор Фрэнка] Побежать в будку охраны, взломать систему камер и отследить мима по мониторам.",
        'act1_opt2': "2. [Выбор Джо] Не раздумывая, броситься в Лабиринт Зеркал наперерез, чтобы перехватить вора по горячим следам.",
        'act1_out1': (
            "\nФрэнк действует рационально. Вы врываетесь в будку охраны. Используя знания электроники,\n"
            "Фрэнк переподключает кабели мониторов и видит на экране мима, который прячет чип в карман возле выхода из зеркал.\n"
            "Вы берете карту карнавала, фонарик и направляетесь на опережение к заброшенному шатру Freak Show.\n"
            "В вашем инвентаре появляется: КАРТА и ФОНАРИК."
        ),
        'act1_out2': (
            "\nДжо мчится вперед! Рев толпы затихает, когда вы забегаете под стеклянные арки лабиринта.\n"
            "Вокруг вас тысячи ваших отражений. Вдруг одна из теней резко поворачивает за угол.\n"
            "Вы бежите вслепую сквозь стеклянные коридоры, ориентируясь только на звук шагов.\n"
            "В вашем инвентаре есть только ФОНАРИК."
        ),
        'act2_title': "\n--- АКТ II: ЛАБИРИНТ ОТРАЖЕНИЙ ---",
        'act2_text': (
            "Лабиринт Зеркал выглядит жутко в ночном освещении. Свет преломляется под странными углами.\n"
            "Вдруг впереди раздается издевательский смех мима, заманивающий вас вглубь ловушки."
        ),
        'act2_frank_branch': (
            "\nБлагодаря просмотру камер охраны Фрэнк точно знает расположение фальшивых зеркал.\n"
            "Вы видите, что мим пытается завлечь вас в тупик с шатким полом."
        ),
        'act2_joe_branch': (
            "\nДжо бежит вслепую. Вдруг зеркала вокруг начинают вращаться, создавая дезориентирующую иллюзию.\n"
            "Настоящий мим исчезает, а перед вами появляется закрытая зеркальная панель с кодовым замком."
        ),
        'act2_q': "Ваше действие для преодоления препятствия?",
        'act2_opt1': "1. Попробовать разгадать закономерность лазерных лучей на зеркалах (логический путь).",
        'act2_opt2': "2. Использовать физическую силу, чтобы выбить шаткую панель плечом (путь действия).",
        'act2_out1': (
            "\nВы внимательно анализируете преломление света фонарика. Фрэнк высчитывает угол падения\n"
            "и находит секретную кнопку, которая открывает панель без единого шума. Вы прокрадываетесь дальше!"
        ),
        'act2_out2': (
            "\nДжо разбегается и с силой бьет плечом по стыку панелей! С грохотом рама поддается,\n"
            "открывая проход к старому шатру Freak Show. Но громкий звук привлек внимание!"
        ),
        'act3_title': "\n--- АКТ III: ЛОВУШКА ПОД КУПОЛОМ И КРЕПКАЯ ГОЛОВА ---",
        'act3_text': (
            "Вы оказываетесь в полутемном, заброшенном шатре Freak Show среди старых клеток и реквизита.\n"
            "Вдруг сверху раздается скрип. Тяжелая железная трапеция срывается с купола и летит прямо на вас!\n"
            "Джо успевает оттолкнуть Фрэнка, но сам получает сильный удар металлической штангой по голове!\n"
            "Джо падает на арену без сознания, а мим запирает за вами тяжелую стальную клетку для тигров!\n\n"
            "Через минуту Джо приходит в себя, потирая большую шишку на затылке:\n"
            "— Ох... Моя бедная голова. Кажется, по мне проехал товарный поезд Бейпорта! (Классический троп!)\n"
            "— Но ничего, бывало и хуже, разберемся с этим клоуном позже. Как нам выбраться?"
        ),
        'act3_q': "Клетка заблокирована магнитным замком. Что вы сделаете?",
        'act3_opt1': "1. [Действие Джо] Использовать старый железный указатель как рычаг, чтобы разогнуть прутья силой.",
        'act3_opt2': "2. [Действие Фрэнка] Использовать знания электроники, чтобы вскрыть пульт замка и замкнуть провода напрямую.",
        'act3_out1_success': (
            "\nДжо вставляет тяжелый металлический указатель между прутьями клетки. Напрягши все силы,\n"
            "вы раздвигаете старые ржавые прутья настолько, что Фрэнк и Джо едва протискиваются на волю!"
        ),
        'act3_out1_fail': (
            "\nВы пытаетесь разогнуть прутья, но железо слишком прочное. Вы лишь напрасно устаете.\n"
            "Нужно искать более умный подход!"
        ),
        'act3_out2_success': (
            "\nФрэнк разбирает защитную крышку электронного пульта. Найдя нужные контакты,\n"
            "он замыкает их батарейкой от фонарика. Искры летят во все стороны — и магнитный замок открывается!"
        ),
        'act4_title': "\n--- АКТ IV: ФИНАЛ НА ЧЕРТОВОМ КОЛЕСЕ ---",
        'act4_text': (
            "Вы выбегаете на площадь карнавала. Мим уже пытается запустить Чертово колесо,\n"
            "чтобы подняться на платформу технического обслуживания, где его ждет сообщник на вертолете!\n"
            "Кабины колеса начинают стремительно вращаться. Микрочип в его руках!"
        ),
        'act4_q': "Как остановить беглеца?",
        'act4_opt1': "1. [Действие Джо] Прыгнуть на металлическую конструкцию колеса и заблокировать механизм ручным тормозом.",
        'act4_opt2': "2. [Действие Фрэнка] Подбежать к пульту управления аттракционом и перегрузить генератор, выключив питание.",
        'act4_out1': (
            "\nДжо совершает отчаянный прыжок на стальные опоры колеса! Цепляясь за балки,\n"
            "он добирается до рычага экстренного торможения и жмет на него всем весом.\n"
            "Колесо останавливается с громким скрежетом! Мим теряет равновесие, падает на сетку, где его вяжет Фрэнк!"
        ),
        'act4_out2': (
            "\nФрэнк подбегает к главному генератору карнавала. Быстро сориентировавшись в тумблерах,\n"
            "он переводит подачу тока в режим максимальной нагрузки. Предохранители взрываются,\n"
            "колесо плавно останавливается, блокируя мима в кабине на высоте трех метров до приезда полиции!"
        ),
        'final_header': "                 ФИНАЛ                       ",
        'final_high': (
            "Поздравляем! Дело раскрыто блестяще! Ваш счет: {score} очков.\n"
            "Секретный микрочип возвращен, а мима и его сообщников арестовал шериф Коллиг.\n"
            "Мистер Дженкинс безмерно благодарен вам и бесплатно угощает горячими бельгийскими вафлями\n"
            "и карамельным мороженым. Чет Мортон уверяет, что это лучший карнавал в его жизни,\n"
            "а Бейпорт снова может спать спокойно!"
        ),
        'final_normal': (
            "Дело успешно завершено! Ваш счет: {score} очков.\n"
            "Хотя Джо получил еще одну крепкую шишку на голове, а Фрэнку пришлось изрядно поломать мозг,\n"
            "вы снова доказали, что для братьев Харди нет неразрешимых загадок!"
        ),
        'final_thanks': "\nСпасибо за игру! Фрэнк и Джо гордились бы вашим выбором."
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
        choice = input(loc.get('lang_choice_prompt', '\n-> ')).strip()
        
        if choice == '1':
            state.route_taken = 'frank'
            state.score += 20
            state.inventory.append('map')
            state.inventory.append('flashlight')
            print_slow(loc['act1_out1'])
            break
        elif choice == '2':
            state.route_taken = 'joe'
            state.score += 10
            state.inventory.append('flashlight')
            print_slow(loc['act1_out2'])
            break
        else:
            print(loc['invalid_input'])
            
    act_2(state)

def act_2(state):
    loc = LOCALIZATION[state.lang]
    print_slow(loc['act2_title'])
    print_slow(loc['act2_text'])
    
    if state.route_taken == 'frank':
        print_slow(loc['act2_frank_branch'])
    else:
        print_slow(loc['act2_joe_branch'])
        
    while True:
        print("\n" + loc['act2_q'])
        print(loc['act2_opt1'])
        print(loc['act2_opt2'])
        choice = input(loc.get('lang_choice_prompt', '\n-> ')).strip()
        
        if choice == '1':
            state.score += 20
            print_slow(loc['act2_out1'])
            break
        elif choice == '2':
            state.score += 10
            print_slow(loc['act2_out2'])
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
        choice = input(loc.get('lang_choice_prompt', '\n-> ')).strip()
        
        if choice == '1':
            if state.route_taken == 'joe' or 'map' not in state.inventory:
                # If they dashed blindly, they are tired or lacks leverage tools, but let's allow it as a struggle
                state.score += 15
                print_slow(loc['act3_out1_success'])
                break
            else:
                state.score += 20
                print_slow(loc['act3_out1_success'])
                break
        elif choice == '2':
            state.score += 25
            print_slow(loc['act3_out2_success'])
            break
        else:
            print(loc['invalid_input'])
            
    act_4(state)

def act_4(state):
    loc = LOCALIZATION[state.lang]
    print_slow(loc['act4_title'])
    print_slow(loc['act4_text'])
    
    while True:
        print("\n" + loc['act4_q'])
        print(loc['act4_opt1'])
        print(loc['act4_opt2'])
        choice = input(loc.get('lang_choice_prompt', '\n-> ')).strip()
        
        if choice == '1':
            state.score += 20
            print_slow(loc['act4_out1'])
            break
        elif choice == '2':
            state.score += 25
            print_slow(loc['act4_out2'])
            break
        else:
            print(loc['invalid_input'])
            
    # Final screen
    print_slow("\n=============================================")
    print_slow(loc['final_header'])
    print_slow("=============================================\n")
    
    if state.score >= 80:
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
