import time
import sys

def print_slow(text, delay=0.01):
    """Prints text slowly for a vintage text adventure feel."""
    for char in text:
        sys.stdout.write(char)
        sys.stdout.flush()
        time.sleep(delay)
    print()

def display_header(lang):
    title_text = {
        'uk': "          БРАТИ ХАРДІ ТА ТАЄМНИЦЯ ПІРАТСЬКОГО ФОРТУ (ЧАСТИНА XV)          ",
        'en': "      THE HARDY BOYS AND THE MYSTERY OF THE PIRATE FORT (PART XV)       ",
        'ru': "          БРАТЬЯ ХАРДИ И ТАЙНА ПИРАТСКОГО ФОРТА (ЧАСТЬ XV)              "
    }
    subtitle_text = {
        'uk': "        Слідами іспанського галеону: Інтерактивний квест Юкатану          ",
        'en': "        On the Trail of the Spanish Galleon: Yucatan Quest              ",
        'ru': "        По следам испанского галеона: Интерактивный квест Юкатана        "
    }
    print("=" * 78)
    print(title_text[lang])
    print(subtitle_text[lang])
    print("=" * 78)
    print()

class GameState:
    def __init__(self):
        self.lang = 'uk'
        self.inventory = []
        self.route_taken = None  # 'frank' (decode/stars) or 'joe' (atv/jungle)
        self.escaped_stealth = False
        self.score = 0

# Localization dictionary
LOCALIZATION = {
    'uk': {
        'select_lang': "Оберіть мову / Select Language / Выберите язык:\n1. Українська\n2. English\n3. Русский",
        'lang_choice_prompt': "Ваш вибір (1-3): ",
        'press_enter': "Натисніть ENTER, щоб розпочати пригоду...",
        'invalid_input': "Будь ласка, введіть 1 або 2.",
        'intro_text': (
            "Ви граєте за відважних братів-детективів Френка та Джо Харді.\n"
            "Після розкриття таємниці іспанського галеону у Флориді, ви знайшли зашифрований\n"
            "бортовий журнал капітана. Записи вказують на те, що головні скарби «Санти-Ізабелли»\n"
            "були заховані у потаємному піратському форті, збудованому в стародавніх руїнах майя\n"
            "посеред непрохідних джунглів півострова Юкатан у Мексиці. Ви вирушаєте в дорогу!"
        ),
        'act1_title': "\n--- АКТ I: ТАКОС У ЮКАТАНІ ТА ШИФР МАЙЯ ---",
        'act1_text': (
            "Ви сидите на терасі невеликого мексиканського кафе на самому краї джунглів.\n"
            "Перед вами — справжнє свято смаку: гарячі кукурудзяні такос із соковитою яловичиною\n"
            "барбакоа, гострим соусом сальса верде, свіжою кінзою та шматочками стиглого авокадо.\n"
            "Поруч димиться запечена кукурудза «елоте», щедро полита соусом і присипана сиром котіха,\n"
            "а Чет Мортон запиває свій третій соковитий буріто холодним солодким чаєм каркаде.\n\n"
            "Френк розкладає на столі старовинну карту з журналу іспанського капітана.\n"
            "Вона містить дивні астрономічні позначки, що вказують шлях до форту крізь джунглі.\n"
            "Але місцеві мешканці попереджають: у джунглях орудує небезпечна банда чорних археологів\n"
            "під керівництвом безжального найманця на прізвисько «Ягуар»!"
        ),
        'act1_q': "Який шлях ви оберете для просування вглиб джунглів?",
        'act1_opt1': "1. [Шлях Френка] Залишитися в таборі, розшифрувати сузір'я на карті та вирахувати безпечну стежку, уникаючи прадавніх пасток.",
        'act1_opt2': "2. [Шлях Джо] Орендувати потужні квадроцикли (ATV) та прорватися навпростець через болотяні стежки, покладаючись на швидкість.",
        'act1_out1': (
            "\nВи залишаєтеся у таборі. Френк порівнює нічне небо Юкатану зі схемами іспанців.\n"
            "Вам вдається розгадати шифр: шлях пролягає вздовж русла висохлої річки, що оминає хиткі піски.\n"
            "Ви берете із собою компас, мотузку, мачете та вирушаєте пішки по безпечному маршруту."
        ),
        'act1_out2': (
            "\nРевіння моторів квадроциклів відлунює в джунглях! Джо тисне на газ, піднімаючи хмари болота.\n"
            "Ви несетеся крізь ліани та бамбукові хащі. Чет Мортон міцно тримається ззаду, кричачи від страху й захвату.\n"
            "Ви долаєте складні перешкоди і виходите прямо до стін форту значно раніше за переслідувачів.\n"
            "У вашому багажнику — ліхтарики, мачете та набір інструментів."
        ),
        'act2_title': "\n--- АКТ II: ШТУРМ ПІРАТСЬКОГО ФОРТУ ---",
        'act2_text': (
            "Перед вами постає величний і похмурий піратський форт, збудований на вершині піраміди майя.\n"
            "Він повністю заріс ліанами, а стародавні кам'яні стіни дихають небезпекою.\n"
            "Біля головних воріт ви помічаєте озброєних найманців Ягуара, які тримають на поготові гвинтівки.\n"
            "У центрі подвір'я стоїть генератор, який живить їхнє пошукове обладнання."
        ),
        'act2_q': "Як ви прокрадетеся всередину форту?",
        'act2_opt1': "1. Вивести з ладу генератор (перерізати паливний шланг за допомогою мачете, щоб знеструмити табір та створити паніку).",
        'act2_opt2': "2. Спробувати залізти через стародавній стічний жолоб з тильного боку піраміди, оминаючи охорону.",
        'act2_out1': (
            "\nФренк непомітно прокрадається до генератора і одним точним ударом мачете перерізає паливний шланг.\n"
            "Генератор чхає і глохне! Світло гасне, найманці починають кричати і метушитися в темряві.\n"
            "Користуючись цим, брати Харді безперешкодно прослизають крізь відкриті ворота форту!"
        ),
        'act2_out2_rope': (
            "\nВикористовуючи мотузку Френка, ви чіпляєтеся за старе кам'яне кільце на стіні форту.\n"
            "Джо першим спритно піднімається по слизькій стіні вгору, допомагаючи братові та Чету.\n"
            "Ви опиняєтеся безпосередньо у внутрішньому дворику форту без жодного шуму!"
        ),
        'act2_out2_climb': (
            "\nВи починаєте дертися по мокрих кам'яних виступах стіни.\n"
            "Раптом з-під ноги Джо виривається камінь і з гуркотом падає вниз! Охорона насторожується,\n"
            "але Чет Мортон вчасно імітує виття дикого ягуара. Перелякані найманці не наважуються перевіряти.\n"
            "Ви успішно перелізаєте через стіну!"
        ),
        'act3_title': "\n--- АКТ III: ПАСТКА ХРАМУ ТА МІЦНА ГОЛОВА JOE ---",
        'act3_text': (
            "Ви спускаєтеся в підземелля форту і потрапляєте до головної скарбниці.\n"
            "Тут стоять скрині, повні іспанських золотих дублонів, срібних кубків та масок майя!\n"
            "Раптом стеля починає дрижати. Стародавня пастка активована! Величезна кам'яна плита зривається вниз!\n"
            "Джо в останню мить сильно штовхає Френка вбік, але сам не встигає відскочити —\n"
            "важкий уламок кам'яної колони б'є його прямо по голові! Джо непритомніє.\n"
            "У цей момент у залу вривається сам Ягуар зі своїми найманцями. Вони зв'язують вас\n"
            "та замикають у залізній клітці посеред затоплюваної зали підземелля.\n\n"
            "За кілька хвилин Джо приходить до тями, сильно трясучи головою та потираючи гулю:\n"
            "— Ох, брате... Здається, на мене наступив мамонт. Але нічого, мій череп міцніший за стародавній камінь! (Класичний троп!)\n"
            "Вода з підземного джерела починає швидко заповнювати залу, піднімаючись до ваших ніг!"
        ),
        'act3_q': "Як ви виберетеся з міцної залізної клітки?",
        'act3_opt1': "1. [Шлях Джо] Використати старий залізний гарпун, що лежить поруч, як важіль, щоб розігнути іржаві прути клітки.",
        'act3_opt2': "2. [Шлях Френка] Спробувати розібрати механізм стародавнього замка клітки за допомогою металевої пряжки від ременя.",
        'act3_out1_success': (
            "\nДжо хапає важкий гарпун, вставляє його між прутами клітки і налягає всією своєю вагою.\n"
            "Старі іржаві залізні прути з голосним скрипом розгинаються! Ви протискуєтеся крізь отвір\n"
            "якраз у той момент, коли вода досягає вашої талії. Ви вільні!"
        ),
        'act3_out1_fail': (
            "\nДжо намагається розігнути прути, але залізо виявляється надто товстим і міцним.\n"
            "Ви лише марно втрачаєте час та сили, поки вода продовжує стрімко прибувати! Потрібно негайно шукати інший спосіб."
        ),
        'act3_out2_success': (
            "\nФренк дістає металеву пряжку ременя, заточує її об камінь і обережно просовує в замкову шпарину.\n"
            "Прислухаючись до кожного клацання стародавнього механізму, він робить точний поворот. Клац!\n"
            "Важкі двері клітки відчиняються. Вибирайтеся швидше!"
        ),
        'act4_title': "\n--- АКТ IV: ФІНАЛЬНИЙ БІЙ ПІД КУПОЛОМ ДЖУНГЛІВ ---",
        'act4_text': (
            "Ви вибігаєте на вершину піраміди. Ягуар уже завантажив скрині зі скарбами у свій гелікоптер,\n"
            "який стоїть на майданчику, і гвинти машини починають шалено обертатися для зльоту.\n"
            "У вас є лічені секунди, щоб зупинити міжнародного злочинця та повернути скарби народу Мексики!"
        ),
        'act4_q': "Як ви зупините гелікоптер Ягуара?",
        'act4_opt1': "1. [Дія Джо] Здійснити відчайдушний стрибок на шасі гелікоптера, що піднімається, пробратися в кабіну та вимкнути двигуни.",
        'act4_opt2': "2. [Дія Френка] Швидко кинути міцний сталевий трос від лебідки навколо хвостового ротора гелікоптера, прикріпивши інший кінець до кам'яної колони.",
        'act4_out1': (
            "\nДжо розбігається і стрибає на лижню гелікоптера, який уже відірвався від землі на два метри!\n"
            "Він вибирається до дверей кабіни, відчиняє їх та вступає у рукопашний бій із Ягуаром.\n"
            "Френк миттєво кидає камінь у лопаті, відволікаючи пілота. Джо вирубує ватажка та вимикає двигун.\n"
            "Гелікоптер м'яко падає на майданчик. Перемога!"
        ),
        'act4_out2': (
            "\nФренк блискавично хапає важкий сталевий трос лебідки, що лежить на майданчику,\n"
            "і робить точний кидок навколо хвостової балки гелікоптера, закріплюючи інший кінець за колону майя.\n"
            "Пілот тисне на газ, гелікоптер різко смикається вперед, але трос натягується і блокує хвіст!\n"
            "Машина втрачає баланс і глохне. Ягуар та його банда затиснуті в пастці та здаються!"
        ),
        'final_header': "                 ФІНАЛ                       ",
        'final_high': (
            "Вітаємо! Ви блискуче розкрили справу та врятували скарби іспанських галеонів! Ваш рахунок: {score} очок.\n"
            "Ягуар та його банда передані федеральній поліції Мексики, а унікальне золото повернуто до музею.\n"
            "Фентон Харді пишається своїми синами, які самостійно розгромили банду чорних археологів!\n"
            "Увечері у місцевому мексиканському селищі на вас чекає грандіозне свято:\n"
            "величезне плато гарячих бурітос, свіжий гуакамоле, кукурудзяні чіпси начос та солодкі чурос!\n"
            "Чет Мортон нарешті щасливий і ситий, а попереду на вас чекають нові розслідування!"
        ),
        'final_normal': (
            "Справу успішно завершено! Ваш рахунок: {score} очок.\n"
            "Хоча підземелля Юкатану ледь не забрали скарби, а голова Джо все ще гуде від удару колони,\n"
            "брати Харді знову довели свій високий детективний клас! Попереду — нові таємниці."
        ),
        'final_thanks': "\nДякуємо за гру! Френк та Джо пишалися б вашими рішеннями."
    },
    'en': {
        'select_lang': "Select Language / Оберіть мову / Выберите язык:\n1. Українська\n2. English\n3. Русский",
        'lang_choice_prompt': "Your choice (1-3): ",
        'press_enter': "Press ENTER to start the adventure...",
        'invalid_input': "Please enter 1 or 2.",
        'intro_text': (
            "You play as the famous detective brothers Frank and Joe Hardy.\n"
            "After cracking the mystery of the Spanish galleon in Florida, you found an encrypted\n"
            "captain's logbook. The records reveal that the main treasures of 'Santa Isabella' were hidden\n"
            "in a secret pirate fort built inside ancient Mayan ruins deep in the impenetrable jungles\n"
            "of the Yucatan Peninsula in Mexico. You set off on a new journey!"
        ),
        'act1_title': "\n--- ACT I: YUCATAN TACOS & THE MAYAN CIPHER ---",
        'act1_text': (
            "You are sitting on the terrace of a small Mexican cafe on the very edge of the jungle.\n"
            "In front of you is a true feast: hot corn tacos with juicy barbacoa beef,\n"
            "spicy salsa verde, fresh cilantro, and slices of ripe avocado.\n"
            "Nearby, roasted corn 'elote' steamed, generously drizzled with sauce and sprinkled with cotija cheese,\n"
            "while Chet Morton washes down his third juicy burrito with cold hibiscus tea.\n\n"
            "Frank spreads out an ancient map from the Spanish captain's logbook on the table.\n"
            "It contains strange astronomical signs indicating the way to the fort through the jungle.\n"
            "But the locals warn: a dangerous gang of black archaeologists is operating in the jungle,\n"
            "led by a ruthless mercenary nicknamed 'The Jaguar'!"
        ),
        'act1_q': "Which path do you choose to go deep into the jungle?",
        'act1_opt1': "1. [Frank's Path] Stay in camp, decode the constellations on the map and calculate a safe path, avoiding ancient traps.",
        'act1_opt2': "2. [Joe's Path] Rent powerful ATVs and break straight through muddy jungle trails, relying on speed.",
        'act1_out1': (
            "\nYou stay in camp. Frank compares the night sky of Yucatan with the Spanish charts.\n"
            "You manage to crack the cipher: the path lies along the bed of a dry river that bypasses quicksand.\n"
            "You take a compass, rope, machete and set off on foot along a safe route."
        ),
        'act1_out2': (
            "\nThe roar of ATV engines echoes in the jungle! Joe hits the gas, raising clouds of mud.\n"
            "You speed through lianas and bamboo thickets. Chet Morton holds on tight behind, screaming in fear and delight.\n"
            "You overcome difficult obstacles and arrive directly at the fort walls much earlier than your pursuers.\n"
            "In your trunk are flashlights, a machete, and a toolkit."
        ),
        'act2_title': "\n--- ACT II: THE ASSAULT ON THE PIRATE FORT ---",
        'act2_text': (
            "Before you rises a majestic and gloomy pirate fort built on top of a Mayan pyramid.\n"
            "It is completely overgrown with vines, and the ancient stone walls breathe danger.\n"
            "Near the main gate, you notice Jaguar's armed mercenaries holding rifles ready.\n"
            "In the center of the yard is a generator powering their exploration equipment."
        ),
        'act2_q': "How will you sneak inside the fort?",
        'act2_opt1': "1. Disable the generator (cut the fuel line with a machete to de-energize the camp and cause panic).",
        'act2_opt2': "2. Try to climb through the ancient drainage chute on the back of the pyramid, bypassing the security.",
        'act2_out1': (
            "\nFrank sneaks up to the generator and cuts the fuel hose with one precise strike.\n"
            "The generator sputters and dies! The light goes out, and the mercenaries start shouting and rushing in the dark.\n"
            "Using this, the Hardy brothers slip through the open gates of the fort unhindered!"
        ),
        'act2_out2_rope': (
            "\nUsing Frank's rope, you hook onto an old stone ring on the fort wall.\n"
            "Joe is the first to climb the slippery wall, helping his brother and Chet.\n"
            "You find yourselves directly in the inner courtyard of the fort without making any noise!"
        ),
        'act2_out2_climb': (
            "\nYou start climbing the wet stone ledges of the wall.\n"
            "Suddenly, a stone breaks from under Joe's foot and crashes down! The guards perk up,\n"
            "but Chet Morton in time imitates the roar of a wild jaguar. The frightened mercenaries do not dare to check.\n"
            "You successfully climb over the wall!"
        ),
        'act3_title': "\n--- ACT III: THE TEMPLE TRAP & JOE'S HARD HEAD ---",
        'act3_text': (
            "You descend into the fort's dungeons and enter the main treasury.\n"
            "Here stand chests full of Spanish gold doubloons, silver cups and Mayan masks!\n"
            "Suddenly the ceiling starts to shake. An ancient trap is activated! A huge stone block falls down!\n"
            "At the last second, Joe pushes Frank aside, but doesn't have time to dodge himself —\n"
            "a heavy fragment of a stone column hits him right on the head! Joe falls unconscious.\n"
            "At that moment, the Jaguar himself bursts into the hall with his mercenaries. They tie you up\n"
            "and lock you in an iron cage in the middle of a flooded dungeon hall.\n\n"
            "A few minutes later, Joe comes to, shaking his head and rubbing a bump:\n"
            "— Ouch, brother... Feels like a mammoth stepped on me. But hey, my skull is harder than ancient stone! (Classic trope!)\n"
            "Water from an underground spring begins to quickly fill the hall, rising to your feet!"
        ),
        'act3_q': "How will you escape the sturdy iron cage?",
        'act3_opt1': "1. [Joe's Path] Use an old iron harpoon lying nearby as a lever to bend the rusty bars of the cage.",
        'act3_opt2': "2. [Frank's Path] Try to pick the mechanism of the ancient cage lock with a metal belt buckle.",
        'act3_out1_success': (
            "\nJoe grabs the heavy harpoon, inserts it between the bars of the cage and leans with all his weight.\n"
            "The old rusty iron bars bend with a loud creak! You squeeze through the opening\n"
            "just as the water reaches your waist. You are free!"
        ),
        'act3_out1_fail': (
            "\nJoe tries to bend the bars, but the iron turns out to be too thick and strong.\n"
            "You only waste time and energy while the water continues to rise rapidly! Another way must be found immediately."
        ),
        'act3_out2_success': (
            "\nFrank takes out his metal belt buckle, sharpens it on a stone and carefully slides it into the keyhole.\n"
            "Listening to every click of the ancient mechanism, he makes a precise turn. Click!\n"
            "The heavy cage door opens. Get out quickly!"
        ),
        'act4_title': "\n--- ACT IV: THE FINAL BATTLE UNDER THE JUNGLE CANOPY ---",
        'act4_text': (
            "You run to the top of the pyramid. The Jaguar has already loaded the treasure chests into his helicopter,\n"
            "which stands on the pad, and the rotors are spinning wildly for takeoff.\n"
            "You have seconds to stop the international criminal and return the treasure to the people of Mexico!"
        ),
        'act4_q': "How will you stop the Jaguar's helicopter?",
        'act4_opt1': "1. [Joe's Action] Make a desperate leap onto the landing gear of the taking-off helicopter, break into the cabin and shut off the engines.",
        'act4_opt2': "2. [Frank's Action] Quickly throw a strong steel winch cable around the helicopter's tail rotor, securing the other end to a Mayan stone column.",
        'act4_out1': (
            "\nJoe runs and jumps onto the helicopter's skid, which has already left the ground by two meters!\n"
            "He climbs to the cabin door, opens it and enters hand-to-hand combat with the Jaguar.\n"
            "Frank instantly throws a stone into the blades, distracting the pilot. Joe knocks out the leader and cuts the engine.\n"
            "The helicopter lands softly on the pad. Victory!"
        ),
        'act4_out2': (
            "\nFrank quickly grabs the heavy steel winch cable lying on the pad\n"
            "and throws it precisely around the tail boom of the helicopter, securing the other end to a Mayan column.\n"
            "The pilot hits the gas, the helicopter jerks forward sharply, but the cable tightens and locks the tail!\n"
            "The machine loses balance and stalls. Jaguar and his gang are trapped and surrender!"
        ),
        'final_header': "                 THE END                     ",
        'final_high': (
            "Congratulations! You solved the case brilliantly and saved the treasure of the Spanish galleon! Your score: {score} points.\n"
            "The Jaguar and his gang are handed over to the Mexican federal police, and the gold is returned to the museum.\n"
            "Fenton Hardy is proud of his sons, who single-handedly defeated the gang of black archaeologists!\n"
            "In the evening, a grand celebration awaits you in the local Mexican village:\n"
            "a huge platter of hot burritos, fresh guacamole, tortilla chips and sweet churros!\n"
            "Chet Morton is finally happy and full, and new investigations await you ahead!"
        ),
        'final_normal': (
            "The case is successfully completed! Your score: {score} points.\n"
            "Although the Yucatan dungeons almost claimed the treasure, and Joe's head is still buzzing from the column blow,\n"
            "the Hardy boys have once again proven their high detective class! Ahead lie new secrets."
        ),
        'final_thanks': "\nThanks for playing! Frank and Joe would be proud of your choices."
    },
    'ru': {
        'select_lang': "Выберите язык / Oберіть мову / Select Language:\n1. Українська\n2. English\n3. Русский",
        'lang_choice_prompt': "Ваш выбор (1-3): ",
        'press_enter': "Нажмите ENTER, чтобы начать приключение...",
        'invalid_input': "Пожалуйста, введите 1 или 2.",
        'intro_text': (
            "Вы играете за известных братьев-детективов Фрэнка и Джо Харди.\n"
            "После раскрытия тайны испанского галеона во Флориде, вы нашли зашифрованный\n"
            "бортовой журнал капитана. Записи указывают на то, что главные сокровища «Санты-Изабеллы»\n"
            "были спрятаны в тайном пиратском форте, построенном в древних руинах майя\n"
            "посреди непроходимых джунглей полуострова Юкатан в Мексике. Вы отправляетесь в путь!"
        ),
        'act1_title': "\n--- АКТ I: ТАКОС В ЮКАТАНЕ И ШИФР МАЙЯ ---",
        'act1_text': (
            "Вы сидите на террасе небольшого мексиканского кафе на самом краю джунглей.\n"
            "Перед вами — настоящий праздник вкуса: горячие кукурузные такос с сочной говядиной\n"
            "барбакоа, острым соусом сальса верде, свежей кинзой и кусочками спелого авокадо.\n"
            "Рядом дымится запеченная кукуруза «элоте», щедро политая соусом и присыпанная сыром котиха,\n"
            "а Чет Мортон запивает свой третий сочный буррито холодным сладким чаем каркаде.\n\n"
            "Фрэнк раскладывает на столе старинную карту из журнала испанского капитана.\n"
            "Она содержит странные астрономические отметки, указывающие путь к форту сквозь джунгли.\n"
            "Но местные жители предупреждают: в джунглях орудует опасная банда черных археологов\n"
            "под руководством безжалостного наемника по прозвищу «Ягуар»!"
        ),
        'act1_q': "Какой путь вы выберете для продвижения вглубь джунглей?",
        'act1_opt1': "1. [Путь Фрэнка] Остаться в лагере, расшифровать созвездия на карте и вычислить безопасную тропу, избегая древних ловушек.",
        'act1_opt2': "2. [Путь Джо] Арендовать мощные квадроциклы (ATV) и прорваться напролом через болотные тропы, полагаясь на скорость.",
        'act1_out1': (
            "\nВы остаетесь в лагере. Фрэнк сравнивает ночное небо Юкатана со схемами испанцев.\n"
            "Вам удается разгадать шифр: путь пролегает вдоль русла высохшей реки, огибающей зыбучие пески.\n"
            "Вы берете с собой компас, веревку, мачете и отправляетесь пешком по безопасному маршруту."
        ),
        'act1_out2': (
            "\nРев моторов квадроциклов разносится по джунглям! Джо жмет на газ, поднимая тучи грязи.\n"
            "Вы несетесь сквозь лианы и бамбуковые заросли. Чет Мортон крепко держится сзади, крича от страха и восторга.\n"
            "Вы преодолеваете сложные препятствия и выходите прямо к стенам форта гораздо раньше преследователей.\n"
            "В вашем багажнике — фонарики, мачете и набор инструментов."
        ),
        'act2_title': "\n--- АКТ II: ШТУРМ ПИРАТСКОГО ФОРТА ---",
        'act2_text': (
            "Перед вами предстает величественный и мрачный пиратский форт, построенный на вершине пирамиды майя.\n"
            "Он полностью зарос лианами, а древние каменные стены дышат опасностью.\n"
            "У главных ворот вы замечаете вооруженных наемников Ягуара, держащих наготове винтовки.\n"
            "В центре двора стоит генератор, питающий их поисковое оборудование."
        ),
        'act2_q': "Как вы проберетесь внутрь форта?",
        'act2_opt1': "1. Вывести из строя генератор (перерезать топливный шланг с помощью мачете, чтобы обесточить лагерь и создать панику).",
        'act2_opt2': "2. Попробовать залезть через старинный сточный желоб с тыльной стороны пирамиды, огибая охрану.",
        'act2_out1': (
            "\nФрэнк незаметно пробирается к генератору и одним точным ударом мачете перерезает топливный шланг.\n"
            "Генератор чихает и глохнет! Свет гаснет, наемники начинают кричать и суетиться в темноте.\n"
            "Пользуясь этим, братья Харди беспрепятственно проскальзывают через открытые ворота форта!"
        ),
        'act2_out2_rope': (
            "\nИспользуя веревку Фрэнка, вы цепляетесь за старое каменное кольцо на стене форта.\n"
            "Джо первым ловко поднимается по скользкой стене вверх, помогая брату и Чету.\n"
            "Вы оказываетесь непосредственно во внутреннем дворике форта без единого шума!"
        ),
        'act2_out2_climb': (
            "\nВы начинаете карабкаться по мокрым каменным выступам стены.\n"
            "Вдруг из-под ноги Джо вырывается камень и с грохотом падает вниз! Охрана настораживается,\n"
            "но Чет Мортон вовремя имитирует вой дикого ягуара. Испуганные наемники не решаются проверять.\n"
            "Вы успешно перелезаете через стену!"
        ),
        'act3_title': "\n--- АКТ III: ЛОВУШКА ХРАМА И КРЕПКАЯ ГОЛОВА JOE ---",
        'act3_text': (
            "Вы спускаетесь в подземелье форта и попадаете в главную сокровищницу.\n"
            "Здесь стоят сундуки, полные испанских золотых дублонов, серебряных кубков и масок майя!\n"
            "Вдруг потолок начинает дрожать. Древняя ловушка активирована! Огромная каменная плита срывается вниз!\n"
            "Джо в последнее мгновение сильно толкает Фрэнка в сторону, но сам не успевает отскочить —\n"
            "тяжелый обломок каменной колонны бьет его прямо по голове! Джо теряет сознание.\n"
            "В этот момент в зал врывается сам Ягуар со своими наемниками. Они связывают вас\n"
            "и запирают в железной клетке посреди затапливаемого зала подземелья.\n\n"
            "Через несколько минут Джо приходит в себя, сильно тряся головой и потирая шишку:\n"
            "— Ох, брат... Кажется, на меня наступил мамонт. Но ничего, мой череп крепче древнего камня! (Классический троп!)\n"
            "Вода из подземного источника начинает быстро заполнять зал, поднимаясь к вашим ногам!"
        ),
        'act3_q': "Как вы выберетесь из крепкой железной клетки?",
        'act3_opt1': "1. [Путь Джо] Использовать старый железный гарпун, лежащий рядом, как рычаг, чтобы разогнуть заржавевшие прутья клетки.",
        'act3_opt2': "2. [Путь Фрэнка] Попробовать разобрать механизм старинного замка клетки с помощью металлической пряжки от ремня.",
        'act3_out1_success': (
            "\nДжо хватает тяжелый гарпун, вставляет его между прутьями клетки и наваливается всем своим весом.\n"
            "Старые ржавые железные прутья с громким скрипом разгибаются! Вы протискиваетесь через отверстие\n"
            "как раз в тот момент, когда вода достигает вашей талии. Вы свободны!"
        ),
        'act3_out1_fail': (
            "\nДжо пытается разогнуть прутья, но железо оказывается слишком толстым и прочным.\n"
            "Вы лишь напрасно тратите время и силы, пока вода продолжает стремительно прибывать! Нужно немедленно искать другой способ."
        ),
        'act3_out2_success': (
            "\nФрэнк достает металлическую пряжку ремня, затачивает ее о камень и осторожно просовывает в замочную скважину.\n"
            "Прислушиваясь к каждому щелчку старинного механизма, он делает точный поворот. Щелк!\n"
            "Тяжелая дверь клетки открывается. Выбирайтесь скорее!"
        ),
        'act4_title': "\n--- АКТ IV: ФИНАЛЬНЫЙ БОЙ ПОД КУПОЛОМ ДЖУНГЛЕЙ ---",
        'act4_text': (
            "Вы выбегаете на вершину пирамиды. Ягуар уже загрузил сундуки с сокровищами в свой вертолет,\n"
            "который стоит на площадке, и винты машины начинают бешено вращаться для взлета.\n"
            "У вас есть считанные секунды, чтобы остановить международного преступника и вернуть сокровища народу Мексики!"
        ),
        'act4_q': "Как вы остановите вертолет Ягуара?",
        'act4_opt1': "1. [Действие Джо] Совершить отчаянный прыжок на шасси взлетающего вертолета, пробраться в кабину и выключить двигатели.",
        'act4_opt2': "2. [Действие Фрэнка] Быстро набросить прочный стальной трос от лебедки вокруг хвостового ротора вертолета, прикрепив другой конец к каменной колонне.",
        'act4_out1': (
            "\nДжо разбегается и прыгает на лыжню вертолета, который уже оторвался от земли на два метра!\n"
            "Он выбирается к двери кабины, открывает ее и вступает в рукопашный бой с Ягуаром.\n"
            "Фрэнк мгновенно бросает камень в лопасти, отвлекая пилота. Джо вырубает главаря и выключает двигатель.\n"
            "Вертолет мягко падает на площадку. Победа!"
        ),
        'act4_out2': (
            "\nФрэнк молниеносно хватает тяжелый стальной трос лебедки, лежащий на площадке,\n"
            "и делает точный бросок вокруг хвостовой балки вертолета, закрепляя другой конец за колонну майя.\n"
            "Пилот жмет на газ, вертолет резко дергается вперед, но трос натягивается и блокирует хвост!\n"
            "Машина теряет баланс и глохнет. Ягуар и его банда зажаты в ловушке и сдаются!"
        ),
        'final_header': "                 ФИНАЛ                       ",
        'final_high': (
            "Поздравляем! Вы блестяще раскрыли дело и спасли сокровища испанских галеонов! Ваш счет: {score} points.\n"
            "Ягуар и его банда переданы федеральной полиции Мексики, а уникальное золото возвращено в музей.\n"
            "Фентон Харди гордится своими сыновьями, которые в одиночку разгромили банду черных археологов!\n"
            "Вечером в местном мексиканском поселке вас ждет грандиозный праздник:\n"
            "огромное плато горячих бурритос, свежий гуакамоле, чипсы тортилья и сладкие чуррос!\n"
            "Чет Мортон наконец-то счастлив и сыт, а впереди вас ждут новые расследования!"
        ),
        'final_normal': (
            "Дело успешно завершено! Ваш счет: {score} points.\n"
            "Хотя подземелья Юкатана едва не забрали сокровища, а голова Джо все еще гудит от удара колонны,\n"
            "братья Харди снова доказали свой высокий детективный класс! Впереди — новые тайны."
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
        choice = input(loc.get('lang_choice_prompt', '\n-> ')).strip()
        
        if choice == '1':
            state.route_taken = 'frank'
            state.score += 20
            state.inventory.append('compass')
            state.inventory.append('rope')
            state.inventory.append('machete')
            print_slow(loc['act1_out1'])
            break
        elif choice == '2':
            state.route_taken = 'joe'
            state.score += 15
            state.inventory.append('machete')
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
            if 'rope' in state.inventory:
                state.score += 25
                print_slow(loc['act2_out2_rope'])
            else:
                state.score += 10
                print_slow(loc['act2_out2_climb'])
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
    print_slow("\n=============================================================")
    print_slow(loc['final_header'])
    print_slow("=============================================================\n")
    
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
