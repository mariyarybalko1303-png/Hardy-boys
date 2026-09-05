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
        'uk': "          БРАТИ ХАРДІ ТА ПРОКЛЯТТЯ ЧОРНОГО ЛІСУ (ЧАСТИНА 9)          ",
        'en': "      THE HARDY BOYS AND THE CURSE OF THE BLACK FOREST (PART 9)     ",
        'ru': "          БРАТЬЯ ХАРДИ И ПРОКЛЯТИЕ ЧЕРНОГО ЛЕСА (ЧАСТЬ 9)           "
    }
    subtitle_text = {
        'uk': "                 Інтерактивний текстовий квест                 ",
        'en': "                 Interactive Text-Based Quest                  ",
        'ru': "                 Интерактивный текстовый квест                 "
    }
    print("=" * 76)
    print(title_text[lang])
    print(subtitle_text[lang])
    print("=" * 76)
    print()

class GameState:
    def __init__(self):
        self.lang = 'uk'
        self.inventory = []
        self.route_taken = None  # 'frank' (science/archives) or 'joe' (dirt bikes/bog)
        self.hard_head_active = True
        self.solved_puzzle = False
        self.score = 0

# Localization dictionary
LOCALIZATION = {
    'uk': {
        'select_lang': "Оберіть мову / Select Language / Выберите язык:\n1. Українська\n2. English\n3. Русский",
        'lang_choice_prompt': "Ваш вибір (1-3): ",
        'press_enter': "Натисніть ENTER, щоб розпочати нову пригоду...",
        'invalid_input': "Будь ласка, введіть 1 або 2.",
        'intro_text': (
            "Ви граєте за Френка та Джо Харді — відомих братів-детективів з Бейпорта.\n"
            "У попередній частині ви знешкодили шпигунів на «Карнавалі Тіней» і здобули загадковий мікрочип.\n"
            "Проте розслідування не закінчується! Нова зачіпка веде вас на північ від міста —\n"
            "у похмурий, оповитий туманом та містичними легендами Чорний Ліс..."
        ),
        'act1_title': "\n--- АКТ I: ГАСТРОНОМІЧНИЙ ТАБІР ТА ПЕРШЕ ВИЙТТЯ ---",
        'act1_text': (
            "Ви розбили табір на лісовій галявині Чорного Лісу під кронами вікових сосен.\n"
            "Ваш найкращий друг Чет Мортон знову перевершив себе у кулінарії!\n"
            "На багатті в чавунному казанку булькає неймовірне рагу: соковиті шматочки свинини,\n"
            "солодка кукурудза, пряні трави та ароматний бульйон. На вугіллі запікається картопля,\n"
            "начинена підсмаженим беконом та розплавленим чеддером. Чет якраз дістає з кошика\n"
            "теплі чорничні пиріжки, коли лісову тишу розриває щось жахливе...\n\n"
            "Це низьке, моторошне вовче виття, від якого холоне кров у жилах.\n"
            "Тієї ж миті крізь туман проноситься велетенська тінь із палаючими червоними очима!\n"
            "Вона зносить ваш намет і зникає у темній хащі. На місці нападу ви знаходите\n"
            "розтоптаний GPS-навігатор відомого еколога доктора Кілпатріка, який зник тиждень тому."
        ),
        'act1_q': "Що ви вирішите робити далі?",
        'act1_opt1': "1. [Шлях Френка] Повернутися до намету охорони заповідника, проаналізувати GPS-дані та зразки дивного люмінесцентного слизу на зламаних гілках.",
        'act1_opt2': "2. [Шлях Джо] Негайно застрибнути на кросові мотоцикли і мчати по свіжих глибоких слідах лап углиб Чорного болота.",
        'act1_out1': (
            "\nВи обираєте логічний підхід. Френк акуратно збирає зразки свіжого зеленкуватого слизу,\n"
            "що дивно світиться в темряві, та підключає пошкоджений GPS-навігатор до портативного комп'ютера.\n"
            "Ви виявляєте зашифровані лог-файли доктора Кілпатріка. Попереду кропітка аналітична робота!"
        ),
        'act1_out2': (
            "\nРевіння ваших мотоциклів лунає на весь ліс! Ви з Джо мчите крізь туман.\n"
            "Сліди лап велетенські — майже вдвічі більші за вовчі, і ведуть вони прямо через підступне Чорне болото.\n"
            "Грязь летить з-під коліс, гілки б'ють по шоломах. Потрібна максимальна концентрація!"
        ),
        'act2_title': "\n--- АКТ II: ПОШУКИ У ТУМАННОМУ ЛІСІ ---",
        'act2_text_frank': (
            "Френк намагається зламати шифр захищених файлів еколога.\n"
            "На екрані комп'ютера з'являється підказка: «Пароль — це назва сузір'я, за яким орієнтуються моряки Бейпорта»."
        ),
        'act2_q_frank': "Введіть пароль англійською (підказка: Велика Ведмедиця / Ursa Major):",
        'act2_frank_success': (
            "\nПравильно! Файли розблоковано. Ви дізнаєтеся, що доктор Кілпатрік зафіксував\n"
            "аномальне ультразвукове випромінювання біля закинутої срібної шахти «Чорний Вовк».\n"
            "Також ви з'ясували, що слиз — це синтетичний фосфорний маркер. Ви вирушаєте туди, взявши детектор хвиль."
        ),
        'act2_frank_fail': (
            "\nНеправильний пароль! Система заблокувалася, але Френк встигає обійти захист апаратним шляхом.\n"
            "Це забирає дорогоцінний час, але ви все ж отримуєте приблизні координати шахти «Чорний Вовк».\n"
            "Ви вирушаєте на місце, проте ваш рахунок зменшено."
        ),
        'act2_text_joe': (
            "Джо мчить по багнюці Чорного болота. Раптом попереду туман згущується,\n"
            "і ви помічаєте, що стежка веде прямо в глибоку трясовину, а попереду падає підпиляна сосна!"
        ),
        'act2_q_joe': "Ваша дія на мотоциклі?",
        'act2_joe_opt1': "1. Зробити різкий занос і спробувати проскочити під стовбуром дерева, що падає.",
        'act2_joe_opt2': "2. Використати природний трамплін з коренів ліворуч, щоб перестрибнути небезпечну ділянку.",
        'act2_joe_out1': (
            "\nВи нахиляєте мотоцикл майже до землі! Шолом чипляє гілки, але ви спритно пролітаєте під сосною.\n"
            "Проте заднє колесо грузне в болоті. Джо доводиться докласти зусиль, щоб витягти байк."
        ),
        'act2_joe_out2': (
            "\nНеймовірний трюк! Ви тиснете на газ, мотоцикл злітає в повітря, перелітає трясовину та дерево,\n"
            "і м'яко приземляється на тверду кам'янисту стежку, що веде прямо до старої шахти! +15 очок!"
        ),
        'act3_title': "\n--- АКТ III: ШАХТА ТА МІЦНА ГОЛОВА ---",
        'act3_text': (
            "Обидва шляхи приводять вас до похмурого входу в закинуту срібну шахту «Чорний Вовк».\n"
            "Всередині пахне вологою, землею та іржею. Старі рейки для вагонеток ведуть углиб.\n"
            "Раптом над головою лунає тріск підпиляних опор! Величезна дерев'яна балка падає вниз!\n\n"
            "Джо блискавично реагує, штовхає Френка вбік, рятуючи його, але сам отримує сильний удар\n"
            "прямо по потилиці! Джо падає непритомний. Злочинці в масках швидко зачиняють важкі\n"
            "залізні двері підземної клітки-шахти на масивний засув.\n\n"
            "За кілька хвилин Джо приходить до тями, трясе головою та посміхається:\n"
            "— Ох, Френк... Наче по мені знову проїхав товарний поїзд. Але моя голова міцніша за ці балки! (Класичний троп!)\n"
            "Ви озираєтесь і бачите, що у сусідньому відсіку клітки лежить зв'язаний доктор Кілпатрік!\n"
            "Він шепоче: «Хлопці, привид вовка — це фальшивка! Це величезний дрон-голограма з ультразвуковим випромінювачем,\n"
            "який викликає у людей паніку й галюцинації. Банда контрабандистів використовує його, щоб відлякувати всіх від\n"
            "шахти, де вони таємно видобувають радіоактивний люмінесцентний мінерал!»"
        ),
        'act3_q': "Як ви виберетеся з заблокованої клітки?",
        'act3_opt1': "1. [Сила Джо] Використати стару іржаву залізничну рейку поруч як важіль, щоб вигнути сталеві лозини решітки.",
        'act3_opt2': "2. [Логіка Френка] Розібрати панель керування ліфтом поруч і спробувати замкнути дроти живлення, щоб підняти решітку.",
        'act3_out1': (
            "\nДжо спирається на рейку всією вагою. Залізо скрипить, лозини решітки повільно розсуваються!\n"
            "Ви з Френком та доктором Кілпатріком протискаєтесь у прохід. Ви вільні, але ваші м'язи гудуть від втоми."
        ),
        'act3_out2': (
            "\nЧиста інженерна робота Френка! Ви знімаєте іржаву кришку щитка, знаходите потрібні фази та\n"
            "спритно замикаєте їх металевим дротом від ліхтарика. З гучним скреготом сталева решітка\n"
            "піднімається вгору! Шлях вільний і без зайвого шуму! +20 очок!"
        ),
        'act4_title': "\n--- АКТ IV: ФІНАЛ ПІД ОБВАЛОМ ---",
        'act4_text': (
            "Ви прокрадаєтесь до центрального залу шахти і бачите ватажка банди — фальшивого геолога Крофта.\n"
            "Він та його спільники встановлюють ящики з динамітом навколо опор шахти!\n"
            "— Швидше вантажте мінерали в машини! — кричить Крофт. — Ми підірвемо цю діру,\n"
            "і ніхто ніколи не дізнається про багатства Чорного Лісу. А еколог завалений під тоннами скель буде чудовим доказом прокляття!\n\n"
            "Раптом з боку виходу чути голоси Чета Мортона та шерифа Колліга з поліцією Бейпорта!\n"
            "Бандити панікують, а Крофт тримає пальці на детонаторі, збираючись підірвати шахту прямо зараз!"
        ),
        'act4_q': "Ваш фінальний крок для знешкодження бомби?",
        'act4_opt1': "1. [Дія Джо] Зробити відчайдушний стрибок з виступу прямо на Крофта, щоб вибити пульт-детонатор з його рук.",
        'act4_opt2': "2. [Дія Френка] Використати детектор хвиль, щоб запустити на повну потужність ультразвуковий дрон-вовк, спрямувавши його хвилі паніки на бандитів.",
        'act4_out1': (
            "\nДжо здійснює фантастичний стрибок! Він збиває Крофта з ніг у ту саму мить, коли той тисне на кнопку.\n"
            "Пульт відлітає вбік. Френк миттєво підхоплює його та вимикає систему підриву.\n"
            "Шериф Колліг забігає в зал і заарештовує бандитів! Шахту врятовано!"
        ),
        'act4_out2': (
            "\nФренк миттєво переналаштовує детектор хвиль і запускає голографічного вовка на повну потужність!\n"
            "У печері лунає жахливе ультразвукове виття. Бандити хапаються за голови від нестерпного страху й паніки,\n"
            "кидаючи зброю та детонатор. Поліція Бейпорта без перешкод затримує повністю деморалізованих злочинців!"
        ),
        'final_header': "                 ФІНАЛ                       ",
        'final_high': (
            "Вітаємо! Ви блискуче розкрили «Прокляття Чорного Лісу»! Ваш рахунок: {score} очок.\n"
            "Доктора Кілпатріка врятовано, незаконний видобуток припинено, а міф про привидного вовка розвіяно!\n"
            "Шериф Колліг пишається вами, а Чет Мортон уже готує нову порцію гарячого рагу на галявині.\n"
            "Попереду на вас чекають нові захоплюючі таємниці! Бейпорт під надійним захистом Братів Харді!"
        ),
        'final_normal': (
            "Справу успішно завершено! Ваш рахунок: {score} очок.\n"
            "Ви пройшли крізь похмурі хащі та болота, врятували еколога і викрили банду Крофта.\n"
            "Хоча потилиця Джо все ще трохи болить, справедливість знову перемогла!\n"
            "Дякуємо за участь у грі!"
        ),
        'final_thanks': "\nДякуємо за гру! Френк та Джо пишалися б вашими рішеннями."
    },
    'en': {
        'select_lang': "Select Language / Оберіть мову / Выберите язык:\n1. Українська\n2. English\n3. Русский",
        'lang_choice_prompt': "Your choice (1-3): ",
        'press_enter': "Press ENTER to start the new adventure...",
        'invalid_input': "Please enter 1 or 2.",
        'intro_text': (
            "You are playing as Frank and Joe Hardy — the famous detective brothers from Bayport.\n"
            "In the previous part, you stopped the spies at the 'Shadow Carnival' and got a mysterious microchip.\n"
            "However, the investigation never ends! A new clue leads you north of the city —\n"
            "into the dark, foggy, and legend-shrouded Black Forest..."
        ),
        'act1_title': "\n--- ACT I: CAMPFIRE FEAST & THE FIRST HOWL ---",
        'act1_text': (
            "You have set up camp on a forest clearing in the Black Forest, under the canopy of ancient pines.\n"
            "Your best friend Chet Morton has outdone himself in cooking again!\n"
            "An incredible stew is bubbling in a cast-iron pot over the campfire: juicy pieces of pork,\n"
            "sweet corn, fresh herbs, and savory broth. In the embers, potatoes stuffed with crispy bacon\n"
            "and melted cheddar are baking. Chet is just pulling warm blueberry pies out of his basket\n"
            "when a terrifying sound shatters the forest silence...\n\n"
            "A low, chilling wolf howl that makes your blood run cold.\n"
            "At that very moment, a giant shadow with glowing red eyes sweeps through the fog!\n"
            "It tears down your tent and vanishes into the thicket. At the site of the attack, you find\n"
            "a crushed GPS navigator belonging to Dr. Kilpatrick, a famous ecologist who went missing a week ago."
        ),
        'act1_q': "What do you decide to do?",
        'act1_opt1': "1. [Frank's Way] Return to the ranger station, analyze the GPS data and samples of strange luminescent slime found on the broken branches.",
        'act1_opt2': "2. [Joe's Way] Instantly hop on your dirt bikes and speed along the deep paw prints into the heart of the Black Bog.",
        'act1_out1': (
            "\nYou choose the logical approach. Frank carefully collects samples of the glowing green slime\n"
            "and connects the damaged GPS navigator to his portable computer.\n"
            "You discover encrypted log files of Dr. Kilpatrick. A lot of analytical work lies ahead!"
        ),
        'act1_out2': (
            "\nThe roar of your dirt bikes echoes through the forest! You and Joe speed through the fog.\n"
            "The paw prints are huge — almost twice the size of a regular wolf's, and they lead straight into the Black Bog.\n"
            "Mud flies from under the tires, branches hit your helmets. Maximum concentration is needed!"
        ),
        'act2_title': "\n--- ACT II: SEARCH IN THE FOGGY FOREST ---",
        'act2_text_frank': (
            "Frank tries to crack the encryption of the ecologist's files.\n"
            "A prompt appears on the screen: 'The password is the name of the constellation Bayport sailors navigate by.'"
        ),
        'act2_q_frank': "Enter the password in English (Hint: Big Dipper / Ursa Major):",
        'act2_frank_success': (
            "\nCorrect! Files decrypted. You learn that Dr. Kilpatrick recorded\n"
            "abnormal ultrasonic radiation near the abandoned silver mine 'Black Wolf'.\n"
            "You also discover the slime is a synthetic phosphorus marker. You head there with a wave detector."
        ),
        'act2_frank_fail': (
            "\nIncorrect password! The system locked down, but Frank bypasses the security with hardware tools.\n"
            "It takes valuable time, but you still get the approximate coordinates of the 'Black Wolf' mine.\n"
            "You head there, but your score is reduced."
        ),
        'act2_text_joe': (
            "Joe speeds through the mud of the Black Bog. Suddenly, the fog thickens,\n"
            "and you notice the path leads straight into a deep quagmire, while a sawed-off pine tree falls ahead!"
        ),
        'act2_q_joe': "Your action on the bike?",
        'act2_joe_opt1': "1. Make a sharp slide and try to slip under the falling tree trunk.",
        'act2_joe_opt2': "2. Use a natural ramp of roots on the left to jump over the dangerous area.",
        'act2_joe_out1': (
            "\nYou lean the bike almost to the ground! Your helmet grazes the branches, but you slide under the pine.\n"
            "However, the rear tire gets stuck in the bog. Joe has to work hard to pull the bike out."
        ),
        'act2_joe_out2': (
            "\nIncredible stunt! You hit the gas, the bike takes off, flies over the quagmire and the tree,\n"
            "landing smoothly on a solid rocky path leading straight to the old mine! +15 points!"
        ),
        'act3_title': "\n--- ACT III: THE MINE & THE HARD HEAD ---",
        'act3_text': (
            "Both paths lead you to the gloomy entrance of the abandoned silver mine 'Black Wolf'.\n"
            "Inside, it smells of dampness, earth, and rust. Old ore cart rails lead deeper.\n"
            "Suddenly, the sound of cracking supports echoes overhead! A giant wooden beam crashes down!\n\n"
            "Joe reacts instantly, pushes Frank aside, saving him, but takes a heavy blow\n"
            "right to the back of his head! Joe falls unconscious. Masked thugs quickly lock the heavy\n"
            "iron gate of the underground mine cage with a massive bolt.\n\n"
            "A few minutes later, Joe wakes up, shakes his head and smiles:\n"
            "— Ouch, Frank... Feels like a freight train hit me again. But my head is harder than these beams! (Classic trope!)\n"
            "You look around and see Dr. Kilpatrick tied up in the adjacent cage compartment!\n"
            "He whispers: 'Guys, the ghost wolf is a fake! It's a huge hologram drone with an ultrasonic emitter\n"
            "that causes panic and hallucinations. The smugglers use it to scare everyone away from\n"
            "the mine where they secretly extract radioactive luminescent minerals!'"
        ),
        'act3_q': "How will you escape from the locked cage?",
        'act3_opt1': "1. [Joe's Strength] Use an old rusty rail nearby as a lever to bend the steel bars of the gate.",
        'act3_opt2': "2. [Frank's Logic] Disassemble the elevator control panel nearby and try to hotwire the wires to raise the gate.",
        'act3_out1': (
            "\nJoe leans on the rail with all his weight. The iron creaks, the bars slowly bend!\n"
            "You, Frank, and Dr. Kilpatrick squeeze through. You are free, but your muscles ache from exhaustion."
        ),
        'act3_out2': (
            "\nPure engineering work by Frank! You remove the rusty cover, find the right phases,\n"
            "and hotwire them with a metal wire from the flashlight. With a loud screech, the steel gate\n"
            "rises up! The way is clear without any extra noise! +20 points!"
        ),
        'act4_title': "\n--- ACT IV: THE FINALE UNDER A CAVE-IN ---",
        'act4_text': (
            "You sneak into the central hall of the mine and see the gang leader — the fake geologist Croft.\n"
            "He and his henchmen are planting dynamite boxes around the mine supports!\n"
            "— Hurry up, load the minerals into the trucks! — Croft shouts. — We will blow this hole up,\n"
            "and no one will ever know about the riches of the Black Forest. An ecologist buried under tons of rock will be great proof of the curse!\n\n"
            "Suddenly, the voices of Chet Morton and Sheriff Collig with the Bayport police are heard from the exit!\n"
            "The bandits panic, and Croft holds his fingers on the detonator, about to blow up the mine right now!"
        ),
        'act4_q': "Your final step to neutralize the bomb?",
        'act4_opt1': "1. [Joe's Action] Make a desperate leap from the ledge directly onto Croft to knock the detonator out of his hands.",
        'act4_opt2': "2. [Frank's Action] Use the wave detector to activate the ultrasonic wolf drone at full power, directing panic waves at the bandits.",
        'act4_out1': (
            "\nJoe makes a fantastic leap! He knocks Croft down at the exact second he presses the button.\n"
            "The remote flies aside. Frank instantly grabs it and disables the detonation system.\n"
            "Sheriff Collig rushes into the hall and arrests the bandits! The mine is saved!"
        ),
        'act4_out2': (
            "\nFrank instantly configures the wave detector and launches the holographic wolf at full power!\n"
            "A terrifying ultrasonic howl echoes in the cave. The bandits grab their heads in unbearable fear and panic,\n"
            "dropping their weapons and the detonator. The Bayport police easily arrest the fully demoralized criminals!"
        ),
        'final_header': "                THE END                      ",
        'final_high': (
            "Congratulations! You solved 'The Curse of the Black Forest' brilliantly! Your score: {score} points.\n"
            "Dr. Kilpatrick is saved, illegal mining is stopped, and the myth of the phantom wolf is debunked!\n"
            "Sheriff Collig is proud of you, and Chet Morton is already cooking a new batch of hot stew on the clearing.\n"
            "New exciting mysteries lie ahead! Bayport is safe with the Hardy Boys on duty!"
        ),
        'final_normal': (
            "The case is successfully completed! Your score: {score} points.\n"
            "You went through the dark thickets and bogs, saved the ecologist, and exposed Croft's gang.\n"
            "Although the back of Joe's head still hurts a bit, justice has prevailed once again!\n"
            "Thank you for playing!"
        ),
        'final_thanks': "\nThanks for playing! Frank and Joe would be proud of your choices."
    },
    'ru': {
        'select_lang': "Выберите язык / Oберіть мову / Select Language:\n1. Українська\n2. English\n3. Русский",
        'lang_choice_prompt': "Ваш выбор (1-3): ",
        'press_enter': "Нажмите ENTER, чтобы начать новое приключение...",
        'invalid_input': "Пожалуйста, введите 1 или 2.",
        'intro_text': (
            "Вы играете за Фрэнка и Джо Харди — известных братьев-детективов из Бейпорта.\n"
            "В предыдущей части вы обезвредили шпионов на «Карнавале Теней» и добыли загадочный микрочип.\n"
            "Однако расследование не заканчивается! Новая зацепка ведет вас на север от города —\n"
            "в мрачный, окутанный туманом и мистическими легендами Черный Лес..."
        ),
        'act1_title': "\n--- АКТ I: СЫТЫЙ СТАРТ И ПЕРВЫЙ ВОЙ ---",
        'act1_text': (
            "Вы разбили лагерь на лесной поляне Черного Леса под кронами вековых сосен.\n"
            "Ваш лучший друг Чет Мортон снова превзошел себя в кулинарии!\n"
            "На костре в чугунном котелке булькает невероятное рагу: сочные кусочки свинины,\n"
            "сладкая кукуруза, пряные травы и ароматный бульон. На углях запекается картофель,\n"
            "начиненный поджаренным беконом и расплавленным чеддером. Чет как раз достает из корзины\n"
            "теплые черничные пирожки, когда лесную тишину разрывает нечто ужасное...\n\n"
            "Это низкий, жуткий волчий вой, от которого стынет кровь в жилах.\n"
            "В то же мгновение сквозь туман проносится гигантская тень с горящими красными глазами!\n"
            "Она сносит вашу палатку и исчезает в темной чаще. На месте нападения вы находите\n"
            "раздавленный GPS-навигатор известного эколога доктора Килпатрика, пропавшего неделю назад."
        ),
        'act1_q': "Что вы решите делать дальше?",
        'act1_opt1': "1. [Путь Фрэнка] Вернуться к будке охраны заповедника, проанализировать GPS-данные и образцы странной светящейся слизи на сломанных ветках.",
        'act1_opt2': "2. [Путь Джо] Немедленно запрыгнуть на кроссовые мотоциклы и мчаться по свежим глубоким следам лап вглубь Черного болота.",
        'act1_out1': (
            "\nВы выбираете логический подход. Фрэнк аккуратно собирает образцы свежей светящейся слизи\n"
            "и подключает поврежденный GPS-навигатор к портативному компьютеру.\n"
            "Вы обнаруживаете зашифрованные лог-файлы доктора Килпатрика. Впереди кропотливая аналитическая работа!"
        ),
        'act1_out2': (
            "\nРев ваших мотоциклов разносится по всему лесу! Вы с Джо мчитесь сквозь туман.\n"
            "Следы лап огромные — почти вдвое больше волчьих, и ведут они прямо через коварное Черное болото.\n"
            "Грязь летит из-под колес, ветки бьют по шлемам. Требуется максимальная концентрация!"
        ),
        'act2_title': "\n--- АКТ II: ПОИСКИ В ТУМАННОМ ЛЕСУ ---",
        'act2_text_frank': (
            "Фрэнк пытается взломать шифр защищенных файлов эколога.\n"
            "На экране компьютера появляется подсказка: «Пароль — это название созвездия, по которому ориентируются моряки Бейпорта»."
        ),
        'act2_q_frank': "Введите пароль на английском (подсказка: Большая Медведица / Ursa Major):",
        'act2_frank_success': (
            "\nПравильно! Файлы разблокированы. Вы узнаете, что доктор Килпатрик зафиксировал\n"
            "аномальное ультразвуковое излучение около заброшенной серебряной шахты «Черный Волк».\n"
            "Также вы выяснили, что слизь — это синтетический фосфорный маркер. Вы отправляетесь туда с детектором волн."
        ),
        'act2_frank_fail': (
            "\nНеправильный пароль! Система заблокировалась, но Фрэнк обходит защиту аппаратным путем.\n"
            "Это отнимает драгоценное время, но вы все же получаете примерные координаты шахты «Черный Волк».\n"
            "Вы отправляетесь на место, но ваш счет уменьшен."
        ),
        'act2_text_joe': (
            "Джо мчит по грязи Черного болота. Вдруг впереди туман сгущается,\n"
            "и вы замечаете, что тропа ведет прямо в глубокую трясину, а впереди падает подпиленная сосна!"
        ),
        'act2_q_joe': "Ваше действие на мотоцикле?",
        'act2_joe_opt1': "1. Сделать резкий занос и попытаться проскочить под стволом падающего дерева.",
        'act2_joe_opt2': "2. Использовать природный трамплин из корней слева, чтобы перепрыгнуть опасный участок.",
        'act2_joe_out1': (
            "\nВы наклоняете мотоцикл почти к земле! Шлем цепляет ветки, но вы ловко пролетаете под сосной.\n"
            "Однако заднее колесо вязнет в болоте. Джо приходится приложить усилия, чтобы вытащить байк."
        ),
        'act2_joe_out2': (
            "\nНевероятный трюк! Вы жмете на газ, мотоцикл взлетает в воздух, перелетает трясину и дерево,\n"
            "и мягко приземляется на твердую каменистую тропу, ведущую прямо к старой шахте! +15 очков!"
        ),
        'act3_title': "\n--- АКТ III: ШАХТА И КРЕПКАЯ ГОЛОВА ---",
        'act3_text': (
            "Оба пути приводят вас к мрачному входу в заброшенную серебряную шахту «Черный Волк».\n"
            "Внутри пахнет сыростью, землей и ржавчиной. Старые рельсы для вагонеток ведут вглубь.\n"
            "Вдруг над головой раздается треск подпиленных опор! Огромная деревянная балка летит вниз!\n\n"
            "Джо молниеносно реагирует, толкает Фрэнка в сторону, спасая его, но сам получает сильный удар\n"
            "прямо по затылку! Джо падает без чувств. Преступники в масках быстро закрывают тяжелую\n"
            "железную дверь подземной клетки-шахты на массивный засов.\n\n"
            "Через несколько минут Джо приходит в себя, трясет головой и улыбается:\n"
            "— Ох, Фрэнк... Как будто по мне снова проехал товарный поезд. Но моя голова крепче этих балок! (Классический троп!)\n"
            "Вы осматриваетесь и видите, что в соседнем отсеке клетки лежит связанный доктор Килпатрик!\n"
            "Он шепчет: «Ребята, призрак волка — это фальшивка! Это огромный дрон-голограмма с ультразвуковым излучателем,\n"
            "вызывающим у людей панику и галлюцинации. Банда контрабандистов использует его, чтобы отпугивать всех от\n"
            "шахты, где они тайно добывают радиоактивный люминесцентный минерал!»"
        ),
        'act3_q': "Как вы выберетесь из заблокированной клетки?",
        'act3_opt1': "1. [Сила Джо] Использовать старый ржавый рельс рядом в качестве рычага, чтобы выгнуть стальные прутья решетки.",
        'act3_opt2': "2. [Логика Фрэнка] Разобрать панель управления лифтом рядом и попытаться замкнуть провода питания, чтобы поднять решетку.",
        'act3_out1': (
            "\nДжо упирается в рельс всем весом. Железо скрипит, прутья решетки медленно раздвигаются!\n"
            "Вы с Фрэнком и доктором Килпатриком протискиваетесь в проход. Вы свободны, но ваши мышцы гудят от усталости."
        ),
        'act3_out2': (
            "\nЧистая инженерная работа Фрэнка! Вы снимаете ржавую крышку щитка, находите нужные фазы и\n"
            "ловко замыкаете их металлической проволокой от фонарика. С громким скрежетом стальная решетка\n"
            "поднимается вверх! Путь свободен и без лишнего шума! +20 очков!"
        ),
        'act4_title': "\n--- АКТ IV: ФИНАЛ ПОД ОБВАЛОМ ---",
        'act4_text': (
            "Вы тихо пробираетесь в центральный зал шахты и видите главаря банды — фальшивого геолога Крофта.\n"
            "Он и его сообщники устанавливают ящики с динамитом вокруг опор шахты!\n"
            "— Быстрее грузите минералы в машины! — кричит Крофт. — Мы взорвем эту дыру,\n"
            "и никто никогда не узнает о богатствах Черного Леса. А эколог, заваленный под тоннами скал, будет отличным доказательством проклятия!\n\n"
            "Вдруг со стороны выхода слышны голоса Чета Мортона и шерифа Коллига с полицией Бейпорта!\n"
            "Бандиты паникуют, а Крофт держит пальцы на детонаторе, собираясь взорвать шахту прямо сейчас!"
        ),
        'act4_q': "Ваш финальный шаг для обезвреживания бомбы?",
        'act4_opt1': "1. [Действие Джо] Совершить отчаянный прыжок с выступа прямо на Крофта, чтобы выбить пульт-детонатор из его рук.",
        'act4_opt2': "2. [Действие Фрэнка] Использовать детектор волн, чтобы запустить на полную мощность ультразвуковой дрон-волк, направив его волны паники на бандитов.",
        'act4_out1': (
            "\nДжо совершает фантастический прыжок! Он сбивает Крофта с ног в ту самую секунду, когда тот жмет на кнопку.\n"
            "Пульт отлетает в сторону. Фрэнк мгновенно подхватывает его и отключает систему подрыва.\n"
            "Шериф Коллиг забегает в зал и арестовывает бандитов! Шахта спасена!"
        ),
        'act4_out2': (
            "\nФрэнк мгновенно перенастраивает детектор волн и запускает голографического вовка на полную мощность!\n"
            "В пещере раздается ужасный ультразвуковой вой. Бандиты хватаются за головы от невыносимого страха и паники,\n"
            "бросая оружие и детонатор. Полиция Бейпорта без препятствий задерживает полностью деморализованных преступников!"
        ),
        'final_header': "                 ФИНАЛ                       ",
        'final_high': (
            "Поздравляем! Вы блестяще раскрыли «Проклятие Черного Леса»! Ваш счет: {score} очков.\n"
            "Доктор Килпатрик спасен, незаконная добыча прекращена, а миф о призрачном волке развенчан!\n"
            "Шериф Коллиг гордится вами, а Чет Мортон уже готовит новую порцию горячего рагу на поляне.\n"
            "Впереди вас ждут новые захватывающие тайны! Бейпорт под надежной защитой Братьев Харди!"
        ),
        'final_normal': (
            "Дело успешно завершено! Ваш счет: {score} очков.\n"
            "Вы прошли сквозь мрачные чащи и болота, спасли эколога и разоблачили банду Крофта.\n"
            "Хотя затылок Джо все еще немного болит, справедливость снова восторжествовала!\n"
            "Спасибо за участие в игре!"
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
            print_slow(loc['act1_out1'])
            act_2_frank(state)
            break
        elif choice == '2':
            state.route_taken = 'joe'
            state.score += 15
            print_slow(loc['act1_out2'])
            act_2_joe(state)
            break
        else:
            print(loc['invalid_input'])

def act_2_frank(state):
    loc = LOCALIZATION[state.lang]
    print_slow(loc['act2_title'])
    print_slow(loc['act2_text_frank'])
    
    attempts = 0
    while attempts < 3:
        ans = input("\n" + loc['act2_q_frank'] + " ").strip().lower()
        if ans == "ursa major" or ans == "ursamajor":
            state.score += 25
            state.solved_puzzle = True
            print_slow(loc['act2_frank_success'])
            break
        else:
            attempts += 1
            if attempts < 3:
                print("Incorrect! Try again." if state.lang == 'en' else "Невірно! Спробуйте ще раз." if state.lang == 'uk' else "Неверно! Попробуйте еще раз.")
            else:
                state.score += 5
                print_slow(loc['act2_frank_fail'])
                
    act_3(state)

def act_2_joe(state):
    loc = LOCALIZATION[state.lang]
    print_slow(loc['act2_title'])
    print_slow(loc['act2_text_joe'])
    
    while True:
        print("\n" + loc['act2_q_joe'])
        print(loc['act2_joe_opt1'])
        print(loc['act2_joe_opt2'])
        choice = input(loc.get('lang_choice_prompt', '\n-> ')).strip()
        
        if choice == '1':
            state.score += 10
            print_slow(loc['act2_joe_out1'])
            break
        elif choice == '2':
            state.score += 25
            print_slow(loc['act2_joe_out2'])
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
            print_slow(loc['act3_out1'])
            break
        elif choice == '2':
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
