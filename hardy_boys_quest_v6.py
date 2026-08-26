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
        'uk': "          БРАТИ ХАРДІ ТА ЗАГАДКА ЕКСПРЕСУ-ПРИВИДА             ",
        'en': "      THE HARDY BOYS AND THE MYSTERY OF THE GHOST EXPRESS     ",
        'ru': "          БРАТЬЯ ХАРДИ И ЗАГАДКА ЭКСПРЕССА-ПРИЗРАКА           "
    }
    subtitle_text = {
        'uk': "                 Частина VI: Інтерактивний квест               ",
        'en': "                 Part VI: Interactive Text Quest               ",
        'ru': "                 Часть VI: Интерактивный квест                 "
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
        self.route_taken = None  # 'frank' (archives/blueprints) or 'joe' (dirt bikes)
        self.fell_together = False
        self.score = 0

# Localization dictionary
LOCALIZATION = {
    'uk': {
        'select_lang': "Оберіть мову / Select Language / Выберите язык:\n1. Українська\n2. English\n3. Русский",
        'lang_choice_prompt': "Ваш вибір (1-3): ",
        'press_enter': "Натисніть ENTER, щоб розпочати пригоду...",
        'invalid_input': "Будь ласка, введіть 1 або 2.",
        'intro_text': (
            "Ви граєте за відомих братів-детективів Френка та Джо Харді з містечка Бейпорт.\n"
            "Після успішного розкриття справи у Вовчій Ущелині ви повернулися додому.\n"
            "Але спокій тривав недовго — на вас чекає нова заплутана залізнична таємниця!\n"
            "Разом зі своїм вірним другом Четом Мортоном ви знову вступаєте у гру."
        ),
        'act1_title': "\n--- АКТ I: ОПІВНІЧНІ МЛИНЦІ ТА ЗАБОР ОСТАННЬОГО РЕЙСУ ---",
        'act1_text': (
            "Ви сидите у цілодобовій забігайлівці Бейпорта за кутовим столиком.\n"
            "Перед вами — справжній гастрономічний тріумф: стопка гарячих, повітряних млинців,\n"
            "з яких апетитно стікає бурштиновий кленовий сироп, шматочки хрусткого бекону,\n"
            "що ще шкварчать від жару, та великі чашки густого гарячого шоколаду зі збитими вершками.\n"
            "Чет Мортон із задоволеним зітханням відкушує шматок і раптом нахиляється ближче:\n\n"
            "— Хлопці, ви чули про залізничне депо на околиці міста? Мій дядько працював там.\n"
            "Він розповідав, що у 1952 році броньований поїзд 'Експрес-Привид', який перевозив\n"
            "крупну партію новеньких банкнот Федерального резерву, безслідно зник у заваленому тунелі.\n"
            "А вчора вночі там бачили дивні зелені вогні та чули примарний свисток паровоза!"
        ),
        'act1_q': "Як ви розпочнете розслідування?",
        'act1_opt1': "1. [Вибір Френка] Вирушити до міського архіву, знайти креслення залізниці 1952 року та розрахувати хід колій.",
        'act1_opt2': "2. [Вибір Джо] Стрибнути на кросові мотоцикли та негайно помчати до закинутого депо під покровом темряви.",
        'act1_out1': (
            "\nВи обираєте шлях логіки. Френк проводить кілька годин у порошному архіві.\n"
            "Він знаходить старі креслення і виявляє секретну залізничну гілку, яка не вказана\n"
            "на сучасних картах! Вона веде до прихованого підземного бункера під депо.\n"
            "Ви берете ліхтарик, блокнот і вирушаєте на місце, знаючи точні координати."
        ),
        'act1_out2': (
            "\nРевіння двигунів ваших мотоциклів розриває нічну тишу! Ви обираєте швидкість.\n"
            "Ви мчите вздовж закинутих, порослих травою колій. Чет ледве встигає за вами.\n"
            "Біля старого депо ви дійсно помічаєте зелений спалах у глибині напівзруйнованого тунелю.\n"
            "Зі спорядження у вас лише кишенькові ліхтарики та пара інструментів."
        ),
        'act2_title': "\n--- АКТ II: ЗАКИДАНЕ ДЕПО ТА ПРИХОВАНА КОЛІЯ ---",
        'act2_text': (
            "Похмурі сталеві конструкції закинутого депо височіють на тлі нічного неба.\n"
            "Тут пахне мазутом, іржею та сирістю. Ви заходите всередину головного ангару.\n"
            "Світло ліхтариків вихоплює залізничні колії, що верифікують напрямок у глибину тунелю.\n"
            "Раптом підлога під вашими ногами починає вібрувати, і лунає глухий металевий гуркіт!\n"
            "Здається, десь глибоко під землею працює потужний генератор або навіть двигун поїзда!"
        ),
        'act2_q': "Як пробратися далі в підземелля?",
        'act2_opt1': "1. [Шлях Френка] Використати знайдені креслення, щоб знайти секретний важіль стрілки за старим залізничним семафором.",
        'act2_opt2': "2. [Шлях Джо] Спробувати зламати заіржавілі ворота шахти за допомогою важкого металевого лому.",
        'act2_out1_success': (
            "\nФренк уважно оглядає семафор і знаходить замаскований під кабель іржавий важіль.\n"
            "Ви тягнете за нього разом із Джо. Зі скреготом величезна стіна з цегли відсувається,\n"
            "відкриваючи вхід до таємного освітленого тунелю, де стоїть справжній старий поїзд!"
        ),
        'act2_out2_success': (
            "\nДжо хапає важкий лом і з усієї сили б'є по засуву воріт шахти. З другої спроби\n"
            "іржаве кріплення ламається, і ворота з гуркотом відчиняються! Ви прослизаєте всередину,\n"
            "але гучний звук відлунням розноситься по всьому депо!"
        ),
        'act3_title': "\n--- АКТ III: ПАСТКА У ВАГОНІ ТА МІЦНА ГОЛОВА ---",
        'act3_text': (
            "У підземному тунелі стоїть легендарний броньований експрес 1952 року!\n"
            "Навколо метушаться люди в масках — це банда грабіжників під керівництвом «Залізничника».\n"
            "Вони використовують потужні автогени, намагаючись прорізати товсті сталеві двері сейфу.\n"
            "Ви намагаєтеся підійти ближче, але Джо випадково наступає на старий костиль колії.\n"
            "Раптом з темряви з'являється охоронець і з усієї сили б'є Джо прикладом по голові!\n"
            "Джо падає непритомний. Вас обох швидко затягують у важкий металевий поштовий вагон і замикають.\n\n"
            "За кілька хвилин Джо приходить до тями, трясучи головою:\n"
            "— Ох, мій череп... Наче по ньому проїхав товарняк. Але зате голова на місці! (Класичний троп!)\n"
            "Поїзд раптово здригається і починає рух! Бандити запускають старий локомотив, щоб вивезти сейф!"
        ),
        'act3_q': "Як вибратися з замкненого вагона, що рухається?",
        'act3_opt1': "1. [Шлях Джо] Використати сталевий гак для кріплення пошти, щоб виламати дерев'яне вентиляційне віконце вгорі.",
        'act3_opt2': "2. [Шлях Френка] Використати мідний дріт від зламаного салонного ліхтаря, щоб закоротити контакти електрозамка дверей.",
        'act3_out1_success': (
            "\nДжо чіпляє гак за решітку вікна, упирається ногами в стіну та робить потужний ривок!\n"
            "Решітка вилітає разом із рамою! Ви спритно вилазите на дах вагона, що мчить у темряві тунелю!"
        ),
        'act3_out2_success': (
            "\nФренк акуратно розбирає ліхтар, дістає дріт і з'єднує контакти в панелі біля дверей.\n"
            "Іскри летять в усі боки, і з голосним клацанням магнітний замок дверей відпускає!\n"
            "Двері прочиняються, і ви опиняєтесь у тамбурі поїзда!"
        ),
        'act4_title': "\n--- АКТ IV: ВЕЛИКА ПОГОНЯ НА ШВИДКОСТІ ---",
        'act4_text': (
            "Експрес вилітає з тунелю на стару покинуту колію, що веде до скелястої ущелини.\n"
            "Попереду — зруйнований міст через річку! Бандити планують відчепити вагони перед мостом,\n"
            "а самі втекти на дрезині. Ви повинні зупинити цей безумний заїзд!"
        ),
        'act4_q': "Як ви зупините неуправлінний поїзд?",
        'act4_opt1': "1. [Дія Джо] Пробратися по даху до кабіни машиніста і вступити у відкриту сутичку з ватажком за важіль гальм.",
        'act4_opt2': "2. [Дія Френка] Пробратися до зчіпного механізму між вагонами та вручну від'єднати важкий локомотив від вагонів зі скарбами.",
        'act4_out1': (
            "\nДжо здійснює відважний стрибок у кабіну локомотива! Ватажок банди кидається на нього,\n"
            "але Френк, що підоспів вчасно, допомагає скрутити злочинця. Джо тягне важіль екстреного гальмування!\n"
            "Зі скреготом та іскрами поїзд зупиняється за кілька метрів від обриву мосту!"
        ),
        'act4_out2': (
            "\nФренк спускається до зчіпки. Незважаючи на шалену вібрацію, він за допомогою лома\n"
            "та мотузки вибиває важкий зчіпний палець! Вагони зі скарбами плавно уповільнюються і зупиняються,\n"
            "а локомотив із бандитами летить вперед і застрягає в тупиковому насипу, де їх уже чекає поліція!"
        ),
        'final_header': "                 ФІНАЛ                       ",
        'final_high': (
            "Вітаємо! Ви блискуче завершили чергове розслідування! Ваш рахунок: {score} очок.\n"
            "Легендарний 'Експрес-Привід' повернуто державі, а банда грабіжників за гратами.\n"
            "Шериф Колліг у захваті від вашої роботи і виписує вам офіційну подяку від залізниці.\n"
            "А ввечері вдома Чет Мортон організовує святкову вечерю з великою лазаньєю та домашнім лимонадом.\n"
            "Бейпорт пишається своїми героями!"
        ),
        'final_normal': (
            "Справу успішно завершено! Ваш рахунок: {score} очок.\n"
            "Незважаючи на небезпеку та нову гулю на голові Джо, ви врятували скарби 'Експресу-Привида'.\n"
            "Попереду на братів Харді чекають нові захоплюючі таємниці!"
        ),
        'final_thanks': "\nДякуємо за гру! Френк та Джо завжди готові до нових детективних викликів."
    },
    'en': {
        'select_lang': "Select Language / Оберіть мову / Выберите язык:\n1. Українська\n2. English\n3. Русский",
        'lang_choice_prompt': "Your choice (1-3): ",
        'press_enter': "Press ENTER to start the adventure...",
        'invalid_input': "Please enter 1 or 2.",
        'intro_text': (
            "You are playing as the famous detective brothers, Frank and Joe Hardy from Bayport.\n"
            "After successfully solving the Wolf Ravine mystery, you returned home.\n"
            "But peace didn't last long — a brand new railway mystery awaits you!\n"
            "Together with your best friend Chet Morton, you step into the game once again."
        ),
        'act1_title': "\n--- ACT I: MIDNIGHT PANCAKES & THE GHOST EXPRESS ---",
        'act1_text': (
            "You are sitting in the 24-hour Bayport diner at a corner table.\n"
            "Before you is a true culinary triumph: a stack of hot, fluffy pancakes\n"
            "dripping with amber maple syrup, strips of crispy bacon sizzling with heat,\n"
            "and large mugs of rich hot chocolate topped with whipped cream.\n"
            "Chet Morton bites into a pancake with a satisfied sigh and suddenly leans in closer:\n\n"
            "— Guys, have you heard about the old railway depot on the edge of town? My uncle worked there.\n"
            "He used to tell me about an armored train called the 'Ghost Express' that carried\n"
            "a huge shipment of Federal Reserve bills and vanished without a trace inside a collapsed tunnel in 1952.\n"
            "And last night, people saw strange green lights and heard a ghostly steam whistle there!"
        ),
        'act1_q': "How will you start the investigation?",
        'act1_opt1': "1. [Frank's Choice] Go to the city archives, find the 1952 railway blueprints, and map the tracks.",
        'act1_opt2': "2. [Joe's Choice] Jump on your dirt bikes and rush to the abandoned depot immediately under the cover of night.",
        'act1_out1': (
            "\nYou choose the path of logic. Frank spends hours in the dusty archives.\n"
            "He uncovers old blueprints and finds a secret railway spur that isn't shown on modern maps!\n"
            "It leads to a hidden underground bunker beneath the depot.\n"
            "You grab a flashlight, a notepad, and set off, armed with the exact coordinates."
        ),
        'act1_out2': (
            "\nThe roar of your dirt bike engines shatters the night! You choose speed.\n"
            "You speed along the overgrown, abandoned tracks. Chet barely keeps up with you.\n"
            "Near the old depot, you notice a green flash deep inside the half-collapsed tunnel.\n"
            "Your only gear is pocket flashlights and a few basic tools."
        ),
        'act2_title': "\n--- ACT II: THE ABANDONED DEPOT & THE HIDDEN SPUR ---",
        'act2_text': (
            "The gloomy steel structures of the abandoned depot loom against the night sky.\n"
            "It smells of fuel oil, rust, and dampness. You step inside the main hanger.\n"
            "Your flashlight beams catch rusty rails leading into the darkness of the tunnel.\n"
            "Suddenly, the ground beneath your feet begins to vibrate, and a low metallic rumble echoes!\n"
            "It seems a generator or even a train engine is running deep underground!"
        ),
        'act2_q': "How will you break into the underground tunnel?",
        'act2_opt1': "1. [Frank's Way] Use the blueprints to locate a secret switch concealed behind an old railway semaphore.",
        'act2_opt2': "2. [Joe's Way] Try to smash open the rusty metal hatch using a heavy iron crowbar.",
        'act2_out1_success': (
            "\nFrank inspects the semaphore and finds a rusty lever disguised as a cable.\n"
            "You and Joe pull it together. With a loud screech, a massive brick wall slides open,\n"
            "revealing an illuminated secret tunnel where the old armored train is idling!"
        ),
        'act2_out2_success': (
            "\nJoe grabs the heavy crowbar and smashes the latch with all his might. On the second try,\n"
            "the rusty lock breaks and the hatch doors swing open! You slip inside,\n"
            "but the loud noise echoes throughout the entire depot!"
        ),
        'act3_title': "\n--- ACT III: THE TRAP IN THE CAR & THE HARD HEAD ---",
        'act3_text': (
            "Inside the underground tunnel stands the legendary 1952 armored express!\n"
            "Masked men are active all around it — a gang of thieves led by 'The Railwayman'.\n"
            "They are using heavy blowtorches, attempting to cut through the thick steel vault doors.\n"
            "You try to sneak closer, but Joe accidentally steps on a loose metal tie.\n"
            "Suddenly, a guard appears from the shadows and hits Joe with his rifle butt!\n"
            "Joe falls unconscious. You are both quickly dragged inside a steel mail car and locked up.\n\n"
            "A few minutes later, Joe wakes up, shaking his head:\n"
            "— Ouch, my head... Feels like a freight train rolled over it. But hey, my head is still attached! (Classic trope!)\n"
            "The train suddenly jolts and begins to move! The thieves are starting the old locomotive to escape with the vault!"
        ),
        'act3_q': "How will you escape the locked, moving train car?",
        'act3_opt1': "1. [Joe's Way] Use a steel mail hanging hook as a lever to smash open the wooden ceiling hatch.",
        'act3_opt2': "2. [Frank's Way] Use copper wire from a broken cabin lamp to short-circuit the electric door lock.",
        'act3_out1_success': (
            "\nJoe hooks the grate, braces his feet against the wall, and pulls with everything he's got!\n"
            "The grate breaks loose with the frame! You quickly climb onto the roof of the speeding train!"
        ),
        'act3_out2_success': (
            "\nFrank disassembles the lamp, grabs the wire, and bridges the contacts in the door control panel.\n"
            "Sparks fly everywhere, and with a loud click, the magnetic lock releases!\n"
            "The door slides open, and you step into the gangway!"
        ),
        'act4_title': "\n--- ACT IV: THE HIGH-SPEED CHASE ---",
        'act4_text': (
            "The express bursts out of the tunnel onto an old abandoned track leading to a deep ravine.\n"
            "Ahead is a collapsed bridge over the river! The thieves plan to uncouple the cars before the bridge\n"
            "and escape on a motorized handcar. You must stop this crazy ride!"
        ),
        'act4_q': "How will you stop the runaway train?",
        'act4_opt1': "1. [Joe's Action] Climb over the roof to the locomotive cab and wrestle the leader for the brake valve.",
        'act4_opt2': "2. [Frank's Action] Climb down to the coupling between cars and manually release the heavy engine from the cargo cars.",
        'act4_out1': (
            "\nJoe leaps bravely into the locomotive cab! The gang leader lunges at him,\n"
            "but Frank arrives just in time to help subdue him. Joe pulls the emergency brake valve!\n"
            "With screams and sparks flying, the train screeches to a halt just yards from the bridge gap!"
        ),
        'act4_out2': (
            "\nFrank climbs down to the coupling. Despite the wild vibration, he uses a metal bar\n"
            "to knock out the heavy coupling pin! The cargo cars slowly drift to a safe halt,\n"
            "while the locomotive carrying the thieves barrels ahead and gets stuck in a dead-end buffer where the police are waiting!"
        ),
        'final_header': "                THE END                      ",
        'final_high': (
            "Congratulations! You solved the case brilliantly! Your score: {score} points.\n"
            "The legendary 'Ghost Express' is recovered, and the thieves are behind bars.\n"
            "Sheriff Collig is thrilled with your work and issues an official commendation from the railway.\n"
            "In the evening, Chet Morton prepares a celebratory dinner with deep-dish lasagna and homemade lemonade.\n"
            "Bayport is proud of its heroes!"
        ),
        'final_normal': (
            "The case is closed! Your score: {score} points.\n"
            "Despite the danger and the fresh bump on Joe's head, you saved the 'Ghost Express' treasure.\n"
            "More exciting mysteries await the Hardy Boys in the future!"
        ),
        'final_thanks': "\nThanks for playing! Frank and Joe are always ready for new detective challenges."
    },
    'ru': {
        'select_lang': "Выберите язык / Oберіть мову / Select Language:\n1. Текст на украинском\n2. English\n3. Русский",
        'lang_choice_prompt': "Ваш выбор (1-3): ",
        'press_enter': "Нажмите ENTER, чтобы начать приключение...",
        'invalid_input': "Пожалуйста, введите 1 или 2.",
        'intro_text': (
            "Вы играете за известных братьев-детективов Фрэнка и Джо Харди из городка Бейпорт.\n"
            "После успешного раскрытия дела в Волчьем Ущелье вы вернулись домой.\n"
            "Но покой длился недолго — вас ждет новая запутанная железнодорожная тайна!\n"
            "Вместе со своим верным другом Четом Мортоном вы снова вступаете в игру."
        ),
        'act1_title': "\n--- АКТ I: ПОЛУНОЧНЫЕ БЛИНЫ И СЕКРЕТ ПОСЛЕДНЕГО РЕЙСА ---",
        'act1_text': (
            "Вы сидите в круглосуточной забегаловке Бейпорта за угловым столиком.\n"
            "Перед вами — настоящий гастрономический триумф: стопка горячих, пышных блинов,\n"
            "с которых аппетитно стекает янтарный кленовый сироп, кусочки хрустящего бекона,\n"
            "еще шкворчащие от жара, и большие чашки густого горячего шоколада со взбитыми сливками.\n"
            "Чет Мортон с довольным вздохом откусывает кусок и вдруг наклоняется ближе:\n\n"
            "— Ребята, вы слышали про старое депо на окраине города? Мой дядя работал там.\n"
            "Он рассказывал, что в 1952 году бронированный поезд 'Экспресс-Призрак', перевозивший\n"
            "крупную партию новеньких банкнот Федерального резерва, бесследно исчез в заваленном туннеле.\n"
            "А вчера ночью там видели странные зеленые огни и слышали призрачный гудок паровоза!"
        ),
        'act1_q': "Как вы начнете расследование?",
        'act1_opt1': "1. [Выбор Фрэнка] Отправиться в городской архив, найти чертежи железной дороги 1952 года и рассчитать ход путей.",
        'act1_opt2': "2. [Выбор Джо] Запрыгнуть на кроссовые мотоциклы и немедленно помчаться к заброшенному депо под покровом темноты.",
        'act1_out1': (
            "\nВы выбираете путь логики. Фрэнк проводит несколько часов в пыльном архиве.\n"
            "Он находит старые чертежи и обнаруживает секретную железнодорожную ветку, которая не указана\n"
            "на современных картах! Она ведет к скрытому подземному бункеру под депо.\n"
            "Вы берете фонарик, блокнот и отправляетесь на место, зная точные координаты."
        ),
        'act1_out2': (
            "\nРев двигателей ваших мотоциклов разрывает ночную тишину! Вы выбираете скорость.\n"
            "Вы мчитесь вдоль заброшенных, поросших травой путей. Чет едва успевает за вами.\n"
            "У старого депо вы действительно замечаете зеленую вспышку в глубине полуразрушенного туннеля.\n"
            "Из снаряжения у вас только карманные фонарики и пара инструментов."
        ),
        'act2_title': "\n--- АКТ II: ЗАБРОШЕННОЕ ДЕПО И СКРЫТЫЙ ПУТЬ ---",
        'act2_text': (
            "Мрачные стальные конструкции заброшенного депо возвышаются на фоне ночного неба.\n"
            "Здесь пахнет мазутом, ржавчиной и сыростью. Вы заходите внутрь главного ангара.\n"
            "Свет фонариков выхватывает рельсы, ведущие в глубину туннеля.\n"
            "Вдруг пол под вашими ногами начинает вибрировать, и раздается глухой металлический грохот!\n"
            "Похоже, где-то глубоко под землей работает мощный генератор или даже двигатель поезда!"
        ),
        'act2_q': "Как пробраться дальше в подземелье?",
        'act2_opt1': "1. [Путь Фрэнка] Использовать найденные чертежи, чтобы найти секретный рычаг стрелки за старым семафором.",
        'act2_opt2': "2. [Путь Джо] Попробовать сломать заржавевшие ворота шахты с помощью тяжелого металлического лома.",
        'act2_out1_success': (
            "\nФрэнк внимательно осматривает семафор и находит замаскированный под кабель ржавый рычаг.\n"
            "Вы тянете за него вместе с Джо. Со скрежетом огромная кирпичная стена отодвигается,\n"
            "открывая вход в тайный туннель, где стоит настоящий старый поезд!"
        ),
        'act2_out2_success': (
            "\nДжо хватает тяжелый лом и со всей силы бьет по засову ворот шахты. Со второй попытки\n"
            "ржавое крепление ломается, и ворота с грохотом распахиваются! Вы проскальзываете внутрь,\n"
            "но громкий звук эхом разносится по всему депо!"
        ),
        'act3_title': "\n--- АКТ III: ЛОВУШКА В ВАГОНЕ И КРЕПКАЯ ГОЛОВА ---",
        'act3_text': (
            "В подземном туннеле стоит легендарный бронированный экспресс 1952 года!\n"
            "Вокруг суетятся люди в масках — это банда грабителей под руководством «Железнодорожника».\n"
            "Они используют мощные автогены, пытаясь прорезать толстую стальную дверь сейфа.\n"
            "Вы пытаетесь подойти ближе, но Джо случайно наступает на старый костыль пути.\n"
            "Вдруг из темноты появляется охранник и со всей силы бьет Джо прикладом по голове!\n"
            "Джо падает без чувств. Вас обоих быстро затаскивают в тяжелый металлический почтовый вагон и запирают.\n\n"
            "Через несколько минут Джо приходит в себя, тряся головой:\n"
            "— Ох, мой череп... Как будто по нему товарняк проехал. Но зато голова на месте! (Классический троп!)\n"
            "Поезд внезапно вздрагивает и начинает движение! Бандиты запускают старый локомотив, чтобы вывезти сейф!"
        ),
        'act3_q': "Как выбраться из запертого движущегося вагона?",
        'act3_opt1': "1. [Путь Джо] Использовать стальной почтовый крюк, чтобы выломать деревянное вентиляционное окошко вверху.",
        'act3_opt2': "2. [Путь Фрэнка] Использовать медную проволоку от сломанного салонного фонаря, чтобы закоротить контакты электрозамка двери.",
        'act3_out1_success': (
            "\nДжо цепляет крюк за решетку окна, упирается ногами в стену и делает мощный рывок!\n"
            "Решетка вылетает вместе с рамой! Вы ловко выбираетесь на крышу вагона, мчащегося в темноте туннеля!"
        ),
        'act3_out2_success': (
            "\nФрэнк аккуратно разбирает фонарь, достает проволоку и соединяет контакты в панели у двери.\n"
            "Искры летят во все стороны, и с громким щелчком магнитный замок двери отпускает!\n"
            "Дверь приоткрывается, и вы оказываетесь в тамбуре поезда!"
        ),
        'act4_title': "\n--- АКТ IV: ВЕЛИКАЯ ПОГОНЯ НА СКОРОСТИ ---",
        'act4_text': (
            "Экспресс вылетает из туннеля на старый заброшенный путь, ведущий к скалистому ущелью.\n"
            "Впереди — разрушенный мост через реку! Бандиты планируют отцепить вагоны перед мостом,\n"
            "а сами сбежать на дрезине. Вы должны остановить этот безумный заезд!"
        ),
        'act4_q': "Как вы остановите неуправляемый поезд?",
        'act4_opt1': "1. [Действие Джо] Пробраться по крыше в кабину машиниста и вступить в открытую схватку с главарем за рычаг тормозов.",
        'act4_opt2': "2. [Действие Фрэнка] Пробраться к сцепному механизму между вагонами и вручную отсоединить тяжелый локомотив от вагонов сокровищами.",
        'act4_out1': (
            "\nДжо совершает отважный прыжок в кабину локомотива! Главарь банды бросается на него,\n"
            "но вовремя подоспевший Фрэнк помогает скрутить преступника. Джо тянет рычаг экстренного торможения!\n"
            "Со скрежетом и искрами поезд останавливается в нескольких метрах от обрыва моста!"
        ),
        'act4_out2': (
            "\nФрэнк спускается к сцепке. Несмотря на безумную вибрацию, он с помощью лома\n"
            "и веревки выбивает тяжелый сцепной палец! Вагоны с сокровищами плавно замедляются и останавливаются,\n"
            "а локомотив с бандитами летит вперед и застревает в тупиковой насыпи, где их уже ждет полиция!"
        ),
        'final_header': "                 ФИНАЛ                       ",
        'final_high': (
            "Поздравляем! Вы блестяще завершили очередное расследование! Ваш счет: {score} очков.\n"
            "Легендарный 'Экспресс-Призрак' возвращен государству, а банда грабителей за решеткой.\n"
            "Шериф Коллиг в восторге от вашей работы и выписывает вам официальную благодарность от железной дороги.\n"
            "А вечером дома Чет Мортон организует праздничный ужин с большой лазаньей и домашним лимонадом.\n"
            "Бейпорт гордится своими героями!"
        ),
        'final_normal': (
            "Дело успешно завершено! Ваш счет: {score} очков.\n"
            "Несмотря на опасность и новую шишку на голове Джо, вы спасли сокровища 'Экспресса-Призрака'.\n"
            "Впереди братьев Харди ждут новые захватывающие тайны!"
        ),
        'final_thanks': "\nСпасибо за игру! Фрэнк и Джо всегда готовы к новым детективным вызовам."
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
        choice = input(loc.get('act1_choice_prompt', '\n-> ')).strip()
        
        if choice == '1':
            state.route_taken = 'frank'
            state.score += 20
            state.inventory.append('blueprints')
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
    
    while True:
        print("\n" + loc['act2_q'])
        print(loc['act2_opt1'])
        print(loc['act2_opt2'])
        choice = input(loc.get('act1_choice_prompt', '\n-> ')).strip()
        
        if choice == '1':
            if state.route_taken == 'frank':
                state.score += 25
                print_slow(loc['act2_out1_success'])
                break
            else:
                # If they took Joe's route but try Frank's method, they don't have blueprints!
                if state.lang == 'uk':
                    print_slow("\nУ вас немає креслень, щоб знайти секретний важіль! Спробуйте інший варіант.")
                elif state.lang == 'en':
                    print_slow("\nYou don't have the blueprints to find the secret lever! Try another option.")
                else:
                    print_slow("\nУ вас нет чертежей, чтобы найти секретный рычаг! Попробуйте другой вариант.")
                continue
        elif choice == '2':
            state.score += 15
            print_slow(loc['act2_out2_success'])
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
        choice = input(loc.get('act1_choice_prompt', '\n-> ')).strip()
        
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
        choice = input(loc.get('act1_choice_prompt', '\n-> ')).strip()
        
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
