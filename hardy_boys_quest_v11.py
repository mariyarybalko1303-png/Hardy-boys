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
        'uk': "          БРАТИ ХАРДІ ТА ТАЄМНИЦЯ ЧОРНОГО ПАКЕТУ (ЧАСТИНА XI)          ",
        'en': "      THE HARDY BOYS AND THE SECRET OF THE BLACK CASE (PART XI)       ",
        'ru': "          БРАТЬЯ ХАРДИ И ТАЙНА ЧЕРНОГО ПАКЕТА (ЧАСТЬ XI)              "
    }
    subtitle_text = {
        'uk': "          Справа від Фентона Харді: Інтерактивний квест               ",
        'en': "          A Fenton Hardy Assignment: Interactive Quest                ",
        'ru': "          Дело от Фентона Харди: Интерактивный квест                  "
    }
    print("=" * 75)
    print(title_text[lang])
    print(subtitle_text[lang])
    print("=" * 75)
    print()

class GameState:
    def __init__(self):
        self.lang = 'uk'
        self.inventory = []
        self.route_taken = None  # 'frank' (decode/museum) or 'joe' (boat/swamp)
        self.stealth_success = False
        self.score = 0

# Localization dictionary
LOCALIZATION = {
    'uk': {
        'select_lang': "Оберіть мову / Select Language / Выберите язык:\n1. Українська\n2. English\n3. Русский",
        'lang_choice_prompt': "Ваш вибір (1-3): ",
        'press_enter': "Натисніть ENTER, щоб розпочати пригоду...",
        'invalid_input': "Будь ласка, введіть 1 або 2.",
        'intro_text': (
            "Ви граєте за відомих братів-детективів Френка та Джо Харді.\n"
            "Сьогодні особливий день. Ваш батько, легендарний приватний детектив Фентон Харді,\n"
            "зателефонував вам із Вашингтона і доручив надзвичайно важливу та конфіденційну справу!\n"
            "Він сказав: «Хлопці, державна безпека під загрозою. Я не можу повернутися в Бейпорт,\n"
            "тому вся надія лише на ваш розум та сміливість»."
        ),
        'act1_title': "\n--- АКТ I: ДОРУЧЕННЯ БАТЬКА ТА СИБІРСЬКІ БУТЕРБРОДИ ---",
        'act1_text': (
            "Ви сидите на кухні будинку Харді. На столі лежать величезні домашні бутерброди,\n"
            "які перед від'їздом приготувала тітка Гертруда: пишний свіжий білий хліб,\n"
            "товсті соковиті шматки запеченої шинки, домашня гірчиця, хрусткі солоні огірочки\n"
            "та теплий чай з чебрецем. Чет Мортон уже доїдає третій сендвіч і тягнеться до четвертого.\n\n"
            "Раптом дзвонить телефон. Це Фентон Харді. Його голос серйозний як ніколи:\n"
            "— Френку, Джо, слухайте уважно. З секретної лабораторії Бейпорта викрали революційний\n"
            "мікрофільм з кресленнями новітнього військового сонара «Полярна Зірка».\n"
            "Головний підозрюваний — іноземний шпигун на прізвисько «Привид». Він переховується\n"
            "у старому елінгу на Болотяному Мисі під виглядом рибалки і планує передати фільм покупцеві сьогодні о 3-й ночі.\n"
            "Поліція Бейпорта безсила, бо у шпигуна є впливові покровителі. Ви повинні дістати мікрофільм!"
        ),
        'act1_q': "З чого ви розпочнете розслідування?",
        'act1_opt1': "1. [Шлях Френка] Проаналізувати робочий кабінет батька, знайти його старі досьє на шпигуна та розшифрувати його улюблені радіочастоти.",
        'act1_opt2': "2. [Шлях Джо] Негайно застрибнути у катер «Нишпорка» і мчати до Болотяного Мису під покровом нічного туману.",
        'act1_out1': (
            "\nВи залишаєтесь у кабінеті Фентона Харді. Френк знаходить секретну папку батька.\n"
            "Серед старих документів ви виявляєте шифрований блокнот «Привида». Завдяки логіці\n"
            "та знанням шифрів, Френк швидко зламує код: шпигун використовує частоту 144.8 МГц для зв'язку.\n"
            "Ви берете із собою портативний радіосканер, ліхтарик та вирушаєте до Болотяного Мису.\n"
            "Тепер ви можете прослуховувати розмови ворога!"
        ),
        'act1_out2': (
            "\nДжо не звик сидіти на місці! Ревіння мотора катера «Нишпорка» розтинає тишу.\n"
            "Ви мчите вздовж темних берегів, де туман стає густішим з кожною хвилиною.\n"
            "Ви прибуваєте до Болотяного Мису непоміченими, причаливши у занедбаній затоці.\n"
            "У вашому розпорядженні ліхтарик, мотузка та набір інструментів."
        ),
        'act2_title': "\n--- АКТ II: ОПЕРАЦІЯ «БОЛОТЯНИЙ МИС» ---",
        'act2_text': (
            "Старий дерев'яний елінг шпигуна самотньо стоїть на палях над брудною водою.\n"
            "Крізь щілини у дошках пробивається слабке світло гасової лампи.\n"
            "Біля входу стоїть озброєний охоронець шпигуна, який пильно вдивляється в темряву.\n"
            "Якщо ви будете необережними, він підніме тривогу і мікрофільм зникне назавжди!"
        ),
        'act2_q': "Як ви нейтралізуєте або обійдете охоронця?",
        'act2_opt1': "1. Спробувати відволікти його (кинути старий залізний якір у воду з іншого боку, щоб виманити його).",
        'act2_opt2': "2. Використати радіосканер (якщо обрали шлях Френка) або здійснити стрімкий обхідний маневр по даху.",
        'act2_out1': (
            "\nДжо з силою кидає іржавий якір у воду. Лунає гучний сплеск!\n"
            "Охоронець здригається, вихоплює ліхтарик і повільно йде до краю причалу з'ясувати причину звуку.\n"
            "У цей момент Френк і Джо спритно прослизають через бічні двері елінгу!"
        ),
        'act2_out2_scanner': (
            "\nВи вмикаєте радіосканер Френка і перехоплюєте радіообмін охоронця.\n"
            "Ви дізнаєтесь, що у нього розрядилася батарея рації і він збирається зайти всередину за новою.\n"
            "Ви терпляче чекаєте у тіні, і коли він заходить, ви безшумно прослизаєте повз нього на склад!"
        ),
        'act2_out2_roof': (
            "\nДжо рішуче підсаджує Френка, і ви разом видираєтесь на слизький, вкритий мохом дах.\n"
            "Ви прокрадаєтесь до старого вентиляційного люка і обережно спускаєтесь всередину елінгу.\n"
            "Проте стара черепиця під ногами Джо з тихим тріском ламається! Охоронець піднімає голову, але\n"
            "сприймає це за звичайних щурів. Вам пощастило!"
        ),
        'act3_title': "\n--- АКТ III: ПАСТКА У ЕЛІНГУ ТА МІЦНА ГОЛОВА ---",
        'act3_text': (
            "Всередині елінгу пахне сухою рибою, машинним мастилом та порохом.\n"
            "У кутку під брезентом ви знаходите металевий сейф із кодовим замком.\n"
            "Раптом ззаду лунає зловісний сміх! Сам шпигун «Привид» виходить із тіні з важким веслом у руках!\n"
            "Він робить підступний замах і з силою б'є Джо ззаду по голові! Джо падає без тями.\n"
            "Френка миттєво скручують двоє спільників шпигуна. Вас обох зачиняють у дерев'яній клітці для риби,\n"
            "яка висить на ланцюгах безпосередньо над крижаною водою затоки!\n\n"
            "За кілька хвилин Джо приходить до тями, трясучи головою:\n"
            "— Ох, брате... Здається, моя потилиця зустрілася з бейсбольною битою. Але нічого,\n"
            "у мене міцна голова! Бувало й гірше! (Фірмовий троп серії книг!)\n"
            "Вода під кліткою піднімається — починається приплив, про який попереджав батько!"
        ),
        'act3_q': "Як ви виберетесь із клітки, що опускається у воду?",
        'act3_opt1': "1. [Сила Джо] Спробувати розхитати старі дерев'яні грати клітки та вибити їх сильним ударом ноги.",
        'act3_opt2': "2. [Розум Френка] Використати металеву пряжку від ременя Джо, щоб відкрутити болти кріплення ланцюга.",
        'act3_out1_success': (
            "\nДжо робить глибокий вдих і з силою б'є обома ногами по нижній частині грат клітки.\n"
            "Старе дерево з тріском ламається! Ви вистрибуєте на дерев'яний поміст якраз у той момент,\n"
            "коли нижня частина клітки занурюється у воду. Ви вільні!"
        ),
        'act3_out1_fail': (
            "\nВи намагаєтесь вибити грати ногами, але дерево виявляється надто міцним і вологим.\n"
            "Ви лише відбиваєте ноги, а вода вже досягає ваших колін! Потрібно негайно спробувати інший спосіб."
        ),
        'act3_out2_success': (
            "\nФренк дістає пряжку і спритно використовує її як імпровізовану викрутку.\n"
            "Він швидко послаблює та відкручує заіржавілий болт головного ланцюга.\n"
            "Клітка різко нахиляється, і ви через утворений отвір у верхній кришці вибираєтесь на балку.\n"
            "Врятовані завдяки кмітливості Френка!"
        ),
        'act4_title': "\n--- АКТ IV: ФІНАЛЬНИЙ ДВОБІЙ ТА ПОВЕРНЕННЯ СПРАВЕДЛИВОСТІ ---",
        'act4_text': (
            "Ви вибираєтесь на сушу і бачите, що «Привид» уже сідає у свій швидкісний гідролітак,\n"
            "щоб назавжди втекти з викраденим мікрофільмом.\n"
            "Гвинт літака починає шалено обертатися, здіймаючи хвилі бризок.\n"
            "У вас є лічені секунди, щоб зупинити шпигуна та виконати доручення Фентона Харді!"
        ),
        'act4_q': "Як ви зупините гідролітак шпигуна?",
        'act4_opt1': "1. [Дія Джо] Стрибнути на поплавок гідролітака, що рушає, розбити скло кабіни та вирвати штурвал.",
        'act4_opt2': "2. [Дія Френка] Кинути важкий кінець мотузки з вузлом у гвинт двигуна літака або заблокувати стерно висоти.",
        'act4_out1': (
            "\nДжо здійснює неймовірний відчайдушний стрибок прямо на поплавок літака!\n"
            "Тримаючись за крило під шаленим вітром, він розбиває скло кабіни ліхтариком\n"
            "і скручує здивованого шпигуна! Френк швидко застрибує слідом і допомагає зв'язати ворога."
        ),
        'act4_out2': (
            "\nФренк миттєво оцінює ситуацію. Він бере міцну мотузку, робить важку петлю\n"
            "і влучно кидає її прямо на хвостове стерно літака, прив'язавши інший кінець до причальної палі!\n"
            "Літак робить різкий ривок, мотузка натягується, і хвіст літака блокується. Шпигун не може злетіти!"
        ),
        'final_header': "                 ФІНАЛ                       ",
        'final_high': (
            "Вітаємо! Ви блискуче виконали особисте доручення батька! Ваш рахунок: {score} очок.\n"
            "Шпигуна «Привида» передано під варту федеральним агентам, а секретний мікрофільм «Полярна Зірка» повернуто.\n"
            "Фентон Харді телефонує вам і з гордістю каже:\n"
            "— Чудова робота, сини! Я ніколи не сумнівався у вашому таланті. Ви справжні детективи.\n"
            "Увечері тітка Гертруда повертається додому і влаштовує грандіозне святкування:\n"
            "вона випікає гігантський яблучний пиріг, а Чет Мортон приносить цілий кошик гарячих пончиків!"
        ),
        'final_normal': (
            "Справу успішно закрито! Ваш рахунок: {score} очок.\n"
            "Хоча шпигунові ледь не вдалося втекти, а потилиця Джо все ще прикрашена величезною гулею,\n"
            "ви змогли повернути мікрофільм та довести батькові, що ваші навички бездоганні.\n"
            "Бейпорт та уся країна в безпеці завдяки братам Харді!"
        ),
        'final_thanks': "\nДякуємо за гру! Френк та Джо пишалися б вашими рішеннями."
    },
    'en': {
        'select_lang': "Select Language / Оберіть мову / Выберите язык:\n1. Українська\n2. English\n3. Русский",
        'lang_choice_prompt': "Your choice (1-3): ",
        'press_enter': "Press ENTER to start the adventure...",
        'invalid_input': "Please enter 1 or 2.",
        'intro_text': (
            "You are playing as the famous detective brothers, Frank and Joe Hardy.\n"
            "Today is a special day. Your father, the legendary private investigator Fenton Hardy,\n"
            "has called you from Washington and assigned you a highly confidential and critical case!\n"
            "He said: 'Boys, national security is at stake. I cannot return to Bayport,\n"
            "so all hope lies in your sharp minds and bravery.'"
        ),
        'act1_title': "\n--- ACT I: FATHER'S ASSIGNMENT & GIGANTIC SANDWICHES ---",
        'act1_text': (
            "You are sitting in the kitchen of the Hardy home. On the table are huge homemade sandwiches\n"
            "prepared by Aunt Gertrude before she left: thick fresh white bread, juicy cuts of baked ham,\n"
            "homemade mustard, crunchy pickles, and warm thyme tea. Chet Morton is already finishing\n"
            "his third sandwich and reaching for a fourth.\n\n"
            "Suddenly, the phone rings. It's Fenton Hardy. His voice is graver than ever:\n"
            "— Frank, Joe, listen carefully. A revolutionary microfilm containing the blueprints\n"
            "for the newest military sonar 'Polar Star' has been stolen from a secure Bayport lab.\n"
            "The prime suspect is a foreign spy known as 'The Phantom'. He is hiding in an old boathouse\n"
            "at Swamp Point disguised as a fisherman, planning to hand over the film to a buyer tonight at 3 AM.\n"
            "The local police are powerless because he has highly placed protectors. You must retrieve that microfilm!"
        ),
        'act1_q': "How will you begin the investigation?",
        'act1_opt1': "1. [Frank's Choice] Analyze your father's home office, find his old files on the spy, and scan his radio frequencies.",
        'act1_opt2': "2. [Joe's Choice] Instantly hop into your speedboat 'The Sleuth' and race to Swamp Point under the cover of night fog.",
        'act1_out1': (
            "\nYou stay in Fenton Hardy's study. Frank finds their father's classified folder.\n"
            "Among old documents, you find 'The Phantom's' encrypted notebook. Using pure logic and math,\n"
            "Frank quickly cracks the code: the spy uses 144.8 MHz frequency for radio communication.\n"
            "You pack a portable radio scanner, a flashlight, and head to Swamp Point, ready to intercept their transmissions!"
        ),
        'act1_out2': (
            "\nJoe isn't one to sit around! The roar of 'The Sleuth's' engine shatters the night.\n"
            "You speed along the dark shoreline as the fog thickens by the minute.\n"
            "You arrive at Swamp Point completely undetected, mooring in a secluded, muddy cove.\n"
            "You only have a flashlight, some rope, and a toolbox with you."
        ),
        'act2_title': "\n--- ACT II: OPERATION SWAMP POINT ---",
        'act2_text': (
            "The spy's old wooden boathouse stands lonely on stilts over the muddy water.\n"
            "A faint light from a kerosene lamp flickers through the cracks in the walls.\n"
            "A heavily armed guard stands at the entrance, scanning the foggy darkness.\n"
            "If you make a noise, he will sound the alarm and the microfilm will be lost forever!"
        ),
        'act2_q': "How do you bypass or neutralize the guard?",
        'act2_opt1': "1. Distract him (throw an old iron anchor into the water on the other side to lure him away).",
        'act2_opt2': "2. Use the radio scanner (if you chose Frank's path) or perform a stealthy climb over the roof.",
        'act2_out1': (
            "\nJoe throws the rusty anchor with full force. A loud splash echoes through the swamp!\n"
            "The guard startles, grabs his flashlight, and slowly walks to the edge of the dock to investigate.\n"
            "In that split second, Frank and Joe slip through the boathouse's side door!"
        ),
        'act2_out2_scanner': (
            "\nYou turn on Frank's radio scanner and intercept the guard's radio talk.\n"
            "You learn his walkie-talkie battery is dying and he is about to step inside to grab a spare.\n"
            "You wait in the shadows, and when he walks in, you quietly slip past him into the warehouse!"
        ),
        'act2_out2_roof': (
            "\nJoe boosts Frank up, and together you scale the slippery, moss-covered roof.\n"
            "You make your way to an old ventilation hatch and carefully slide down inside.\n"
            "However, a loose tile cracks under Joe's foot! The guard looks up, but shrugs it off\n"
            "as rats. Talk about a close call!"
        ),
        'act3_title': "\n--- ACT III: THE BOATHOUSE TRAP & THE HARD HEAD ---",
        'act3_text': (
            "Inside, the boathouse smells of dried fish, motor oil, and gunpowder.\n"
            "Under a tarp in the corner, you find a steel safe with a combination lock.\n"
            "Suddenly, sinister laughter echoes from behind! 'The Phantom' himself steps out\n"
            "holding a heavy wooden oar! He swings and strikes Joe hard on the back of his head!\n"
            "Joe drops cold. Frank is quickly overpowered by two henchmen.\n"
            "You are both locked in a wooden fish cage hanging on chains directly over the freezing harbor water!\n\n"
            "A few minutes later, Joe wakes up, shaking his head:\n"
            "— Ouch, brother... Feels like my skull met a freight train. But hey,\n"
            "I've got a hard head! I've had worse! (A classic trope of the books!)\n"
            "The water below is rising — the high tide Fenton warned you about has begun!"
        ),
        'act3_q': "How will you escape the cage before it submerges?",
        'act3_opt1': "1. [Joe's Strength] Try to loosen the old wooden bars of the cage and smash them with a powerful kick.",
        'act3_opt2': "2. [Frank's Logic] Use the metal buckle from Joe's belt to unscrew the rusty bolt holding the chain.",
        'act3_out1_success': (
            "\nJoe takes a deep breath and kicks the bottom wooden bars with all his might.\n"
            "The rotten wood splinters! You squeeze out onto the wooden platform just as\n"
            "the bottom of the cage sinks into the freezing water. Free at last!"
        ),
        'act3_out1_fail': (
            "\nYou try to kick the bars, but the wet wood is too elastic and holds firm.\n"
            "You only bruise your feet, and the water is already up to your knees! Try another way quickly!"
        ),
        'act3_out2_success': (
            "\nFrank grabs the belt buckle and masterfully uses it as an improvised screwdriver.\n"
            "He quickly loosens and unscrews the rusty bolt of the main suspension chain.\n"
            "The cage tilts sharply, allowing you to climb out through the top hatch onto the rafters.\n"
            "Saved by Frank's quick thinking!"
        ),
        'act4_title': "\n--- ACT IV: THE FINAL CONFRONTATION ---",
        'act4_text': (
            "You sprint outside and see 'The Phantom' boarding his fast seaplane\n"
            "to escape forever with the stolen microfilm.\n"
            "The plane's propeller starts spinning violently, kicking up huge sprays of water.\n"
            "You have mere seconds to stop the spy and fulfill Fenton Hardy's mission!"
        ),
        'act4_q': "How will you stop the seaplane?",
        'act4_opt1': "1. [Joe's Action] Make an athletic leap onto the plane's pontoon, smash the cabin glass, and grab the throttle.",
        'act4_opt2': "2. [Frank's Action] Throw a heavy looped rope into the tail rudder or tie the plane to a harbor pile.",
        'act4_out1': (
            "\nJoe makes an incredible, desperate leap straight onto the plane's pontoon!\n"
            "Clinging to the wing struts against the roaring wind, he smashes the cabin glass with his flashlight\n"
            "and subdues the shocked spy! Frank leaps aboard right after and helps tie him up."
        ),
        'act4_out2': (
            "\nFrank acts instantly. He grabs a heavy dock rope, loops it, and throws it accurately\n"
            "around the plane's tail rudder, securing the other end to a heavy mooring pile!\n"
            "The plane surges forward, the rope snaps tight, and the tail is locked. The spy cannot take off!"
        ),
        'final_header': "                THE END                      ",
        'final_high': (
            "Congratulations! You solved the case brilliantly! Your score: {score} points.\n"
            "The spy 'The Phantom' is in federal custody, and the secret microfilm 'Polar Star' is secure.\n"
            "Fenton Hardy calls you and says with pride:\n"
            "— Outstanding work, sons! I never doubted you for a second. You are true detectives.\n"
            "In the evening, Aunt Gertrude returns and throws a grand celebration:\n"
            "she bakes a massive apple pie, and Chet Morton brings a whole basket of warm glazed donuts!"
        ),
        'final_normal': (
            "The case is closed successfully! Your score: {score} points.\n"
            "Though the spy almost escaped and Joe has a bump the size of an egg on his head,\n"
            "you retrieved the microfilm and proved to your father that you can handle anything.\n"
            "Bayport is safe once again thanks to the Hardy Boys!"
        ),
        'final_thanks': "\nThanks for playing! Frank and Joe would be proud of your choices."
    },
    'ru': {
        'select_lang': "Выберите язык / Oберіть мову / Select Language:\n1. Українська\n2. English\n3. Русский",
        'lang_choice_prompt': "Ваш выбор (1-3): ",
        'press_enter': "Нажмите ENTER, чтобы начать приключение...",
        'invalid_input': "Пожалуйста, введите 1 или 2.",
        'intro_text': (
            "Вы играете за знаменитых братьев-детективов Фрэнка и Джо Харди.\n"
            "Сегодня особенный день. Ваш отец, легендарный частный детектив Фентон Харди,\n"
            "позвонил вам из Вашингтона и поручил важнейшее конфиденциальное дело!\n"
            "Он сказал: «Ребята, государственная безопасность под угрозой. Я не могу вернуться в Бейпорт,\n"
            "так что вся надежда только на ваш ум и смелость»."
        ),
        'act1_title': "\n--- АКТ I: ПОРУЧЕНИЕ ОТЦА И ГИГАНТСКИЕ БУТЕРБРОДЫ ---",
        'act1_text': (
            "Вы сидите на кухне дома Харди. На столе лежат огромные домашние бутерброды,\n"
            "которые перед отъездом приготовила тетя Гертруда: пышный свежий белый хлеб,\n"
            "толстые сочные куски запеченной ветчины, домашняя горчица, хрустящие соленые огурчики\n"
            "и теплый чай с чабрецом. Чет Мортон уже доедает третий сэндвич и тянется за четвертым.\n\n"
            "Вдруг звонит телефон. Это Фентон Харди. Его голос серьезен как никогда:\n"
            "— Фрэнк, Джо, слушайте внимательно. Из секретной лаборатории Бейпорта похитили революционный\n"
            "микрофильм с чертежами новейшего военного сонара «Полярная Звезда».\n"
            "Главный подозреваемый — иностранный шпион по кличке «Призрак». Он скрывается\n"
            "в старом эллинге на Болотном Мысе под видом рыбака и планирует передать фильм покупателю сегодня в 3 часа ночи.\n"
            "Полиция Бейпорта бессильна, так как у шпиона есть влиятельные покровители. Вы должны вернуть микрофильм!"
        ),
        'act1_q': "С чего вы начнете расследование?",
        'act1_opt1': "1. [Путь Фрэнка] Проанализировать рабочий кабинет отца, найти его старые досье на шпиона и расшифровать радиочастоты.",
        'act1_opt2': "2. [Путь Джо] Немедленно запрыгнуть в катер «Ищейка» и мчаться к Болотному Мысу под покровом ночного тумана.",
        'act1_out1': (
            "\nВы остаетесь в кабинете Фентона Харди. Фрэнк находит секретную папку отца.\n"
            "Среди старых документов вы обнаруживаете шифрованный блокнот «Призрака». Благодаря логике\n"
            "и знанию шифров, Фрэнк быстро взламывает код: шпион использует частоту 144.8 МГц для связи.\n"
            "Вы берете портативный радиосканер, фонарик и отправляетесь к Болотному Мысу.\n"
            "Теперь вы можете прослушивать переговоры врага!"
        ),
        'act1_out2': (
            "\nДжо не привык сидеть на месте! Рев мотора катера «Ищейка» разрезает тишину.\n"
            "Вы мчитесь вдоль темных берегов, где туман с каждой минутой становится все гуще.\n"
            "Вы прибываете к Болотному Мысу незамеченными, причалив в заброшенной бухте.\n"
            "Из вещей у вас с собой только фонарик, веревка и набор инструментов."
        ),
        'act2_title': "\n--- АКТ II: ОПЕРАЦИЯ «БОЛОТНЫЙ МЫС» ---",
        'act2_text': (
            "Старый деревянный эллинг шпиона одиноко стоит на сваях над грязной водой.\n"
            "Сквозь щели в досках пробивается слабый свет керосиновой лампы.\n"
            "У входа стоит вооруженный охранник шпиона, пристально вглядывающийся в темноту.\n"
            "Если вы будете неосторожны, он поднимет тревогу и микрофильм исчезнет навсегда!"
        ),
        'act2_q': "Как вы нейтрализуете или обойдете охранника?",
        'act2_opt1': "1. Попробовать отвлечь его (бросить старый железный якорь в воду с другой стороны эллинга, чтобы выманить его).",
        'act2_opt2': "2. Использовать радиосканер (если выбрали путь Фрэнка) или совершить бесшумный обход по крыше.",
        'act2_out1': (
            "\nДжо с силой бросает ржавый якорь в воду. Раздается громкий всплеск!\n"
            "Охранник вздрагивает, выхватывает фонарь и медленно идет к краю причала выяснить причину шума.\n"
            "В этот момент Фрэнк и Джо ловко проскальзывают через боковую дверь эллинга!"
        ),
        'act2_out2_scanner': (
            "\nВы включаете радиосканер Фрэнка и перехватываете переговоры охраны.\n"
            "Вы узнаете, что у него разрядилась батарея рации и он собирается зайти внутрь за новой.\n"
            "Вы терпеливо ждете в тени, и когда он заходит, бесшумно проскальзываете мимо него на склад!"
        ),
        'act2_out2_roof': (
            "\nДжо решительно подсаживает Фрэнка, и вы вместе карабкаетесь на скользкую крышу.\n"
            "Вы пробираетесь к старому вентиляционному люку и осторожно спускаетесь внутрь эллинга.\n"
            "Однако старая черепица под ногами Джо с тихим треском ломается! Охранник поднимает голову, но\n"
            "принимает звук за обычных крыс. Пронесло!"
        ),
        'act3_title': "\n--- АКТ III: ЛОВУШКА В ЭЛЛИНГЕ И КРЕПКАЯ ГОЛОВА ---",
        'act3_text': (
            "Внутри эллинга пахнет сухой рыбой, машинным маслом и порохом.\n"
            "В углу под брезентом вы находите металлический сейф с кодовым замком.\n"
            "Вдруг сзади раздается зловещий смех! Сам шпион «Призрак» выходит из тени с тяжелым веслом!\n"
            "Он делает подлый замах и с силой бьет Джо сзади по голове! Джо падает без чувств.\n"
            "Фрэнка мгновенно скручивают двое сообщников шпиона. Вас обоих запирают в деревянной садке для рыбы,\n"
            "которая висит на цепях прямо над ледяной водой залива!\n\n"
            "Через несколько минут Джо приходит в себя, тряся головой:\n"
            "— Ох, брат... Кажется, мой затылок встретился с товарным поездом. Но ничего,\n"
            "у меня крепкая голова! Бывало и хуже! (Фирменный троп серии книг!)\n"
            "Вода под клеткой поднимается — начинается прилив, о котором предупреждал отец!"
        ),
        'act3_q': "Как вы выберетесь из клетки, опускающейся в воду?",
        'act3_opt1': "1. [Сила Джо] Попробовать расшатать старые деревянные прутья клетки и выбить их сильным ударом ноги.",
        'act3_opt2': "2. [Ум Фрэнка] Использовать металлическую пряжку от ремня Джо, чтобы открутить болты крепления цепи.",
        'act3_out1_success': (
            "\nДжо делает глубокий вдох и с силой бьет обеими ногами по нижней части прутьев клетки.\n"
            "Старое дерево с треском ломается! Вы выпрыгиваете на деревянный помост как раз в тот момент,\n"
            "когда нижняя часть клетки погружается в воду. Вы свободны!"
        ),
        'act3_out1_fail': (
            "\nВы пытаетесь выбить прутья ногами, но дерево оказывается слишком прочным.\n"
            "Вы только отбиваете ноги, а вода уже достигает колен! Нужно срочно попробовать другой способ."
        ),
        'act3_out2_success': (
            "\nФрэнк достает пряжку и ловко использует ее как импровизированную отвертку.\n"
            "Он быстро ослабляет и откручивает заржавевший болт подвесной цепи.\n"
            "Клетка резко наклоняется, позволяя вам выбраться через верхний люк на балки.\n"
            "Спасены благодаря смекалке Фрэнка!"
        ),
        'act4_title': "\n--- АКТ IV: ФИНАЛЬНАЯ СХВАТКА И ТОРЖЕСТВО ЗАКОНА ---",
        'act4_text': (
            "Вы выбираетесь на сушу и видите, что «Призрак» уже садится в свой гидросамолет,\n"
            "чтобы навсегда скрыться с похищенным микрофильмом.\n"
            "Винт самолета начинает бешено вращаться, поднимая фонтаны брызг.\n"
            "У вас есть считанные секунды, чтобы остановить шпиона и выполнить поручение Фентона Харди!"
        ),
        'act4_q': "Как вы остановите гидросамолет шпиона?",
        'act4_opt1': "1. [Действие Джо] Прыгнуть на поплавок взлетающего гидросамолета, разбить стекло кабины и вырвать штурвал.",
        'act4_opt2': "2. [Действие Фрэнка] Бросить тяжелый конец веревки с узлом в хвостовой руль самолета или привязать его к причалу.",
        'act4_out1': (
            "\nДжо совершает невероятный отчаянный прыжок прямо на поплавок самолета!\n"
            "Удерживаясь за крыло под яростным ветром, он разбивает стекло кабины фонариком\n"
            "и скручивает удивленного шпиона! Фрэнк быстро запрыгивает следом и помогает связать врага."
        ),
        'act4_out2': (
            "\nФрэнк мгновенно оценивает ситуацию. Он берет прочную веревку, делает тяжелую петлю\n"
            "и метко бросает ее прямо на хвостовой руль самолета, привязав другой конец к причальной свае!\n"
            "Самолет делает резкий рывок, веревка натягивается, и хвост блокируется. Шпион не может взлететь!"
        ),
        'final_header': "                 ФИНАЛ                       ",
        'final_high': (
            "Поздравляем! Вы блестяще выполнили личное поручение отца! Ваш счет: {score} очков.\n"
            "Шпион «Призрак» передан федеральным агентам, а секретный микрофильм «Полярная Звезда» возвращен.\n"
            "Фентон Харди звонит вам и с гордостью говорит:\n"
            "— Отличная работа, сыновья! Я никогда не сомневался в вашем таланте. Вы настоящие детективы.\n"
            "Вечером тетя Гертруда возвращается домой и устраивает грандиозный праздник:\n"
            "она выпекает огромный яблочный пирог, а Чет Мортон приносит целую корзину горячих пончиков!"
        ),
        'final_normal': (
            "Дело успешно закрыто! Ваш счет: {score} очков.\n"
            "Хотя шпиону едва не удалось скрыться, а затылок Джо все еще украшен огромной шишкой,\n"
            "вы смогли вернуть микрофильм и доказать отцу, что ваши навыки безупречны.\n"
            "Бейпорт и вся страна в безопасности благодаря братьям Харди!"
        ),
        'final_thanks': "\nСпасибо за игру! Фрэнк и Джо гордились бы вашими решениями."
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
        choice = input("-> ").strip()
        
        if choice == '1':
            state.route_taken = 'frank'
            state.score += 25
            state.inventory.append('radio_scanner')
            state.inventory.append('flashlight')
            print_slow(loc['act1_out1'])
            break
        elif choice == '2':
            state.route_taken = 'joe'
            state.score += 15
            state.inventory.append('flashlight')
            state.inventory.append('rope')
            print_slow(loc['act1_out2'])
            break
        else:
            print(loc['invalid_input'])
            
    act_2(state)

def act_2(state):
    loc = LOCALIZATION[state.lang]
    print_slow(loc['act2_title'])
    print_slow(loc['act2_text'])
    
    while True:
        print("\n" + loc['act2_q'])
        print(loc['act2_opt1'])
        print(loc['act2_opt2'])
        choice = input("-> ").strip()
        
        if choice == '1':
            state.score += 15
            print_slow(loc['act2_out1'])
            break
        elif choice == '2':
            if state.route_taken == 'frank':
                state.score += 25
                state.stealth_success = True
                print_slow(loc['act2_out2_scanner'])
            else:
                state.score += 10
                print_slow(loc['act2_out2_roof'])
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
        choice = input("-> ").strip()
        
        if choice == '1':
            if state.route_taken == 'joe' or state.stealth_success:
                state.score += 20
                print_slow(loc['act3_out1_success'])
                break
            else:
                print_slow(loc['act3_out1_fail'])
                continue
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
        choice = input("-> ").strip()
        
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
