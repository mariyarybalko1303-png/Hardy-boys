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
        'uk': "          БРАТИ ХАРДІ ТА ТАЄМНИЦЯ ГІРСЬКОГО ПРИТУЛКУ (ЧАСТИНА XIII)          ",
        'en': "      THE HARDY BOYS AND THE MYSTERY OF THE MOUNTAIN RETREAT (PART XIII)     ",
        'ru': "          БРАТЬЯ ХАРДИ И ТАЙНА ГОРНОГО ПРИЮТА (ЧАСТЬ XIII)              "
    }
    subtitle_text = {
        'uk': "          Спільна операція з Фентоном: Інтерактивний квест            ",
        'en': "          A Joint Fenton Hardy Operation: Interactive Quest           ",
        'ru': "          Совместная операция с Фентоном: Интерактивный квест         "
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
        self.route_taken = None  # 'frank' (archive/hack) or 'joe' (snowmobile/action)
        self.team_assembled = True
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
            "Сьогодні ви дієте разом зі своїм легендарним батьком, приватним детективом Фентоном Харді.\n"
            "Після розгрому бази в Залізних Пагорбах, останні вцілілі члени шпигунського синдикату\n"
            "«Диригент» разом із головним сервером даних забарикадувалися на покинутому гірському\n"
            "курорті «Альпійські Вершини», що закритий після лавини 1980-х років."
        ),
        'act1_title': "\n--- АКТ I: ГІРСЬКИЙ БЕНКЕТ ТА ОСТАННІЙ ПРИТУЛОК ---",
        'act1_text': (
            "Ви сидите в затишному дерев'яному мисливському будиночку біля підніжжя засніжених гір.\n"
            "У старому кам'яному каміні потріскують дрова. На столі чекає справжній шедевр зимової кухні:\n"
            "гаряче густе рагу з лісовими грибами та соковитим м'ясом, запечена з розмарином картопля\n"
            "із золотистою скоринкою, пишна домашня чиабата з часниковим маслом та великі глиняні\n"
            "кухлі з гарячим яблучним сидром та корицею. Чет Мортон уминає вже третю порцію рагу.\n\n"
            "Фентон Харді розкладає на столі карту закинутого курорту «Альпійські Вершини»:\n"
            "— Хлопці, це наше фінальне завдання. Шпигуни готують до евакуації свій головний сервер.\n"
            "Вся територія курорту занесена снігом, а єдина дорога туди перекрита завалами.\n"
            "Вони почуваються в безпеці, але ми застанемо їх зненацька!"
        ),
        'act1_q': "Який план проникнення ви оберете разом із батьком?",
        'act1_opt1': "1. [Шлях Френка] Пробратися до занедбаної станції канатної дороги, зламати систему енергопостачання та вимкнути радари шпигунів.",
        'act1_opt2': "2. [Шлях Джо] Застрибнути на швидкісні снігоходи та здійснити стрімкий рейд по крутому обледенілому схилу прямо до чорного входу.",
        'act1_out1': (
            "\nВи вирушаєте до старої станції канатної дороги. Поки батько прикриває вас ззовні,\n"
            "Френк підключається до старого розподільного щитка. Використовуючи свої технічні знання,\n"
            "ви обходите систему безпеки і повністю знеструмлюєте радари та прожектори шпигунів!\n"
            "Ви забираєте портативний тестер, ліхтарик та обережно заходите всередину головного шале."
        ),
        'act1_out2': (
            "\nРевіння двигунів снігоходів лунає крізь завивання хуртовини! Джо веде групу вперед.\n"
            "Ви мчите по крутих кучугурах снігу, маневруючи між віковими соснами та камінням.\n"
            "Хуртовина приховує ваш рух, і ви без перешкод причалюєте до занедбаних технічних дверей шале.\n"
            "З речей у вас із собою є ліхтарик, міцна мотузка з альпіністським гаком та набір інструментів."
        ),
        'act2_title': "\n--- АКТ II: ТІНІ ЗАКИДАННОГО КУРОРТУ ---",
        'act2_text': (
            "Головне шале курорту виглядає похмурим та занедбаним: облуплена позолота, величезні\n"
            "кришталеві люстри, вкриті товстим шаром пилу, та старі лижі на стінах.\n"
            "Проте у коридорах видно свіжі сліди від військових черевиків та кабелі, що тягнуться до підвалу.\n"
            "Раптом з бокового коридору долинають кроки двох патрульних синдикату."
        ),
        'act2_q': "Як ви вчините, щоб не підняти тривогу?",
        'act2_opt1': "1. Створити звукову пастку (використати старе залізне спорядження на стіні, щоб скинути його і відвернути увагу патрульних).",
        'act2_opt2': "2. Сховатися за портьєрами та використати димову шашку Чета (якщо з вами Джо), або зламати замок сусідніх дверей.",
        'act2_out1': (
            "\nДжо спритно штовхає стару металеву лижну палицю. Вона з гуркотом падає на підлогу!\n"
            "Патрульні миттєво повертають туди і з витягнутими ліхтарями йдуть з'ясовувати причину.\n"
            "Фентон Харді робить швидкий обхідний маневр і безшумно знешкоджує обох супротивників!\n"
            "Ви забираєте їхні рації та продовжуєте шлях до серверної."
        ),
        'act2_out2_smoke': (
            "\nДжо дістає димову шашку, яку Чет Мортон завбачливо поклав у його рюкзак.\n"
            "Ви кидаєте її під ноги патрульним. Густий білий дим миттєво заповнює коридор!\n"
            "Зловмисники починають кашляти та втрачають орієнтацію. Батько швидко нейтралізує їх.\n"
            "Шлях вільний, ви прямуєте далі!"
        ),
        'act2_out2_lock': (
            "\nФренк миттєво оцінює ситуацію, дістає відмички і за три секунди відкриває важкі дубові двері\n"
            "сусіднього кабінету. Ви всі разом ховаєтеся всередині, затамувавши поди.\n"
            "Патрульні проходять мимо, не помітивши нічого підозрілого. Ви продовжуєте розслідування!"
        ),
        'act3_title': "\n--- АКТ III: ПАСТКА ПІД ЛЮСТРОЮ ТА МІЦНА ГОЛОВА ---",
        'act3_text': (
            "У підвальному приміщенні старого ресторану ви нарешті знаходите головний сервер.\n"
            "Він миготить синіми вогнями — процес копіювання даних синдикату завершено на 90%.\n"
            "Раптом зверху лунає злісний сміх! Новий ватажок синдикату на прізвисько «Полковник»\n"
            "стоїть на балконі другого поверху зі зброєю у руках.\n"
            "Він тисне на кнопку ручного скидання вантажу, і величезна обледеніла кришталева люстра\n"
            "летить прямо на Фентона Харді!\n\n"
            "Джо реагує блискавично: він штовхає батька вбік, але сам отримує сильний удар\n"
            "уламком сталевого кріплення прямо по потилиці! Джо падає без тями.\n"
            "Френка та Фентона блокують сталеві грати, що автоматично опускаються зі стелі.\n"
            "Зловмисники замикають вас у морозильній камері кухні ресторану, де температура швидко падає!\n\n"
            "За кілька хвилин Джо приходить до тями, потираючи міцну потилицю:\n"
            "— Ох... Здається, на мене впала не просто люстра, а цілий айсберг. Але у мене міцна голова,\n"
            "ви ж знаєте! Бувало й гірше! (Класичний детективний троп)\n"
            "Температура падає до -15 градусів. Потрібно терміново діяти!"
        ),
        'act3_q': "Як ви виберетесь із зачиненої морозильної камери?",
        'act3_opt1': "1. [Сила Джо та Фентона] Використати заморожену тушу або важку металеву трубу полиці як важіль, щоб виламати дверні петлі.",
        'act3_opt2': "2. [Розум Френка] Розібрати температурний датчик на стіні та замкнути контакти, щоб викликати коротке замикання та автоматичне розблокування дверей.",
        'act3_out1_success': (
            "\nДжо разом із батьком беруть важку металеву стійку від стелажа.\n"
            "Використовуючи її як міцний важіль, ви просуваєте її в щілину дверей і тиснете з усієї сили.\n"
            "З гучним тріском сталева петля вилітає зі стіни! Двері відчиняються, ви вільні!"
        ),
        'act3_out1_fail': (
            "\nВи намагаєтесь виламати двері силою, але петлі виявляються надто міцними та замерзлими.\n"
            "Ви лише марно витрачаєте дорогоцінний час, а холод стає дедалі сильнішим. Спробуйте інший варіант!"
        ),
        'act3_out2_success': (
            "\nФренк швидко знімає захисну кришку температурного пульта.\n"
            "Він акуратно перерізає дроти і замикає головний кабель живлення.\n"
            "Спалахує сніп іскор! Електромагнітний замок дверей видає гучне клацання і відкривається.\n"
            "Блискуче рішення Френка врятувало вас від обмороження!"
        ),
        'act4_title': "\n--- АКТ IV: ПЕРЕГОНИ ПО СНІГУ ТА ФІНАЛЬНИЙ ТРІУМФ ---",
        'act4_text': (
            "Ви вибігаєте назовні і бачите, що «Полковник» завантажив сервер на важкий гусеничний\n"
            "снігоочисник (ратрак) і на шаленій швидкості намагається втекти по схилу гори.\n"
            "Хуртовина посилюється, і якщо він дійде до підніжжя, його забере вертоліт.\n"
            "Фентон Харді кричить:\n"
            "— Хлопці, ми не можемо дозволити йому піти з даними! Треба діяти негайно!"
        ),
        'act4_q': "Як ви зупините важкий ратрак «Полковника»?",
        'act4_opt1': "1. [Дія Джо] Наздогнати ратрак на снігоході, здійснити небезпечний стрибок на ходу на кабіну та заблокувати кермо.",
        'act4_opt2': "2. [Дія Френка] Використати сигнальну ракетницю станції, щоб підірвати сніговий карниз вище по схилу і викликати невеликий завал прямо перед машиною.",
        'act4_out1': (
            "\nДжо витискає максимум із двигуна снігохода, злітає з кучугури і стрибає прямо на дах ратрака!\n"
            "Він розбиває бокове скло, вривається в кабіну і вимикає запалювання. Френк та Фентон\n"
            "наздоганяють машину і допомагають скрутити ватажка. Сервер у наших руках!"
        ),
        'act4_out2': (
            "\nФренк миттєво розраховує кут обстрілу. Ви стріляєте з ракетниці точно у слабку точку снігового навісу.\n"
            "З гуркотом тони снігу зсуваються вниз, перегороджуючи дорогу ратраку великим завалом!\n"
            "Машина шпигунів грузне у снігу. Батько та хлопці швидко затримують збентежених злочинців!"
        ),
        'final_header': "                 ФІНАЛ                       ",
        'final_high': (
            "Вітаємо! Ви блискуче розкрили справу та знищили синдикат! Ваш рахунок: {score} очок.\n"
            "Усі дані «Диригента» повернуто спецслужбам, а «Полковник» заарештований.\n"
            "Фентон Харді з гордістю обіймає вас:\n"
            "— Хлопці, ви дієте як справжні професіонали. Я пишаюся вами!\n"
            "Увечері у мисливському будиночку Чет Мортон замовляє гігантську порцію гарячих вафель\n"
            "зі збитими вершками та полуничним джемом, і ви разом святкуєте тріумф справедливості!"
        ),
        'final_normal': (
            "Справу успішно завершено! Ваш рахунок: {score} очок.\n"
            "Незважаючи на холод, синдикат повністю ліквідовано. Хоча потилиця Джо все ще трохи болить\n"
            "від кришталевої люстри, серце гріє відчуття виконаного обов'язку перед батьком та Бейпортом!"
        ),
        'final_thanks': "\nДякуємо за гру! Брати Харді та їхній батько Фентон пишалися б вашими детективними навичками."
    },
    'en': {
        'select_lang': "Select Language / Оберіть мову / Выберите язык:\n1. Українська\n2. English\n3. Русский",
        'lang_choice_prompt': "Your choice (1-3): ",
        'press_enter': "Press ENTER to start the adventure...",
        'invalid_input': "Please enter 1 or 2.",
        'intro_text': (
            "You are playing as the famous detective brothers Frank and Joe Hardy.\n"
            "Today you are working alongside your legendary father, private investigator Fenton Hardy.\n"
            "After crushing the Iron Hills base, the last remaining members of the 'Conductor' syndicate\n"
            "have barricaded themselves with their main server in the abandoned 'Alpine Peaks'\n"
            "ski resort, closed since a mysterious avalanche in the 1980s."
        ),
        'act1_title': "\n--- ACT I: MOUNTAIN FEAST & THE LAST RETREAT ---",
        'act1_text': (
            "You are sitting in a cozy wooden hunting lodge at the foot of snow-capped mountains.\n"
            "Logs crackle in an old stone fireplace. A masterpiece of winter comfort food awaits on the table:\n"
            "a thick, hot forest mushroom stew with juicy meat, crispy rosemary baked potatoes,\n"
            "warm homemade sourdough bread with garlic butter, and large clay mugs\n"
            "of hot mulled apple cider with cinnamon. Chet Morton is devouring his third bowl of stew.\n\n"
            "Fenton Hardy spreads a map of the abandoned 'Alpine Peaks' resort on the table:\n"
            "— Boys, this is our final mission. The smugglers are preparing to evacuate their main server.\n"
            "The resort's entire territory is buried in snow, and the only road is blocked by avalanches.\n"
            "They feel safe up there, but we are going to surprise them!"
        ),
        'act1_q': "What entrance plan will you choose with your father?",
        'act1_opt1': "1. [Frank's Way] Sneak to the abandoned cable car station, hack the power grid, and disable the spy radars.",
        'act1_opt2': "2. [Joe's Way] Jump on high-speed snowmobiles and make a swift raid up the steep icy slope straight to the back door.",
        'act1_out1': (
            "\nYou head to the old cable car station. While your father covers you from the outside,\n"
            "Frank plugs into the old distribution board. Using your technical knowledge,\n"
            "you bypass the security system and completely power down the spy radars and searchlights!\n"
            "You take a portable tester, a flashlight, and carefully enter the main chalet."
        ),
        'act1_out2': (
            "\nThe roar of snowmobile engines echoes through the howling blizzard! Joe leads the way.\n"
            "You speed across steep snowbanks, maneuvering between ancient pines and rocks.\n"
            "The blizzard conceals your movement, and you easily arrive at the chalet's technical door.\n"
            "You have a flashlight, a sturdy rope with a climbing hook, and a set of tools with you."
        ),
        'act2_title': "\n--- ACT II: SHADOWS OF THE ABANDONED RESORT ---",
        'act2_text': (
            "The main chalet of the resort looks dark and decaying: peeling gold leaf, massive\n"
            "crystal chandeliers covered in thick dust, and old skis mounted on the walls.\n"
            "However, fresh boot tracks and thick cables stretching to the basement are visible in the corridors.\n"
            "Suddenly, footsteps of two syndicate patrolmen echo from the side corridor."
        ),
        'act2_q': "What will you do to avoid raising the alarm?",
        'act2_opt1': "1. Create a sound trap (use old iron ski gear on the wall to drop it and distract the guards).",
        'act2_opt2': "2. Hide behind the drapes and use Chet's smoke bomb (if with Joe) or pick the lock of a nearby door.",
        'act2_out1': (
            "\nJoe deftly pushes an old metal ski pole. It falls to the floor with a loud clang!\n"
            "The patrolmen instantly turn and head with their flashlights to investigate the sound.\n"
            "Fenton Hardy makes a swift flanking maneuver and quietly neutralizes both opponents!\n"
            "You take their walkie-talkies and proceed to the server room."
        ),
        'act2_out2_smoke': (
            "\nJoe pulls out a smoke bomb that Chet Morton thoughtfully packed in his backpack.\n"
            "You throw it at the patrolmen's feet. Thick white smoke instantly fills the corridor!\n"
            "The smugglers begin to cough and lose their bearings. Your father quickly neutralizes them.\n"
            "The path is clear, you move forward!"
        ),
        'act2_out2_lock': (
            "\nFrank quickly assesses the situation, pulls out his lockpicks, and opens the heavy oak door\n"
            "of a nearby office in three seconds. You all hide inside, holding your breath.\n"
            "The patrolmen pass by without noticing anything suspicious. You continue your investigation!"
        ),
        'act3_title': "\n--- ACT III: CHANDELIER TRAP & THE HARD HEAD ---",
        'act3_text': (
            "In the basement of the old restaurant, you finally locate the main server.\n"
            "It flashes with blue lights — the syndicate's data copy process is 90% complete.\n"
            "Suddenly, a sinister laugh echoes from above! The new syndicate leader, 'The Colonel',\n"
            "stands on the second-floor balcony with a weapon in his hands.\n"
            "He presses a release button, and a massive, ice-laden crystal chandelier\n"
            "plummets straight toward Fenton Hardy!\n\n"
            "Joe reacts instantly: he shoves his father aside but takes a heavy blow\n"
            "from a sharp steel fixture fragment right on the back of his head! Joe falls unconscious.\n"
            "Frank and Fenton are blocked by heavy iron bars that slide down from the ceiling.\n"
            "The criminals lock you in the restaurant kitchen's walk-in freezer, where the temp is dropping fast!\n\n"
            "A few minutes later, Joe wakes up, rubbing his sturdy head:\n"
            "— Ouch... Feels like an iceberg fell on me, not just a chandelier. But I've got a hard head,\n"
            "as you know! I've had worse! (Classic detective book trope)\n"
            "The temperature drops to -15 degrees. We must act quickly!"
        ),
        'act3_q': "How will you escape from the locked freezer?",
        'act3_opt1': "1. [Joe & Fenton's Strength] Use a frozen carcass or a heavy metal shelf pipe as a lever to pry open the door hinges.",
        'act3_opt2': "2. [Frank's Brains] Disassemble the temperature sensor on the wall and short the contacts to trigger a power failure and unlock the doors.",
        'act3_out1_success': (
            "\nJoe and his father grab a heavy metal shelf post.\n"
            "Using it as a sturdy lever, you jam it into the door gap and pry with all your might.\n"
            "With a loud crack, the steel hinge tears out of the wall! The door opens, you are free!"
        ),
        'act3_out1_fail': (
            "\nYou try to break the door by force, but the hinges are too sturdy and frozen.\n"
            "You only waste precious time, and the cold grows stronger. Try another option!"
        ),
        'act3_out2_success': (
            "\nFrank quickly unscrews the cover of the temperature control unit.\n"
            "He carefully cuts the wires and shorts the main power cable.\n"
            "A shower of sparks erupts! The door's electromagnetic lock clicks loudly and opens.\n"
            "Frank's brilliant solution saved you from freezing!"
        ),
        'act4_title': "\n--- ACT IV: SNOW RACE & THE FINAL TRIUMPH ---",
        'act4_text': (
            "You run outside and see 'The Colonel' has loaded the server onto a heavy tracked\n"
            "snowcat (snow groomer) and is speeding down the mountainside.\n"
            "The blizzard is intensifying, and if he reaches the base, a helicopter will pick him up.\n"
            "Fenton Hardy shouts:\n"
            "— Boys, we can't let him get away with that data! We must act now!"
        ),
        'act4_q': "How will you stop 'The Colonel's' heavy snowcat?",
        'act4_opt1': "1. [Joe's Action] Catch up on a snowmobile, make a dangerous leap onto the moving cab, and block the steering wheel.",
        'act4_opt2': "2. [Frank's Action] Use the station's flare gun to trigger a small controlled avalanche on the snow cornice above, blocking his path.",
        'act4_out1': (
            "\nJoe pushes the snowmobile to its limit, flies off a snowdrift, and jumps onto the snowcat's roof!\n"
            "He breaks the side window, bursts into the cab, and shuts off the ignition. Frank and Fenton\n"
            "catch up and help subdue the leader. The server is in our hands!"
        ),
        'act4_out2': (
            "\nFrank instantly calculates the trajectory. You shoot the flare gun precisely at the weak point of the snow overhang.\n"
            "With a roar, tons of snow slide down, blocking the snowcat with a massive drift!\n"
            "The spy machine gets stuck in the snow. Fenton and the boys quickly apprehend the startled criminals!"
        ),
        'final_header': "                THE END                      ",
        'final_high': (
            "Congratulations! You solved the case brilliantly and destroyed the syndicate! Your score: {score} points.\n"
            "All 'Conductor' data has been secured, and 'The Colonel' is arrested.\n"
            "Fenton Hardy hugs you proudly:\n"
            "— Boys, you act like real professionals. I am proud of you!\n"
            "In the evening at the lodge, Chet Morton orders a giant plate of hot waffles\n"
            "with whipped cream and strawberry jam, and you celebrate the triumph of justice together!"
        ),
        'final_normal': (
            "The case is successfully closed! Your score: {score} points.\n"
            "Despite the freezing cold, the syndicate is completely liquidated. Although Joe's head still hurts\n"
            "from the crystal chandelier, the feeling of duty fulfilled to your father and Bayport warms your heart!"
        ),
        'final_thanks': "\nThanks for playing! The Hardy Boys and their father Fenton would be proud of your detective skills."
    },
    'ru': {
        'select_lang': "Выберите язык / Oберіть мову / Select Language:\n1. Українська\n2. English\n3. Русский",
        'lang_choice_prompt': "Ваш выбор (1-3): ",
        'press_enter': "Нажмите ENTER, чтобы начать приключение...",
        'invalid_input': "Пожалуйста, введите 1 или 2.",
        'intro_text': (
            "Вы играете за известных братьев-детективов Фрэнка и Джо Харди.\n"
            "Сегодня вы действуете вместе со своим легендарным отцом, частным детективом Фентоном Харди.\n"
            "После разгрома базы в Железных Холмах последние уцелевшие члены шпионского синдиката\n"
            "«Дирижер» вместе с главным сервером данных забаррикадировались на заброшенном горном\n"
            "курорте «Альпийские Вершины», закрытом после лавины 1980-х годов."
        ),
        'act1_title': "\n--- АКТ I: ГОРНЫЙ ПИР И ПОСЛЕДНЕЕ ПРИСТАНИЩЕ ---",
        'act1_text': (
            "Вы сидите в уютном деревянном охотничьем домике у подножия заснеженных гор.\n"
            "В старом каменном камине потрескивают дрова. На столе ждет настоящий шедевр зимней кухни:\n"
            "горячее густое рагу с лесными грибами и сочным мясом, запеченный с розмарином картофель\n"
            "с золотистой корочкой, пышная домашняя чиабатта с чесночным маслом и огромные глиняные\n"
            "кружки с горячим яблочным сидром и корицей. Чет Мортон уминает уже третью порцию рагу.\n\n"
            "Фентон Харди раскладывает на столе карту заброшенного курорта «Альпийские Вершины»:\n"
            "— Ребята, это наше финальное задание. Шпионы готовят к эвакуации свой главный сервер.\n"
            "Вся территория курорта занесена снегом, а единственная дорога туда перекрыта завалами.\n"
            "Они чувствуют себя в безопасности, но мы застанем их врасплох!"
        ),
        'act1_q': "Какой план проникновения вы выберете вместе с отцом?",
        'act1_opt1': "1. [Путь Фрэнка] Пробраться к заброшенной станции канатной дороги, взломать систему энергоснабжения и отключить радары шпионов.",
        'act1_opt2': "2. [Путь Джо] Запрыгнуть на скоростные снегоходы и совершить стремительный рейд по крутому обледенелому склону прямо к черному входу.",
        'act1_out1': (
            "\nВы отправляетесь к старой станции канатной дороги. Пока отец прикрывает вас снаружи,\n"
            "Фрэнк подключается к старому распределительному щитку. Используя свои технические знания,\n"
            "вы обходите систему безопасности и полностью обесточиваете радары и прожекторы шпионов!\n"
            "Вы берете с собой портативный тестер, фонарик и осторожно заходите внутрь главного шале."
        ),
        'act1_out2': (
            "\nРев двигателей снегоходов раздается сквозь вой метели! Джо ведет группу вперед.\n"
            "Вы мчитесь по крутым сугробам снега, маневрируя между вековыми соснами и камнями.\n"
            "Метель скрывает ваше движение, и вы беспрепятственно причаливаете к заброшенным техническим дверям шале.\n"
            "Из вещей у вас с собой фонарик, крепкая веревка с альпинистским крюком и набор инструментов."
        ),
        'act2_title': "\n--- АКТ II: ТЕНИ ЗАБРОШЕННОГО КУРОРТА ---",
        'act2_text': (
            "Главное шале курорта выглядит мрачным и заброшенным: облупившаяся позолота, огромные\n"
            "хрустальные люстры, покрытые толстым слоем пыли, и старые лыжи на стенах.\n"
            "Однако в коридорах видны свежие следы от военных ботинок и кабели, тянущиеся в подвал.\n"
            "Вдруг из бокового коридора доносятся шаги двух патрульных синдиката."
        ),
        'act2_q': "Как вы поступите, чтобы не поднять тревогу?",
        'act2_opt1': "1. Создать звуковую ловушку (использовать старое железное снаряжение на стене, чтобы сбросить его и отвлечь патрульных).",
        'act2_opt2': "2. Спрятаться за портьерами и использовать дымовую шашку Чета (если с вами Джо), или взломать замок соседней двери.",
        'act2_out1': (
            "\nДжо ловко толкает старую металлическую лыжную палку. Она с грохотом падает на пол!\n"
            "Патрульные мгновенно поворачивают туда и с вытянутыми фонариками идут выяснять причину.\n"
            "Фентон Харди делает быстрый обходной маневр и бесшумно обезвреживает обоих противников!\n"
            "Вы забираете их рации и продолжаете путь к серверной."
        ),
        'act2_out2_smoke': (
            "\nДжо достает дымовую шашку, которую Чет Мортон предусмотрительно положил в его рюкзак.\n"
            "Вы бросаете ее под ноги патрульным. Густой белый дым мгновенно заполняет коридор!\n"
            "Злоумышленники начинают кашлять и теряют ориентацию. Отец быстро нейтрализует их.\n"
            "Путь свободен, вы направляетесь дальше!"
        ),
        'act2_out2_lock': (
            "\nФрэнк мгновенно оценивает ситуацию, достает отмычки и за три секунды открывает тяжелую дубовую дверь\n"
            "соседнего кабинета. Вы все вместе прячетесь внутри, затаив дыхание.\n"
            "Патрульные проходят мимо, не заметив ничего подозрительного. Вы продолжаете расследование!"
        ),
        'act3_title': "\n--- АКТ III: ЛОВУШКА ПОД ЛЮСТРОЙ И КРЕПКАЯ ГОЛОВА ---",
        'act3_text': (
            "В подвальном помещении старого ресторана вы наконец находите главный сервер.\n"
            "Он мигает синими огнями — процесс копирования данных синдиката завершен на 90%.\n"
            "Вдруг сверху раздается злобный смех! Новый главарь синдиката по прозвищу «Полковник»\n"
            "стоит на балконе второго этажа с оружием в руках.\n"
            "Он жмет на кнопку ручного сброса груза, и огромная обледеневшая хрустальная люстра\n"
            "летит прямо на Фентона Харди!\n\n"
            "Джо реагирует молниеносно: он толкает отца в сторону, но сам получает сильный удар\n"
            "осколком стального крепления прямо по затылку! Джо падает без чувств.\n"
            "Фрэнка и Фентона блокирует стальная решетка, автоматически опускающаяся с потолка.\n"
            "Злоумышленники запирают вас в морозильной камере кухни ресторана, где температура быстро падает!\n\n"
            "Через несколько минут Джо приходит в себя, потирая крепкий затылок:\n"
            "— Ох... Кажется, на меня упала не просто люстра, а целый айсберг. Но у меня крепкая голова,\n"
            "вы же знаете! Бывало и хуже! (Классический штамп детективных книг)\n"
            "Температура падает до -15 градусов. Нужно срочно действовать!"
        ),
        'act3_q': "Как вы выберетесь из закрытой морозильной камеры?",
        'act3_opt1': "1. [Сила Джо и Фентона] Использовать замороженную тушу или тяжелую металлическую трубу полки как рычаг, чтобы выломать дверные петли.",
        'act3_opt2': "2. [Разум Фрэнка] Разобрать температурный датчик на стене и замкнуть контакты, чтобы вызвать короткое замыкание и автоматическую разблокировку двери.",
        'act3_out1_success': (
            "\nДжо вместе с отцом берут тяжелую металлическую стойку от стеллажа.\n"
            "Используя ее как прочный рычаг, вы просовываете ее в щель двери и давите изо всех сил.\n"
            "С громким треском стальная петля вылетает из стены! Дверь открывается, вы свободны!"
        ),
        'act3_out1_fail': (
            "\nВы пытаетесь выломать дверь силой, но петли оказываются слишком прочными и замерзшими.\n"
            "Вы лишь напрасно тратите драгоценное время, а холод становится все сильнее. Попробуйте другой вариант!"
        ),
        'act3_out2_success': (
            "\nФрэнк быстро снимает защитную крышку температурного пульта.\n"
            "Он аккуратно перерезает провода и замыкает главный кабель питания.\n"
            "Вспыхивает сноп искр! Электромагнитный замок двери издает громкий щелчок и открывается.\n"
            "Блестящее решение Фрэнка спасло вас от обморожения!"
        ),
        'act4_title': "\n--- АКТ IV: ГОНКА ПО СНЕГУ И ФИНАЛЬНЫЙ ТРИУМФ ---",
        'act4_text': (
            "Вы выбегаете наружу и видите, что «Полковник» загрузил сервер на тяжелый гусеничный\n"
            "снегоочиститель (ратрак) и на бешеной скорости пытается скрыться по склону горы.\n"
            "Метель усиливается, и если он дойдет до подножия, его заберет вертолет.\n"
            "Фентон Харди кричит:\n"
            "— Ребята, мы не можем позволить ему уйти с данными! Надо действовать немедленно!"
        ),
        'act4_q': "Как вы остановите тяжелый ратрак «Полковника»?",
        'act4_opt1': "1. [Действие Джо] Догнать ратрак на снегоходе, совершить опасный прыжок на ходу на кабину и заблокировать руль.",
        'act4_opt2': "2. [Действие Фрэнка] Использовать сигнальную ракетницу станции, чтобы взорвать снежный карниз выше по склону и вызвать небольшой завал прямо перед машиной.",
        'act4_out1': (
            "\nДжо выжимает максимум из двигателя снегохода, взлетает с сугроба и прыгает прямо на крышу ратрака!\n"
            "Он разбивает боковое стекло, врывается в кабину и выключает зажигание. Фрэнк и Фентон\n"
            "догоняют машину и помогают скрутить главаря. Сервер в наших руках!"
        ),
        'act4_out2': (
            "\nФрэнк мгновенно рассчитывает угол обстрела. Вы стреляете из ракетницы точно в слабую точку снежного навеса.\n"
            "С грохотом тонны снега сдвигаются вниз, преграждая дорогу ратраку большим завалом!\n"
            "Машина шпионов вязнет в снегу. Отец и ребята быстро задерживают растерянных преступников!"
        ),
        'final_header': "                 ФИНАЛ                       ",
        'final_high': (
            "Поздравляем! Вы блестяще раскрыли дело и уничтожили синдикат! Ваш счет: {score} points.\n"
            "Все данные «Дирижера» возвращены спецслужбам, а «Полковник» арестован.\n"
            "Фентон Харди с гордостью обнимает вас:\n"
            "— Ребята, вы действуете как настоящие профессионалы. Я горжусь вами!\n"
            "Вечером в охотничьем домике Чет Мортон заказывает гигантскую порцию горячих вафель\n"
            "со взбитыми сливками и клубничным джемом, и вы вместе празднуете триумф справедливости!"
        ),
        'final_normal': (
            "Дело успешно завершено! Ваш счет: {score} points.\n"
            "Несмотря на мороз, синдикат полностью ликвидирован. Хотя затылок Джо все еще немного болит\n"
            "от хрустальной люстры, сердце греет чувство исполненного долга перед отцом и Бейпортом!"
        ),
        'final_thanks': "\nСпасибо за игру! Братья Харди и их отец Фентон гордились бы вашими детективными навыками."
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
            state.inventory.append('tester')
            state.inventory.append('flashlight')
            print_slow(loc['act1_out1'])
            break
        elif choice == '2':
            state.route_taken = 'joe'
            state.score += 10
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
        choice = input(loc.get('lang_choice_prompt', '\n-> ')).strip()
        
        if choice == '1':
            state.score += 15
            print_slow(loc['act2_out1'])
            break
        elif choice == '2':
            if state.route_taken == 'joe':
                state.score += 20
                print_slow(loc['act2_out2_smoke'])
            else:
                state.score += 25
                print_slow(loc['act2_out2_lock'])
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
            state.score += 25
            print_slow(loc['act4_out1'])
            break
        elif choice == '2':
            state.score += 20
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