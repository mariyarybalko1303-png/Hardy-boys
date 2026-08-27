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
        'uk': "          БРАТИ ХАРДІ ТА СЕКРЕТ МАЯКА ОДИНОКОЇ СКЕЛІ          ",
        'en': "     THE HARDY BOYS AND THE SECRET OF LONELY ROCK LIGHTHOUSE   ",
        'ru': "          БРАТЬЯ ХАРДИ И СЕКРЕТ МАЯКА ОДИНОКОЙ СКАЛЫ          "
    }
    subtitle_text = {
        'uk': "          Епізод VII: Інтерактивний текстовий квест            ",
        'en': "          Episode VII: Interactive Text-Based Quest            ",
        'ru': "          Эпизод VII: Интерактивный текстовый квест            "
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
        self.route_taken = None  # 'frank' (decode) or 'joe' (boat)
        self.generator_fixed = False
        self.score = 0

LOCALIZATION = {
    'uk': {
        'select_lang': "Оберіть мову / Select Language / Выберите язык:\n1. Українська\n2. English\n3. Русский",
        'lang_choice_prompt': "Ваш вибір (1-3): ",
        'press_enter': "Натисніть ENTER, щоб розпочати пригоду...",
        'invalid_input': "Будь ласка, введіть 1 або 2.",
        'intro_text': (
            "Ви граєте за відважних братів-детективів Френка та Джо Харді з прибережного Бейпорта.\n"
            "Позаду лишилися потяг-привид, срібні шахти та Острів Черепа. Але лідер синдикату контрабандистів,\n"
            "відомий як «Диригент», втік під час тюремного конвою! Його останні сліди ведуть до\n"
            "занедбаного Маяка Одинокої Скелі посеред розбурханого моря неподалік від Бейпорта..."
        ),
        'act1_title': "\n--- АКТ I: СІМЕЙНИЙ БЕНКЕТ ТА СВІТЛОВИЙ ШИФР ---",
        'act1_text': (
            "Ви сидите на затишній кухні дому Харді. Тітка Гертруда перевершила саму себе:\n"
            "на столі парує величезна супниця з ніжним вершковим крем-супом із молюсків (Clam Chowder),\n"
            "стоїть кошик із гарячим домашнім хлібом на заквасці, змащеним часниковим маслом, та ароматний\n"
            "ягідний пиріг із кулькою танучого морозива. Чет Мортон уже змітає третю тарілку супу.\n\n"
            "Раптом у вітальню входить ваш батько, відомий детектив Фентон Харді. Його обличчя серйозне:\n"
            "— Хлопці, «Диригент» переховується на Маяку Одинокої Скелі. Місцеві рибалки бачили,\n"
            "як із вершини маяка хтось надсилає зашифровані світлові сигнали у море. Насувається потужний шторм,\n"
            "і берегова охорона не зможе підійти до скелі. Ми маємо діяти негайно!"
        ),
        'act1_q': "Який план дій ви оберете?",
        'act1_opt1': "1. [Шлях Френка] Залишитися на 10 хвилин, щоб проаналізувати ритм спалахів маяка за допомогою морських книг батька.",
        'act1_opt2': "2. [Шлях Джо] Не втрачати ні секунди! Негайно бігти в порт, заводити наш катер «Нишпорка» і мчати крізь шторм.",
        'act1_out1': (
            "\nФренк швидко відкриває старі навігаційні довідники Бейпорта та порівнює записи.\n"
            "Через кілька хвилин логіка перемагає: ви розгадуєте код спалахів! Це сигнал координації для іноземної субмарини,\n"
            "а також попередження про небезпечну підводну течію біля західного рифу. Тепер ви знаєте безпечний шлях!\n"
            "Ви берете ліхтарик, важкий трос, штурмовий дощовик і вирушаєте в порт."
        ),
        'act1_out2': (
            "\nДжо впевнено хапає ключі від катера! Ревіння мотора «Нишпорки» заглушає перші гуркоти грому.\n"
            "Ви виходите у відкрите море. Хвилі підіймаються все вище, вітер шпурляє солоні бризки в обличчя.\n"
            "Чет Мортон блідне і міцно тримається за борт, шкодуючи, що не з'їв ще один шматок пирога.\n"
            "У вашому розпорядженні лише ліхтарики та базовий набір інструментів катера."
        ),
        'act2_title': "\n--- АКТ II: ШТОРМОВИЙ ПЕРЕХІД ТА ДИТЯЧІ ЗУБИ ---",
        'act2_text': (
            "Чорні хвилі штовхають ваш катер прямо на гострі скелі, які моряки називають «Диявольські Зуби».\n"
            "Злива стоїть стіною, видимість майже нульова. Попереду, наче велетенський привид,\n"
            "вимальовується силует старого кам'яного маяка. Раптом гігантська хвиля підкидає катер!"
        ),
        'act2_q': "Як ви проведете катер крізь рифи?",
        'act2_opt1': "1. Спробувати обійти рифи по небезпечній західній дузі, де хвилі здаються меншими.",
        'act2_opt2': "2. Довіритися розрахункам (або інтуїції) і йти навпростець крізь вузьку ущелину між скелями.",
        'act2_out1_success': (
            "\nЗавдяки розшифровці Френка ви знаєте, що західна течія оманлива! Ви вчасно коригуєте курс,\n"
            "огинаєте небезпечну мілину і м'яко швартуєте катер у прихованій бетонній бухті маяка. Чиста перемога!"
        ),
        'act2_out1_fail': (
            "\nВи повертаєте на захід, але сильна підводна течія кидає катер прямо на прихований камінь!\n"
            "Лунає страшний тріск. Корпус пошкоджено, але Джо дивом втримує штурвал і викидає катер на берег.\n"
            "«Нишпорка» потребуватиме серйозного ремонту, але ви дісталися суходолу!"
        ),
        'act2_out2': (
            "\nДжо міцно стискає штурвал, робить крутий віраж і скеровує катер прямо у вузьку ущелину між скелями!\n"
            "Катер пролітає в кількох сантиметрах від гострого каміння, підхоплений піною. Неймовірний маневр!\n"
            "Ви влітаєте в тиху гавань біля підніжжя маяка. Чет нарешті починає дихати."
        ),
        'act3_title': "\n--- АКТ III: ТЕМРЯВА, ГЕНЕРАТОР ТА МІЦНА ГОЛОВА ---",
        'act3_text': (
            "Ви заходите всередину маяка. Залізні гвинтові сходи ведуть вгору в повній темряві.\n"
            "Раптом згори лунає металевий скрегіт. Ви підіймаєтесь у машинне відділення.\n"
            "Тут холодно, пахне мазутом та іржавим залізом. Раптом важка сталева балка талів,\n"
            "підпиляна злочинцями, зривається з кріплення і летить прямо на вас!"
        ),
        'act3_q': "Ваша реакція?",
        'act3_opt1': "1. [Вибір Джо] Прийняти удар на себе, закривши Френка, та спробувати відштовхнути важку залізяку плечем.",
        'act3_opt2': "2. [Вибір Френка] Спробувати миттєво відскочити назад та ухилитися від падіння.",
        'act3_out1_head': (
            "\nДжо штовхає Френка вбік, але важка залізна деталь б'є його прямо по голові!\n"
            "Джо падає на підлогу без тями. Френк у жаху підбігає до брата.\n"
            "За хвилину Джо розплющує очі, потираючи величезну гулю на потилиці:\n"
            "— Ох, Френку... Здається, я зустрівся з ковадлом. Але нічого, мій череп міцніший за сталь! (Класичний троп!)\n"
            "Тим часом ви помічаєте, що генератор маяка пошкоджено, а ліфт на верхній майданчик заблоковано."
        ),
        'act3_out2_dodge': (
            "\nВи обоє синхронно відскакуєте назад! Балка з гуркотом падає на бетонну підлогу,\n"
            "висікаючи іскри всього в кількох сантиметрах від ваших ніг. Справжня спритність!\n"
            "Проте ударна хвиля перебиває головний кабель живлення. Маяк занурюється у повну темряву,\n"
            "а електронний замок нагору зачиняється."
        ),
        'act3_lock_q': "Електронний замок заблокував хід до лампової кімнати. Як ви його відчините?",
        'act3_lock_opt1': "1. [Дія Джо] Використати залізний лом, знайдений біля генератора, щоб виламати двері ліфтової шахти.",
        'act3_lock_opt2': "2. [Дія Френка] Перезапустити генератор, з'єднавши дроти живлення напряму через реле за допомогою мультиметра.",
        'act3_lock_out1': (
            "\nДжо вставляє лом у щілину дверей, напружує всі м'язи і з криком тисне на важіль.\n"
            "Метал гнеться із жахливим скреготом, і заклинені двері нарешті розсуваються. Шлях вгору вільний,\n"
            "але ваші руки гудуть від напруги!"
        ),
        'act3_lock_out2': (
            "\nФренк спокійно розкриває щиток генератора. Використовуючи свої знання електроніки,\n"
            "він знаходить обірвану лінію, зачищає дроти та з'єднує їх в обхід перегорілого запобіжника.\n"
            "Генератор радісно пирхає, світло спалахує, і двері ліфта автоматично відчиняються! Елегантне вирішення."
        ),
        'act4_title': "\n--- АКТ IV: ФІНАЛ НА ВЕРШИНІ ШТОРМУ ---",
        'act4_text': (
            "Ви підіймаєтесь на зовнішній оглядовий майданчик маяка. Вітер тут має таку силу, що ледве не збиває з ніг.\n"
            "Блискавки розривають небо, освітлюючи шалене море внизу. Біля перил стоїть «Диригент» у мокрому плащі.\n"
            "Він тримає в руках валізу з документами синдикату. Поруч над майданчиком завис гелікоптер,\n"
            "з якого скинули мотузяну драбину! Злочинець хапається за неї та починає підійматися!"
        ),
        'act4_q': "«Диригент» втікає! Що ви зробите?",
        'act4_opt1': "1. [Рішення Джо] Зробити шалений розбіг і стрибнути на мотузяну драбину слідом за ним, щоб стягнути його вниз.",
        'act4_opt2': "2. [Рішення Френка] Спритно кинути важкий рятувальний круг на лопаті хвостового гвинта або зачепити драбину за залізний гак маяка.",
        'act4_out1': (
            "\nДжо здійснює неймовірний стрибок через перила і чіпляється за низ драбини!\n"
            "Гелікоптер хитається від раптової ваги. Джо швидко лізе вгору, хапає «Диригента» за ногу\n"
            "і сильним ривком стягує його назад на мокрий майданчик маяка! Френк миттєво допомагає скрутити злочинця."
        ),
        'act4_out2': (
            "\nФренк миттєво оцінює ситуацію. Він хапає міцний сталевий гак для вантажів,\n"
            "закріплений на стіні маяка, і спритним кидком чіпляє його за нижню сходинку мотузяної драбини!\n"
            "Гелікоптер намагається злетіти вгору, але натягнутий трос блокує його рух. Пілот, боячись катастрофи,\n"
            "скидає драбину разом із «Диригентом» на майданчик, де ви його негайно затримуєте!"
        ),
        'final_header': "                 ФІНАЛ                       ",
        'final_high': (
            "Вітаємо! Ви блискуче закрили справу всього синдикату! Ваш рахунок: {score} очок.\n"
            "«Диригент» знову за ґратами, а всі секретні документи контрабандистів опинилися в руках поліції.\n"
            "Шериф Колліг та ваш батько Фентон Харді прибувають на маяк на рятувальному судні берегової охорони.\n"
            "Вони пишаються вашою сміливістю та розумом!\n"
            "А ввечері вдома на вас чекає подвійна порція гарячого ягідного пирога від тітки Гертруди,\n"
            "і Чет Мортон уже замовляє додаткову доставку піци, святкуючи повний тріумф!"
        ),
        'final_normal': (
            "Справу успішно завершено! Ваш рахунок: {score} очок.\n"
            "Хоча шторм потріпав ваш катер, а потилиця Джо прикрашена новою бойовою гулею,\n"
            "лідера злочинців затримано, а Бейпорт може спати спокійно, поки на варті стоять Брати Харді!"
        ),
        'final_thanks': "\nДякуємо за гру! Френк та Джо пишалися б вашим детективним талантом."
    },
    'en': {
        'select_lang': "Select Language / Оберіть мову / Выберите язык:\n1. Українська\n2. English\n3. Русский",
        'lang_choice_prompt': "Your choice (1-3): ",
        'press_enter': "Press ENTER to start the adventure...",
        'invalid_input': "Please enter 1 or 2.",
        'intro_text': (
            "You play as the brave detective brothers, Frank and Joe Hardy from coastal Bayport.\n"
            "The ghost train, silver mines, and Skull Island are behind you. But the leader of the smugglers,\n"
            "known as 'The Conductor', has escaped from the prison convoy! His latest tracks lead to the\n"
            "abandoned Lonely Rock Lighthouse in the middle of a raging sea near Bayport..."
        ),
        'act1_title': "\n--- ACT I: THE FAMILY FEAST AND THE LIGHT CODE ---",
        'act1_text': (
            "You are sitting in the cozy kitchen of the Hardy home. Aunt Gertrude has outdone herself:\n"
            "a huge tureen of steaming, creamy Clam Chowder is on the table, along with a basket of hot\n"
            "homemade sourdough bread brushed with garlic butter, and a fragrant berry pie with a scoop of melting ice cream.\n"
            "Chet Morton is already wiping out his third bowl of soup.\n\n"
            "Suddenly, your father, the famous detective Fenton Hardy, enters the living room. His face is serious:\n"
            "— Boys, 'The Conductor' is hiding on Lonely Rock Lighthouse. Local fishermen saw someone flashing\n"
            "coded light signals out to sea. A powerful storm is coming, and the coast guard won't be able to approach.\n"
            "We must act immediately!"
        ),
        'act1_q': "What plan of action will you choose?",
        'act1_opt1': "1. [Frank's Way] Stay for 10 minutes to analyze the lighthouse's flashing rhythm using your father's marine books.",
        'act1_opt2': "2. [Joe's Way] Don't waste a second! Run to the port, start our boat 'The Sleuth' and rush through the storm.",
        'act1_out1': (
            "\nFrank quickly opens Bayport's old marine directories and compares the records.\n"
            "After a few minutes, logic wins: you crack the flashing code! It is a coordination signal for a foreign submarine,\n"
            "and a warning about a dangerous underwater current near the western reef. Now you know the safe path!\n"
            "You grab a flashlight, a heavy rope, a storm raincoat and head to the port."
        ),
        'act1_out2': (
            "\nJoe confidently grabs the boat keys! The engine roar of 'The Sleuth' drowns out the first claps of thunder.\n"
            "You head out into the open sea. The waves are rising higher, the wind throws salty spray into your face.\n"
            "Chet Morton turns pale and holds on tight to the side, wishing he had eaten another slice of pie.\n"
            "You only have flashlights and the boat's basic tool kit at your disposal."
        ),
        'act2_title': "\n--- ACT II: STORMY CROSSING AND THE DEVIL'S TEETH ---",
        'act2_text': (
            "Black waves push your boat straight toward the sharp rocks that sailors call 'The Devil's Teeth'.\n"
            "The downpour is a wall, visibility is almost zero. Ahead, like a giant ghost,\n"
            "the silhouette of the old stone lighthouse looms. Suddenly, a giant wave tosses the boat!"
        ),
        'act2_q': "How will you guide the boat through the reefs?",
        'act2_opt1': "1. Try to bypass the reefs along the dangerous western arc where the waves seem smaller.",
        'act2_opt2': "2. Trust the calculations (or intuition) and go straight through the narrow gorge between the rocks.",
        'act2_out1_success': (
            "\nThanks to Frank's decoding, you know the western current is deceptive! You correct the course in time,\n"
            "bypass the dangerous shallow and smoothly dock the boat in the lighthouse's hidden concrete bay. Clean victory!"
        ),
        'act2_out1_fail': (
            "\nYou turn west, but a strong underwater current throws the boat straight onto a hidden rock!\n"
            "A terrible crash is heard. The hull is damaged, but Joe miraculously holds the wheel and beaches the boat.\n"
            "'The Sleuth' will need serious repairs, but you made it to dry land!"
        ),
        'act2_out2': (
            "\nJoe tightly grips the wheel, makes a sharp turn and steers the boat straight into the narrow gorge between the rocks!\n"
            "The boat flies centimeters from the sharp stones, caught in the foam. An incredible maneuver!\n"
            "You fly into a quiet harbor at the foot of the lighthouse. Chet finally starts breathing."
        ),
        'act3_title': "\n--- ACT III: DARKNESS, GENERATOR AND THE HARD HEAD ---",
        'act3_text': (
            "You step inside the lighthouse. Iron spiral stairs lead up in pitch darkness.\n"
            "Suddenly, a metallic screech is heard from above. You climb into the engine room.\n"
            "It is cold, smelling of fuel oil and rusty iron. Suddenly, a heavy steel hoist beam,\n"
            "filed by criminals, breaks from its mount and flies straight at you!"
        ),
        'act3_q': "Your reaction?",
        'act3_opt1': "1. [Joe's Choice] Take the blow, shielding Frank, and try to push the heavy iron beam away with your shoulder.",
        'act3_opt2': "2. [Frank's Choice] Try to instantly jump back and dodge the falling object.",
        'act3_out1_head': (
            "\nJoe pushes Frank aside, but the heavy iron piece hits him right on the head!\n"
            "Joe falls to the floor unconscious. Frank runs to his brother in horror.\n"
            "A minute later, Joe opens his eyes, rubbing a huge bump on the back of his head:\n"
            "— Ouch, Frank... I think I met an anvil. But hey, my skull is tougher than steel! (Classic trope!)\n"
            "Meanwhile, you notice that the lighthouse generator is damaged, and the lift to the top is blocked."
        ),
        'act3_out2_dodge': (
            "\nYou both jump back in sync! The beam crashes onto the concrete floor,\n"
            "showering sparks just centimeters from your feet. True agility!\n"
            "However, the shockwave breaks the main power cable. The lighthouse plunges into complete darkness,\n"
            "and the electronic lock to the top shuts."
        ),
        'act3_lock_q': "An electronic lock has blocked the way to the lamp room. How will you open it?",
        'act3_lock_opt1': "1. [Joe's Action] Use an iron crowbar found near the generator to pry open the lift shaft doors.",
        'act3_lock_opt2': "2. [Frank's Action] Restart the generator by connecting the power wires directly through a relay using a multimeter.",
        'act3_lock_out1': (
            "\nJoe inserts the crowbar into the door gap, strains all his muscles and with a shout presses the lever.\n"
            "The metal bends with a horrible screech, and the jammed doors finally slide open. The way up is free,\n"
            "but your hands are buzzing from the tension!"
        ),
        'act3_lock_out2': (
            "\nFrank calmly opens the generator panel. Using his knowledge of electronics,\n"
            "he finds the broken line, strips the wires and connects them bypassing the blown fuse.\n"
            "The generator happily purrs, the light flashes, and the lift doors automatically open! Elegant solution."
        ),
        'act4_title': "\n--- ACT IV: FINALE AT THE PEAK OF THE STORM ---",
        'act4_text': (
            "You climb onto the lighthouse's outer observation deck. The wind here is so strong that it almost knocks you off your feet.\n"
            "Lightning tears the sky, illuminating the wild sea below. 'The Conductor' stands by the railing in a wet coat.\n"
            "He holds a suitcase with the syndicate's documents. Nearby, a helicopter hovers over the deck,\n"
            "from which a rope ladder has been dropped! The criminal grabs it and begins to climb!"
        ),
        'act4_q': "'The Conductor' is escaping! What will you do?",
        'act4_opt1': "1. [Joe's Decision] Make a wild run and jump onto the rope ladder after him to pull him down.",
        'act4_opt2': "2. [Frank's Decision] Cleverly throw a heavy lifebuoy into the tail rotor blades or hook the ladder to the lighthouse's iron hook.",
        'act4_out1': (
            "\nJoe makes an incredible jump over the railing and grabs the bottom of the ladder!\n"
            "The helicopter wobbles from the sudden weight. Joe quickly climbs up, grabs 'The Conductor' by the leg\n"
            "and with a strong pull drags him back onto the wet deck! Frank instantly helps secure the criminal."
        ),
        'act4_out2': (
            "\nFrank instantly assesses the situation. He grabs a sturdy steel cargo hook\n"
            "mounted on the lighthouse wall and with a clever throw catches the bottom rung of the rope ladder!\n"
            "The helicopter tries to take off, but the tight cable blocks its movement. The pilot, fearing a crash,\n"
            "drops the ladder along with 'The Conductor' onto the deck, where you immediately apprehend him!"
        ),
        'final_header': "                THE END                      ",
        'final_high': (
            "Congratulations! You solved the case of the entire syndicate brilliantly! Your score: {score} points.\n"
            "'The Conductor' is behind bars again, and all the secret documents are in the hands of the police.\n"
            "Sheriff Collig and your father Fenton Hardy arrive at the lighthouse on a coast guard rescue vessel.\n"
            "They are proud of your courage and intelligence!\n"
            "And in the evening at home, a double portion of hot berry pie from Aunt Gertrude awaits you,\n"
            "and Chet Morton is already ordering extra pizza delivery, celebrating full triumph!"
        ),
        'final_normal': (
            "The case is successfully closed! Your score: {score} points.\n"
            "Although the storm battered your boat, and Joe's head is decorated with a new battle bump,\n"
            "the leader of the criminals is apprehended, and Bayport can sleep soundly with the Hardy Boys on duty!"
        ),
        'final_thanks': "\nThanks for playing! Frank and Joe would be proud of your detective talent."
    },
    'ru': {
        'select_lang': "Выберите язык / Oберіть мову / Select Language:\n1. Українська\n2. English\n3. Русский",
        'lang_choice_prompt': "Ваш выбор (1-3): ",
        'press_enter': "Нажмите ENTER, чтобы начать приключение...",
        'invalid_input': "Пожалуйста, введите 1 или 2.",
        'intro_text': (
            "Вы играете за отважных братьев-детективов Фрэнка и Джо Харди из прибрежного Бейпорта.\n"
            "Позади остались поезд-призрак, серебряные шахты и Остров Черепа. Но лидер синдиката контрабандистов,\n"
            "известный как «Дирижер», сбежал во время тюремного конвоя! Его последние следы ведут к\n"
            "заброшенному Маяку Одинокой Скалы посреди бушующего моря недалеко от Бейпорта..."
        ),
        'act1_title': "\n--- АКТ I: СЕМЕЙНЫЙ ПИР И СВЕТОВОЙ ШИФР ---",
        'act1_text': (
            "Вы сидите на уютной кухне дома Харди. Тетя Гертруда превзошла саму себя:\n"
            "на столе дымится огромная супница с нежным сливочным крем-супом из моллюсков (Clam Chowder),\n"
            "стоит корзина с горячим домашним хлебом на закваске, смазанным чесночным маслом, и ароматный\n"
            "ягодный пирог с шариком тающего мороженого. Чет Мортон уже сметает третью тарелку супа.\n\n"
            "Вдруг в гостиную входит ваш отец, известный детектив Фентон Харди. Его лицо серьезно:\n"
            "— Ребята, «Дирижер» скрывается на Маяке Одинокой Скалы. Местные рыбаки видели,\n"
            "как с вершины маяка кто-то посылает зашифрованные световые сигналы в море. Надвигается мощный шторм,\n"
            "и береговая охрана не сможет подойти к скале. Мы должны действовать немедленно!"
        ),
        'act1_q': "Какой план действий вы выберете?",
        'act1_opt1': "1. [Путь Фрэнка] Остаться на 10 минут, чтобы проанализировать ритм вспышек маяка с помощью морских книг отца.",
        'act1_opt2': "2. [Путь Джо] Не терять ни секунды! Немедленно бежать в порт, заводить наш катер «Ищейка» и мчаться сквозь шторм.",
        'act1_out1': (
            "\nФрэнк быстро открывает старые навигационные справочники Бейпорта и сравнивает записи.\n"
            "Через несколько минут логика побеждает: вы разгадываете код вспышек! Это сигнал координации для иностранной субмарины,\n"
            "а также предупреждение об опасном подводном течении возле западного рифа. Теперь вы знаете безопасный путь!\n"
            "Вы берете фонарик, тяжелый трос, штурмовой дождевик и отправляетесь в порт."
        ),
        'act1_out2': (
            "\nДжо уверенно хватает ключи от катера! Рев мотора «Ищейки» заглушает первые раскаты грома.\n"
            "Вы выходите в открытое море. Волны поднимаются все выше, ветер швыряет соленые брызги в лицо.\n"
            "Чет Мортон бледнеет и крепко держится за борт, жалея, что не съел еще один кусок пирога.\n"
            "В вашем распоряжении только фонарики и базовый набор инструментов катера."
        ),
        'act2_title': "\n--- АКТ II: ШТОРМОВОЙ ПЕРЕХОД И ДЬЯВОЛЬСКИЕ ЗУБЫ ---",
        'act2_text': (
            "Черные волны толкают ваш катер прямо на острые скалы, которые моряки называют «Дьявольские Зубы».\n"
            "Ливень стоит стеной, видимость почти нулевая. Впереди, как гигантский призрак,\n"
            "вырисовывается силуэт старого каменного маяка. Вдруг гигантская волна подбрасывает катер!"
        ),
        'act2_q': "Как вы проведете катер сквозь рифы?",
        'act2_opt1': "1. Попробовать обойти рифы по опасному западному направлению, где волны кажутся меньше.",
        'act2_opt2': "2. Довериться расчетам (или интуиции) и идти напролом через узкое ущелье между скалами.",
        'act2_out1_success': (
            "\nБлагодаря расшифровке Фрэнка вы знаете, что западное течение обманчиво! Вы вовремя корректируете курс,\n"
            "огибаете опасную мель и мягко швартуете катер в скрытой бетонной бухте маяка. Чистая победа!"
        ),
        'act2_out1_fail': (
            "\nВы поворачиваете на запад, но сильное подводное течение бросает катер прямо на скрытый камень!\n"
            "Слышится страшный треск. Корпус поврежден, но Джо чудом удерживает штурвал и выбрасывает катер на берег.\n"
            "«Ищейка» потребует серьезного ремонта, но вы добрались до суши!"
        ),
        'act2_out2': (
            "\nДжо крепко сжимает штурвал, делает крутой вираж и направляет катер прямо во узкое ущелье между скалами!\n"
            "Катер пролетает в нескольких сантиметрах от острых камней, подхваченный пеной. Невероятный маневр!\n"
            "Вы влетаете в тихую гавань у подножия маяка. Чет наконец начинает дышать."
        ),
        'act3_title': "\n--- АКТ III: ТЕМНОТА, ГЕНЕРАТОР И КРЕПКАЯ ГОЛОВА ---",
        'act3_text': (
            "Вы заходите внутрь маяка. Железная винтовая лестница ведет вверх в полной темноте.\n"
            "Вдруг сверху раздается металлический скрежет. Вы поднимаетесь в машинное отделение.\n"
            "Здесь холодно, пахнет мазутом и ржавым железом. Вдруг тяжелая стальная балка талей,\n"
            "подпиленная преступниками, срывается с крепления и летит прямо на вас!"
        ),
        'act3_q': "Ваша реакция?",
        'act3_opt1': "1. [Выбор Джо] Принять удар на себя, закрыв Фрэнка, и попытаться оттолкнуть тяжелую железяку плечом.",
        'act3_opt2': "2. [Выбор Фрэнка] Попробовать мгновенно отскочить назад и уклониться от падения.",
        'act3_out1_head': (
            "\nДжо толкает Фрэнка в сторону, но тяжелая железная деталь бьет его прямо по голове!\n"
            "Джо падает на пол без чувств. Фрэнк в ужасе подбегает к брату.\n"
            "Через минуту Джо открывает глаза, потирая огромную шишку на затылке:\n"
            "— Ох, Фрэнк... Кажется, я встретился с наковальней. Но ничего, мой череп крепче стали! (Классический троп!)\n"
            "Тем временем вы замечаете, что генератор маяка поврежден, а лифт на верхнюю площадку заблокирован."
        ),
        'act3_out2_dodge': (
            "\nВы оба синхронно отскакиете назад! Балка с грохотом падает на бетонный пол,\n"
            "высекая искры всего в нескольких сантиметрах от ваших ног. Настоящая ловкость!\n"
            "Тем не менее ударная волна перебивает главный кабель питания. Маяк погружается в полную темноту,\n"
            "а электронный замок наверх закрывается."
        ),
        'act3_lock_q': "Электронный замок заблокировал ход в ламповую комнату. Как вы его откроете?",
        'act3_lock_opt1': "1. [Действие Джо] Использовать железный лом, найденный возле генератора, чтобы выломать двери лифтовой шахты.",
        'act3_lock_opt2': "2. [Действие Фрэнка] Перезапустить генератор, соединив провода питания напрямую через реле с помощью мультиметра.",
        'act3_lock_out1': (
            "\nДжо вставляет лом в щель двери, напрягает все мышцы и с криком давит на рычаг.\n"
            "Металл гнется с ужасным скрежетом, и заклиненные двери наконец раздвигаются. Путь вверх свободен,\n"
            "но ваши руки гудят от напряжения!"
        ),
        'act3_lock_out2': (
            "\nФрэнк спокойно вскрывает щиток генератора. Используя свои знания электроники,\n"
            "он находит оборванную линию, зачищает провода и соединяет их в обход перегоревшего предохранителя.\n"
            "Генератор радостно пыхтит, свет загорается, и двери лифта автоматически открываются! Элегантное решение."
        ),
        'act4_title': "\n--- АКТ IV: ФИНАЛ НА ВЕРШИНЕ ШТОРМА ---",
        'act4_text': (
            "Вы поднимаетесь на внешнюю смотровую площадку маяка. Ветер здесь такой силы, что едва не сбивает с ног.\n"
            "Молнии разрывают небо, освещая бушующее море внизу. У перил стоит «Дирижер» в мокром плаще.\n"
            "Он держит в руках чемодан с документами синдиката. Рядом над площадкой завис вертолет,\n"
            "с которого сбросили веревочную лестницу! Преступник хватается за нее и начинает подниматься!"
        ),
        'act4_q': "«Дирижер» убегает! Что вы сделаете?",
        'act4_opt1': "1. [Решение Джо] Сделать безумный разбег и прыгнуть на веревочную лестницу вслед за ним, чтобы стянуть его вниз.",
        'act4_opt2': "2. [Решение Фрэнка] Ловко бросить тяжелый спасательный круг на лопасти хвостового винта или зацепить лестницу за железный крюк маяка.",
        'act4_out1': (
            "\nДжо совершает невероятный прыжок через перила и цепляется за низ лестницы!\n"
            "Вертолет шатается от внезапного веса. Джо быстро лезет вверх, хватает «Дирижера» за ногу\n"
            "и сильным рывком стаскивает его обратно на мокрую площадку маяка! Фрэнк мгновенно помогает скрутить преступника."
        ),
        'act4_out2': (
            "\nФрэнк мгновенно оценивает ситуацию. Он хватает прочный стальной крюк для грузов,\n"
            "закрепленный на стене маяка, и ловким броском цепляет его за нижнюю ступеньку веревочной лестницы!\n"
            "Вертолет пытается взлететь вверх, но натянутый трос блокирует его движение. Пилот, боясь катастрофы,\n"
            "сбрасывает лестницу вместе с «Дирижером» на площадку, где вы его немедленно задерживаете!"
        ),
        'final_header': "                 ФИНАЛ                       ",
        'final_high': (
            "Поздравляем! Вы блестяще закрыли дело всего синдиката! Ваш счет: {score} очков.\n"
            "«Дирижер» снова за решеткой, а все секретные документы контрабандистов оказались в руках полиции.\n"
            "Шериф Коллиг и ваш отец Фентон Харди прибывают на маяк на спасательном судне береговой охраны.\n"
            "Они гордятся вашей смелостью и умом!\n"
            "А вечером дома вас ждет двойная порция горячего ягодного пирога от тети Гертруды,\n"
            "и Чет Мортон уже заказывает дополнительную доставку пиццы, празднуя полный триумф!"
        ),
        'final_normal': (
            "Дело успешно завершено! Ваш счет: {score} очок.\n"
            "Хотя шторм потрепал ваш катер, а затылок Джо украшен новой боевой шишкой,\n"
            "лидер преступников задержан, а Бейпорт может спать спокойно, пока на посту стоят Братья Харди!"
        ),
        'final_thanks': "\nСпасибо за игру! Фрэнк и Джо гордились бы вашим детективным талантом."
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
            state.inventory.append('rope')
            state.inventory.append('flashlight')
            state.inventory.append('decrypted_code')
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
    
    while True:
        print("\n" + loc['act2_q'])
        print(loc['act2_opt1'])
        print(loc['act2_opt2'])
        choice = input(loc.get('lang_choice_prompt', '\n-> ')).strip()
        
        if choice == '1':
            if state.route_taken == 'frank':
                state.score += 25
                print_slow(loc['act2_out1_success'])
            else:
                state.score += 5
                print_slow(loc['act2_out1_fail'])
            break
        elif choice == '2':
            state.score += 20
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
            state.score += 15
            print_slow(loc['act3_out1_head'])
            break
        elif choice == '2':
            state.score += 25
            print_slow(loc['act3_out2_dodge'])
            break
        else:
            print(loc['invalid_input'])
            
    # Act 3 Door Lock part
    print_slow(loc['act3_lock_q'])
    while True:
        print(loc['act3_lock_opt1'])
        print(loc['act3_lock_opt2'])
        choice = input(loc.get('lang_choice_prompt', '\n-> ')).strip()
        
        if choice == '1':
            state.score += 15
            print_slow(loc['act3_lock_out1'])
            break
        elif choice == '2':
            state.score += 25
            print_slow(loc['act3_lock_out2'])
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
    
    if state.score >= 85:
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
