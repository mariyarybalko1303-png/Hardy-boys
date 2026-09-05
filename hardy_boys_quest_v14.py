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
        'uk': "          БРАТИ ХАРДІ ТА СКАРБИ ІСПАНСЬКИХ ГАЛЕОНІВ (ЧАСТИНА XIV)       ",
        'en': "      THE HARDY BOYS AND THE SPANISH GALLEON TREASURE (PART XIV)      ",
        'ru': "          БРАТЬЯ ХАРДИ И СОКРОВИЩА ИСПАНСКИХ ГАЛЕОНОВ (ЧАСТЬ XIV)     "
    }
    subtitle_text = {
        'uk': "          Нічні занурення та небезпеки сонячної Флориди               ",
        'en': "          Night Dives and Dangers of Sunny Florida                    ",
        'ru': "          Ночные погружения и опасности солнечной Флориды             "
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
        self.route_taken = None  # 'frank' (archives/decode) or 'joe' (jetski/chase)
        self.escaped_stealth = False
        self.score = 0

LOCALIZATION = {
    'uk': {
        'select_lang': "Оберіть мову / Select Language / Выберите язык:\n1. Українська\n2. English\n3. Русский",
        'lang_choice_prompt': "Ваш вибір (1-3): ",
        'press_enter': "Натисніть ENTER, щоб розпочати пригоду...",
        'invalid_input': "Будь ласка, введіть 1 або 2.",
        'intro_text': (
            "Після перемоги над синдикатом «Диригент» Френк, Джо та їхній вірний друг Чет Мортон\n"
            "вирушають на заслужений відпочинок до сонячного архіпелагу Кі-Вест у Флориді.\n"
            "Проте замість спокійного пляжного відпочинку на хлопців чекає нова захоплююча таємниця,\n"
            "пов'язана із затонулим у XVII столітті іспанським галеоном «Санта-Ізабелла»!"
        ),
        'act1_title': "\n--- АКТ I: ФЛОРИДСЬКИЙ ПІКНІК ТА СТАРА ПІАСТРА ---",
        'act1_text': (
            "Ви сидите на відкритій веранді затишного прибережного кафе «Мушля». Навколо шумить океан.\n"
            "Перед вами — справжнє кулінарне диво: тарілка із хрусткими золотавими фріттерами з молюсків,\n"
            "традиційний флоридський лаймовий пиріг з пишним білковим кремом та склянки холодного лимонаду.\n"
            "Чет Мортон якраз відправляє у рот останній шматочок пирога і задоволено мружиться.\n\n"
            "Раптом до вашого столика підходить літній капітан Біллі — старий шукач скарбів із пов'язкою на оці.\n"
            "— Хлопці, я чув, ви ті самі кмітливі брати Харді! — хрипко шепоче він і кладе на стіл важку,\n"
            "вкриту коралами золоту іспанську піастру. — Мені вдалося знайти координати легендарного\n"
            "галеона «Санта-Ізабелла», що затонув у 1682 році. Але за мною стежить банда «Баракуда».\n"
            "Вони хочуть відібрати мою карту! Якщо я зникну — скарби мають дістатися світу, а не піратам!\n\n"
            "Тієї ж миті з туману на причалі вибігають двоє чоловіків у чорних гідрокостюмах,\n"
            "виривають сумку капітана Біллі і стрімко тікають у ніч!"
        ),
        'act1_q': "Що ви вирішите робити?",
        'act1_opt1': "1. [Шлях Френка] Залишитися з пораненим капітаном Біллі, надати йому першу допомогу та дослідити залишену піастру на наявність прихованих шифрів.",
        'act1_opt2': "2. [Шлях Джо] Одразу схопити ключі від гідроциклів на причалі та кинутися в погоню за човном грабіжників крізь мангрові хащі.",
        'act1_out1': (
            "\nВи допомагаєте капітану Біллі підвестися. Він вдячний вам і показує секрет піастри:\n"
            "на її ребрі є мікроскопічні насічки. Френк під лупою з'ясовує, що це кутові координати сектора рифу!\n"
            "Завдяки логіці та знанням навігації, Френк точно визначає місце затонулого корабля.\n"
            "Ви берете професійне спорядження для дайвінгу, ліхтарі, карту течій та вирушаєте до вказаного рифу."
        ),
        'act1_out2': (
            "\nРевіння двигуна гідроцикла розтинає нічний океан! Джо мчить у темряву.\n"
            "Бризки солоної води летять в обличчя. Ви бачите силует моторного човна шпигунів попереду.\n"
            "Джо вправно лавірує між небезпечними мангровими коріннями, змушуючи грабіжників панікувати.\n"
            "Вони викидають сумку капітана Біллі у воду, намагаючись відволікти вас. Ви рятуєте сумку,\n"
            "але човен злочинців зникає за поворотом. Всередині сумки — детальна підводна карта рифу!"
        ),
        'act2_title': "\n--- АКТ II: ТАЄМНИЦЯ ЗАТОНУЛОГО ГАЛЕОНА ---",
        'act2_text': (
            "Нічний океан спокійний, але темний як чорнило. Ви занурюєтесь під воду з аквалангами.\n"
            "Промені ліхтарів вихоплюють із безодні дивовижні коралові сади, зграї кольорових риб\n"
            "та величні рештки іспанського галеона «Санта-Ізабелла», що наполовину занесені піском.\n"
            "Раптом ви помічаєте підводні ліхтарі іншої групи водолазів — бандити «Баракуди» вже тут!\n"
            "Вони готують вибухівку, щоб підірвати заблокований люк капітанської каюти, де лежить золото."
        ),
        'act2_q': "Які ваші дії під водою?",
        'act2_opt1': "1. Спробувати непомітно перерізати дроти їхніх підводних вибухових пристроїв за допомогою дайверського ножа.",
        'act2_opt2': "2. Влаштувати підводну диверсію: випустити повітря з балонів ворога або заплутати їхні сигнальні троси.",
        'act2_out1': (
            "\nФренк обережно підпливає до детонатора. Рука детектива не здригається.\n"
            "Він акуратно перерізає червоний кабель підводного підривника! Злочинці намагаються\n"
            "активувати заряд, але нічого не відбувається. Вони спантеличені й починають шукати причину."
        ),
        'act2_out2': (
            "\nДжо стрімко діє під водою! Він тихо підкрадається ззаду і перекриває вентилі балонів\n"
            "двох аквалангістів. Бандити починають задихатися, панічно махати руками і змушені терміново\n"
            "спливати на поверхню для декомпресії. Проте один із лідерів банди помічає вас!"
        ),
        'act3_title': "\n--- АКТ III: ПАСТКА НА ДНІ ТА МІЦНА ГОЛОВА JOE ---",
        'act3_text': (
            "Ви проникаєте всередину затонулої каюти галеона через пролом у гнилій палубі.\n"
            "Серед мулу та уламків височіє обкована залізом дубова скриня, наповнена золотими злитками!\n"
            "Раптом сильна підводна течія або підступний штуршок ворога обрушує важку дубову балку каюти.\n"
            "Балка летить прямо на Френка! Джо блискавично відштовхує брата, приймаючи удар на себе.\n"
            "Важке дерево б'є Джо прямо по шолому акваланга. Джо на мить непритомніє, а Френк відтягує його вбік.\n\n"
            "За хвилину Джо відкриває очі під маскою, показує жест 'OK' і весело булькає у рацію:\n"
            "— Ох... Здається, іспанський дуб такий же міцний, як моя голова! (Класичний троп!)\n"
            "Але ситуація критична: вихід завалено, а запаси кисню у ваших балонах стрімко вичерпуються!"
        ),
        'act3_q': "Як ви виберетесь із затонулої пастки?",
        'act3_opt1': "1. [Дія Джо] Використати залізний румпель старовинного корабля як важіль, щоб підняти важку завальну плиту.",
        'act3_opt2': "2. [Дія Френка] Використати портативний балон високого тиску, щоб підірвати заклинений замок дверей спрямованим струменем газу.",
        'act3_out1_success': (
            "\nДжо збирає всі сили, впирається ногами в шпангоут і за допомогою важкого румпеля\n"
            "піднімає уламок палуби! Френк швидко прослизає в отвір і допомагає вибратися Джо.\n"
            "Ви вільні, а золото у ваших руках!"
        ),
        'act3_out1_fail': (
            "\nВи намагаєтеся підняти балку важілем, але дерево занадто глибоко загрузло в мулі.\n"
            "Важіль ламається, а дорогоцінні хвилини та повітря втрачені! Доведеться шукати інший вихід."
        ),
        'act3_out2_success': (
            "\nФренк діє технічно: він під'єднує шланг високого тиску до замкового механізму дверей\n"
            "і різко подає повітря. Потужний тиск вибиває іржаві петлі старовинних дверей навстіж!\n"
            "Вихід вільний, і ви випливаєте у відкриту воду."
        ),
        'act4_title': "\n--- АКТ IV: ПОГОНЯ У ТУМАННИХ РИФАХ ТА ФІНАЛ ---",
        'act4_text': (
            "Ви спливаєте на поверхню біля вашого катера «Нишпорка» разом із врятованими скарбами.\n"
            "Але лідер «Баракуд» на прізвисько «Акула» вже помітив вас і мчить на перехоплення\n"
            "на потужному чорному катері. Починається шалена нічна погоня серед гострих коралових рифів!\n"
            "Хвилі здіймаються вище, а ворог намагається протаранити ваш борт!"
        ),
        'act4_q': "Як ви нейтралізуєте катер переслідувачів?",
        'act4_opt1': "1. [Маневр Джо] Спрямувати «Нишпорку» прямо на небезпечну мілину «Риф Сирен», щоб ворог на повній швидкості налетів на гостре каміння.",
        'act4_opt2': "2. [Тактика Френка] Кинути за корму плавучий трос із сигнальним буєм, щоб він намотався на гвинт двигуна переслідувачів.",
        'act4_out1': (
            "\nДжо робить крутий віраж в сантиметрах від гострих скель! Катер «Баракуди» не встигає\n"
            "звернути і з жахливим скреготом вилітає на рифи, повністю втративши хід.\n"
            "Ви перемогли!"
        ),
        'act4_out2': (
            "\nФренк блискавично скидає міцний трос у кільватерний слід. Канат миттєво затягує\n"
            "під корму ворожого катера і намотує на гвинт. Двигун «Баракуди» глухне з металевим стуком,\n"
            "і катер безпорадно зупиняється посеред хвиль!"
        ),
        'final_header': "                 ФІНАЛ                       ",
        'final_high': (
            "Вітаємо з перемогою! Ваш рахунок: {score} очок.\n"
            "Ви повернули легендарне золото іспанської корони капітану Біллі та Морському музею Кі-Веста!\n"
            "Увечері на вас чекає святковий бенкет на березі океану: велике блюдо з королівськими креветками,\n"
            "запечений на вогнищі лобстер та величезний додатковий лаймовий пиріг особисто для Чета!\n"
            "Батько Фентон Харді надсилає вітальну телеграму: «Пишаюся вами, хлопці. Справжня робота професіоналів!»"
        ),
        'final_normal': (
            "Справу успішно завершено! Ваш рахунок: {score} очок.\n"
            "Іспанські скарби врятовані від піратів, хоча шолом Джо тепер потребує ремонту,\n"
            "а Чет Мортон ледь не з'їв усю призову рибу сам. Брати Харді знову довели свій високий клас!"
        ),
        'final_thanks': "\nДякуємо за гру! Френк, Джо та Чет завжди готові до нових детективних пригод!"
    },
    'en': {
        'select_lang': "Select Language / Оберіть мову / Выберите язык:\n1. Українська\n2. English\n3. Русский",
        'lang_choice_prompt': "Your choice (1-3): ",
        'press_enter': "Press ENTER to start the adventure...",
        'invalid_input': "Please enter 1 or 2.",
        'intro_text': (
            "After defeating the 'Conductor' syndicate, Frank, Joe, and their loyal friend Chet Morton\n"
            "head to the sunny Key West archipelago in Florida for a well-deserved vacation.\n"
            "However, instead of quiet sunbathing, a thrilling new mystery awaits the boys,\n"
            "connected to the 17th-century Spanish galleon 'Santa Isabella'!"
        ),
        'act1_title': "\n--- ACT I: FLORIDA PICNIC AND THE OLD PIECE OF EIGHT ---",
        'act1_text': (
            "You are sitting on the outdoor veranda of the cozy waterfront cafe 'Conch Shell'.\n"
            "Before you is a culinary masterpiece: a plate of crispy golden clam fritters,\n"
            "traditional Key Lime Pie with fluffy meringue, and glasses of ice-cold lemonade.\n"
            "Chet Morton is just sending the last piece of pie into his mouth with a satisfied squint.\n\n"
            "Suddenly, elderly Captain Billy—an old one-eyed treasure hunter—approaches your table.\n"
            "— Boys, I heard you are those clever Hardy boys! — he whispers hoarsely, placing a heavy,\n"
            "coral-encrusted gold piece of eight on the table. — I managed to find the coordinates\n"
            "of the legendary galleon 'Santa Isabella', which sank in 1682. But 'The Barracuda' gang is after me.\n"
            "They want my map! If I disappear, the treasure must go to the world, not to pirates!\n\n"
            "At that very moment, two men in black wetsuits rush out of the harbor fog,\n"
            "snatch Captain Billy's bag, and bolt into the night!"
        ),
        'act1_q': "What do you decide to do?",
        'act1_opt1': "1. [Frank's Path] Stay with the injured Captain Billy, administer first aid, and inspect the gold coin for hidden codes.",
        'act1_opt2': "2. [Joe's Path] Grab the jet-ski keys from the dock and launch into a high-speed chase through the mangrove channels.",
        'act1_out1': (
            "\nYou help Captain Billy up. He is grateful and reveals the coin's secret:\n"
            "there are tiny markings on its edge. Under a magnifying glass, Frank discovers\n"
            "they are coordinates for the reef sector! Thanks to his navigational knowledge,\n"
            "Frank pinpoints the exact wreck location. You grab scuba gear and head out."
        ),
        'act1_out2': (
            "\nThe roar of the jet-ski engine shatters the night ocean! Joe speeds into the dark.\n"
            "Salty spray hits your face as you track the smugglers' speedboat.\n"
            "Joe maneuvers expertly through dangerous mangrove roots, forcing the thieves to panic.\n"
            "They throw Captain Billy's bag into the water to distract you. You rescue the bag,\n"
            "but their boat slips away. Inside the bag is a detailed underwater map of the reef!"
        ),
        'act2_title': "\n--- ACT II: THE MYSTERY OF THE SUNKEN GALLEON ---",
        'act2_text': (
            "The night ocean is calm, but dark as ink. You descend with scuba gear.\n"
            "Flashlight beams reveal coral gardens, schools of colorful fish,\n"
            "and the majestic, half-buried remains of the Spanish galleon 'Santa Isabella'.\n"
            "Suddenly, you spot underwater lights from another diving group—'The Barracudas' are here!\n"
            "They are setting explosives to blast open the locked door to the captain's quarters where the gold is."
        ),
        'act2_q': "What are your underwater actions?",
        'act2_opt1': "1. Quietly cut the wires of their underwater explosive charges using a diving knife.",
        'act2_opt2': "2. Create an underwater diversion: turn off their air valves or tangle their dive lines.",
        'act2_out1': (
            "\nFrank swims carefully to the detonator. His hand is steady.\n"
            "He cuts the red cable of the explosive device! The smugglers try to trigger it,\n"
            "but nothing happens. Confused, they begin searching for the cause."
        ),
        'act2_out2': (
            "\nJoe acts swiftly underwater! He sneaks up from behind and closes the air valves\n"
            "of two divers. Panicking, they gasp for air and are forced to immediately\n"
            "ascend to the surface. However, the gang leader spots you!"
        ),
        'act3_title': "\n--- ACT III: THE UNDERWATER TRAP & JOE'S HARD HEAD ---",
        'act3_text': (
            "You slip into the sunken captain's cabin through a hole in the rotting deck.\n"
            "Amidst the silt and debris stands an iron-bound oak chest filled with gold bars!\n"
            "Suddenly, a strong undercurrent or a foe's shove collapses a heavy oak beam.\n"
            "The timber crashes toward Frank! Joe reacts instantly, shoving his brother aside and taking the blow.\n"
            "The heavy wood strikes Joe directly on his scuba helmet. Joe is knocked out cold.\n\n"
            "A minute later, Joe opens his eyes under his mask, gives an 'OK' sign, and bubbles:\n"
            "— Ouch... Guess Spanish oak is just as tough as my head! (Classic book series trope!)\n"
            "But the situation is critical: the exit is blocked, and your oxygen is running low!"
        ),
        'act3_q': "How will you escape the sunken trap?",
        'act3_opt1': "1. [Joe's Action] Use the ship's old iron rudder post as a lever to lift the heavy debris.",
        'act3_opt2': "2. [Frank's Action] Use a portable high-pressure air blast to blow the jammed lock off the door.",
        'act3_out1_success': (
            "\nJoe gathers all his strength and uses the heavy iron rudder post to lever the timbers!\n"
            "Frank quickly slips through and helps Joe out. You are free with the gold!"
        ),
        'act3_out1_fail': (
            "\nYou try to lift the beam with a lever, but the wood is buried too deep in the silt.\n"
            "The lever snaps, wasting precious air! You must try another way."
        ),
        'act3_out2_success': (
            "\nFrank acts technically: he connects a high-pressure hose to the door's locking mechanism\n"
            "and releases a blast of air. The intense pressure blows the rusty hinges wide open!\n"
            "The exit is clear, and you swim into the open water."
        ),
        'act4_title': "\n--- ACT IV: THE CHASE IN THE MISTY REEFS ---",
        'act4_text': (
            "You surface near your boat, the 'Sleuth', with the rescued treasure.\n"
            "But the leader of 'The Barracudas', nicknamed 'Shark', has already spotted you\n"
            "and speeds on a powerful black boat to intercept. A wild night chase begins among the reefs!\n"
            "The waves rise high, and the enemy tries to ram your hull!"
        ),
        'act4_q': "How will you neutralize the pursuers' boat?",
        'act4_opt1': "1. [Joe's Maneuver] Steer 'Sleuth' directly over 'Siren Reef' shallows so the enemy crashes on the rocks.",
        'act4_opt2': "2. [Frank's Tactics] Throw a floating rope with a marker buoy astern to tangle their propeller.",
        'act4_out1': (
            "\nJoe makes a sharp turn inches away from the jagged rocks! The Barracuda's boat\n"
            "fails to turn and crashes onto the reef with a horrific metal screech, completely disabled.\n"
            "You won!"
        ),
        'act4_out2': (
            "\nFrank drops a strong rope into the wake. The line is instantly sucked under the enemy's hull\n"
            "and tangles their propeller. The engine stalls, leaving them helpless amidst the waves!"
        ),
        'final_header': "                 THE END                     ",
        'final_high': (
            "Congratulations on your victory! Your score: {score} points.\n"
            "You returned the legendary gold to Captain Billy and the Key West Maritime Museum!\n"
            "Tonight, a celebratory feast awaits you on the beach: a grand platter of royal shrimp,\n"
            "roasted lobster, and a huge extra Key Lime Pie just for Chet!\n"
            "Father Fenton Hardy sends a telegram: 'Proud of you, boys. A true professional job!'"
        ),
        'final_normal': (
            "The case is successfully solved! Your score: {score} points.\n"
            "The Spanish treasures are saved, though Joe's helmet now needs major repairs,\n"
            "and Chet almost ate all the prize fish. The Hardy Boys prove their class once again!"
        ),
        'final_thanks': "\nThanks for playing! Frank, Joe, and Chet are always ready for new mysteries!"
    },
    'ru': {
        'select_lang': "Выберите язык / Oберіть мову / Select Language:\n1. Украинский\n2. English\n3. Русский",
        'lang_choice_prompt': "Ваш выбор (1-3): ",
        'press_enter': "Нажмите ENTER, чтобы начать приключение...",
        'invalid_input': "Пожалуйста, введите 1 или 2.",
        'intro_text': (
            "После разгрома синдиката «Дирижер» Фрэнк, Джо и их верный друг Чет Мортон\n"
            "отправляются на заслуженный отдых на солнечный архипелаг Ки-Вест во Флориде.\n"
            "Однако вместо спокойного пляжного отдыха парней ждет новая захватывающая тайна,\n"
            "связанная с затонувшим в XVII веке испанским галеоном «Санта-Изабелла»!"
        ),
        'act1_title': "\n--- АКТ I: ФЛОРИДСКИЙ ПИКНИК И СТАРАЯ ПИАСТРА ---",
        'act1_text': (
            "Вы сидите на открытой веранде уютного прибрежного кафе «Ракушка». Вокруг шумит океан.\n"
            "Перед вами — настоящее кулинарное чудо: тарелка с хрустящими золотистыми фриттерами из моллюсков,\n"
            "традиционный флоридский лаймовый пирог с пышным белковым кремом и стаканы холодного лимонада.\n"
            "Чет Мортон как раз отправляет в рот последний кусочек пирога и довольный жмурится.\n\n"
            "Вдруг к вашему столику подходит пожилой капитан Билли — старый искатель сокровищ с повязкой на глазу.\n"
            "— Ребята, я слышал, вы те самые смышленые братья Харди! — хрипло шепчет он и кладет на стол тяжелую,\n"
            "покрытую кораллами золотую испанскую пиастру. — Мне удалось найти координаты легендарного\n"
            "галеона «Санта-Изабелла», затонувшего в 1682 году. Но за мной следит банда «Баракуда».\n"
            "Они хотят отобрать мою карту! Если я исчезну — сокровища должны достаться миру, а не пиратам!\n\n"
            "В то же мгновение из тумана на причале выбегают двое мужчин в черных гидрокостюмах,\n"
            "вырывают сумку капитана Билли и стремительно скрываются в ночи!"
        ),
        'act1_q': "Что вы решите делать?",
        'act1_opt1': "1. [Путь Фрэнка] Остаться с раненым капитаном Билли, оказать ему первую помощь и исследовать оставленную пиастру на наличие скрытых шифров.",
        'act1_opt2': "2. [Путь Джо] Сразу схватить ключи от гидроциклов на причале и броситься в погоню за лодкой грабителей через мангровые заросли.",
        'act1_out1': (
            "\nВы помогаете капитану Билли подняться. Он благодарен вам и показывает секрет пиастры:\n"
            "на ее ребре есть микроскопические насечки. Фрэнк под лупой выясняет, что это угловые координаты сектора рифа!\n"
            "Благодаря логике и знаниям навигации, Фрэнк точно определяет место затонувшего корабля.\n"
            "Вы берете профессиональное снаряжение для дайвинга, фонари, карту течений и отправляетесь к рифу."
        ),
        'act1_out2': (
            "\nРев двигателя гидроцикла разрезает ночной океан! Джо мчится в темноту.\n"
            "Брызги соленой воды летят в лицо. Вы видите силуэт моторной лодки шпионов впереди.\n"
            "Джо умело лавирует между опасными мангровыми корнями, заставляя грабителей паниковать.\n"
            "Они выбрасывают сумку капитана Билли в воду, пытаясь отвлечь вас. Вы спасаете сумку,\n"
            "но лодка злоумышленников скрывается за поворотом. Внутри сумки — подробная подводная карта рифа!"
        ),
        'act2_title': "\n--- АКТ II: ТАЙНА ЗАТОНУВШЕГО ГАЛЕОНА ---",
        'act2_text': (
            "Ночной океан спокоен, но темен как чернила. Вы погружаетесь под воду с аквалангами.\n"
            "Лучи фонарей выхватывают из бездны удивительные коралловые сады, стаи цветных рыб\n"
            "и величественные останки испанского галеона «Санта-Изабелла», наполовину занесенные песком.\n"
            "Вдруг вы замечаете подводные фонари другой группы водолазов — бандиты «Баракуды» уже здесь!\n"
            "Они готовят взрывчатку, чтобы взорвать заблокированный люк капитанской каюты, где лежит золото."
        ),
        'act2_q': "Каковы ваши действия под водой?",
        'act2_opt1': "1. Попробовать незаметно перерезать провода их подводных взрывных устройств с помощью дайверского ножа.",
        'act2_opt2': "2. Устроить подводную диверсию: выпустить воздух из баллонов врага или запутать их сигнальные тросы.",
        'act2_out1': (
            "\nФрэнк осторожно подплывает к детонатору. Рука детектива не дрогнет.\n"
            "Он аккуратно перерезает красный кабель подводного взрывателя! Преступники пытаются\n"
            "активировать заряд, но ничего не происходит. Они озадачены и начинают искать причину."
        ),
        'act2_out2': (
            "\nДжо стремительно действует под водой! Он тихо подкрадывается сзади и перекрывает вентили баллонов\n"
            "двух аквалангистов. Бандиты начинают задыхаться, панически махать руками и вынуждены срочно\n"
            "всплывать на поверхность для декомпрессии. Однако один из лидеров банды замечает вас!"
        ),
        'act3_title': "\n--- АКТ III: ЛОВУШКА НА ДНЕ И КРЕПКАЯ ГОЛОВА JOE ---",
        'act3_text': (
            "Вы проникаете внутрь затонувшей каюты галеона через пролом в гнилой палубе.\n"
            "Среди ила и обломков возвышается окованный железом дубовый сундук, наполненный золотыми слитками!\n"
            "Вдруг сильное подводное течение или подлый толчок врага обрушивает тяжелую дубовую балку каюты.\n"
            "Балка летит прямо на Фрэнка! Джо молниеносно отталкивает брата, принимая удар на себя.\n"
            "Тяжелое дерево бьет Джо прямо по шлему акваланга. Джо на мгновение теряет сознание, а Фрэнк оттаскивает его.\n\n"
            "Через минуту Джо открывает глаза под маской, показывает жест 'OK' и весело булькает в рацию:\n"
            "— Ох... Кажется, испанский дуб такой же крепкий, как моя голова! (Классический троп книг!)\n"
            "Но ситуация критическая: выход завален, а запасы кислорода в ваших баллонах стремительно иссякают!"
        ),
        'act3_q': "Как вы выберетесь из затонувшей ловушки?",
        'act3_opt1': "1. [Действие Джо] Использовать железный румпель старинного корабля как рычаг, чтобы поднять тяжелую плиту завала.",
        'act3_opt2': "2. [Действие Фрэнка] Использовать портативный баллон высокого давления, чтобы взорвать заклинивший замок двери направленной струей газа.",
        'act3_out1_success': (
            "\nДжо собирает все силы, упирается ногами в шпангоут и с помощью тяжелого румпеля\n"
            "поднимает обломок палубы! Фрэнк быстро проскальзывает в отверстие и помогает выбраться Джо.\n"
            "Вы свободны, а золото в ваших руках!"
        ),
        'act3_out1_fail': (
            "\nВы пытаетесь поднять балку рычагом, но дерево слишком глубоко увязло в иле.\n"
            "Рычаг ломается, а драгоценные минуты и воздух потеряны! Придется искать другой выход."
        ),
        'act3_out2_success': (
            "\nФрэнк действует технично: он подсоединяет шланг высокого давления к замковому механизму двери\n"
            "и резко подает воздух. Мощное давление выбивает ржавые петли старинной двери настежь!\n"
            "Выход свободен, и вы выплываете в открытую воду."
        ),
        'act4_title': "\n--- АКТ IV: ПОГОНЯ В ТУМАННЫХ РИФАХ И ФИНАЛ ---",
        'act4_text': (
            "Вы всплываете на поверхность возле вашего катера «Ищейка» вместе со спасенными сокровищами.\n"
            "Но лидер «Баракуд» по прозвищу «Акула» уже заметил вас и мчится на перехват\n"
            "на мощном черном катере. Начинается безумная ночная погоня среди острых коралловых рифов!\n"
            "Волны вздымаются выше, а враг пытается протаранить ваш борт!"
        ),
        'act4_q': "Как вы нейтрализуете катер преследователей?",
        'act4_opt1': "1. [Маневр Джо] Направить «Ищейку» прямо на опасную мель «Риф Сирен», чтобы враг на полной скорости налетел на острые камни.",
        'act4_opt2': "2. [Тактика Фрэнка] Бросить за корму плавучий трос с сигнальным буем, чтобы он намотался на винт двигателя преследователей.",
        'act4_out1': (
            "\nДжо делает крутой вираж в сантиметрах от острых скал! Катер «Баракуды» не успевает\n"
            "повернуть и с ужасным скрежетом вылетает на рифы, полностью потеряв ход.\n"
            "Вы победили!"
        ),
        'act4_out2': (
            "\nФрэнк молниеносно сбрасывает прочный трос в кильватерный след. Канат мгновенно затягивает\n"
            "под корму вражеского катера и наматывает на винт. Двигатель «Баракуды» глохнет с металлическим стуком,\n"
            "и катер беспомощно останавливается посреди волн!"
        ),
        'final_header': "                 ФИНАЛ                       ",
        'final_high': (
            "Поздравляем с победой! Ваш счет: {score} очков.\n"
            "Вы вернули легендарное золото испанской короны капитану Билли и Морскому музею Ки-Веста!\n"
            "Вечером вас ждет праздничный ужин на берегу океана: большое блюдо с королевскими креветками,\n"
            "запеченный на костре лобстер и огромный дополнительный лаймовый пирог лично для Чета!\n"
            "Отец Фентон Харди присылает поздравительную телеграмму: «Горжусь вами, парни. Настоящая работа профессионалов!»"
        ),
        'final_normal': (
            "Дело успешно завершено! Ваш счет: {score} очок.\n"
            "Испанские сокровища спасены от пиратов, хотя шлем Джо теперь требует ремонта,\n"
            "а Чет почти съел всю призовую рыбу в одиночку. Братья Харди снова доказали свой класс!"
        ),
        'final_thanks': "\nСпасибо за игру! Фрэнк, Джо и Чет всегда готовы к новым детективным приключениям!"
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
            state.inventory.append('diving_knife')
            state.inventory.append('flashlight')
            print_slow(loc['act1_out1'])
            break
        elif choice == '2':
            state.route_taken = 'joe'
            state.score += 15
            state.inventory.append('diving_knife')
            state.inventory.append('flashlight')
            state.inventory.append('map')
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
            state.escaped_stealth = True
            state.score += 25
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
