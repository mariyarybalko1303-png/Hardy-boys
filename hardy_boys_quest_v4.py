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
        'uk': "          БРАТИ ХАРДІ ТА ЗАГАДКА ОСТРОВА ЧЕРЕПА (ЧАСТИНА IV)          ",
        'en': "      THE HARDY BOYS AND THE RIDDLE OF SKULL ISLAND (PART IV)        ",
        'ru': "          БРАТЬЯ ХАРДИ И ЗАГАДКА ОСТРОВА ЧЕРЕПА (ЧАСТЬ IV)           "
    }
    subtitle_text = {
        'uk': "                 Інтерактивний детективний квест                     ",
        'en': "                 Interactive Detective Text Quest                    ",
        'ru': "                 Интерактивный детективный квест                     "
    }
    print("=" * 75)
    print(title_text[lang])
    print(subtitle_text[lang])
    print("=" * 75)
    print()

class GameState:
    def __init__(self):
        self.lang = 'uk'
        self.inventory = ["мідний циліндр"]
        self.route_taken = None  # 'frank' (radio/decode) or 'joe' (boat/stealth)
        self.found_cipher_key = False
        self.solved_altar = False
        self.score = 0

# Huge localization dictionary containing Ukraine, English, Russian.
LOCALIZATION = {
    'uk': {
        'select_lang': "Оберіть мову / Select Language / Выберите язык:\n1. Українська\n2. English\n3. Русский",
        'lang_choice_prompt': "Ваш вибір (1-3): ",
        'press_enter': "Натисніть ENTER, щоб розпочати нову главу...",
        'invalid_input': "Будь ласка, введіть 1 або 2.",
        'intro_text': (
            "Ви граєте за неперевершених братів-детективів Френка та Джо Харді з містечка Бейпорт.\n"
            "Після успішного підняття скарбів іспанської шхуни «Морська Німфа» ви розгромили банду «Акул».\n"
            "Однак ватажок усього синдикату контрабандистів на прізвисько «Восьминіг» все ще на волі.\n"
            "Знайдений серед підводних уламків запечатаний мідний циліндр приховує ключ до його лігва..."
        ),
        'act1_title': "\n--- АКТ I: СВЯТКУВАННЯ ТА ТАЄМНИЧИЙ ЦИЛІНДР ---",
        'act1_text': (
            "Ви перебуваєте на задньому дворі будинку Харді. Ваша тітка Гертруда приготувала приголомшливу вечерю\n"
            "на честь вашої перемоги: пишний, золотисто-коричневий пиріг із соковитим курячим філе, грибами та ніжною вершковою підливкою,\n"
            "що тане в роті, та свіжий прохолодний яблучний сидр. Чет Мортон уже наминає третій шматок пирога,\n"
            "доволі прижмурюючи очі.\n\n"
            "— Хлопці, це найкраще розслідування в моєму житті, якщо після нього так годують! — регоче Чет.\n"
            "Френк дістає знайдений на шхуні мідний циліндр і за допомогою батькових інструментів обережно розкриває його.\n"
            "Всередині виявляється зашифрована навігаційна карта, яка вказує на Острів Черепа — скелястий безлюдний острівець\n"
            "на самому краю Бейпортської затоки. Саме там розташована секретна база «Восьминога»!"
        ),
        'act1_q': "Як ви почнете підготовку до висадки на Острів Черепа?",
        'act1_opt1': "1. [Шлях Френка] Налаштувати домашню радіостанцію, щоб перехопити хвилі контрабандистів та розгадати їхні шифри.",
        'act1_opt2': "2. [Шлях Джо] Негайно підготувати ваш катер «Нишпорка» і здійснити швидкісний розвідувальний рейд до острова.",
        'act1_out1': (
            "\nФренк сідає за короткохвильовий радіоприймач. Години напруженого прослуховування ефіру дають результат:\n"
            "ви перехоплюєте шифрований сигнал «Восьминога». Завдяки логіці ви розгадуєте радіокод синдикату:\n"
            "«Прохід через Рифи Сирен відкритий тільки по вектору 45-90».\n"
            "Тепер ви знаєте безпечний шлях! Ви забираєте карту, ліхтарики та мотузку."
        ),
        'act1_out2': (
            "\nДжо вмикає потужний двигун катера «Нишпорка». Разом із Френком та Четом ви мчите до острова крізь туман.\n"
            "Морські бризки б'ють в обличчя, а катер стрибає по хвилях. На підході до Острова Черепа ви помічаєте,\n"
            "що весь периметр патрулюється прожекторами, а прохід заблоковано гострими рифами. Доведеться маневрувати в темряві!"
        ),
        'act2_title': "\n--- АКТ II: ШТУРМ ОСТРОВА ЧЕРЕПА ---",
        'act2_text': (
            "Острів Черепа виглядає зловісно. Гострі чорні скелі нагадують зуби хижака, що стирчать з води.\n"
            "Туман згущується, роблячи видимість майже нульовою. На березі видніються замасковані ангари."
        ),
        'act2_q_frank': "Френк пропонує використати розгаданий шифр для безпечного проходу. Що ви зробите?",
        'act2_opt1_frank': "1. Пройти через Рифи Сирен строго за вектором 45-90, як вказано в радіоперехопленні.",
        'act2_opt2_frank': "2. Спробувати обійти острів з півночі, де патрульні прожектори здаються слабшими.",
        'act2_out1_frank': (
            "\nВи ідеально проходите крізь смертоносні рифи! Карта і шифр виявилися точними.\n"
            "Ви непомітно причалюєте у прихованій бухті острова і знаходите вхід до підземних печер.\n"
            "Френк забирає з катера корисні радіодеталі, які можуть знадобитися."
        ),
        'act2_out2_frank': (
            "\nВи намагаєтесь обійти острів, але сильна підводна течія зносить катер прямо на підводну скелю!\n"
            "Пролунав глухий удар, катер отримує пробоїну. Ви встигаєте вискочити на берег,\n"
            "але катер серйозно пошкоджено. Доведеться діяти швидко!"
        ),
        'act2_q_joe': "Джо веде катер уперед. Патрульний прожектор раптово повертається у ваш бік! Ваші дії?",
        'act2_opt1_joe': "1. Зробити різкий маневр і сховати катер у тіні великої навислої скелі.",
        'act2_opt2_joe': "2. Додати газу та спробувати проскочити зону освітлення на максимальній швидкості.",
        'act2_out1_joe': (
            "\nСпритність Джо рятує ситуацію! Ви ковзаєте в глибоку тінь скелі за секунду до того, як промінь прожектора\n"
            "проноситься над водою. Ви тихо причалюєте біля підніжжя скелі та висаджуєтесь на берег."
        ),
        'act2_out2_joe': (
            "\nВи даєте повний газ, але гучний рев двигуна привертає увагу охорони! Спалахує тривога,\n"
            "і по катеру відкривають вогонь сигнальними ракетами. Одна з ракет влучає в борт, змушуючи вас\n"
            "екстрено викинутися на гостре каміння берега. Ви врятувалися, але катер втрачено!"
        ),
        'act3_title': "\n--- АКТ III: ЛІГВО ВОСЬМИНОГА ТА МІЦНА ГОЛОВА ---",
        'act3_text': (
            "Ви проникаєте в глибокі лабіринти підземних печер Острова Черепа.\n"
            "Стіни тут вологі, а повітря пахне мазутом та порохом. Ви чуєте гул генераторів у глибині.\n"
            "Раптом ви виходите до великої зали з кам'яним вівтарем, на якому висічено зображення черепа з вісьмома щупальцями.\n"
            "Френк наближається, щоб оглянути вівтар, але раптом важка сталева решітка падає згори, відрізаючи вихід!\n\n"
            "З темряви вискакує здоровань у масці і з усієї сили б'є Джо по голові важким ліхтарем!\n"
            "Джо падає без свідомості. Зловмисники забирають вашу сумку з картами та зникають, зачинивши за собою решітку.\n\n"
            "За хвилину Джо з трудом розплющує очі й потирає величезну гулю на потилиці:\n"
            "— Ох, здається, мені знову перевірили міцність черепа... Голова тріщить, але кістки цілі! (Класичний троп!)\n"
            "Але ми заблоковані, а лиходії ось-ось втечуть із острова з усіма награбованими багатствами."
        ),
        'act3_q': "Як ви відчините сталеву решітку вівтаря?",
        'act3_opt1': "1. [Логіка Френка] Спробувати розгадати рельєфний пазл на кам'яному вівтарі, який керує решіткою.",
        'act3_opt2': "2. [Сила Джо] Використати застряглий у скелі сталевий гарпун як важіль, щоб підняти решітку силою.",
        'act3_out1_success': (
            "\nФренк помічає, що очі черепа на вівтарі — це кнопки, а щупальця мають різну довжину.\n"
            "Зіставивши довжину щупалець із римськими цифрами на мідному циліндрі, ви натискаєте кнопки в правильній послідовності:\n"
            "3 - 8 - 5. З голосним брязкотом противаги решітка піднімається вгору! Ви вільні!"
        ),
        'act3_out1_fail': (
            "\nВи натискаєте кнопки навмання. Система блокується, і з отворів у стінах починає виходити\n"
            "їдкий дим! Вам доводиться терміново шукати інше рішення, втрачаючи дорогоцінний час."
        ),
        'act3_out2_success': (
            "\nДжо хапає важкий сталевий гарпун, вставляє його під нижній край решітки й тисне всією своєю вагою.\n"
            "Френк допомагає братові. З неймовірним зусиллям ви піднімаєте важку залізну конструкцію достатньо,\n"
            "щоб Чет підставив під неї кам'яну брилу. Ви пролазите під решіткою!"
        ),
        'act4_title': "\n--- АКТ IV: ФІНАЛЬНЕ ЗІТКНЕННЯ З ВОСЬМИНОГОМ ---",
        'act4_text': (
            "Ви забігаєте до секретного підземного доку. Вода в басейні бурлить.\n"
            "Біля пірсу готується до занурення чорний міні-підводний човен. На містку стоїть сам «Восьминіг»!\n"
            "Коли він повертається, ви відчуваєте шок: це Артур Венс, поважний і відомий банкір Бейпорта,\n"
            "який мав бездоганну репутацію та часто вечеряв у будинку вашого батька!\n\n"
            "— Ха-ха-ха! Дурні хлопчиська! — регоче Венс. — Ваш батько Фентон ніколи не зможе довести мою провину,\n"
            "бо всі документи та золото пливуть зі мною на глибину! Прощавайте!\n"
            "Люк субмарини зачиняється, і гвинти починають обертатися. Субмарина рушає!"
        ),
        'act4_q': "Субмарина відходить від причалу! Як ви її зупините?",
        'act4_opt1': "1. [Дія Джо] Стрибнути у воду з тросом і зачепити його за рульовий гвинт підводного човна.",
        'act4_opt2': "2. [Дія Френка] Стрибнути в кабіну портового крана і скинути масивний контейнер прямо перед виходом з доку.",
        'act4_out1': (
            "\nДжо без вагань пірнає у холодну воду! Долаючи сильний опір гвинтів, він обмотує міцний сталевий трос\n"
            "навколо керма субмарини і закріплює інший кінець за залізну кнехту на пірсі.\n"
            "Трос натягується як струна, двигун підводного човна захлинається і зупиняється! Джо виринає, переможний і мокрий!"
        ),
        'act4_out2': (
            "\nФренк заскакує в кабіну крана, смикає за важелі керування і розкручує стрілу.\n"
            "Гігантський залізний контейнер з гуркотом падає прямо у вузькі ворота виходу з доку, повністю блокуючи шлях!\n"
            "Міні-субмарина з силою врізається в перешкоду і зупиняється з пом'ятим носом. Шлях перекрито!"
        ),
        'final_header': "                 ФІНАЛ                       ",
        'final_high': (
            "Вітаємо! Ви блискуче розкрили наймасштабнішу справу року! Ваш рахунок: {score} очок.\n"
            "Артур Венс («Восьминіг») заарештований шерифом Коллігом безпосередньо в доку.\n"
            "Усі контрабандні активи та докази вилучено. Ваш батько Фентон Харді прибуває на вертольоті\n"
            "та з гордістю тисне ваші руки перед спалахами камер репортерів.\n"
            "Увечері вдома тітка Гертруда виставляє на стіл величезний теплий чорничний пиріг із ванільним морозивом,\n"
            "а Чет Мортон уже обіцяє більше ніколи не лізти в пляшки з картами (хоча всі знають, що це неправда).\n"
            "Бейпорт у повній безпеці!"
        ),
        'final_normal': (
            "Справу успішно завершено! Ваш рахунок: {score} очок.\n"
            "Хоча ваш катер пошкоджено, а у Джо на голові красується нова величезна гуля від ліхтаря,\n"
            "ватажка контрабандистів затримано, а його підводне лігво ліквідовано.\n"
            "Попереду на братів Харді чекають нові, ще більш небезпечні та заплутані розслідування!"
        ),
        'final_thanks': "\nДякуємо за проходження детективної квадрології! Ви — справжній майстер розслідувань."
    },
    'en': {
        'select_lang': "Select Language / Оберіть мову / Выберите язык:\n1. Українська\n2. English\n3. Русский",
        'lang_choice_prompt': "Your choice (1-3): ",
        'press_enter': "Press ENTER to start the new chapter...",
        'invalid_input': "Please enter 1 or 2.",
        'intro_text': (
            "You are playing as the brilliant detective brothers Frank and Joe Hardy from Bayport.\n"
            "After successfully recovering the treasures of the Spanish galleon 'Sea Nymph', you crushed the 'Sharks' gang.\n"
            "However, the mastermind of the entire smuggling syndicate, known as 'The Octopus', is still at large.\n"
            "A sealed copper cylinder found among the underwater wreckage holds the key to his secret lair..."
        ),
        'act1_title': "\n--- ACT I: CELEBRATION & THE MYSTERIOUS CYLINDER ---",
        'act1_text': (
            "You are in the backyard of the Hardy home. Your Aunt Gertrude has prepared a spectacular dinner\n"
            "to celebrate your victory: a rich, golden-brown chicken pot pie with fresh mushrooms and a velvety cream gravy\n"
            "that melts in your mouth, along with ice-cold apple cider. Chet Morton is already eating his third slice of pie,\n"
            "half-closing his eyes with pure pleasure.\n\n"
            "— Guys, this is the best investigation of my life, if this is how we get fed afterwards! — Chet laughs.\n"
            "Frank pulls out the copper cylinder found on the shipwreck and carefully opens it using his father's tools.\n"
            "Inside is an encrypted navigation chart pointing to Skull Island — a rocky, uninhabited islet\n"
            "at the far edge of Bayport Bay. This is where the secret base of 'The Octopus' is hidden!"
        ),
        'act1_q': "How will you prepare for the landing on Skull Island?",
        'act1_opt1': "1. [Frank's Way] Set up the shortwave radio to intercept the smugglers' frequencies and crack their cipher.",
        'act1_opt2': "2. [Joe's Way] Immediately prep your boat 'The Sleuth' and make a high-speed reconnaissance run to the island.",
        'act1_out1': (
            "\nFrank sits down at the radio receiver. Hours of tense listening pay off:\n"
            "you intercept the coded signal of 'The Octopus'. Using pure logic, you crack the syndicate's cipher:\n"
            "'Passage through the Siren Reefs is open only along the 45-90 vector.'\n"
            "Now you know a safe path! You pack the map, flashlights, and a rope."
        ),
        'act1_out2': (
            "\nJoe starts up the powerful engine of 'The Sleuth'. Together with Frank and Chet, you speed through the fog.\n"
            "Sea spray hits your faces as the boat jumps over the waves. Approaching Skull Island, you notice\n"
            "that the entire perimeter is patrolled by searchlights, and the passage is blocked by sharp reefs. You must maneuver in the dark!"
        ),
        'act2_title': "\n--- ACT II: STORMING SKULL ISLAND ---",
        'act2_text': (
            "Skull Island looks ominous. Sharp black cliffs resemble predator teeth jutting out of the water.\n"
            "The fog thickens, reducing visibility to almost zero. Camouflaged hangars can be seen on the shore."
        ),
        'act2_q_frank': "Frank suggests using the decoded cipher for safe passage. What do you do?",
        'act2_opt1_frank': "1. Pass through the Siren Reefs strictly along the 45-90 vector, as indicated in the radio intercept.",
        'act2_opt2_frank': "2. Attempt to bypass the island from the north, where the patrol searchlights seem weaker.",
        'act2_out1_frank': (
            "\nYou navigate through the deadly reefs perfectly! The map and cipher were 100% accurate.\n"
            "You quietly dock in a hidden cove and find an entrance to the underground caves.\n"
            "Frank grabs some useful radio parts from the boat that might come in handy."
        ),
        'act2_out2_frank': (
            "\nYou try to bypass the island, but a strong underwater current sweeps the boat right onto a hidden reef!\n"
            "With a dull thud, the hull is punctured. You manage to jump ashore,\n"
            "but the boat is severely damaged. You must act fast!"
        ),
        'act2_q_joe': "Joe guides the boat forward. A patrol searchlight suddenly sweeps in your direction! Your actions?",
        'act2_opt1_joe': "1. Make a sharp maneuver and hide the boat in the deep shadow of a large overhanging cliff.",
        'act2_opt2_joe': "2. Hit the throttle and try to dash through the lighted zone at maximum speed.",
        'act2_out1_joe': (
            "\nJoe's agility saves the day! You slide into the deep shadow of the cliff a second before the searchlight\n"
            "sweeps over the water. You quietly dock at the foot of the cliff and disembark."
        ),
        'act2_out2_joe': (
            "\nYou go full throttle, but the loud roar of the engine alerts the guards! Alarm sirens blare,\n"
            "and they open fire on the boat with flare guns. One flare hits the hull, forcing you\n"
            "to crash onto the sharp rocks of the shore. You escaped, but the boat is lost!"
        ),
        'act3_title': "\n--- ACT III: THE OCTOPUS'S LAIR & THE HARD HEAD ---",
        'act3_text': (
            "You penetrate deep into the damp, dark caverns of Skull Island.\n"
            "The walls are wet, and the air smells of fuel and gunpowder. You hear generators humming in the depths.\n"
            "Suddenly, you enter a large hall with a stone altar carved with a skull and eight tentacles.\n"
            "Frank approaches to inspect the altar, but a heavy steel portcullis drops from above, cutting off your escape!\n\n"
            "A masked thug leaps from the shadows and strikes Joe over the head with a heavy flashlight!\n"
            "Joe falls unconscious. The thugs take your bag with the maps and vanish, locking the gate behind them.\n\n"
            "A minute later, Joe opens his eyes with a groan, rubbing a massive bump on his head:\n"
            "— Ouch, feels like they checked my skull's durability again... Head's splitting, but the bone is intact! (Classic trope!)\n"
            "But we are locked in, and the villains are about to escape the island with all their stolen riches."
        ),
        'act3_q': "How will you open the steel portcullis of the altar?",
        'act3_opt1': "1. [Frank's Logic] Solve the relief puzzle on the stone altar that controls the gate.",
        'act3_opt2': "2. [Joe's Strength] Use a steel harpoon wedged in the rock as a lever to pry the gate open.",
        'act3_out1_success': (
            "\nFrank notices that the skull's eyes on the altar are buttons, and the tentacles have different lengths.\n"
            "Matching the tentacle lengths with the Roman numerals on your copper cylinder, you press the buttons in order:\n"
            "3 - 8 - 5. With a loud metallic clang of counterweights, the gate slides up! You are free!"
        ),
        'act3_out1_fail': (
            "\nYou press the buttons at random. The system locks down, and an noxious gas\n"
            "starts pouring from vents in the walls! You must quickly find another solution, losing precious time."
        ),
        'act3_out2_success': (
            "\nJoe grabs the heavy steel harpoon, jams it under the gate, and presses down with all his weight.\n"
            "Frank joins in. With a massive collective effort, you lift the heavy iron gate just enough\n"
            "for Chet to slide a boulder underneath. You scramble through!"
        ),
        'act4_title': "\n--- ACT IV: FINAL CONFRONTATION WITH THE OCTOPUS ---",
        'act4_text': (
            "You run into the secret submarine dock. The water in the pool is churning.\n"
            "A sleek black mini-submarine is preparing to submerge. 'The Octopus' himself stands on the bridge!\n"
            "As he turns around, you gasp in shock: it is Arthur Vance, a highly respected Bayport banker\n"
            "who had an impeccable reputation and often dined at your father's house!\n\n"
            "— Haha! Foolish boys! — Vance laughs. — Your father Fenton will never prove my guilt,\n"
            "because all the gold and documents are diving with me to the deep! Farewell!\n"
            "The submarine hatch clangs shut, and the propellers begin to spin. The sub is moving!"
        ),
        'act4_q': "The submarine is leaving the dock! How will you stop it?",
        'act4_opt1': "1. [Joe's Action] Dive into the water with a heavy cable and snag it on the submarine's propeller.",
        'act4_opt2': "2. [Frank's Action] Leap into the cabin of the harbor crane and drop a massive shipping container in front of the exit.",
        'act4_out1': (
            "\nJoe dives into the cold water without a second thought! Fighting the wash of the propellers, he wraps the heavy steel cable\n"
            "around the submarine's rudder and secures the other end to an iron bollard on the pier.\n"
            "The cable snaps taut, the submarine's engine chokes and stalls! Joe surfaces, wet but victorious!"
        ),
        'act4_out2': (
            "\nFrank leaps into the crane's cabin, pulls the controls, and swings the boom.\n"
            "A gigantic iron container drops with a massive crash right into the narrow exit gates of the dock, blocking the way!\n"
            "The mini-submarine collides with the container and grinds to a halt with a dented nose. The way is shut!"
        ),
        'final_header': "                THE END                      ",
        'final_high': (
            "Congratulations! You solved the biggest case of the year brilliantly! Your score: {score} points.\n"
            "Arthur Vance ('The Octopus') is arrested by Sheriff Collig right in the dock.\n"
            "All smuggled assets and evidence have been seized. Your father Fenton Hardy arrives by helicopter\n"
            "and proudly shakes your hands in front of flashing news cameras.\n"
            "In the evening at home, Aunt Gertrude puts a massive, warm blueberry cobbler with vanilla ice cream on the table,\n"
            "while Chet Morton promises never to touch any bottled maps again (though everyone knows that's not true).\n"
            "Bayport is completely safe!"
        ),
        'final_normal': (
            "The case is successfully closed! Your score: {score} points.\n"
            "Although your boat is damaged, and Joe has a new massive bump on his head, the smuggler chief\n"
            "has been captured and his underwater lair dismantled. More dangerous cases await the Hardy Boys!"
        ),
        'final_thanks': "\nThanks for playing this detective tetralogy! You are a true master of mystery."
    },
    'ru': {
        'select_lang': "Выберите язык / Oберіть мову / Select Language:\n1. Українська\n2. English\n3. Русский",
        'lang_choice_prompt': "Ваш выбор (1-3): ",
        'press_enter': "Нажмите ENTER, чтобы начать новую главу...",
        'invalid_input': "Пожалуйста, введите 1 или 2.",
        'intro_text': (
            "Вы играете за знаменитых братьев-детективов Фрэнка и Джо Харди из городка Бейпорт.\n"
            "После успешного поднятия сокровищ испанской шхуны «Морская Нимфа» вы разгромили банду «Акул».\n"
            "Однако главарь всего контрабандного синдиката по кличке «Осьминог» всё еще на свободе.\n"
            "Найденный среди подводных обломков запечатанный медный цилиндр скрывает ключ к его логову..."
        ),
        'act1_title': "\n--- АКТ I: ПРАЗДНОВАНИЕ И ТАИНСТВЕННЫЙ ЦИЛИНДР ---",
        'act1_text': (
            "Вы находитесь на заднем дворе дома Харди. Ваша тетя Гертруда приготовила потрясающий ужин\n"
            "в честь вашей победы: пышный, золотисто-коричневый пирог с сочным куриным филе, грибами и нежной сливочной подливкой,\n"
            "тающей во рту, и свежий прохладный яблочный сидр. Чет Мортон уже уплетает третий кусок пирога,\n"
            "довольно прищуривая глаза.\n\n"
            "— Ребята, это лучшее расследование в моей жизни, если после него так кормят! — хохочет Чет.\n"
            "Фрэнк достает найденный на шхуне медный цилиндр и с помощью отцовских инструментов аккуратно вскрывает его.\n"
            "Внутри обнаруживается зашифрованная навигационная карта, указывающая на Остров Черепа — скалистый необитаемый островок\n"
            "на самом краю Бейпортского залива. Именно там находится секретная база «Осьминога»!"
        ),
        'act1_q': "Как вы начнете подготовку к высадке на Остров Черепа?",
        'act1_opt1': "1. [Путь Фрэнка] Настроить домашнюю радиостанцию, чтобы перехватить частоты контрабандистов и разгадать их шифр.",
        'act1_opt2': "2. [Путь Джо] Немедленно подготовить ваш катер «Ищейка» и совершить скоростной разведывательный рейд к острову.",
        'act1_out1': (
            "\nФрэнк садится за коротковолновый радиоприемник. Часы напряженного прослушивания эфира дают результат:\n"
            "вы перехватываете шифрованный сигнал «Осьминога». Благодаря логике вы разгадываете радиокод синдиката:\n"
            "«Проход через Рифы Сирен открыт только по вектору 45-90».\n"
            "Теперь вы знаете безопасный путь! Вы берете карту, фонарики и веревку."
        ),
        'act1_out2': (
            "\nДжо запускает мощный двигатель катера «Ищейка». Вместе с Фрэнком и Четом вы мчитесь к острову сквозь туман.\n"
            "Морские брызги бьют в лицо, а катер прыгает по волнам. На подходе к Острову Черепа вы замечаете,\n"
            "что весь периметр патрулируется прожекторами, а проход заблокирован острыми рифами. Придется маневрировать в темноте!"
        ),
        'act2_title': "\n--- АКТ II: ШТУРМ ОСТРОВА ЧЕРЕПА ---",
        'act2_text': (
            "Остров Черепа выглядит зловеще. Острые черные скалы напоминают зубы хищника, торчащие из воды.\n"
            "Туман сгущается, делая видимость почти нулевой. На берегу виднеются замаскированные ангары."
        ),
        'act2_q_frank': "Фрэнк предлагает использовать разгаданный шифр для безопасного прохода. Что вы сделаете?",
        'act2_opt1_frank': "1. Пройти через Рифы Сирен строго по вектору 45-90, как указано в радиоперехвате.",
        'act2_opt2_frank': "2. Попробовать обойти остров с севера, где патрульные прожекторы кажутся слабее.",
        'act2_out1_frank': (
            "\nВы идеально проходите сквозь смертоносные рифы! Карта и шифр оказались точными.\n"
            "Вы незаметно причаливаете в скрытой бухте острова и находите вход в подземные пещеры.\n"
            "Фрэнк забирает с катера полезные радиодетали, которые могут пригодиться."
        ),
        'act2_out2_frank': (
            "\nВы пытаетесь обойти остров, но сильное подводное течение сносит катер прямо на подводную скалу!\n"
            "Раздается глухой удар, катер получает пробоину. Вы успеваете выскочить на берег,\n"
            "но катер серьезно поврежден. Придется действовать быстро!"
        ),
        'act2_q_joe': "Джо ведет катер вперед. Патрульный прожектор внезапно поворачивается в вашу сторону! Ваши действия?",
        'act2_opt1_joe': "1. Совершить резкий маневр и спрятать катер в тени большой нависшей скалы.",
        'act2_opt2_joe': "2. Прибавить газу и попытаться проскочить зону освещения на максимальной скорости.",
        'act2_out1_joe': (
            "\nЛовкость Джо спасает ситуацию! Вы скользите в глубокую тень скалы за секунду до того, как луч прожектора\n"
            "проносится над водой. Вы тихо причаливаете у подножия скалы и высаживаетесь на берег."
        ),
        'act2_out2_joe': (
            "\nВы даете полный газ, но громкий рев двигателя привлекает внимание охраны! Вспыхивает тревога,\n"
            "и по катеру открывают огонь сигнальными ракетами. Одна из ракет попадает в борт, вынуждая вас\n"
            "экстренно выброситься на острые камни берега. Вы спаслись, но катер потерян!"
        ),
        'act3_title': "\n--- АКТ III: ЛОГОВО ОСЬМИНОГА И КРЕПКАЯ ГОЛОВА ---",
        'act3_text': (
            "Вы проникаете в глубокие лабиринты подземных пещер Острова Черепа.\n"
            "Стены здесь влажные, а воздух пахнет мазутом и порохом. Вы слышите гул генераторов в глубине.\n"
            "Вдруг вы выходите к большому залу с каменным алтарем, на котором высечено изображение черепа с восемью щупальцами.\n"
            "Фрэнк приближается, чтобы осмотреть алтарь, но вдруг тяжелая стальная решетка падает сверху, отрезая выход!\n\n"
            "Из темноты выскакиет громила в маске и со всей силы бьет Джо по голове тяжелым фонарем!\n"
            "Джо падает без сознания. Злоумышленники забирают вашу сумку с картами и скрываются, заперев за собой решетку.\n\n"
            "Через минуту Джо с трудом открывает глаза и потирает огромную шишку на затылке:\n"
            "— Ох, кажется, мне снова проверили прочность черепа... Голова трещит, но кости целы! (Классический троп!)\n"
            "Но мы заблокированы, а злодеи вот-вот сбегут с острова со всеми награбленными богатствами."
        ),
        'act3_q': "Как вы откроете стальную решетку алтаря?",
        'act3_opt1': "1. [Логика Фрэнка] Попробовать разгадать рельефный пазл на каменном алтаре, который управляет решеткой.",
        'act3_opt2': "2. [Сила Джо] Использовать застрявший в скале стальной гарпун как рычаг, чтобы поднять решетку силой.",
        'act3_out1_success': (
            "\nФрэнк замечает, что глаза черепа на алтаре — это кнопки, а щупальца имеют разную длину.\n"
            "Сопоставив длину щупалец с римскими цифрами на медном цилиндре, вы нажимаете кнопки в правильной последовательности:\n"
            "3 - 8 - 5. С громким лязгом противовеса решетка поднимается вверх! Вы свободны!"
        ),
        'act3_out1_fail': (
            "\nВы нажимаете кнопки наугад. Система блокируется, и из отверстий в стенах начинает выходить\n"
            "едкий дым! Вам приходится срочно искать другое решение, теряя драгоценное время."
        ),
        'act3_out2_success': (
            "\nДжо хватает тяжелый стальной гарпун, вставляет его под нижний край решетки и давит всем своим весом.\n"
            "Фрэнк помогает брату. С невероятным усилием вы приподнимаете тяжелую железную конструкцию достаточно,\n"
            "чтобы Чет подставил под нее каменную глыбу. Вы пролезаете под решеткой!"
        ),
        'act4_title': "\n--- АКТ IV: ФИНАЛЬНОЕ СТОЛКНОВЕНИЕ С ОСЬМИНОГОМ ---",
        'act4_text': (
            "Вы забегаете в секретный подземный док. Вода в бассейне бурлит.\n"
            "У пирса готовится к погружению черная мини-подводная лодка. На мостике стоит сам «Осьминог»!\n"
            "Когда он поворачивается, вы испытываете шок: это Артур Вэнс, уважаемый и известный банкир Бейпорта,\n"
            "который имел безупречную репутацию и часто ужинал в доме вашего отца!\n\n"
            "— Ха-ха-ха! Глупые мальчишки! — хохочет Вэнс. — Ваш отец Фентон никогда не сможет доказать мою вину,\n"
            "потому что все золото и документы уплывают со мной на глубину! Прощайте!\n"
            "Люк субмарины захлопывается, и винты начинают вращаться. Субмарина трогается!"
        ),
        'act4_q': "Субмарина отходит от причала! Как вы её остановите?",
        'act4_opt1': "1. [Действие Джо] Прыгнуть в воду с тросом и зацепить его за рулевой винт подлодки.",
        'act4_opt2': "2. [Действие Фрэнка] Прыгнуть в кабину портового крана и сбросить массивный контейнер прямо перед выходом из дока.",
        'act4_out1': (
            "\nДжо без колебаний ныряет в холодную воду! Преодолевая сильное сопротивление винтов, он обматывает прочный стальной трос\n"
            "вокруг руля субмарины и закрепляет другой конец за железную кнехту на пирсе.\n"
            "Трос натягивается как струна, двигатель подводной лодки захлебывается и останавливается! Джо выныривает, мокрый и победивший!"
        ),
        'act4_out2': (
            "\nФрэнк заскакивает в кабину крана, дергает за рычаги управления и раскручивает стрелу.\n"
            "Гигантский железный контейнер с грохотом падает прямо в узкие ворота выхода из дока, полностью блокируя путь!\n"
            "Мини-субмарина с силой врезается в препятствие и останавливается с помятым носом. Путь перекрыт!"
        ),
        'final_header': "                 ФИНАЛ                       ",
        'final_high': (
            "Поздравляем! Вы блестяще раскрыли самое масштабное дело года! Ваш счет: {score} очков.\n"
            "Артур Вэнс («Осьминог») арестован шерифом Коллигом непосредственно в доке.\n"
            "Все контрабандные активы и улики изъяты. Ваш отец Фентон Харди прибывает на вертолете\n"
            "и с гордостью жмет ваши руки перед вспышками камер репортеров.\n"
            "Вечером дома тетя Гертруда выставляет на стол огромный теплый черничный пирог с ванильным мороженым,\n"
            "а Чет Мортон уже обещает больше никогда не лезть в бутылки с картами (хотя все знают, что это неправда).\n"
            "Бейпорт в полной безопасности!"
        ),
        'final_normal': (
            "Дело успешно завершено! Ваш счет: {score} очков.\n"
            "Хотя ваш катер поврежден, а у Джо на голове красуется новая огромная шишка от фонаря,\n"
            "главарь контрабандистов задержан, а его подводное логово ликвидировано.\n"
            "Впереди братьев Харди ждут новые, еще более опасные и запутанные расследования!"
        ),
        'final_thanks': "\nСпасибо за прохождение детективной квадрологии! Вы — настоящий мастер расследований."
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
            state.found_cipher_key = True
            state.inventory.append('radio_key')
            print_slow(loc['act1_out1'])
            break
        elif choice == '2':
            state.route_taken = 'joe'
            state.score += 10
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
        if state.route_taken == 'frank':
            print("\n" + loc['act2_q_frank'])
            print(loc['act2_opt1_frank'])
            print(loc['act2_opt2_frank'])
            choice = input(loc.get('lang_choice_prompt', '\n-> ')).strip()
            
            if choice == '1':
                state.score += 25
                state.solved_altar = True
                print_slow(loc['act2_out1_frank'])
                break
            elif choice == '2':
                state.score += 5
                print_slow(loc['act2_out2_frank'])
                break
            else:
                print(loc['invalid_input'])
        else:
            print("\n" + loc['act2_q_joe'])
            print(loc['act2_opt1_joe'])
            print(loc['act2_opt2_joe'])
            choice = input(loc.get('lang_choice_prompt', '\n-> ')).strip()
            
            if choice == '1':
                state.score += 20
                print_slow(loc['act2_out1_joe'])
                break
            elif choice == '2':
                state.score += 5
                print_slow(loc['act2_out2_joe'])
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
            if state.solved_altar:
                state.score += 25
                print_slow(loc['act3_out1_success'])
                break
            else:
                print_slow(loc['act3_out1_fail'])
                state.solved_altar = True  # force puzzle unlock after fail penalty
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
