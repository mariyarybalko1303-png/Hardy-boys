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
        'uk': "          БРАТИ ХАРДІ ТА ТАЄМНИЦЯ ЗАЛІЗНОГО БУНКЕРА (ЧАСТИНА XII)          ",
        'en': "      THE HARDY BOYS AND THE IRON BUNKER MYSTERY (PART XII)       ",
        'ru': "          БРАТЬЯ ХАРДИ И ТАЙНА ЖЕЛЕЗНОГО БУНКЕРА (ЧАСТЬ XII)          "
    }
    subtitle_text = {
        'uk': "          Спільна операція з Фентоном Харді: Інтерактивний квест          ",
        'en': "          Joint Operation with Fenton Hardy: Interactive Quest             ",
        'ru': "          Совместная операция с Фентоном Харди: Интерактивный квест        "
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
        self.route_taken = None  # 'frank' (decode/intel) or 'joe' (action/bikes)
        self.bypassed_lasers = False
        self.score = 0

# Localization dictionary containing Ukrainian, English, and Russian translations
LOCALIZATION = {
    'uk': {
        'select_lang': "Оберіть мову / Select Language / Выберите язык:\n1. Українська\n2. English\n3. Русский",
        'lang_choice_prompt': "Ваш вибір (1-3): ",
        'press_enter': "Натисніть ENTER, щоб розпочати пригоду...",
        'invalid_input': "Будь ласка, введіть 1 або 2.",
        'intro_text': (
            "Ви граєте за відомих братів-детективів Френка та Джо Харді.\n"
            "Сьогодні особливий день! У цьому розслідуванні ви працюєте не самі.\n"
            "Ваш батько, легендарний приватний детектив Фентон Харді, особисто бере участь у справі!\n"
            "Разом ви вирушаєте штурмувати секретне лігво міжнародного синдикату."
        ),
        'act1_title': "\n--- АКТ I: ВЕЛИКИЙ СНІДАНОК ТА ПЛАН БАТЬКА ---",
        'act1_text': (
            "Ранок у будинку Харді починається з неймовірних ароматів.\n"
            "Тітка Гертруда перевершила себе: на столі стоїть гора золотистих пухких млинців,\n"
            "щедро поливаних кленовим сиропом, тарілка з хрусткими гарячими сосисками, пишна яєчня з зеленню\n"
            "та глечик холодного апельсинового соку. Чет Мортон уже уминає п'ятий млинець, запевняючи,\n"
            "що детективна робота вимагає колосальних вуглеводів.\n\n"
            "Раптом двері кабінету відчиняються, і входить Фентон Харді в своєму класичному плащі.\n"
            "Він кладе на стіл залізний кейс:\n"
            "— Хлопці, відкладіть виделки. Нам пора в дорогу. Мої джерела підтвердили, що ватажок синдикату,\n"
            "відомий як «Генерал», ховається в підземному високотехнологічному бункері в Залізних Пагорбах.\n"
            "Він збирається продати вкрадені урядові коди. Ми виїжджаємо негайно, і цього разу я йду з вами!"
        ),
        'act1_q': "Як ви підійдете до периметра бункера в Залізних Пагорбах?",
        'act1_opt1': "1. [Спільний план Френка та батька] Використати портативний дешифратор для зламу частоти прожекторів охорони та тихо пройти через ворота.",
        'act1_opt2': "2. [Спільний план Джо та батька] Використати димові шашки та здійснити стрімкий прорив на кросових мотоциклах прямо через огорожу.",
        'act1_out1': (
            "\nФренк та Фентон Харді підключають дешифратор до розподільного щитка.\n"
            "Завдяки блискучим знанням електроніки, ви перехоплюєте керування турелями спостереження.\n"
            "Автоматичні прожектори гаснуть саме тоді, коли ви перелазите через огорожу!\n"
            "Ви берете із собою лазерний різак, ліхтарик і безшумно проникаєте до бункера."
        ),
        'act1_out2': (
            "\nДжо з ревом заводить свій кросовий мотоцикл! Фентон посміхається і кидає димову шашку.\n"
            "Густий білий дим застилає весь двір. Ви на шаленій швидкості прориваєтесь крізь огорожу,\n"
            "залишаючи розгублену охорону кашляти в диму! Ви прибуваєте до входу безпосередньо на колесах.\n"
            "З речей у вас є лише ліхтарики, мотузка з гаком та набір інструментів Джо."
        ),
        'act2_title': "\n--- АКТ II: СТАЛЕВИЙ ЛАБІРИНТ ---",
        'act2_text': (
            "Ви опиняєтесь у коридорах підземного бункера. Стіни зроблені з товстої броньованої сталі.\n"
            "Попереду — герметичні двері до серверної, але прохід перекривають смертоносні лазерні промені.\n"
            "Найменший дотик до червоного світла запустить систему самознищення бази.\n"
            "Фентон Харді уважно оглядає стіни:"
        ),
        'act2_q': "Як ви подолаєте лазерну перешкоду?",
        'act2_opt1': "1. [Рішення Френка] Використати дзеркальні осколки для заломлення лазерних променів і перенаправлення їх на власні фотоелементи.",
        'act2_opt2': "2. [Рішення Джо] Використати важкий металевий візок для вантажів, щоб заблокувати випромінювачі та прослизнути під ними.",
        'act2_out1_success': (
            "\nФренк акуратно дістає невелике кишенькове дзеркальце і розділяє його на кілька частин.\n"
            "Разом із батьком ви закріплюєте осколки на стінах під точним кутом.\n"
            "Промені заломлюються, замикають датчики, і лазерна сітка з тихим гудінням зникає!\n"
            "Шлях вільний без жодного ризику!"
        ),
        'act2_out2_success': (
            "\nДжо хапає масивний сталевий візок, який стояв поруч.\n"
            "Разом із батьком ви штовхаєте його вперед. Візок застрягає між променями, блокуючи головні випромінювачі.\n"
            "Ви швидко ковзаєте по підлозі під візком один за одним і опиняєтесь на іншій стороні!\n"
            "Проте спрацьовує тиха тривога, і залізні гермодвері за вашими спинами зачиняються!"
        ),
        'act3_title': "\n--- АКТ III: ПАСТКА ДЛЯ ХАРДІ ТА МІЦНА ГОЛОВА ---",
        'act3_text': (
            "Ви входите до головної зали управління, але це виявляється пасткою!\n"
            "На великому екрані з'являється обличчя «Генерала»:\n"
            "— Ласкаво просимо, родина Харді! Ви запізнилися. Мої люди вже завантажують коди.\n\n"
            "Раптом важка залізна консоль, підвішена до стелі, зривається з кріплень і летить на Фентона!\n"
            "Джо блискавично реагує, відштовхує батька вбік, але сам отримує сильний удар сталевим кутом по голові!\n"
            "Джо падає без тями. Вас негайно замикають у залізній камері з вакуумними дверима.\n"
            "За кілька хвилин Джо приходить до тями, тримаючись за потилицю:\n"
            "— Ох, тату... Френку... Здається, на мою голову впав цілий ковадло. Але не хвилюйтеся,\n"
            "ви ж знаєте — у мене міцна голова! Бувало й гірше! (Класичний троп серії книг!)\n"
            "Раптом з вентиляції починає виходити зелений сонний газ. Потрібно діяти негайно!"
        ),
        'act3_q': "Як ви виберетесь із заблокованої залізної камери?",
        'act3_opt1': "1. [Технологія Френка] Використати лазерний різак (якщо ви обрали шлях Френка) або зламати замок за допомогою дешифратора.",
        'act3_opt2': "2. [Винахідливість батька та сила Джо] Використати газовий балон із вогнегасника як важіль та вибити решітку витяжки.",
        'act3_out1_success': (
            "\nФренк дістає свій лазерний різак (або дешифратор) і починає акуратно плавити електронну плату дверей.\n"
            "Іскри летять в усі боки! Фентон допомагає утримувати провідники.\n"
            "Клац! Магнітний замок вимикається, і важкі залізні двері відчиняються!"
        ),
        'act3_out1_fail': (
            "\nВи намагаєтесь зламати замок простим інструментом, але мікросхема надійно захищена бронею.\n"
            "Сонний газ швидко заповнює кімнату, у вас починає паморочитися в голові!\n"
            "Потрібно терміново спробувати силове рішення батька!"
        ),
        'act3_out2_success': (
            "\nФентон швидко зриває вогнегасник зі стіни. Джо, попри біль у голові, хапає його,\n"
            "вставляє металевий розтруб між прутами вентиляційної решітки та натискає як важіль.\n"
            "Завдяки неймовірній силі та досвіду батька, решітка вилітає з кріплень із гуркотом!\n"
            "Ви швидко вибираєтесь через шахту вентиляції на волю!"
        ),
        'act4_title': "\n--- АКТ IV: ОСТАННІЙ РУБІЖ ---",
        'act4_text': (
            "Ви вибігаєте до підземного ангару. «Генерал» уже застрибує в кабіну свого броньованого всюдихода,\n"
            "готовий прорватися через тунель і втекти.\n"
            "Потужний дизельний двигун реве на весь ангар, піднімаючи хмари пилу.\n"
            "Фентон Харді кричить:\n"
            "— Френку, Джо, ми повинні заблокувати вихідні ворота ангару, інакше він втече!"
        ),
        'act4_q': "Як ви зупините всюдихід «Генерала»?",
        'act4_opt1': "1. [План Джо та батька] Стрибнути на підйомний кран ангару, щоб опустити важкий сталевий контейнер прямо перед всюдиходом.",
        'act4_opt2': "2. [План Френка та батька] Швидко перепрограмувати гідравлічні ворота тунелю, заблокувавши виїзд сталевою плитою.",
        'act4_out1': (
            "\nДжо за підтримки батька спритно видирається по драбині на платформу крана.\n"
            "Він смикає за важіль, і гігантський контейнер з гуркотом падає на підлогу за метр від капота всюдихода!\n"
            "«Генерал» різко тисне на гальма. Фентон та Френк миттєво відчиняють двері кабіни та затримують лиходія!\n"
            "Успіх!"
        ),
        'act4_out2': (
            "\nФренк підбігає до головного пульта ангару, а батько диктує йому аварійні коди перекриття.\n"
            "Пальці Френка блискавично літають по клавіатурі.\n"
            "За секунду до виїзду всюдихода гігантська гідравлічна плита опускається вниз, перекриваючи тунель!\n"
            "Всюдихід врізається в неї на гальмах. Ви затискаєте «Генерала» в пастку!"
        ),
        'final_header': "                 ФІНАЛ                       ",
        'final_high': (
            "Вітаємо! Ви блискуче виконали місію разом із батьком! Ваш рахунок: {score} очок.\n"
            "Синдикат «Генерала» повністю знищено, урядові коди повернуто в безпеку.\n"
            "Фентон Харді з гордістю плескає вас по плечах:\n"
            "— Хлопці, ви дієте як справжні професіонали. Я пишаюся тим, що ви мої сини!\n"
            "Увечері вдома тітка Гертруда влаштовує грандіозний святковий обід із запеченим м'ясним рулетом,\n"
            "а Чет Мортон уже доїдає другу порцію картопляного пюре та підморгує вам!"
        ),
        'final_normal': (
            "Місію успішно завершено! Ваш рахунок: {score} очок.\n"
            "Хоча розслідування було небезпечним, а потилиця Джо знову прикрашена великою гулею,\n"
            "команда родини Харді довела, що перед їхньою спільною силою не встоїть жоден синдикат!\n"
            "Фентон Харді тисне вам руки — Бейпорт знову під надійним захистом!"
        ),
        'final_thanks': "\nДякуємо за гру! Родина Харді пишається вашим детективним талантом."
    },
    'en': {
        'select_lang': "Select Language / Оберіть мову / Выберите язык:\n1. Українська\n2. English\n3. Русский",
        'lang_choice_prompt': "Your choice (1-3): ",
        'press_enter': "Press ENTER to start the adventure...",
        'invalid_input': "Please enter 1 or 2.",
        'intro_text': (
            "You are playing as the famous detective brothers, Frank and Joe Hardy.\n"
            "Today is a very special day! In this investigation, you are not working alone.\n"
            "Your father, the legendary private investigator Fenton Hardy, is personally in the field!\n"
            "Together, you set off to raid the secret base of an international syndicate."
        ),
        'act1_title': "\n--- ACT I: THE BIG BREAKFAST & FATHER'S PLAN ---",
        'act1_text': (
            "Morning at the Hardy home begins with incredible aromas.\n"
            "Aunt Gertrude has outdone herself: on the table is a mountain of golden fluffy pancakes\n"
            "generously drizzled with maple syrup, a plate of crispy hot sausages, scrambled eggs with herbs,\n"
            "and a pitcher of cold orange juice. Chet Morton is already devouring his fifth pancake,\n"
            "claiming that detective work requires massive amounts of carbohydrates.\n\n"
            "Suddenly, the study door opens, and Fenton Hardy enters in his classic trench coat.\n"
            "He places a steel briefcase on the table:\n"
            "— Boys, put down your forks. It's time to hit the road. My sources confirmed that the syndicate leader,\n"
            "known as 'The General', is hiding in a high-tech underground bunker in the Iron Hills.\n"
            "He is about to sell stolen government codes. We leave immediately, and this time I'm going with you!"
        ),
        'act1_q': "How will you approach the bunker perimeter in the Iron Hills?",
        'act1_opt1': "1. [Frank & Father's Plan] Use a portable decoder to hack the security spotlight frequency and slip through the gates quietly.",
        'act1_opt2': "2. [Joe & Father's Plan] Use smoke bombs and make a rapid break on dirt bikes directly through the fence.",
        'act1_out1': (
            "\nFrank and Fenton Hardy connect the decoder to the power junction box.\n"
            "Thanks to brilliant electronic skills, you hijack the security cameras and turrets.\n"
            "The automated spotlights turn off exactly as you scale the fence!\n"
            "You take a laser cutter, a flashlight, and slip into the bunker silently."
        ),
        'act1_out2': (
            "\nJoe revs his dirt bike engine! Fenton smiles and throws a smoke grenade.\n"
            "Thick white smoke blankets the entire yard. You burst through the fence at high speed,\n"
            "leaving the confused guards coughing in the smoke! You arrive at the entrance on wheels.\n"
            "The only gear you have with you are flashlights, a rope with a grapple, and Joe's tool kit."
        ),
        'act2_title': "\n--- ACT II: THE STEEL LABYRINTH ---",
        'act2_text': (
            "You find yourselves in the corridors of the underground bunker. The walls are made of thick steel.\n"
            "Ahead is a hermetic door to the server room, but the corridor is blocked by deadly laser beams.\n"
            "The slightest touch of the red light will trigger the base self-destruction system.\n"
            "Fenton Hardy carefully examines the walls:"
        ),
        'act2_q': "How will you bypass the laser obstacle?",
        'act2_opt1': "1. [Frank's Solution] Use mirror shards to refract the laser beams and redirect them back to their photosensors.",
        'act2_opt2': "2. [Joe's Solution] Use a heavy metal transport cart to block the emitters and slide under them.",
        'act2_out1_success': (
            "\nFrank carefully pulls out a small pocket mirror and splits it into several pieces.\n"
            "Together with your father, you secure the shards on the walls at a precise angle.\n"
            "The beams refract, shorting the sensors, and the laser grid vanishes with a soft hum!\n"
            "The path is clear without any risk!"
        ),
        'act2_out2_success': (
            "\nJoe grabs a massive steel cart that was standing nearby.\n"
            "Together with your father, you push it forward. The cart jams between the beams, blocking the main emitters.\n"
            "You quickly slide along the floor under the cart one after another and find yourselves on the other side!\n"
            "However, a silent alarm is tripped, and the steel hermetic doors close behind you!"
        ),
        'act3_title': "\n--- ACT III: THE HARDY TRAP & THE HARD HEAD ---",
        'act3_text': (
            "You enter the main control room, but it turns out to be a trap!\n"
            "The General's face appears on a large screen:\n"
            "— Welcome, Hardy family! You are too late. My men are already uploading the codes.\n\n"
            "Suddenly, a heavy iron console suspended from the ceiling snaps and falls toward Fenton!\n"
            "Joe reacts lightning-fast, pushes his father aside, but gets hit hard on the head by the steel console!\n"
            "Joe falls unconscious. You are immediately locked in a steel cell with vacuum doors.\n"
            "A few minutes later, Joe wakes up, rubbing the back of his head:\n"
            "— Ouch, Dad... Frank... Feels like an anvil fell on my head. But don't worry,\n"
            "you know me — I have a hard head! I've had worse! (Classic book series trope!)\n"
            "Suddenly, green sleeping gas begins to hiss from the ventilation. You must act now!"
        ),
        'act3_q': "How will you escape the locked steel cell?",
        'act3_opt1': "1. [Frank's Tech] Use the laser cutter (if you chose Frank's path) or bypass the lock with the decoder.",
        'act3_opt2': "2. [Father's Wit & Joe's Strength] Use the fire extinguisher gas cylinder as a lever to pry open the exhaust grate.",
        'act3_out1_success': (
            "\nFrank gets his laser cutter (or decoder) and begins to carefully melt the door's electronic board.\n"
            "Sparks fly everywhere! Fenton helps hold the wires.\n"
            "Click! The magnetic lock deactivates, and the heavy steel door swings open!"
        ),
        'act3_out1_fail': (
            "\nYou try to pick the lock with a simple tool, but the chip is heavily armored.\n"
            "The sleeping gas is rapidly filling the room, making your head spin!\n"
            "You must quickly try your father's brute force solution!"
        ),
        'act3_out2_success': (
            "\nFenton quickly rips a fire extinguisher off the wall. Joe, despite his head pain, grabs it,\n"
            "jams the metal nozzle between the bars of the ventilation grate, and presses it as a lever.\n"
            "Thanks to incredible strength and father's leverage, the grate bursts off the wall with a crash!\n"
            "You quickly climb out through the ventilation shaft to freedom!"
        ),
        'act4_title': "\n--- ACT IV: THE FINAL FRONTIER ---",
        'act4_text': (
            "You run out into the underground hangar. The General is already jumping into his armored SUV,\n"
            "ready to blast through the exit tunnel and escape.\n"
            "The powerful diesel engine roars through the hangar, kicking up clouds of dust.\n"
            "Fenton Hardy shouts:\n"
            "— Frank, Joe, we must block the main hangar doors, or he'll get away!"
        ),
        'act4_q': "How will you stop The General's SUV?",
        'act4_opt1': "1. [Joe & Father's Plan] Jump onto the hangar crane to drop a heavy steel container right in front of the SUV.",
        'act4_opt2': "2. [Frank & Father's Plan] Quickly reprogram the hydraulic tunnel gates to block the exit with a steel plate.",
        'act4_out1': (
            "\nJoe, supported by his father, quickly climbs the ladder to the crane controls.\n"
            "He pulls the lever, and a giant container crashes onto the floor just a yard from the SUV's hood!\n"
            "The General slams on the brakes. Fenton and Frank immediately open the cabin doors and subdue the villain!\n"
            "Success!"
        ),
        'act4_out2': (
            "\nFrank runs to the main hangar console while father dictates the emergency override codes.\n"
            "Frank's fingers fly across the keyboard.\n"
            "A split second before the SUV exits, a giant hydraulic plate slams down, blocking the tunnel!\n"
            "The SUV crashes into it on brakes. You trap The General!"
        ),
        'final_header': "                 THE END                     ",
        'final_high': (
            "Congratulations! You solved the mission brilliantly with your father! Your score: {score} points.\n"
            "The General's syndicate is completely destroyed, and the government codes are returned to safety.\n"
            "Fenton Hardy proudly pats your shoulders:\n"
            "— Boys, you act like real professionals. I am proud to have you as my sons!\n"
            "In the evening at home, Aunt Gertrude hosts a grand celebratory dinner with a baked meatloaf,\n"
            "and Chet Morton is already eating his second portion of mashed potatoes, giving you a wink!"
        ),
        'final_normal': (
            "Mission successfully completed! Your score: {score} points.\n"
            "Although the investigation was dangerous, and Joe's head is decorated with a massive bump,\n"
            "the Hardy family team proved that no syndicate can stand against their combined power!\n"
            "Fenton Hardy shakes your hands — Bayport is safe once more!"
        ),
        'final_thanks': "\nThanks for playing! The Hardy family is proud of your detective skills."
    },
    'ru': {
        'select_lang': "Выберите язык / Oберіть мову / Select Language:\n1. Русский\n2. English\n3. Українська",
        'lang_choice_prompt': "Ваш выбор (1-3): ",
        'press_enter': "Нажмите ENTER, чтобы начать приключение...",
        'invalid_input': "Пожалуйста, введите 1 или 2.",
        'intro_text': (
            "Вы играете за известных братьев-детективов Фрэнка и Джо Харди.\n"
            "Сегодня особенный день! В этом расследовании вы работаете не одни.\n"
            "Ваш отец, легендарный частный детектив Фентон Харди, лично участвует в деле!\n"
            "Вместе вы отправляетесь на штурм секретного логова международного синдиката."
        ),
        'act1_title': "\n--- АКТ I: ВЕЛИКИЙ ЗАВТРАК И ПЛАН ОТЦА ---",
        'act1_text': (
            "Утро в доме Харди начинается с невероятных ароматов.\n"
            "Тетя Гертруда превзошла себя: на столе стоит гора золотистых пышных блинов,\n"
            "щедро политых кленовым сиропом, тарелка с хрустящими горячими сосисками, пышная яичница с зеленью\n"
            "и кувшин холодного апельсинового сока. Чет Мортон уже уминает пятый блин, уверяя,\n"
            "что детективная работа требует колоссальных углеводов.\n\n"
            "Вдруг дверь кабинета открывается, и входит Фентон Харди в своем классическом плаще.\n"
            "Он кладет на стол железный кейс:\n"
            "— Ребята, отложите вилки. Нам пора в дорогу. Мои источники подтвердили, что главарь синдиката,\n"
            "известный как «Генерал», скрывается в подземном высокотехнологичном бункере в Железных Холмах.\n"
            "Он собирается продать украденные правительственные коды. Мы выезжаем немедленно, и в этот раз я иду с вами!"
        ),
        'act1_q': "Как вы подойдете к периметру бункера в Железных Холмах?",
        'act1_opt1': "1. [Совместный план Фрэнка и отца] Использовать портативный дешифратор для взлома частоты прожекторов охраны и тихо пройти через ворота.",
        'act1_opt2': "2. [Совместный план Джо и отца] Использовать дымовые шашки и совершить стремительный прорыв на кроссовых мотоциклах прямо через ограду.",
        'act1_out1': (
            "\nФрэнк и Фентон Харди подключают дешифратор к распределительному щитку.\n"
            "Благодаря блестящим знаниям электроники, вы перехватываете управление турелями наблюдения.\n"
            "Автоматические прожекторы гаснут именно тогда, когда вы перелезаете через ограду!\n"
            "Вы берете с собой лазерный резак, фонарик и бесшумно проникаете в бункер."
        ),
        'act1_out2': (
            "\nДжо с ревом заводит свой кроссовый мотоцикл! Фентон улыбается и бросает дымовую шашку.\n"
            "Густой белый дым застилает весь двор. Вы на бешеной скорости прорываетесь сквозь ограду,\n"
            "оставляя растерянную охрану кашлять в дыму! Вы прибываете к входу прямо на колесах.\n"
            "Из вещей у вас есть только фонарики, веревка с крюком и набор инструментов Джо."
        ),
        'act2_title': "\n--- АКТ II: СТАЛЬНОЙ ЛАБИРИНТ ---",
        'act2_text': (
            "Вы оказываетесь в коридорах подземного бункера. Стены сделаны из толстой бронированной стали.\n"
            "Впереди — герметичная дверь в серверную, но проход перекрывают смертоносные лазерные лучи.\n"
            "Малейшее прикосновение к красному свету запустит систему самоуничтожения базы.\n"
            "Фентон Харди внимательно осматривает стены:"
        ),
        'act2_q': "Как вы преодолеете лазерное препятствие?",
        'act2_opt1': "1. [Решение Фрэнка] Использовать зеркальные осколки для преломления лазерных лучей и перенаправления их на собственные фотоэлементы.",
        'act2_opt2': "2. [Решение Джо] Использовать тяжелую металлическую тележку для грузов, чтобы заблокировать излучатели и проскользнуть под ними.",
        'act2_out1_success': (
            "\nФрэнк аккуратно достает небольшое карманное зеркальце и разделяет его на несколько частей.\n"
            "Вместе с отцом вы закрепляете осколки на стенах под точным углом.\n"
            "Лучи преломляются, замыкают датчики, и лазерная сетка с тихим гудением исчезает!\n"
            "Путь свободен без всякого риска!"
        ),
        'act2_out2_success': (
            "\nДжо хватает массивную стальную тележку, стоявшую рядом.\n"
            "Вместе с отцом вы толкаете ее вперед. Тележка застревает между лучами, блокируя главные излучатели.\n"
            "Вы быстро скользите по полу под тележкой один за другим и оказываетесь на другой стороне!\n"
            "Однако срабатывает тихая тревога, и железная гермодверь за вашими спинами закрывается!"
        ),
        'act3_title': "\n--- АКТ III: ЛОВУШКА ДЛЯ ХАРДИ И КРЕПКАЯ ГОЛОВА ---",
        'act3_text': (
            "Вы входите в главный зал управления, но это оказывается ловушкой!\n"
            "На большом экране появляется лицо «Генерала»:\n"
            "— Добро пожаловать, семья Харди! Вы опоздали. Мои люди уже загружают коды.\n\n"
            "Вдруг тяжелая железная консоль, подвешенная к потолку, срывается с креплений и летит на Фентона!\n"
            "Джо молниеносно реагирует, отталкивает отца в сторону, но сам получает сильный удар стальным углом по голове!\n"
            "Джо падает без чувств. Вас немедленно запирают в железной камере с вакуумными дверями.\n"
            "Через несколько минут Джо приходит в себя, держась за затылок:\n"
            "— Ох, пап... Фрэнк... Кажется, на мою голову упала целая наковальня. Но не волнуйтесь,\n"
            "вы же знаете — у меня крепкая голова! Бывало и хуже! (Классический троп серии книг!)\n"
            "Вдруг из вентиляции начинает выходить зеленый сонный газ. Нужно действовать немедленно!"
        ),
        'act3_q': "Как вы выберетесь из заблокированной железной камеры?",
        'act3_opt1': "1. [Технология Фрэнка] Использовать лазерный резак (если вы выбрали путь Фрэнка) или взломать замок с помощью дешифратора.",
        'act3_opt2': "2. [Изобретательность отца и сила Джо] Использовать газовый баллон от огнетушителя как рычаг и выбить решетку вытяжки.",
        'act3_out1_success': (
            "\nФрэнк достает свой лазерный резак (или дешифратор) и начинает аккуратно плавить электронную плату двери.\n"
            "Искры летят во все стороны! Фентон помогает удерживать проводники.\n"
            "Щелк! Магнитный замок отключается, и тяжелая железная дверь открывается!"
        ),
        'act3_out1_fail': (
            "\nВы пытаетесь взломать замок простым инструментом, но микросхема надежно защищена броней.\n"
            "Сонный газ быстро заполняет комнату, у вас начинает кружиться голова!\n"
            "Нужно срочно попробовать силовое решение отца!"
        ),
        'act3_out2_success': (
            "\nФентон быстро срывает огнетушитель со стены. Джо, несмотря на боль в голове, хватает его,\n"
            "вставляет металлический раструб между прутьями вентиляционной решетки и нажимает как рычаг.\n"
            "Благодаря невероятной силе и опыту отца, решетка вылетает из креплений с грохотом!\n"
            "Вы быстро выбираетесь через шахту вентиляции на свободу!"
        ),
        'act4_title': "\n--- АКТ IV: ПОСЛЕДНИЙ РУБЕЖ ---",
        'act4_text': (
            "Вы выбегаете в подземный ангар. «Генерал» уже запрыгивает в кабину своего бронированного вездехода,\n"
            "готовый прорваться через туннель и сбежать.\n"
            "Мощный дизельный двигатель ревет на весь ангар, поднимая облака пыли.\n"
            "Фентон Харди кричит:\n"
            "— Фрэнк, Джо, мы должны заблокировать выходные ворота ангара, иначе он уйдет!"
        ),
        'act4_q': "Как вы остановите вездеход «Генерала»?",
        'act4_opt1': "1. [План Джо и отца] Прыгнуть на подъемный кран ангара, чтобы опустить тяжелый стальной контейнер прямо перед вездеходом.",
        'act4_opt2': "2. [План Фрэнка и отца] Быстро перепрограммировать гидравлические ворота туннеля, заблокировав выезд стальной плитой.",
        'act4_out1': (
            "\nДжо при поддержке отца ловко карабкается по лестнице на платформу крана.\n"
            "Он дергает за рычаг, и гигантский контейнер с грохотом падает на пол в метре от капота вездехода!\n"
            "«Генерал» резко жмет на тормоза. Фентон и Фрэнк мгновенно открывают двери кабины и задерживают злодея!\n"
            "Успех!"
        ),
        'act4_out2': (
            "\nФрэнк подбегает к главному пульту ангара, а отец диктует ему аварийные коды перекрытия.\n"
            "Пальцы Фрэнка молниеносно летают по клавиатуре.\n"
            "За долю секунды до выезда вездехода гигантская гидравлическая плита опускается вниз, перекрывая тунель!\n"
            "Вездеход врезается в нее на тормозах. Вы зажимаете «Генерала» в ловушку!"
        ),
        'final_header': "                 ФИНАЛ                       ",
        'final_high': (
            "Поздравляем! Вы блестяще выполнили миссию вместе с отцом! Ваш счет: {score} очков.\n"
            "Синдикат «Генерала» полностью уничтожен, правительственные коды возвращены в безопасность.\n"
            "Фентон Харди с гордостью хлопает вас по плечам:\n"
            "— Ребята, вы действуете как настоящие профессионалы. Я горжусь тем, что вы мои сыновья!\n"
            "Вечером дома тетя Гертруда устраивает грандиозный праздничный ужин с запеченным мясным рулетом,\n"
            "а Чет Мортон уже доедает вторую порцию картофельного пюре и подмигивает вам!"
        ),
        'final_normal': (
            "Миссия успешно завершена! Ваш счет: {score} очков.\n"
            "Хотя расследование было опасным, а затылок Джо снова украшен большой шишкой,\n"
            "команда семьи Харди доказала, что перед их общей силой не устоит ни один синдикат!\n"
            "Фентон Харди жмет вам руки — Бейпорт снова под надежной защитой!"
        ),
        'final_thanks': "\nСпасибо за игру! Семья Харди гордится вашим детективным талантом."
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
            state.inventory.append('laser_cutter')
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
        choice = input(loc.get('lang_choice_prompt', '\n-> ')).strip()
        
        if choice == '1':
            state.bypassed_lasers = True
            state.score += 20
            print_slow(loc['act2_out1_success'])
            break
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
        choice = input(loc.get('lang_choice_prompt', '\n-> ')).strip()
        
        if choice == '1':
            if state.route_taken == 'frank':
                state.score += 25
                print_slow(loc['act3_out1_success'])
                break
            else:
                print_slow(loc['act3_out1_fail'])
                continue
        elif choice == '2':
            state.score += 20
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
    
    if state.score >= 75:
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
