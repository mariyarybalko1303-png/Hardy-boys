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
        'uk': "          БРАТИ ХАРДІ ТА ТАЄМНИЦЯ АЛЯСКИНСЬКОГО БУНКЕРА (ЧАСТИНА XVIII)          ",
        'en': "      THE HARDY BOYS AND THE MYSTERY OF THE ALASKAN BUNKER (PART XVIII)       ",
        'ru': "          БРАТЬЯ ХАРДИ И ТАЙНА АЛЯСКИНСКОГО БУНКЕРА (ЧАСТЬ XVIII)             "
    }
    subtitle_text = {
        'uk': "          Спільна експедиція з Фентоном Харді: Інтерактивний квест            ",
        'en': "          A Joint Expedition with Fenton Hardy: Interactive Quest             ",
        'ru': "          Совместная экспедиция с Фентоном Харди: Интерактивный квест         "
    }
    print("=" * 85)
    print(title_text[lang])
    print(subtitle_text[lang])
    print("=" * 85)
    print()

class GameState:
    def __init__(self):
        self.lang = 'uk'
        self.inventory = []
        self.route_taken = None  # 'frank' (triangulation) or 'joe' (snowmobile)
        self.fell_together = False
        self.score = 0

# Localization dictionary
LOCALIZATION = {
    'uk': {
        'select_lang': "Оберіть мову / Select Language / Выберите язык:\\n1. Українська\\n2. English\\n3. Русский",
        'lang_choice_prompt': "Ваш вибір (1-3): ",
        'press_enter': "Натисніть ENTER, щоб розпочати велику північну пригоду...",
        'invalid_input': "Будь ласка, введіть 1 або 2.",
        'intro_text': (
            "Ви граєте за відомих братів-детективів Френка та Джо Харді.\\n"
            "Сьогодні особлива справа — ваш батько, Фентон Харді, не просто дає вам доручення,\\n"
            "а вирушає в експедицію разом із вами! На вас чекає сувора та велична Аляска,\\n"
            "занедбані військові секрети та смертельна небезпека серед вічної криги."
        ),
        'act1_title': "\n--- АКТ I: ПІВНІЧНИЙ БЕНКЕТ ТА СПІЛЬНИЙ ВИЛІТ ---",
        'act1_text': (
            "Ви сидите у затишному дерев'яному мисливському будиночку на околиці Анкориджа, Аляска.\\n"
            "За вікном лютує крижаний вітер, але всередині тріщить камін та панують божественні аромати.\\n"
            "Чет Мортон примудрився замовити традиційну місцеву вечерю: величезні соковиті стейки з оленини,\\n"
            "гарячий густий картопляний суп-пюре з вершками, диким лососем та зеленою цибулею, свіжоспечений\\n"
            "домашній хліб на заквасці з ароматним маслом, а на десерт — гарячий пиріг із тайговою чорницею.\\n\\n"
            "Батько Фентон Харді розгортає на великому дерев'яному столі карту супутникових знімків:\\n"
            "— Хлопці, це не просто чергове розслідування. Уряд США виявив, що під кригою Аляски запеленговано\\n"
            "сигнали з секретного радянського бункера часів Холодної війни «Об'єкт-88». Злочинний синдикат\\n"
            "«Полярний Вовк» уже вилетів туди, щоб викрасти прототип квантового шифратора, здатного зламати будь-яку мережу.\\n"
            "Ми вирушаємо туди негайно, всі троє! Літак готовий. Але ущелину засипало снігом.\n"
        ),
        'act1_q': "Як ви з батьком почнете пошук прихованого входу в бункер у крижаній долині?",
        'act1_opt1': "1. [Шлях Френка та Фентона] Налаштувати портативний тепловізор і провести радіотріангуляцію, щоб знайти вентиляційну шахту під снігом.",
        'act1_opt2': "2. [Шлях Джо та Фентона] Сідлати потужні снігоходи і мчати через замерзлий каньйон, орієнтуючись на свіжі сліди гусениць бандитів.",
        'act1_out1': (
            "\nЗавдяки науковому підходу батька та логіці Френка, ви налаштовуєте тепловізійні датчики.\\n"
            "На екрані з'являється слабка червона пляма теплого повітря, що пробивається крізь товщу криги!\\n"
            "Ви берете альпіністське спорядження, датчики та обережно висуваєтесь до знайденої точки.\\n"
            "Тепер ви точно знаєте розташування прихованого входу!"
        ),
        'act1_out2': (
            "\nРевіння двигунів снігоходів розриває полярну тишу! Джо тисне на газ, піднімаючи хмари снігу.\\n"
            "Батько Фентон веде групу, вміло маневруючи між гігантськими крижаними брилами.\\n"
            "Ви пролітаєте над самою прірвою, коли під ногами Джо з тріском руйнується крижаний міст!\\n"
            "Але завдяки реакції Джо здійснює неймовірний стрибок і виводить снігохід на міцний лід."
        ),
        'act2_title': "\n--- АКТ II: КРИЖАНА СТІНА ТА ОХОРОНА СИНДИКАТУ ---",
        'act2_text': (
            "Перед вами — гігантська стіна льодовика, в якій замасковано сталеві гермодвері бункера.\\n"
            "Навколо входу виставлено озброєні патрулі синдикату «Полярний Вовк». Вони використовують\\n"
            "потужні прожектори, що сканують білу пустелю. Прорватися силою без плану — самогубство.\\n"
            "Фентон Харді шепоче: «Хлопці, діємо разом. Нам потрібно проникнути всередину без зайвого шуму».\n"
        ),
        'act2_q': "Яку тактику ви оберете разом із батьком?",
        'act2_opt1': "1. Створити диверсію: влаштувати контрольований підрив снігової шапки на скелі вище, щоб засипати прожектори снігом.",
        'act2_opt2': "2. Використати радіодешифратор (якщо обрали шлях Френка) для короткого замикання системи освітлення бази.",
        'act2_out1': (
            "\nФентон і Джо швидко закладають невеликий заряд у верхню частину схилу.\\n"
            "Лунає глухий хлопок, і гігантська снігова лавина акуратно засипає генераторну будку та прожектори бандитів!\\n"
            "У повній темряві та хаосі ви троє безшумно прослизаєте всередину залізобетонного тамбура бункера."
        ),
        'act2_out2_scanner': (
            "\nФренк підключає радіодешифратор до кабелю живлення прожекторів.\\n"
            "Батько допомагає обійти військовий протокол безпеки. Кілька секунд роботи з кодом... КЛАЦ!\\n"
            "Вся електрика на базі гасне. Охорона в паніці кричить про аварію, а ви спокійно заходите через головні двері!"
        ),
        'act2_out2_stealth': (
            "\nВи вирішуєте здійснити обхідний маневр по замерзлих металевих трубах під стелею.\\n"
            "Френк допомагає батькові піднятися, але Джо робить необережний рух, і його ніж падає з тихим дзвоном на підлогу!\\n"
            "Охоронець піднімає голову, але Чет Мортон, який залишився на зв'язку по рації, вмикає запис крику полярної сови,\\n"
            "що рятує вашу команду від викриття!"
        ),
        'act3_title': "\n--- АКТ III: ЗАЛ ШИФРУВАННЯ ТА МІЦНА ГОЛОВА ДЖО ---",
        'act3_text': (
            "Ви опиняєтесь у величній підземній залі, заставленій старими радянськими суперкомп'ютерами.\\n"
            "Посеред зали на сталевому постаменті світиться той самий квантовий шифратор.\\n"
            "Раптом важкі залізні двері за вами блокуються, а зверху опускається гігантська сталева вентиляційна решітка!\\n"
            "З гучномовців лунає сміх лідера синдикату: «Детективи Харді! Ласкаво просимо в морозильну камеру!»\\n"
            "У цей момент стара іржава балка підвісної стелі з тріском обривається і летить прямо на Фентона Харді!\\n"
            "Джо блискавично реагує, штовхає батька вбік, але сам отримує сильний удар сталевою конструкцією по потилиці!\\n"
            "Він падає непритомний. Температура в залі починає стрімко падати до мінус сорока градусів...\\n\\n"
            "За хвилину Джо приходить до тями, потираючи потилицю:\\n"
            "— Ох... Здається, на мене наїхав полярний експрес. Але нічого, мій череп міцніший за аляскинську кригу! (Класичний троп!)\\n"
            "Ворожа система вентиляції починає викачувати кисень з приміщення."
        ),
        'act3_q': "Як ви виберетесь із заблокованого залу шифрування?",
        'act3_opt1': "1. [Сила Джо та батька] Використати важкий металевий лом як важіль, щоб виламати петлі гермодверей спільною силою.",
        'act3_opt2': "2. [Розум Френка та батька] Спробувати зламати електронний пульт керування кліматом, перевантаживши ланцюг за допомогою акумулятора ліхтарика.",
        'act3_out1_success': (
            "\nДжо та Фентон беруться за іржавий залізний лом. Напруживши всі сили, підбадьорювані Френком,\\n"
            "вони роблять потужний ривок. З металевим скреготом старі завіси дверей лопаються!\\n"
            "Двері відчиняються, і ви вириваєтесь у коридор бункера!"
        ),
        'act3_out1_fail': (
            "\nВи намагаєтеся виламати важкі герметичні двері ломом, але військова сталь тримається намертво.\\n"
            "Ви лише марно витрачаєте дорогоцінний кисень та сили. Потрібно діяти розумніше!"
        ),
        'act3_out2_success': (
            "\nФренк швидко розбирає пульт, а Фентон за допомогою тонкого дроту підключає батарею ліхтаря\\n"
            "безпосередньо до головного реле контролера. Яскравий спалах, синій дим... і замок дверей з клацанням відчиняється!\\n"
            "Блискуча інженерна робота в екстремальних умовах!"
        ),
        'act4_title': "\n--- АКТ IV: ФІНАЛЬНА ПОГОНЯ ПО КРИЖАНОМУ ОЗЕРУ ---",
        'act4_text': (
            "Ви хапаєте квантовий шифратор і вибігаєте на поверхню підземного доку.\\n"
            "Лідер синдикату «Полярний Вовк» уже застрибнув у гігантський броньований ратрак (снігохідний всюдихід)\\n"
            "і на повній швидкості мчить через замерзле озеро до свого гелікоптера.\\n"
            "Лід під всюдиходом тріщить, створюючи смертельні крижані хвилі. Фентон кричить: «Ми не можемо відпустити його!»\n"
        ),
        'act4_q': "Як ви зупините всюдихід лідера синдикату?",
        'act4_opt1': "1. [Дія Джо] Стрибнути на снігохід, наздогнати ратрак і на ходу застрибнути на капот, щоб заблокувати лобове скло та вихлопну трубу брезентом.",
        'act4_opt2': "2. [Дія Френка] Кинути сигнальну ракету в тріщину льоду перед всюдиходом, щоб викликати миттєве провалювання важкої машини під лід.",
        'act4_out1': (
            "\nДжо вижимає максимум із двигуна снігохода, злітає з крижаного трампліна прямо на бронекапот всюдихода!\\n"
            "Він миттєво накидає брезент на решітку радіатора та лобове скло. Двигун всюдихода перегрівається і глохне з гучним свистом.\\n"
            "Фентон та Френк швидко під'їжджають і допомагають скрутити ватажка бандитів. Справа зроблена!"
        ),
        'act4_out2': (
            "\nФренк миттєво оцінює товщину льоду. Він стріляє з ракетниці точно у велику тріщину прямо по курсу всюдихода.\\n"
            "Яскравий спалах підпалює паливну каністру на льоду, лід миттєво руйнується, і важкий всюдихід намертво\\n"
            "провалюється передньою частиною у крижану воду, застрягши на мілині. Бандити здаються!"
        ),
        'final_header': "                 ФІНАЛ ВЕЛИКОЇ ЕКСПЕДИЦІЇ                       ",
        'final_high': (
            "Вітаємо! Ви разом із батьком блискуче розкрили справу державної ваги! Ваш рахунок: {score} очок.\\n"
            "Синдикат «Полярний Вовк» повністю знешкоджено, а квантовий шифратор передано в надійні руки.\\n"
            "Фентон Харді з гордістю плескає вас по плечах: «Ви справжні детективи, якими я неймовірно пишаюся!\\n"
            "А тепер — бігом до хатинки, Чет обіцяв приготувати другу порцію чорничного пирога!»"
        ),
        'final_normal': (
            "Справу успішно завершено! Ваш рахунок: {score} очок.\\n"
            "Незважаючи на лютий мороз, забиту потилицю Джо та підступні лавини, родина Харді знову довела,\\n"
            "що для них немає нерозв'язних загадок. Попереду на вас чекає теплий камін та ситна вечеря!"
        ),
        'final_thanks': "\nДякуємо за гру! Френк, Джо та Фентон Харді пишалися б вашою сміливістю та розумом."
    },
    'en': {
        'select_lang': "Select Language / Оберіть мову / Выберите язык:\n1. Українська\n2. English\n3. Русский",
        'lang_choice_prompt': "Your choice (1-3): ",
        'press_enter': "Press ENTER to start the great northern adventure...",
        'invalid_input': "Please enter 1 or 2.",
        'intro_text': (
            "You are playing as the famous detective brothers, Frank and Joe Hardy.\\n"
            "Today is a very special case — your father, Fenton Hardy, doesn't just assign you a case,\\n"
            "he sets off on an expedition with you! Ahead of you lies harsh Alaska,\\n"
            "abandoned military secrets, and deadly danger among the eternal ice."
        ),
        'act1_title': "\n--- ACT I: NORTHERN FEAST & A JOINT FLIGHT ---",
        'act1_text': (
            "You are sitting in a cozy wooden hunting lodge on the outskirts of Anchorage, Alaska.\\n"
            "An icy wind rages outside, but inside a fireplace crackles and divine aromas fill the air.\\n"
            "Chet Morton managed to order a traditional local dinner: huge juicy venison steaks,\\n"
            "hot thick potato chowder with cream, wild salmon, and green onions, freshly baked\\n"
            "sourdough bread with butter, and for dessert — hot wild blueberry pie.\\n\\n"
            "Fenton Hardy spreads a map of satellite images on a large wooden table:\\n"
            "— Boys, this isn't just another routine investigation. The US government detected\\n"
            "signals from a secret Cold War Soviet bunker 'Object-88' under the Alaskan ice. The 'Polar Wolf'\\n"
            "syndicate has already flown there to steal a prototype quantum cipher device capable of cracking any network.\\n"
            "We are going there immediately, all three of us! The plane is ready. But the canyon is snowed in.\n"
        ),
        'act1_q': "How will you and your father start searching for the hidden entrance to the bunker in the ice valley?",
        'act1_opt1': "1. [Frank & Fenton's Path] Set up a portable thermal imager and perform radio triangulation to find a ventilation shaft under the snow.",
        'act1_opt2': "2. [Joe & Fenton's Path] Saddle up powerful snowmobiles and race through the frozen canyon, following fresh tracks of the bandits' snowcats.",
        'act1_out1': (
            "\nThanks to Fenton's scientific approach and Frank's logic, you set up the thermal imaging sensors.\\n"
            "A faint red spot of warm air breaking through the thick ice appears on the screen!\\n"
            "You grab climbing gear and head to the identified point. You now know the exact location of the entrance!"
        ),
        'act1_out2': (
            "\nThe roar of snowmobile engines breaks the polar silence! Joe hits the gas, raising snow clouds.\\n"
            "Fenton leads the group, skillfully maneuvering between giant ice blocks.\\n"
            "You fly over the very edge of an abyss as an ice bridge collapses under Joe!\\n"
            "But thanks to Joe's reaction, he makes an incredible jump and lands the snowmobile on solid ice."
        ),
        'act2_title': "\n--- ACT II: THE ICE WALL & SYNDICATE GUARDS ---",
        'act2_text': (
            "Before you is a giant glacier wall, where the steel doors of the bunker are camouflaged.\\n"
            "Armed patrols of the 'Polar Wolf' syndicate are stationed around the entrance, scanning with searchlights.\\n"
            "Rushing in without a plan is suicide. Fenton Hardy whispers:\\n"
            "— Boys, we act together. We need to get inside without making any noise.\n"
        ),
        'act2_q': "What tactic will you and your father choose?",
        'act2_opt1': "1. Create a diversion: detonate a small charge on the snow cap above to bury the searchlights under snow.",
        'act2_opt2': "2. Use a radio decoder (if you chose Frank's path) to short-circuit the base's searchlight grid.",
        'act2_out1': (
            "\nFenton and Joe quickly set a small charge on the upper slope.\\n"
            "A muffled pop sounds, and a small avalanche buries the generator shack and the bandits' searchlights!\\n"
            "In complete darkness, you three quietly slip inside the concrete bunker anteroom."
        ),
        'act2_out2_scanner': (
            "\nFrank connects the radio decoder to the searchlight power cable.\\n"
            "Fenton helps bypass the military security protocol. A few seconds of coding... CLICK!\\n"
            "All power on the base shuts down. The guards panic, while you calmly walk in through the main doors!"
        ),
        'act2_out2_stealth': (
            "\nYou decide to make a flanking maneuver along the frozen metal pipes under the ceiling.\\n"
            "Frank helps Fenton up, but Joe makes a careless move, and his pocket knife falls with a quiet clang!\\n"
            "A guard raises his head, but Chet Morton, who stayed on comms, mimics a polar owl's cry, saving your team!"
        ),
        'act3_title': "\n--- ACT III: THE CIPHER HALL & JOE'S HARD HEAD ---",
        'act3_text': (
            "You find yourselves in a giant underground hall filled with old Cold War mainframe computers.\\n"
            "In the center of the hall, the quantum cipher device glows on a steel pedestal.\\n"
            "Suddenly, the heavy iron doors lock, and a giant metal security grate drops from above!\\n"
            "A voice laughs from the intercom: 'Welcome to the deep freezer, Hardy Boys!'\\n"
            "At that moment, a heavy rusty ceiling beam snaps and falls right toward Fenton Hardy!\\n"
            "Joe reacts instantly, pushes his father out of the way, but gets hit hard on the back of his head!\\n"
            "He falls unconscious. The temperature in the hall begins to drop rapidly to minus forty...\\n\\n"
            "A minute later, Joe wakes up, rubbing his head:\\n"
            "— Ouch... Feels like a train ran over my head. But hey, my skull is harder than Alaskan ice! (Classic trope!)\\n"
            "The enemy ventilation system begins pumping oxygen out of the room."
        ),
        'act3_q': "How will you escape the locked cipher hall?",
        'act3_opt1': "1. [Joe & Fenton's Strength] Use a heavy metal crowbar nearby as a lever to break the door hinges by brute force.",
        'act3_opt2': "2. [Frank & Fenton's Mind] Try to hack the electronic climate control panel, shorting the relay with a flashlight battery.",
        'act3_out1_success': (
            "\nJoe and Fenton grab the rusty iron crowbar. Putting all their strength into it,\\n"
            "they make a powerful heave. With a loud metallic screech, the old hinges snap!\\n"
            "The door swings open, and you break out into the bunker corridor!"
        ),
        'act3_out1_fail': (
            "\nYou try to break the heavy door with the crowbar, but the military steel holds firm.\\n"
            "You only waste precious oxygen and energy. You must try another option!"
        ),
        'act3_out2_success': (
            "\nFrank quickly disassembles the panel, while Fenton uses a thin wire to connect the flashlight battery\\n"
            "directly to the controller's master relay. A bright spark, blue smoke... and the door lock clicks open!\\n"
            "Brilliant engineering work in extreme conditions!"
        ),
        'act4_title': "\n--- ACT IV: THE FINAL CHASE ON THE ICE LAKE ---",
        'act4_text': (
            "You grab the quantum cipher device and run out to the underground dock.\\n"
            "The leader of the 'Polar Wolf' syndicate is already in a giant armored snowcat\\n"
            "and is rushing at full speed across the frozen lake to his helicopter.\\n"
            "The ice under the massive vehicle cracks, creating deadly fissures. Fenton yells: 'We can't let him escape!'\n"
        ),
        'act4_q': "How will you stop the syndicate leader's snowcat?",
        'act4_opt1': "1. [Joe's Action] Push the snowmobile to its limit, catch up with the snowcat, and jump onto its hood to block the windshield and exhaust with a tarp.",
        'act4_opt2': "2. [Frank's Action] Shoot a flare into an ice fissure right in front of the snowcat to break the ice and trap the heavy machine.",
        'act4_out1': (
            "\nJoe pushes his snowmobile, flies off an ice ramp directly onto the armored hood of the snowcat!\\n"
            "He quickly drapes a tarp over the radiator grill and windshield. The engine overheats and stalls with a loud hiss.\\n"
            "Fenton and Frank quickly arrive and help secure the bandit leader. The job is done!"
        ),
        'act4_out2': (
            "\nFrank instantly estimates the ice thickness. He fires the flare gun precisely into a major fissure right ahead.\\n"
            "The bright flare ignites a fuel canister on the ice, destroying the structural integrity, and the heavy snowcat\\n"
            "falls nose-first into the freezing water, getting stuck on the shallow rocks. The bandits surrender!"
        ),
        'final_header': "                 FINALE OF THE GREAT EXPEDITION                 ",
        'final_high': (
            "Congratulations! Together with your father, you solved a case of national security! Your score: {score} points.\\n"
            "The 'Polar Wolf' syndicate is completely crushed, and the cipher device is in safe hands.\\n"
            "Fenton Hardy proudly pats your shoulders: 'You are true detectives, I am incredibly proud of you!\\n"
            "Now let's head back to the lodge, Chet promised to bake another round of blueberry pies!'"
        ),
        'final_normal': (
            "The case is successfully completed! Your score: {score} points.\\n"
            "Despite the severe frost, Joe's bruised head, and treacherous avalanches, the Hardy family proved once again\\n"
            "that there are no insolvable mysteries for them. A warm fireplace and a hearty dinner await you!"
        ),
        'final_thanks': "\nThanks for playing! Frank, Joe, and Fenton Hardy would be proud of your bravery and intellect."
    },
    'ru': {
        'select_lang': "Выберите язык / Oберіть мову / Select Language:\n1. Українська\n2. English\n3. Русский",
        'lang_choice_prompt': "Ваш выбор (1-3): ",
        'press_enter': "Нажмите ENTER, чтобы начать великое северное приключение...",
        'invalid_input': "Пожалуйста, введите 1 или 2.",
        'intro_text': (
            "Вы играете за известных братьев-детективов Фрэнка и Джо Харди.\\n"
            "Сегодня особое дело — ваш отец, Фрэнклин 'Фентон' Харди, не просто даёт вам поручение,\\n"
            "а отправляется в экспедицию вместе с вами! Вас ждёт суровая и величественная Аляска,\\n"
            "заброшенные военные секреты и смертельная опасность среди вечных льдов."
        ),
        'act1_title': "\n--- АКТ I: СЕВЕРНЫЙ ПИР И СОВМЕСТНЫЙ ВЫЛЕТ ---",
        'act1_text': (
            "Вы сидите в уютном деревянном охотничьем домике на окраине Анкориджа, Аляска.\\n"
            "За окном бушует ледяной ветер, но внутри трещит камин и царят божественные ароматы.\\n"
            "Чет Мортон умудрился заказать традиционный местный ужин: огромные сочные стейки из оленины,\\n"
            "горячий густой картофельный суп-пюре со сливками, диким лососем и зелёным луком, свежеиспечённый\\n"
            "домашний хлеб на закваске с ароматным маслом, а на десерт — горячий пирог с таёжной черникой.\\n\\n"
            "Отец Фентон Харди раскладывает на большом деревянном столе карту спутниковых снимков:\\n"
            "— Ребята, это не просто очередное расследование. Правительство США обнаружило, что под льдами Аляски\\n"
            "запеленгованы сигналы из секретного советского бункера времён Холодной войны «Объект-88». Преступный синдикат\\n"
            "«Полярный Волк» уже вылетел туда, чтобы похитить прототип квантового шифратора, способного взломать любую сеть.\\n"
            "Мы отправляемся туда немедленно, все трое! Самолёт готов. Но ущелье засыпало снегом.\n"
        ),
        'act1_q': "Как вы с отцом начнёте поиск скрытого входа в бункер в ледяной долине?",
        'act1_opt1': "1. [Путь Фрэнка и Фентона] Настроить портативный тепловизор и провести радиотриангуляцию, чтобы найти вентиляционную шахту под снегом.",
        'act1_opt2': "2. [Путь Джо и Фентона] Оседлать мощные снегоходы и мчаться через замерзший каньон, ориентируясь на свежие следы гусениц бандитов.",
        'act1_out1': (
            "\nБлагодаря научному подходу отца и логике Фрэнка, вы настраиваете тепловизионные датчики.\\n"
            "На экране появляется слабое красное пятно тёплого воздуха, пробивающееся сквозь толщу льда!\\n"
            "Вы берёте альпинистское снаряжение, датчики и осторожно выдвигаетесь к найденной точке.\\n"
            "Теперь вы точно знаете расположение скрытого входа!"
        ),
        'act1_out2': (
            "\nРёв двигателей снегоходов разрывает полярную тишину! Джо жмёт на газ, поднимая тучи снега.\\n"
            "Отец Фентон ведёт группу, умело маневрируя между гигантскими ледяными глыбами.\\n"
            "Вы пролетаете над самой пропастью, когда под ногами Джо с треском рушится ледяной мост!\\n"
            "Но благодаря реакции Джо совершает невероятный прыжок и выводит снегоход на прочный лёд."
        ),
        'act2_title': "\n--- АКТ II: ЛЕДЯНАЯ СТЕНА И ОХРАНА СИНДИКАТА ---",
        'act2_text': (
            "Перед вами — гигантская стена ледника, в которой замаскированы стальные гермодвери бункера.\\n"
            "Вокруг входа выставлены вооружённые патрули синдиката «Полярный Вовк». Они используют\\n"
            "мощные прожекторы, сканирующие белую пустыню. Прорваться силой без плана — самоубийство.\\n"
            "Фентон Харди шепчет: «Ребята, действуем вместе. Нам нужно проникнуть внутрь без лишнего шума».\n"
        ),
        'act2_q': "Какую тактику вы выберете вместе с отцом?",
        'act2_opt1': "1. Создать диверсию: устроить контролируемый подрыв снежной шапки на скале выше, чтобы засыпать прожекторы снегом.",
        'act2_opt2': "2. Использовать радиодешифратор (если выбрали путь Фрэнка) для короткого замыкания системы освещения базы.",
        'act2_out1': (
            "\nФентон и Джо быстро закладывают небольшой заряд в верхней части склона.\\n"
            "Раздаётся глухой хлопок, и гигантская снежная лавина аккуратно засыпает генераторную будку и прожекторы бандитов!\\n"
            "В полной темноте и хаосе вы трое бесшумно проскальзываете внутрь железобетонного тамбура бункера."
        ),
        'act2_out2_scanner': (
            "\nФрэнк подключает радиодешифратор к кабелю питания прожекторов.\\n"
            "Отец помогает обойти военный протокол безопасности. Несколько секунд работы с кодом... ЩЕЛЧОК!\\n"
            "Всё электричество на базе гаснет. Охрана в панике кричит об аварии, а вы спокойно заходите через главную дверь!"
        ),
        'act2_out2_stealth': (
            "\nВы решаете совершить обходной манёвр по замёрзшим металлическим трубам под потолком.\\n"
            "Фрэнк помогает отцу подняться, но Джо делает неосторожное движение, и его нож падает с тихим звоном на пол!\\n"
            "Охранник поднимает голову, но Чет Мортон, оставшийся на связи по рации, вовремя включает запись крика полярной совы,\\n"
            "что спасает вашу команду от разоблачения!"
        ),
        'act3_title': "\n--- АКТ III: ЗАЛ ШИФРОВАНИЯ И КРЕПКАЯ ГОЛОВА ДЖО ---",
        'act3_text': (
            "Вы оказываетесь в величественном подземном зале, уставленном старыми советскими суперкомпьютерами.\\n"
            "Посреди зала на стальном постаменте светится тот самый квантовый шифратор.\\n"
            "Вдруг тяжёлые железные двери за вами блокируются, а сверху опускается гигантская стальная решётка!\\n"
            "Из громкоговорителей раздаётся смех лидера синдиката: «Детективы Харди! Добро пожаловать в морозилку!»\\n"
            "В этот момент старая ржавая балка подвесного потолка с треском обрывается и летит прямо на Фентона Харди!\\n"
            "Джо молниеносно реагирует, толкает отца в сторону, но сам получает сильный удар стальной конструкцией по затылку!\\n"
            "Он падает без чувств. Температура в зале начинает стремительно падать до минус сорока градусов...\\n\\n"
            "Через минуту Джо приходит в себя, потирая затылок:\\n"
            "— Ох... Такое ощущение, будто по мне проехал полярный экспресс. Но ничего, мой череп крепче аляскинского льда! (Классический троп!)\\n"
            "Вражеская система вентиляции начинает выкачивать кислород из помещения."
        ),
        'act3_q': "Как вы выберетесь из заблокированного зала шифрования?",
        'act3_opt1': "1. [Сила Джо и отца] Использовать тяжёлый металлический лом как рычаг, чтобы выломать петли гермодвери совместными усилиями.",
        'act3_opt2': "2. [Разум Фрэнка и отца] Попробовать взломать электронный пульт управления климатом, перегрузив цепь с помощью батарейки фонарика.",
        'act3_out1_success': (
            "\nДжо и Фентон берутся за ржавый железный лом. Напрягая все силы, подбадриваемые Фрэнком,\\n"
            "они делают мощный рывок. С металлическим скрежетом старые петли двери лопаются!\\n"
            "Дверь распахивается, и вы вырываетесь в коридор бункера!"
        ),
        'act3_out1_fail': (
            "\nВы пытаетесь выломать тяжёлую герметичную дверь ломом, но военная сталь держится намертво.\\n"
            "Вы лишь напрасно тратите драгоценный кислород и силы. Нужно действовать умнее!"
        ),
        'act3_out2_success': (
            "\nФрэнк быстро разбирает пульт, а Фентон с помощью тонкой проволоки подключает батарею фонаря\\n"
            "напрямую к главному реле контроллера. Яркая вспышка, синий дым... и замок двери со щелчком открывается!\\n"
            "Блестящая инженерная работа в экстремальных условиях!"
        ),
        'act4_title': "\n--- АКТ IV: ФИНАЛЬНАЯ ПОГОНЯ ПО ЛЕДЯНОМУ ОЗЕРУ ---",
        'act4_text': (
            "Вы хватаете квантовый шифратор и выбегаете на поверхность подземного дока.\\n"
            "Лидер синдиката «Полярный Волк» уже запрыгнул в гигантский бронированный ратрак (вездеход)\\n"
            "и на полной скорости мчится через замёрзшее озеро к своему вертолёту.\\n"
            "Лёд под вездеходом трещит, создавая смертельные ледяные промоины. Фентон кричит: «Мы не можем упустить его!»\n"
        ),
        'act4_q': "Как вы остановите вездеход лидера синдиката?",
        'act4_opt1': "1. [Действие Джо] Выжать максимум из двигателя снегохода, догнать ратрак и на ходу запрыгнуть на капот, чтобы заблокировать лобовое стекло и выхлопную трубу брезентом.",
        'act4_opt2': "2. [Действие Фрэнка] Бросить сигнальную ракету в трещину льда перед вездеходом, чтобы вызвать мгновенное проваливание тяжёлой машины под лёд.",
        'act4_out1': (
            "\nДжо выжимает максимум из двигателя снегохода, взлетает с ледяного трамплина прямо на бронекапот вездехода!\\n"
            "Он мгновенно накидывает брезент на решётку радиатора и лобовое стекло. Двигатель вездехода перегревается и глохнет с громким свистом.\\n"
            "Фентон и Фрэнк быстро подъезжают и помогают скрутить главаря бандитов. Дело сделано!"
        ),
        'act4_out2': (
            "\nФрэнк мгновенно оценивает толщину льда. Он стреляет из ракетницы точно в большую трещину прямо по курсу вездехода.\\n"
            "Яркая вспышка поджигает топливную канистру на льду, лёд мгновенно рушится, и тяжёлый вездеход намертво\\n"
            "проваливается передней частью в ледяную воду, застряв на мели. Бандиты сдаются!"
        ),
        'final_header': "                 ФИНАЛ ВЕЛИКОЙ ЭКСПЕДИЦИИ                       ",
        'final_high': (
            "Поздравляем! Вы вместе с отцом блестяще раскрыли дело государственной важности! Ваш счёт: {score} очков.\\n"
            "Синдикат «Полярный Волк» полностью обезврежен, а квантовый шифратор передан в надёжные руки.\\n"
            "Фентон Харди с гордостью хлопает вас по плечам: «Вы настоящие детективы, которыми я невероятно горжусь!\\n"
            "А теперь — бегом в хижину, Чет обещал приготовить вторую порцию черничного пирога!»"
        ),
        'final_normal': (
            "Дело успешно завершено! Ваш счёт: {score} очков.\\n"
            "Несмотря на лютый мороз, ушибленный затылок Джо и коварные лавины, семья Харди снова доказала,\\n"
            "что для них нет неразрешимых загадок. Впереди вас ждёт тёплый камин и сытный ужин!"
        ),
        'final_thanks': "\nСпасибо за игру! Фрэнк, Джо и Фентон Харди гордились бы вашей смелостью и умом."
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
        choice = input('\n-> ').strip()
        
        if choice == '1':
            state.route_taken = 'frank'
            state.score += 25
            state.inventory.append('thermal_imager')
            state.inventory.append('radio_decoder')
            print_slow(loc['act1_out1'])
            break
        elif choice == '2':
            state.route_taken = 'joe'
            state.score += 20
            state.inventory.append('rope')
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
        choice = input('\n-> ').strip()
        
        if choice == '1':
            state.score += 20
            print_slow(loc['act2_out1'])
            break
        elif choice == '2':
            if state.route_taken == 'frank':
                state.score += 25
                print_slow(loc['act2_out2_scanner'])
            else:
                state.score += 15
                print_slow(loc['act2_out2_stealth'])
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
        choice = input('\n-> ').strip()
        
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
        choice = input('\n-> ').strip()
        
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
    
    if state.score >= 90:
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
