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
        'uk': "          БРАТИ ХАРДІ ТА ТАЄМНИЦЯ ВОВЧОЇ УЩЕЛИНИ              ",
        'en': "      THE HARDY BOYS AND THE MYSTERY OF WOLF CREEK GORGE       ",
        'ru': "          БРАТЬЯ ХАРДИ И ТАЙНА ВОЛЧЬЕГО УЩЕЛЬЯ                "
    }
    subtitle_text = {
        'uk': "                 Інтерактивний текстовий квест (Частина V)     ",
        'en': "                 Interactive Text-Based Quest (Part V)         ",
        'ru': "                 Интерактивный текстовый квест (Часть V)       "
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
        self.route_taken = None  # 'frank' (lookout/files) or 'joe' (tracks/cliff)
        self.investigated_cave = False
        self.score = 0

# Localization dictionary with Ukrainian, English, and Russian languages.
LOCALIZATION = {
    'uk': {
        'select_lang': "Оберіть мову / Select Language / Выберите язык:\n1. Українська\n2. English\n3. Русский",
        'lang_choice_prompt': "Ваш вибір (1-3): ",
        'press_enter': "Натисніть ENTER, щоб розпочати пригоду...",
        'invalid_input': "Будь ласка, введіть 1 або 2.",
        'intro_text': (
            "Ви граєте за невтомних братів-детективів Френка та Джо Харді з містечка Бейпорт.\n"
            "У цій п'ятій частині пригоди вириваються за межі міста — у похмуру Вовчу Ущелину,\n"
            "що розташована неподалік від Бейпорта. Разом із вірним другом Четом Мортоном\n"
            "вам доведеться розплутати містичну загадку «привида ущелини» та знайти зникле обладнання!"
        ),
        'act1_title': "\n--- АКТ I: ПІКНІК З ТРИВОГОЮ ТА СТАРИЙ РЕЙНДЖЕР ---",
        'act1_text': (
            "Сонячний день неподалік від Бейпорта у державному заповіднику «Вовча Ущелина».\n"
            "Ви сидите на затишній лісовій галявині біля розлогого дуба. Чет Мортон, як завжди,\n"
            "перевершив самого себе: перед вами розстелено плед, заставлений контейнерами з їжею.\n"
            "Тут лежать пишні, товсті сендвічі із копченою індичкою, плавленим сиром чеддер та кислуватим\n"
            "журавлинним соусом, ароматна домашня картопляна салата з кропом та свіжоспечені гарячі\n"
            "чорничні пиріжки, з яких витікає солодкий фіолетовий сік. (Класичний гастрономічний троп!)\n\n"
            "Раптом лісову тишу розриває дике, металеве виття з глибини ущелини, яке точно не належить тварині.\n"
            "За хвилину з кущів вибігає лісовий рейнджер Боб — його обличчя бліде, а дихання важке.\n"
            "— Хлопці! — хрипить він. — Там... у закинутій срібній шахті знову завиває Привид!\n"
            "Вчора зникла група вчених, яка картографувала підземелля за допомогою коштовного сонара!\n"
            "Карсон Дрю та ваш батько Фентон закликали нас діяти обережно, але час спливає."
        ),
        'act1_q': "З чого почнемо розслідування?",
        'act1_opt1': "1. [Шлях Френка] Оглянути закинуту пожежну вежу рейнджерів, щоб проаналізувати старі карти та записи про шахту.",
        'act1_opt2': "2. [Шлях Джо] Прямувати одразу по свіжих слідах у глибину ущелини, щоб спробувати знайти вчених гарячими слідами.",
        'act1_out1': (
            "\nФренк пропонує розумний підхід. Ви піднімаєтеся на вершину старої дерев'яної вежі.\n"
            "Серед покинутих паперів Френк знаходить щоденник першого власника шахти та стару схему вентиляції.\n"
            "Ви забираєте блокнот із записами та міцну мотузку, що лежала в кутку.\n"
            "Тепер ви знаєте, що в шахту є таємний хід через дренажну систему!"
        ),
        'act1_out2': (
            "\nДжо не звик сидіти на місці! Ревіння двигунів ваших позашляхових мотоциклів лунає лісом.\n"
            "Ви швидко спускаєтеся крутим схилом у саму ущелину, де панує волога прохолода та густий туман.\n"
            "Сліди автомобільних шин ведуть прямо в ущелину, але раптово обриваються біля крутої скелі.\n"
            "З речей у вас із собою є лише ліхтарики та важкий альпіністський гак-кішка."
        ),
        'act2_title': "\n--- АКТ II: ЗАГАДКИ СРІБНОЇ ШАХТИ ---",
        'act2_text': (
            "Ви дістаєтеся до масивного, оббитого залізом входу у стару срібну шахту «Блеквуд».\n"
            "Тут дуже темно, повітря пахне сіркою та старою деревиною.\n"
            "Раптом попереду знову лунає те саме моторошне металеве виття!\n"
            "Чет Мортон тремтить так, що в його рюкзаку торохтять залишки пиріжків:\n"
            "— Ой, хлопці, це точно привид старої шахти! Давайте повернемося у Бейпорт, я знаю чудову піцерію..."
        ),
        'act2_q': "Як ви проберетеся всередину шахти?",
        'act2_opt1': "1. Спробувати зламати іржавий навісний замок на головних воротах (потрібен інструмент або сила).",
        'act2_opt2': "2. Обійти скелю та скористатися дренажною вентиляційною шахтою (потрібні знання карти або мотузка).",
        'act2_out1_success': (
            "\nДжо знаходить у багажнику мотоцикла монтування. Одним сильним і влучним ударом\n"
            "він збиває старий навісний замок! Головні двері зі скрипом відчиняються.\n"
            "Ви заходите всередину, але гучний звук удару міг розлетітися підземеллям..."
        ),
        'act2_out1_fail': (
            "\nБез потрібних інструментів ви марно намагаєтеся зламати замок руками.\n"
            "Ви лише створюєте багато галасу, але замок тримається міцно.\n"
            "На щастя, Френк помічає збоку стару напіввідчинену вентиляційну решітку!"
        ),
        'act2_out2_success': (
            "\nВикористовуючи записи з пожежної вежі, Френк легко знаходить прихований вентиляційний хід.\n"
            "Ви прив'язуєте мотузку до міцного дерева та акуратно, один за одним,\n"
            "спускаєтеся у сухий і чистий дренажний тунель. Абсолютно безшумно!"
        ),
        'act2_out2_fail': (
            "\nВи намагаєтеся знайти вентиляційний хід навпомацки в тумані, але без карти це важко.\n"
            "Ви ледь не зриваєтеся в глибокий яр. Доводиться повернутися до головних воріт\n"
            "та спробувати пролізти через щілину в дерев'яній обшивці двері."
        ),
        'act3_title': "\n--- АКТ III: ПАСТКА У ГЛИБИНІ ТА МІЦНА ГОЛОВА ---",
        'act3_text': (
            "Підземелля вражає своїми масштабами. Світло ліхтариків вихоплює залізничні рейки для вагонеток.\n"
            "Раптом з темряви на вас вилітає величезна чорна тінь з палаючими червоними очима!\n"
            "Це виявляється високотехнологічний дрон, обшитий штучним хутром та обладнаний динаміком!\n"
            "Поки ви розглядаєте цю містифікацію, з-за кутка лунає постріл сіткометом!\n"
            "Вас накриває міцною капроновою сіткою, а зверху падає великий уламковий камінь,\n"
            "який з усього маху влучає Джо прямо по потилиці! Джо падає непритомний.\n\n"
            "За кілька хвилин Джо розплющує очі й трясе головою:\n"
            "— Ух... наче зустрівся лобом із товарним потягом Бейпорта! Але голова на місці, бувало й гірше! (Міцна голова!)\n"
            "Ви виявляєте, що зачинені в глибокій шахтній каверні за сталевою решіткою.\n"
            "Поруч бандити під керівництвом фальшивого геолога доктора Крофта пакують викрадений сонар\n"
            "та ящики з незаконно видобутою самородною срібною рудою."
        ),
        'act3_q': "Як вибратися зі сталевої клітки підземелля?",
        'act3_opt1': "1. [Дія Джо] Використати застряглий у стіні старий буровий лом як важіль, щоб розсунути іржаві прути решітки.",
        'act3_opt2': "2. [Дія Френка] Розібрати пульт керування старим підйомником поруч та замкнути дроти, щоб підняти решітку.",
        'act3_out1_success': (
            "\nДжо налягає на залізний лом усім своїм вагою. З гучним скреготом іржаві прути\n"
            "піддаються і розсуваються на достатню відстань! Ви спритно прослизаєте на волю."
        ),
        'act3_out1_fail': (
            "\nПрути решітки виявляються занадто міцними і новими. Ви лише гнете старий лом,\n"
            "але прохід залишається закритим. Потрібно знайти інше рішення!"
        ),
        'act3_out2_success': (
            "\nФренк акуратно знімає кришку старого електричного щитка.\n"
            "Швидко проаналізувавши схему живлення, він перекушує два дроти і з'єднує їх напряму.\n"
            "Пролітає сніп іскор, старий мотор гуде, і важка залізна решітка повільно повзе вгору!"
        ),
        'act4_title': "\n--- АКТ IV: ПОГОНЯ ПО ГРЯЗЮЦІ ТА ПОВНЕ ВИКРИТТЯ ---",
        'act4_text': (
            "Ви вибираєтеся на поверхню якраз у той момент, коли доктор Крофт та його спільники\n"
            "вантажать ящики у свій потужний повнопривідний вантажівку, збираючись втекти польовими дорогами.\n"
            "Чет Мортон привів на допомогу лісового шерифа та підкріплення, але бандити вже тиснуть на газ!\n"
            "Вантажівка зривається з місця, викидаючи з-під коліс шматки болота та лісового ґрунту.\n"
            "Ви сідаєте на свої позашляхові мотоцикли та починаєте екстремальну гонку лісом!"
        ),
        'act4_q': "Як зупинити вантажівку втікачів?",
        'act4_opt1': "1. [Маневр Джо] Спробувати зблизитися на мотоциклі та закинути гак-кішку на задній борт вантажівки, щоб залізти на ходу.",
        'act4_opt2': "2. [План Френка] Зрізати дорогу лісовою стежкою та влаштувати пастку, обваливши старе сухе дерево на дорогу перед ними.",
        'act4_out1': (
            "\nДжо демонструє дива каскадерської майстерності! Він підлітає на трампліні,\n"
            "закидає гак і за лічені секунди опиняється в кузові! Поки Крофт намагається маневрувати,\n"
            "Джо глушить двигун вантажівки через капот. Машина зупиняється у глибокій калюжі!"
        ),
        'act4_out2': (
            "\nФренк чудово знає лісову карту. Ви зрізаєте поворот через яр, опиняєтеся попереду вантажівки.\n"
            "Френк швидко накидає трос на підгнилу сосну і за допомогою мотоцикла валить її прямо перед колесами втікачів!\n"
            "Доктор Крофт різко тисне на гальма, вантажівка врізається в стовбур і міцно застрягає в болоті!"
        ),
        'final_header': "                 ФІНАЛ                       ",
        'final_high': (
            "Вітаємо! Справа про «Привида Вовчої Ущелини» блискуче розкрита! Ваш рахунок: {score} очок.\n"
            "Доктора Крофта та його спільників заарештовано, а вчені та їхнє обладнання в безпеці.\n"
            "Рейнджер Боб безмежно вдячний вам і дарує хлопцям почесні зірки рятувальників заповідника.\n"
            "Увечері ви повертаєтеся додому до Бейпорта, де мама чекає на вас із величезним гарячим\n"
            "м'ясним пирогом, а Чет нарешті може спокійно доїсти свої чорничні пиріжки у повній безпеці!"
        ),
        'final_normal': (
            "Справу успішно розкрито! Ваш рахунок: {score} очок.\n"
            "Хоча погоня була небезпечною, а на лобі у Джо виблискує нова чимала гуля,\n"
            "Брати Харді знову довели, що навіть неподалік від Бейпорта жоден злочинець не сховається від правосуддя!\n"
            "Попереду на вас чекають нові захоплюючі розслідування!"
        ),
        'final_thanks': "\nДякуємо за гру! Френк та Джо пишалися б вашою сміливістю та кмітливістю."
    },
    'en': {
        'select_lang': "Select Language / Оберіть мову / Выберите язык:\n1. Українська\n2. English\n3. Русский",
        'lang_choice_prompt': "Your choice (1-3): ",
        'press_enter': "Press ENTER to start the adventure...",
        'invalid_input': "Please enter 1 or 2.",
        'intro_text': (
            "You play as the indefatigable detective brothers Frank and Joe Hardy from the town of Bayport.\n"
            "In this fifth part, the adventure breaks out of the city limits — into the gloomy Wolf Creek Gorge,\n"
            "located not far from Bayport. Together with your loyal friend Chet Morton,\n"
            "you will have to unravel the mystical mystery of the 'ghost of the gorge' and find the missing equipment!"
        ),
        'act1_title': "\n--- ACT I: ANXIOUS PICNIC AND THE OLD RANGER ---",
        'act1_text': (
            "A sunny day not far from Bayport in the Wolf Creek Gorge State Nature Reserve.\n"
            "You are sitting on a cozy forest clearing near a spreading oak tree. Chet Morton, as always,\n"
            "has outdone himself: a picnic blanket is spread out before you, loaded with food containers.\n"
            "There are plump, thick sandwiches with smoked turkey, melted cheddar cheese, and tart\n"
            "cranberry sauce, fragrant homemade potato salad with dill, and freshly baked, hot\n"
            "blueberry pies with sweet purple juice oozing out. (Classic food description trope!)\n\n"
            "Suddenly, a wild, metallic howl from the depths of the gorge shatters the forest silence.\n"
            "A minute later, forest ranger Bob runs out of the bushes — his face is pale, his breathing heavy.\n"
            "— Boys! — he gasps. — Over there... in the abandoned silver mine, the Ghost is howling again!\n"
            "Yesterday, a group of scientists mapping the underground with a costly sonar went missing!\n"
            "Carson Drew and your father Fenton urged us to act with caution, but time is running out."
        ),
        'act1_q': "Where do we start our investigation?",
        'act1_opt1': "1. [Frank's Route] Inspect the abandoned ranger lookout tower to analyze old maps and mine records.",
        'act1_opt2': "2. [Joe's Route] Head directly along the fresh tracks into the gorge to find the scientists hot on the trail.",
        'act1_out1': (
            "\nFrank suggests a smart approach. You climb to the top of the old wooden tower.\n"
            "Among the discarded papers, Frank finds the diary of the first mine owner and an old ventilation scheme.\n"
            "You take the notebook with records and a sturdy rope that was lying in the corner.\n"
            "Now you know there is a secret entrance to the mine through the drainage system!"
        ),
        'act1_out2': (
            "\nJoe is not used to sitting still! The roar of your off-road motorcycle engines echoes through the woods.\n"
            "You quickly descend the steep slope into the gorge itself, where damp cold and thick fog reign.\n"
            "Tire tracks lead straight into the gorge but suddenly end near a steep cliff.\n"
            "The only gear you have with you are flashlights and a heavy climbing grappling hook."
        ),
        'act2_title': "\n--- ACT II: RIDDLES OF THE SILVER MINE ---",
        'act2_text': (
            "You reach the massive, iron-clad entrance to the old Blackwood Silver Mine.\n"
            "It is very dark here, the air smells of sulfur and old wood.\n"
            "Suddenly, that same eerie metallic howl echoes ahead of you!\n"
            "Chet Morton is trembling so hard that the leftover pies rattle in his backpack:\n"
            "— Oh, boys, that's definitely the ghost of the old mine! Let's go back to Bayport, I know a great pizzeria..."
        ),
        'act2_q': "How will you get inside the mine?",
        'act2_opt1': "1. Try to break the rusty padlock on the main gates (requires tools or strength).",
        'act2_opt2': "2. Go around the cliff and use the drainage ventilation shaft (requires map knowledge or a rope).",
        'act2_out1_success': (
            "\nJoe finds a crowbar in the motorcycle trunk. With one strong and accurate blow\n"
            "he knocks off the old padlock! The main doors creak open.\n"
            "You go inside, but the loud sound of the blow could have echoed through the dungeon..."
        ),
        'act2_out1_fail': (
            "\nWithout the right tools, you try in vain to break the lock with your hands.\n"
            "You only make a lot of noise, but the lock holds firm.\n"
            "Fortunately, Frank notices an old half-open ventilation grate on the side!"
        ),
        'act2_out2_success': (
            "\nUsing the notes from the lookout tower, Frank easily finds the hidden ventilation shaft.\n"
            "You tie the rope to a sturdy tree and carefully, one by one,\n"
            "descend into the dry and clean drainage tunnel. Absolutely silent!"
        ),
        'act2_out2_fail': (
            "\nYou try to find the ventilation shaft by touch in the fog, but without a map it is difficult.\n"
            "You almost fall into a deep ravine. You have to return to the main gates\n"
            "and try to squeeze through a gap in the wooden paneling of the door."
        ),
        'act3_title': "\n--- ACT III: THE DEEP TRAP AND THE HARD HEAD ---",
        'act3_text': (
            "The dungeon is impressive in scale. The flashlights catch railroad tracks for mine carts.\n"
            "Suddenly, a huge black shadow with burning red eyes flies out of the darkness at you!\n"
            "It turns out to be a high-tech drone covered in faux fur and equipped with a speaker!\n"
            "While you are examining this mystification, a net gun shot echoes from around the corner!\n"
            "You are covered with a strong nylon net, and a large chunk of rock falls from above,\n"
            "hitting Joe right on the back of his head! Joe falls unconscious.\n\n"
            "A few minutes later, Joe opens his eyes and shakes his head:\n"
            "— Ouch... felt like meeting a Bayport freight train forehead-first! But my head is on, I've had worse! (Hard head!)\n"
            "You find yourselves locked in a deep mine cavern behind a steel grate.\n"
            "Nearby, bandits led by the fake geologist Dr. Croft are packing the stolen sonar\n"
            "and boxes of illegally mined silver ore."
        ),
        'act3_q': "How to escape from the steel cage dungeon?",
        'act3_opt1': "1. [Joe's Action] Use an old drill crowbar stuck in the wall as a lever to pry open the rusty grate bars.",
        'act3_opt2': "2. [Frank's Action] Disassemble the control panel of the old hoist nearby and jump the wires to raise the grate.",
        'act3_out1_success': (
            "\nJoe leans on the iron bar with all his weight. With a loud screech, the rusty bars\n"
            "give way and open wide enough! You quickly slip out to freedom."
        ),
        'act3_out1_fail': (
            "\nThe grate bars turn out to be too strong and new. You only bend the old crowbar,\n"
            "but the passage remains closed. You need to find another solution!"
        ),
        'act3_out2_success': (
            "\nFrank carefully removes the cover of the old electrical panel.\n"
            "After quickly analyzing the power scheme, he cuts two wires and connects them directly.\n"
            "A shower of sparks flies, the old motor hums, and the heavy iron grate slowly crawls up!"
        ),
        'act4_title': "\n--- ACT IV: MUD CHASE AND FULL EXPOSURE ---",
        'act4_text': (
            "You climb to the surface just as Dr. Croft and his accomplices\n"
            "are loading boxes into their powerful four-wheel-drive truck, preparing to escape along field roads.\n"
            "Chet Morton has brought the forest sheriff and backup to help, but the bandits are already pressing the gas!\n"
            "The truck tears off, throwing chunks of mud and forest soil from under the wheels.\n"
            "You get on your off-road motorcycles and start an extreme race through the woods!"
        ),
        'act4_q': "How to stop the escaping truck?",
        'act4_opt1': "1. [Joe's Maneuver] Try to get close on the motorcycle and throw the grappling hook onto the tailgate of the truck to climb on the move.",
        'act4_opt2': "2. [Frank's Plan] Cut the road along a forest path and set a trap by collapsing an old dry tree onto the road ahead of them.",
        'act4_out1': (
            "\nJoe demonstrates wonders of stunt mastery! He flies up on a ramp,\n"
            "throws the hook, and in a matter of seconds finds himself in the bed! While Croft tries to maneuver,\n"
            "Joe kills the truck's engine under the hood. The truck stops in a deep puddle!"
        ),
        'act4_out2': (
            "\nFrank knows the forest map perfectly. You cut the turn through a ravine, appearing ahead of the truck.\n"
            "Frank quickly throws a cable over a rotten pine tree and falls it with the help of his motorcycle right in front of the escapees!\n"
            "Dr. Croft slams on the brakes, the truck crashes into the trunk and gets firmly stuck in the mud!"
        ),
        'final_header': "                 THE END                     ",
        'final_high': (
            "Congratulations! The case of the 'Ghost of Wolf Creek Gorge' is brilliantly solved! Your score: {score} points.\n"
            "Dr. Croft and his accomplices are arrested, and the scientists and their equipment are safe.\n"
            "Ranger Bob is immensely grateful to you and gives the boys honorary star badges of reserve rescuers.\n"
            "In the evening, you return home to Bayport, where Mom is waiting for you with a huge hot\n"
            "meat pie, and Chet can finally finish his blueberry pies in complete safety!"
        ),
        'final_normal': (
            "The case is successfully solved! Your score: {score} points.\n"
            "Although the chase was dangerous, and Joe has a new sizable lump shining on his forehead,\n"
            "the Hardy Boys have once again proven that even not far from Bayport, no criminal can hide from justice!\n"
            "New exciting investigations lie ahead of you!"
        ),
        'final_thanks': "\nThanks for playing! Frank and Joe would be proud of your courage and wits."
    },
    'ru': {
        'select_lang': "Выберите язык / Oберіть мову / Select Language:\n1. Українська\n2. English\n3. Русский",
        'lang_choice_prompt': "Ваш выбор (1-3): ",
        'press_enter': "Нажмите ENTER, чтобы начать приключение...",
        'invalid_input': "Пожалуйста, введите 1 или 2.",
        'intro_text': (
            "Вы играете за неутомимых братьев-детективов Фрэнка и Джо Харди из городка Бейпорт.\n"
            "В этой пятой части приключения вырываются за пределы города — в мрачное Волчье Ущелье,\n"
            "расположенное неподалеку от Бейпорта. Вместе с верным другом Четом Мортоном\n"
            "вам предстоит распутать мистическую загадку «призрака ущелья» и найти пропавшее оборудование!"
        ),
        'act1_title': "\n--- АКТ I: ПИКНИК С ТРЕВОГОЙ И СТАРЫЙ РЕЙНДЖЕР ---",
        'act1_text': (
            "Солнечный день неподалеку от Бейпорта в государственном заповеднике «Волчье Ущелье».\n"
            "Вы сидите на уютной лесной поляне у раскидистого дуба. Чет Мортон, как обычно,\n"
            "превзошел самого себя: перед вами расстелен плед, уставленный контейнерами с едой.\n"
            "Здесь лежат пышные, толстые сэндвичи с копченой индейкой, плавленым сыром чеддер и кислым\n"
            "клюквенным соусом, ароматный домашний картофельный салат с укропом и свежеиспеченные горячие\n"
            "черничные пирожки, из которых вытекает сладкий фиолетовый сок. (Классический гастрономический троп!)\n\n"
            "Вдруг лесную тишину разрывает дикий, металлический вой из глубины ущелья, точно не принадлежащий животному.\n"
            "Через минуту из кустов выбегает лесной рейнджер Боб — его лицо бледно, а дыхание тяжело.\n"
            "— Ребята! — хрипит он. — Там... в заброшенной серебряной шахте снова завывает Призрак!\n"
            "Вчера исчезла группа ученых, которая картографировала подземелье с помощью дорогого сонара!\n"
            "Карсон Дрю и ваш отец Фентон призывали нас действовать осторожно, но время уходит."
        ),
        'act1_q': "С чего начнем расследование?",
        'act1_opt1': "1. [Путь Фрэнка] Осмотреть заброшенную пожарную вышку рейнджеров, чтобы проанализировать старые карты и записи о шахте.",
        'act1_opt2': "2. [Путь Джо] Направиться сразу по свежим следам в глубину ущелья, чтобы попытаться найти ученых по горячим следам.",
        'act1_out1': (
            "\nФрэнк предлагает разумный подход. Вы поднимаетесь на вершину старой деревянной вышки.\n"
            "Среди брошенных бумаг Фрэнк находит дневник первого владельца шахты и старую схему вентиляции.\n"
            "Вы забираете блокнот с записями и крепкую веревку, лежавшую в углу.\n"
            "Теперь вы знаете, что в шахту есть тайный ход через дренажную систему!"
        ),
        'act1_out2': (
            "\nДжо не привык сидеть на месте! Рев двигателей ваших внедорожных мотоциклов оглашает лес.\n"
            "Вы быстро спускаетесь по крутому склону в само ущелье, где царит влажная прохлада и густой туман.\n"
            "Следы автомобильных шин ведут прямо в ущелье, но внезапно обрываются у крутой скалы.\n"
            "Из вещей у вас с собой только фонарики и тяжелый альпинистский крюк-кошка."
        ),
        'act2_title': "\n--- АКТ II: ЗАГАДКИ СЕРЕБРЯНОЙ ШАХТЫ ---",
        'act2_text': (
            "Вы добираетесь до массивного, обитого железом входа в старую серебряную шахту «Блэквуд».\n"
            "Здесь очень темно, воздух пахнет серой и старым деревом.\n"
            "Вдруг впереди снова раздается тот самый жуткий металлический вой!\n"
            "Чет Мортон дрожит так, что в его рюкзаке гремят остатки пирожков:\n"
            "— Ой, ребята, это точно призрак старой шахты! Давайте вернемся в Бейпорт, я знаю отличную пиццерию..."
        ),
        'act2_q': "Как вы проберетесь внутрь шахты?",
        'act2_opt1': "1. Попробовать взломать ржавый навесной замок на главных воротах (требуется инструмент или сила).",
        'act2_opt2': "2. Обойти скалу и воспользоваться дренажной вентиляционной шахтой (требуются знания карты или веревка).",
        'act2_out1_success': (
            "\nДжо находит в багажнике мотоцикла монтировку. Одним сильным и точным ударом\n"
            "он сбивает старый навесной замок! Главные двери со скрипом открываются.\n"
            "Вы заходите внутрь, но громкий звук удара мог разнестись по подземелью..."
        ),
        'act2_out1_fail': (
            "\nБез нужных инструментов вы тщетно пытаетесь сломать замок руками.\n"
            "Вы только создаете много шума, но замок держится крепко.\n"
            "К счастью, Фрэнк замечает сбоку старую полуоткрытую вентиляционную решетку!"
        ),
        'act2_out2_success': (
            "\nИспользуя записи с пожарной вышки, Фрэнк легко находит скрытый вентиляционный ход.\n"
            "Вы привязываете веревку к крепкому дереву и аккуратно, один за другим,\n"
            "спускаетесь в сухой и чистый дренажный туннель. Абсолютно бесшумно!"
        ),
        'act2_out2_fail': (
            "\nВы пытаетесь найти вентиляционный ход на ощупь в тумане, но без карты это сложно.\n"
            "Вы едва не срываетесь в глубокий овраг. Приходится вернуться к главным воротам\n"
            "и попробовать пролезть через щель в деревянной обшивке двери."
        ),
        'act3_title': "\n--- АКТ III: ЛОВУШКА В ГЛУБИНЕ И КРЕПКАЯ ГОЛОВА ---",
        'act3_text': (
            "Подземелье поражает своими масштабами. Свет фонариков выхватывает железнодорожные рельсы для вагонеток.\n"
            "Вдруг из темноты на вас вылетает огромная черная тень с горящими красными глазами!\n"
            "Это оказывается высокотехнологичный дрон, обшитый искусственным мехом и оборудованный динамиком!\n"
            "Пока вы рассматриваете эту мистификацию, из-за угла раздается выстрел сеткометом!\n"
            "Вас накрывает прочной капроновой сеткой, а сверху падает крупный обломок камня,\n"
            "который со всего маху попадает Джо прямо по затылку! Джо падает без чувств.\n\n"
            "Через несколько минут Джо открывает глаза и трясет головой:\n"
            "— Ух... как будто встретился лбом с товарным поездом Бейпорта! Но голова на месте, бывало и хуже! (Крепкая голова!)\n"
            "Вы обнаруживаете, что заперты в глубокой шахтной каверне за стальной решеткой.\n"
            "Рядом бандиты под руководством фальшивого геолога доктора Крофта пакуют похищенный сонар\n"
            "и ящики с незаконно добытой самородной серебряной рудой."
        ),
        'act3_q': "Как выбраться из стальной клетки подземелья?",
        'act3_opt1': "1. [Действие Джо] Использовать застрявший в стене старый буровой лом как рычаг, чтобы раздвинуть ржавые прутья решетки.",
        'act3_opt2': "2. [Действие Фрэнка] Разобрать пульт управления старым подъемником рядом и замкнуть провода, чтобы поднять решетку.",
        'act3_out1_success': (
            "\nДжо нажимает на железный лом всем своим весом. С громким скрежетом ржавые прутья\n"
            "поддаются и раздвигаются на достаточное расстояние! Вы ловко проскальзываете на свободу."
        ),
        'act3_out1_fail': (
            "\nПрутья решетки оказываются слишком прочными и новыми. Вы только гнете старый лом,\n"
            "но проход остается закрытым. Нужно найти другое решение!"
        ),
        'act3_out2_success': (
            "\nФрэнк аккуратно снимает крышку старого электрического щитка.\n"
            "Быстро проанализировав схему питания, он перекусывает два провода и соединяет их напрямую.\n"
            "Пролетает сноп искр, старый мотор гудит, и тяжелая железная решетка медленно ползет вверх!"
        ),
        'act4_title': "\n--- АКТ IV: ПОГОНЯ ПО ГРЯЗИ И ПОЛНОЕ РАЗОБЛАЧЕНИЕ ---",
        'act4_text': (
            "Вы выбираетесь на поверхность как раз в тот момент, когда доктор Крофт и его сообщники\n"
            "грузят ящики в свой мощный полноприводный грузовик, собираясь сбежать по проселочным дорогам.\n"
            "Чет Мортон привел на помощь лесного шерифа и подкрепление, но бандиты уже жмут на газ!\n"
            "Грузовик срывается с места, выбрасывая из-под колес комья грязи и лесной почвы.\n"
            "Вы садитесь на свои внедорожные мотоциклы и начинаете экстремальную гонку по лесу!"
        ),
        'act4_q': "Как остановить грузовик беглецов?",
        'act4_opt1': "1. [Маневр Джо] Попробовать сблизиться на мотоцикле и забросить крюк-кошку на задний борт грузовика, чтобы залезть на ходу.",
        'act4_opt2': "2. [План Фрэнка] Срезать дорогу по лесной тропинке и устроить ловушку, обрушив старое сухое дерево на дорогу перед ними.",
        'act4_out1': (
            "\nДжо демонстрирует чудеса каскадерского мастерства! Он взлетает на трамплине,\n"
            "забрасывает крюк и за считанные секунды оказывается в кузове! Пока Крофт пытается маневрировать,\n"
            "Джо глушит двигатель грузовика под капотом. Машина останавливается в глубокой луже!"
        ),
        'act4_out2': (
            "\nФрэнк отлично знает лесную карту. Вы срезаете поворот через овраг, оказываясь впереди грузовика.\n"
            "Фрэнк быстро набрасывает трос на подгнившую сосну и с помощью мотоцикла валит ее прямо перед колесами беглецов!\n"
            "Доктор Крофт резко жмет на тормоза, грузовик врезается в ствол и крепко застревает в грязи!"
        ),
        'final_header': "                 ФИНАЛ                       ",
        'final_high': (
            "Поздравляем! Дело о «Призраке Волчьего Ущелья» блестяще раскрыто! Ваш счет: {score} очков.\n"
            "Доктора Крофта и его сообщников арестовали, а ученые и их оборудование в безопасности.\n"
            "Рейнджер Боб бесконечно благодарен вам и дарит ребятам почетные звезды спасателей заповедника.\n"
            "Вечером вы возвращаетесь домой в Бейпорт, где мама ждет вас с огромным горячим\n"
            "мясным пирогом, а Чет наконец-то может спокойно доесть свои черничные пирожки в полной безопасности!"
        ),
        'final_normal': (
            "Дело успешно раскрыто! Ваш счет: {score} очок.\n"
            "Хотя погоня была опасной, а на лбу у Джо красуется новая приличная шишка,\n"
            "Братья Харди снова доказали, что даже неподалеку от Бейпорта ни один преступник не скроется от правосудия!\n"
            "Впереди вас ждут новые увлекательные расследования!"
        ),
        'final_thanks': "\nСпасибо за игру! Фрэнк и Джо гордились бы вашей смелостью и сообразительностью."
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
            print_slow(loc['act1_out1'])
            break
        elif choice == '2':
            state.route_taken = 'joe'
            state.score += 10
            state.inventory.append('flashlight')
            state.inventory.append('grappling_hook')
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
            if state.route_taken == 'joe':
                state.score += 20
                print_slow(loc['act2_out1_success'])
            else:
                state.score += 5
                print_slow(loc['act2_out1_fail'])
                # continue with safety vent fallback
                state.score += 10
                print_slow(loc['act2_out2_success'])
            break
        elif choice == '2':
            if state.route_taken == 'frank':
                state.score += 20
                print_slow(loc['act2_out2_success'])
            else:
                state.score += 5
                print_slow(loc['act2_out2_fail'])
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
            if state.route_taken == 'joe':
                state.score += 25
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
