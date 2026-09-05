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
        'uk': "          БРАТИ ХАРДІ ТА ТАЄМНИЦЯ КАРИБСЬКОГО ЛАЙНЕРА (ЧАСТИНА XVI)          ",
        'en': "     THE HARDY BOYS AND THE MYSTERY OF THE CARIBBEAN LINER (PART XVI)       ",
        'ru': "          БРАТЬЯ ХАРДИ И ТАЙНА КАРИБСКОГО ЛАЙНЕРА (ЧАСТЬ XVI)               "
    }
    subtitle_text = {
        'uk': "                 Інтерактивний текстовий детективний квест                  ",
        'en': "                 Interactive Text-Based Detective Quest                     ",
        'ru': "                 Интерактивный текстовый детективный квест                  "
    }
    print("=" * 80)
    print(title_text[lang])
    print(subtitle_text[lang])
    print("=" * 80)
    print()

class GameState:
    def __init__(self):
        self.lang = 'uk'
        self.inventory = []
        self.route_taken = None  # 'frank' (security/decode) or 'joe' (stealth/casino)
        self.stealth_success = False
        self.score = 0

# Localization dictionary
LOCALIZATION = {
    'uk': {
        'select_lang': "Оберіть мову / Select Language / Выберите язык:\n1. Українська\n2. English\n3. Русский",
        'lang_choice_prompt': "Ваш вибір (1-3): ",
        'press_enter': "Натисніть ENTER, щоб розпочати круїз та розслідування...",
        'invalid_input': "Будь ласка, введіть 1 або 2.",
        'intro_text': (
            "Ви граєте за відомих братів-детективів Френка та Джо Харді.\n"
            "Після успішного штурму піратського форту в джунглях Юкатану, хлопці разом із Четом Мортоном\n"
            "вирішили використати отриману винагороду для розкішного круїзу Карибським морем на лайнері «Ocean Queen».\n"
            "Проте, де б не з'являлися брати Харді, таємниці та небезпеки завжди прямують за ними по п'ятах!"
        ),
        'act1_title': "\n--- АКТ I: БЕЗЛІМІТНИЙ БУФЕТ ТА ЗНИКЛА ЗІРКА ---",
        'act1_text': (
            "Ви перебуваєте у розкішному ресторані першого класу на борту лайнера «Ocean Queen».\n"
            "Навколо панує справжній рай для гурманів, і Чет Мортон перебуває на сьомому небі від щастя.\n"
            "На вашому столі — хрусткі кокосові креветки під солодким соусом чилі, ніжний запечений рібай-стейк,\n"
            "золотава картопля з вершковим соусом та зеленою цибулею, а посередині підноситься величезний\n"
            "шоколадний фонтан із соковитою полуницею. Чет якраз умочує туди п'яту шпажку і задоволено муркоче.\n\n"
            "Раптом гасне світло, а за хвилину вмикається аварійна червона сирена! Капітан лайнера оголошує:\n"
            "— Шановні пасажири, зберігайте спокій. З сейфу каюти мільйонера Ван дер Білта щойно викрали\n"
            "легендарний блакитний діамант «Зірка Океану» вартістю 10 мільйонів доларів!\n"
            "Корабель перебуває у відкритому морі, злодій усе ще на борту. Брати Харді розуміють: це робота для них!"
        ),
        'act1_q': "З чого ви розпочнете пошуки викраденого діаманта?",
        'act1_opt1': "1. [Шлях Френка] Пробратися до кімнати охорони, зламати систему цифрових логів та з'ясувати, чия електронна картка відчинила двері каюти.",
        'act1_opt2': "2. [Шлях Джо] Вирушити до елітного казино лайнера, щоб непомітно простежити за підозрілим помічником Ван дер Білта.",
        'act1_out1': (
            "\nВи використовуючи логіку Френка проникаєте до серверної кімнати охорони.\n"
            "Завдяки вашим знанням комп'ютерних мереж, ви швидко перехоплюєте лог доступу:\n"
            "сейф був відкритий клонованою карткою, код якої веде до технічного персоналу машинного відділення.\n"
            "Ви берете із собою міні-дешифратор та ліхтарики, готові спуститися на нижні палуби."
        ),
        'act1_out2': (
            "\nДжо вирішує діяти рішуче та швидко! Ви вирушаєте до шумного казино лайнера.\n"
            "Серед блиску гральних автоматів та рулеток ви помічаєте нервового секретаря Ван дер Білта,\n"
            "який поспіхом обмінює фішки на готівку та постійно озирається в бік дверей.\n"
            "У вашому розпорядженні спритність, мотузка та компактна рація."
        ),
        'act2_title': "\n--- АКТ II: СЛІД НА ПАЛУБАХ ---",
        'act2_text': (
            "Ви слідуєте за ланцюжком доказів. Навколо шумить нічний океан, туман огортає палуби лайнера.\n"
            "Раптом у темному проході біля рятувальних шлюпок ви помічаєте силует у формі офіцера,\n"
            "який передає чорний шкіряний кейс кремезному чоловіку в масці. Це спільники злодія!\n"
            "Якщо вони вас помітять, то викинуть докази за борт і зникнуть у темряві."
        ),
        'act2_q': "Як ви вчините у цій ситуації?",
        'act2_opt1': "1. Спробувати відволікти їх (Чет Мортон випадково упустить важкий шезлонг на іншій палубі, створивши гучний шум).",
        'act2_opt2': "2. Використати дешифратор (якщо ви обрали шлях Френка) для блокування дверей палуби або зробити швидкий підкат під перилами (шлях Джо).",
        'act2_out1': (
            "\nЧет з гуркотом кидає дерев'яний шезлонг. Офіцер та чоловік у масці здригаються,\n"
            "думаючи, що їх виявили з іншого боку, і біжать до протилежних дверей.\n"
            "Френк та Джо блискавично кидаються вперед та блокують шлях чоловіку з кейсом!"
        ),
        'act2_out2_decoder': (
            "\nФренк швидко підключає дешифратор до панелі керування герметичними дверима палуби.\n"
            "За секунду до того, як злочинці встигають втекти, важкі залізні двері з шипінням зачиняються,\n"
            "блокуючи їм шлях! Ви затискаєте їх у глухому куті."
        ),
        'act2_out2_slide': (
            "\nДжо робить неймовірний спортивний підкат по мокрій від бризок палубі прямо під ногами чоловіка в масці!\n"
            "Злодій перечіплюється через ноги Джо і з криком падає на підлогу, випускаючи кейс із рук.\n"
            "Френк миттєво підбирає кейс, але офіцер встигає втекти вглиб технічних коридорів!"
        ),
        'act3_title': "\n--- АКТ III: МАШИННЕ ВІДДІЛЕННЯ ТА МІЦНА ГОЛОВА ---",
        'act3_text': (
            "Пошуки офіцера приводять вас у саме серце лайнера — галасливе та спекотне машинне відділення.\n"
            "Навколо гудуть гігантські турбіни, пара виривається з труб, а під ногами вібрує сталева підлога.\n"
            "Раптом з хмари пари ззаду вискакує спільник злодія і щосили б'є Джо важким розвідним ключем по потилиці!\n"
            "Джо непритомніє і падає на підлогу. Френка миттєво оточують озброєні бандити.\n\n"
            "За кілька хвилин Джо приходить до тями, потираючи голову:\n"
            "— Ох, мій череп... Наче по ньому вдарив якір авіаносця. Але нічого, у мене міцна голова! (Фірмовий троп!)\n"
            "Ви виявляєте, що вас обох зачинили у герметичній сушильній камері суднової пральні,\n"
            "де температура стрімко зростає і вже важко дихати. Потрібно негайно вибиратися!"
        ),
        'act3_q': "Як ви виберетесь із сушильної пастки?",
        'act3_opt1': "1. [Сила Джо] Використати важку металеву штангу для розвішування білизни як важіль, щоб відігнути петлі сталевих дверей.",
        'act3_opt2': "2. [Розум Френка] Використати шпильку з волосся Countess, яку Джо випадково підібрав у казино, щоб закоротити контакти термостата на стіні.",
        'act3_out1_success': (
            "\nДжо хапає товсту сталеву штангу, вставляє її між дверима та рамою і з усієї сили тисне.\n"
            "М'язи хлопця напружуються, метал зі скрипом гнеться, і замок з брязкотом вилітає! \n"
            "Ви вільні, хоча гаряче повітря пральні обпікає обличчя."
        ),
        'act3_out1_fail': (
            "\nВи намагаєтесь зламати двері штангою, але замок пральні виявляється надто міцним.\n"
            "Ви лише марно витрачаєте сили в задушливій кімнаті. Спробуйте інший підхід!"
        ),
        'act3_out2_success': (
            "\nФренк обережно розкриває панель термостата за допомогою шпильки і закорочує головні дроти.\n"
            "Виникає потужний спалах і коротке замикання! Система безпеки автоматично розблоковує\n"
            "всі двері пральні, рятуючи вас від перегріву. Чиста логіка перемагає!"
        ),
        'act4_title': "\n--- АКТ IV: ФІНАЛЬНИЙ СПУСК НА ШЛЮПКАХ ---",
        'act4_text': (
            "Ви вибігаєте на шлюпкову палубу. Головний злодій — капітан безпеки лайнера — уже застрибнув\n"
            "у швидкісний моторний катер, який на міцних металевих тросах крана починають опускати на воду.\n"
            "Катер висить на висоті десяти метрів над хвилями штормового океану. У вас є лише кілька секунд!"
        ),
        'act4_q': "Яку фінальну дію ви оберете для знешкодження втікача?",
        'act4_opt1': "1. [Дія Джо] Здійснити відчайдушний стрибок з палуби прямо на борт катера, що опускається, і вступити у рукопашний бій.",
        'act4_opt2': "2. [Дія Френка] Швидко підбігти до пульта керування краном та заблокувати лебідку гальмівним важелем, підвісивши катер у повітрі.",
        'act4_out1': (
            "\nДжо розбігається і стрибає у прірву, приземляючись прямо на м'яке сидіння катера!\n"
            "Злодій з переляку стріляє, але промахується. Джо миттєво збиває його з ніг коротким хуком.\n"
            "Френк швидко спускає катер на воду та допомагає братові зв'язати ватажка!"
        ),
        'act4_out2': (
            "\nФренк блискавично реагує, підбігає до пульта і з силою смикає червоний аварійний важіль.\n"
            "Металеві троси натягуються зі страшним скреготом, і катер намертво застигає в повітрі!\n"
            "Злодій безпорадно борсається на висоті, не в змозі спуститися або втекти, поки шериф та охорона біжать на допомогу."
        ),
        'final_header': "                 ФІНАЛ                       ",
        'final_high': (
            "Вітаємо! Ви блискуче розкрили справу на лайнері! Ваш рахунок: {score} очок.\n"
            "Блакитний діамант «Зірка Океану» повернуто пану Ван дер Білту. На честь вашої сміливості\n"
            "капітан влаштовує грандіозну вечірку біля басейну. Чет Мортон отримує довічний безкоштовний доступ\n"
            "до шоколадного фонтану, а Френк та Джо насолоджуються свіжим морським бризом та заслуженою славою!"
        ),
        'final_normal': (
            "Справу успішно розкрито! Ваш рахунок: {score} очок.\n"
            "Хоча потилиця Джо все ще пристойно болить після зустрічі з розвідним ключем,\n"
            "а Чет випадково з'їв забагато полуниці з шоколадом, діамант врятований, а злочинців заарештовано!\n"
            "Кариби можуть спати спокійно, коли на борту брати Харді!"
        ),
        'final_thanks': "\nДякуємо за гру! Справжні поціновувачі класичного детективу пишалися б вашими діями."
    },
    'en': {
        'select_lang': "Select Language / Оберіть мову / Выберите язык:\n1. Українська\n2. English\n3. Русский",
        'lang_choice_prompt': "Your choice (1-3): ",
        'press_enter': "Press ENTER to start the cruise and investigation...",
        'invalid_input': "Please enter 1 or 2.",
        'intro_text': (
            "You are playing as the famous detective brothers, Frank and Joe Hardy.\n"
            "After successfully storming the pirate fort in the jungles of Yucatan, the boys and Chet Morton\n"
            "decided to spend their reward on a luxury Caribbean cruise aboard the 'Ocean Queen'.\n"
            "However, wherever the Hardy boys go, mystery and danger are always close behind!"
        ),
        'act1_title': "\n--- ACT I: ALL-YOU-CAN-EAT BUFFET & THE MISSING STAR ---",
        'act1_text': (
            "You are in a luxurious first-class restaurant aboard the 'Ocean Queen'.\n"
            "A gourmet paradise surrounds you, and Chet Morton is in seventh heaven.\n"
            "On your table are crispy coconut shrimp with sweet chili sauce, a tender baked ribeye steak,\n"
            "golden potatoes with sour cream and chives, and a massive chocolate fountain with fresh strawberries.\n"
            "Chet is just dipping his fifth skewer and purring with satisfaction.\n\n"
            "Suddenly, the lights go out, and a minute later an emergency red siren blares! The captain announces:\n"
            "— Dear passengers, please remain calm. The legendary blue diamond 'Star of the Ocean'\n"
            "valued at $10 million has just been stolen from Mr. Van der Bilt's stateroom vault!\n"
            "The ship is in the open sea, the thief is still on board. The Hardy boys know: this is a job for them!"
        ),
        'act1_q': "How will you start your search for the stolen diamond?",
        'act1_opt1': "1. [Frank's Way] Sneak into the security room, bypass the digital logs, and find out whose keycard opened the stateroom door.",
        'act1_opt2': "2. [Joe's Way] Head to the ship's high-stakes casino to secretly tail Mr. Van der Bilt's suspicious assistant.",
        'act1_out1': (
            "\nUsing Frank's logical approach, you sneak into the security server room.\n"
            "Relying on your computer networking skills, you quickly intercept the access log:\n"
            "the vault was opened with a cloned card belonging to the engine room technical staff.\n"
            "You take a mini-decoder and flashlights, ready to head down to the lower decks."
        ),
        'act1_out2': (
            "\nJoe decides to act decisively and quickly! You head to the ship's noisy casino.\n"
            "Amidst the flashing slot machines and roulette wheels, you spot Van der Bilt's nervous secretary,\n"
            "who is hastily exchanging chips for cash and constantly looking back at the door.\n"
            "You have agility, a rope, and a compact walkie-talkie at your disposal."
        ),
        'act2_title': "\n--- ACT II: THE TRAIL ON THE DECKS ---",
        'act2_text': (
            "You follow the trail of clues. Around you, the night ocean roars, and fog blankets the decks.\n"
            "Suddenly, in a dark corridor near the lifeboats, you spot a figure in an officer's uniform\n"
            "handing a black leather case to a burly masked man. These are the thief's accomplices!\n"
            "If they spot you, they will throw the evidence overboard and vanish into the darkness."
        ),
        'act2_q': "What will you do in this situation?",
        'act2_opt1': "1. Try to distract them (Chet Morton will accidentally drop a heavy sun lounger on another deck, making a loud noise).",
        'act2_opt2': "2. Use the decoder (if Frank's path was chosen) to lock the deck doors, or perform a fast slide under the railings (Joe's path).",
        'act2_out1': (
            "\nChet drops a wooden sun lounger with a crash. The officer and the masked man flinch,\n"
            "thinking they've been spotted from the other side, and run toward the opposite doors.\n"
            "Frank and Joe leap forward instantly, blocking the path of the man with the case!"
        ),
        'act2_out2_decoder': (
            "\nFrank quickly connects the decoder to the control panel of the heavy deck doors.\n"
            "A second before the criminals can escape, the heavy iron doors slide shut with a hiss,\n"
            "blocking their exit! You trap them in a dead end."
        ),
        'act2_out2_slide': (
            "\nJoe makes an incredible athletic slide across the spray-slicked deck right under the feet of the masked man!\n"
            "The thief trips over Joe's legs and falls with a shout, dropping the case.\n"
            "Frank quickly snatches the case, but the officer manages to escape deep into the technical corridors!"
        ),
        'act3_title': "\n--- ACT III: THE ENGINE ROOM & THE HARD HEAD ---",
        'act3_text': (
            "The search for the officer leads you to the heart of the liner — the noisy and hot engine room.\n"
            "Huge turbines hum around you, steam vents from pipes, and the steel floor vibrates underfoot.\n"
            "Suddenly, a thug jumps out of a steam cloud and hits Joe on the back of the head with a heavy wrench!\n"
            "Joe falls unconscious. Frank is instantly surrounded by armed criminals.\n\n"
            "A few minutes later, Joe wakes up, rubbing his head:\n"
            "— Ouch, my skull... Feels like an aircraft carrier's anchor hit it. But hey, I've got a hard head! (Classic trope!)\n"
            "You discover that you have both been locked in a hermetic drying chamber of the ship's laundry,\n"
            "where the temperature is rising rapidly and it's already hard to breathe. You must escape immediately!"
        ),
        'act3_q': "How will you escape the drying trap?",
        'act3_opt1': "1. [Joe's Strength] Use a heavy metal clothes rod as a lever to bend the hinges of the steel door.",
        'act3_opt2': "2. [Frank's Mind] Use a hairpin belonging to the Countess (which Joe picked up in the casino) to short-circuit the thermostat on the wall.",
        'act3_out1_success': (
            "\nJoe grabs the thick steel rod, wedges it between the door and the frame, and pushes with all his might.\n"
            "His muscles strain, the metal groans and bends, and the lock pops open with a metallic clang!\n"
            "You are free, though the hot air of the laundry burns your face."
        ),
        'act3_out1_fail': (
            "\nYou try to break the door with the rod, but the laundry lock is too strong.\n"
            "You only waste your energy in the suffocating room. Try another approach!"
        ),
        'act3_out2_success': (
            "\nFrank carefully opens the thermostat panel with the hairpin and short-circuits the main wires.\n"
            "A bright spark and a short circuit occur! The safety system automatically unlocks\n"
            "all laundry doors, saving you from overheating. Pure logic wins!"
        ),
        'act4_title': "\n--- ACT IV: THE FINAL BOAT DESCENT ---",
        'act4_text': (
            "You run out onto the boat deck. The main thief — the liner's security chief — has already jumped\n"
            "into a fast motorboat, which is being lowered into the water on the strong metal cables of a crane.\n"
            "The boat hangs ten meters above the waves of the stormy ocean. You only have a few seconds!"
        ),
        'act4_q': "What final action will you choose to stop the escapee?",
        'act4_opt1': "1. [Joe's Action] Make a desperate leap from the deck directly onto the lowering boat and engage in hand-to-hand combat.",
        'act4_opt2': "2. [Frank's Action] Quickly run to the crane control panel and lock the winch with the brake lever, suspending the boat in mid-air.",
        'act4_out1': (
            "\nJoe runs and leaps into the abyss, landing right on the soft seat of the boat!\n"
            "The thief fires out of fear but misses. Joe instantly knocks him down with a short hook.\n"
            "Frank quickly lowers the boat into the water and helps his brother tie up the leader!"
        ),
        'act4_out2': (
            "\nFrank reacts lightning-fast, runs to the panel, and pulls the red emergency lever with force.\n"
            "The metal cables tighten with a terrifying screech, and the boat freezes in mid-air!\n"
            "The thief thrashes helplessly, unable to lower the boat or escape, while the sheriff and guards run to help."
        ),
        'final_header': "                THE END                      ",
        'final_high': (
            "Congratulations! You solved the case on the liner brilliantly! Your score: {score} points.\n"
            "The blue diamond 'Star of the Ocean' has been returned to Mr. Van der Bilt. In honor of your courage,\n"
            "the captain hosts a grand pool party. Chet Morton gets lifetime free access\n"
            "to the chocolate fountain, and Frank and Joe enjoy the fresh sea breeze and well-deserved glory!"
        ),
        'final_normal': (
            "The case is successfully closed! Your score: {score} points.\n"
            "Although the back of Joe's head still hurts from the wrench,\n"
            "and Chet accidentally ate too many strawberries with chocolate, the diamond is saved and the criminals are arrested!\n"
            "The Caribbean can sleep soundly with the Hardy Boys on board!"
        ),
        'final_thanks': "\nThanks for playing! True mystery lovers would be proud of your actions."
    },
    'ru': {
        'select_lang': "Выберите язык / Oберіть мову / Select Language:\n1. Українська\n2. English\n3. Русский",
        'lang_choice_prompt': "Ваш выбор (1-3): ",
        'press_enter': "Нажмите ENTER, чтобы начать круиз и расследование...",
        'invalid_input': "Пожалуйста, введите 1 или 2.",
        'intro_text': (
            "Вы играете за известных братьев-детективов Фрэнка и Джо Харди.\n"
            "После успешного штурма пиратского форта в джунглях Юкатана, парни вместе с Четом Мортоном\n"
            "решили использовать полученную награду для роскошного круиза по Карибскому морю на лайнере «Ocean Queen».\n"
            "Однако, где бы ни появлялись братья Харди, тайны и опасности всегда следуют за ними по пятам!"
        ),
        'act1_title': "\n--- АКТ I: БЕЗЛИМИТНЫЙ БУФЕТ И ПРОПАВШАЯ ЗВЕЗДА ---",
        'act1_text': (
            "Вы находитесь в роскошном ресторане первого класса на борту лайнера «Ocean Queen».\n"
            "Вокруг царит настоящий рай для гурманов, и Чет Мортон пребывает на седьмом небе от счастья.\n"
            "На вашем столе — хрустящие кокосовые креветки под сладким соусом чили, сочный запеченный рибай-стейк,\n"
            "золотистый картофель со сметанным соусом и зеленым луком, а посередине возвышается огромный\n"
            "шоколадный фонтан со свежей клубникой. Чет как раз макает туда пятую шпажку и довольно урчит.\n\n"
            "Вдруг гаснет свет, а через минуту включается аварийная красная сирена! Капитан лайнера объявляет:\n"
            "— Уважаемые пассажиры, сохраняйте спокойствие. Из сейфа каюты миллионера Ван дер Билта только что похитили\n"
            "легендарный голубой алмаз «Звезда Океана» стоимостью 10 миллионов долларов!\n"
            "Корабль находится в открытом море, вор все еще на борту. Братья Харди понимают: это работа для них!"
        ),
        'act1_q': "С чего вы начнете поиски украденного алмаза?",
        'act1_opt1': "1. [Путь Фрэнка] Пробраться в комнату охраны, взломать систему цифровых логов и выяснить, чья электронная карта открыла дверь каюты.",
        'act1_opt2': "2. [Путь Джо] Отправиться в элитное казино лайнера, чтобы незаметно проследить за подозрительным помощником Ван дер Билта.",
        'act1_out1': (
            "\nИспользуя логику Фрэнка, вы проникаете в серверную комнату охраны.\n"
            "Благодаря вашим знаниям компьютерных сетей, вы быстро перехватываете лог доступа:\n"
            "сейф был открыт клонированной картой, код которой ведет к техническому персоналу машинного отделения.\n"
            "Вы берете с собой мини-дешифратор и фонарики, готовые спуститься на нижние палубы."
        ),
        'act1_out2': (
            "\nДжо решает действовать решительно и быстро! Вы отправляетесь в шумное казино лайнера.\n"
            "Среди блеска игровых автоматов и рулеток вы замечаете нервного секретаря Ван дер Билта,\n"
            "который наспех обменивает фишки на наличные и постоянно оглядывается на дверь.\n"
            "В вашем распоряжении ловкость, веревка и компактная рация."
        ),
        'act2_title': "\n--- АКТ II: СЛЕД НА ПАЛУБАХ ---",
        'act2_text': (
            "Вы следуете за цепочкой улик. Вокруг шумит ночной океан, туман окутывает палубы лайнера.\n"
            "Вдруг в темном проходе у спасательных шлюпок вы замечаете силуэт в форме офицера,\n"
            "который передает черный кожаный кейс крепкому мужчине в маске. Это сообщники вора!\n"
            "Если они вас заметят, то выбросят улики за борт и исчезнут в темноте."
        ),
        'act2_q': "Как вы поступите в этой ситуации?",
        'act2_opt1': "1. Попробовать отвлечь их (Чет Мортон случайно уронит тяжелый шезлонг на другой палубе, создав громкий шум).",
        'act2_opt2': "2. Использовать дешифратор (если вы выбрали путь Фрэнка) для блокировки дверей палубы или совершить быстрый подкат под перилами (путь Джо).",
        'act2_out1': (
            "\nЧет с грохотом роняет деревянный шезлонг. Офицер и человек в маске вздрагивают,\n"
            "думая, что их обнаружили с другой стороны, и бегут к противоположным дверям.\n"
            "Фрэнк и Джо молниеносно бросаются вперед и блокируют путь человеку с кейсом!"
        ),
        'act2_out2_decoder': (
            "\nФрэнк быстро подключает дешифратор к панели управления герметичными дверями палубы.\n"
            "За секунду до того, как преступники успевают сбежать, тяжелые железные двери с шипением закрываются,\n"
            "блокируя им путь! Вы зажимаете их в глухом углу."
        ),
        'act2_out2_slide': (
            "\nДжо делает невероятный спортивный подкат по мокрой от брызг палубе прямо под ногами человека в маске!\n"
            "Вор спотыкается о ноги Джо и с криком падает на пол, выпуская кейс из рук.\n"
            "Фрэнк мгновенно подбирает кейс, но офицер успевает скрыться в глубине технических коридоров!"
        ),
        'act3_title': "\n--- АКТ III: МАШИННОЕ ОТДЕЛЕНИЕ И КРЕПКАЯ ГОЛОВА ---",
        'act3_text': (
            "Поиски офицера приводят вас в самое сердце лайнера — шумное и жаркое машинное отделение.\n"
            "Вокруг гудят гигантские турбины, пар вырывается из труб, а под ногами вибрирует стальной пол.\n"
            "Вдруг из облака пара сзади выскакивает сообщник вора и изо всей силы бьет Джо тяжелым разводным ключом по затылку!\n"
            "Джо теряет сознание и падает на пол. Фрэнка мгновенно окружают вооруженные бандиты.\n\n"
            "Через несколько минут Джо приходит в себя, потирая голову:\n"
            "— Ох, мой череп... Как будто по нему ударил якорь авианосца. Но ничего, у меня крепкая голова! (Фирменный троп!)\n"
            "Вы обнаруживаете, что вас обоих заперли в герметичной сушильной камере судовой прачечной,\n"
            "где температура стремительно растет и уже тяжело дышать. Нужно немедленно выбираться!"
        ),
        'act3_q': "Как вы выберетесь из сушильной ловушки?",
        'act3_opt1': "1. [Сила Джо] Использовать тяжелую металлическую штангу для развешивания белья как рычаг, чтобы отогнуть петли стальной двери.",
        'act3_opt2': "2. [Разум Фрэнка] Использовать шпильку для волос Countess (которую Джо случайно подобрал в казино), чтобы закоротить контакты термостата на стене.",
        'act3_out1_success': (
            "\nДжо хватает толстую стальную штангу, вставляет ее между дверью и рамой и изо всей силы давит.\n"
            "Мышцы парня напрягаются, металл со скрипом гнется, и замок с грохотом вылетает!\n"
            "Вы свободны, хотя горячий воздух прачечной обжигает лицо."
        ),
        'act3_out1_fail': (
            "\nВы пытаетесь сломать дверь штангой, но замок прачечной оказывается слишком прочным.\n"
            "Вы лишь напрасно тратите силы в душной комнате. Попробуйте другой подход!"
        ),
        'act3_out2_success': (
            "\nФрэнк осторожно вскрывает панель термостата с помощью шпильки и закорачивает главные провода.\n"
            "Возникает мощная вспышка и короткое замыкание! Система безопасности автоматически разблокирует\n"
            "все двери прачечной, спасая вас от перегрева. Чистая логика побеждает!"
        ),
        'act4_title': "\n--- АКТ IV: ФИНАЛЬНЫЙ СПУСК НА ШЛЮПКАХ ---",
        'act4_text': (
            "Вы выбегаете на шлюпочную палубу. Главный вор — начальник безопасности лайнера — уже запрыгнул\n"
            "в скоростной моторный катер, который на прочных металлических тросах крана начинают опускать на воду.\n"
            "Катер висит на высоте десяти метров над волнами штормового океана. У вас есть всего несколько секунд!"
        ),
        'act4_q': "Какое финальное действие вы выберете для обезвреживания беглеца?",
        'act4_opt1': "1. [Действие Джо] Совершить отчаянный прыжок с палубы прямо на борт опускающегося катера и вступить в рукопашный бой.",
        'act4_opt2': "2. [Действие Фрэнка] Быстро подбежать к пульту управления краном и заблокировать лебедку тормозным рычагом, подвесив катер в воздухе.",
        'act4_out1': (
            "\nДжо разбегается и прыгает в пропасть, приземляясь прямо на мягкое сиденье катера!\n"
            "Вор с испугу стреляет, но промахивается. Джо мгновенно сбивает его с ног коротким хуком.\n"
            "Фрэнк быстро спускает катер на воду и помогает брату связать главаря!"
        ),
        'act4_out2': (
            "\nФрэнк молниеносно реагирует, подбегает к пульту и с силой дергает красный аварийный рычаг.\n"
            "Металлические тросы натягиваются со страшным скрежетом, и катер намертво застывает в воздухе!\n"
            "Вор беспомощно возится на высоте, не в силах спуститься или сбежать, пока шериф и охрана бегут на помощь."
        ),
        'final_header': "                ФИНАЛ                        ",
        'final_high': (
            "Поздравляем! Вы блестяще раскрыли дело на лайнере! Ваш счет: {score} очков.\n"
            "Голубой алмаз «Звезда Океана» возвращен господину Ван дер Билту. В честь вашей смелости\n"
            "капитан устраивает грандиозную вечеринку у бассейна. Чет Мортон получает пожизненный бесплатный доступ\n"
            "к шоколадному фонтану, а Фрэнк и Джо наслаждаются свежим морским бризом и заслуженной славой!"
        ),
        'final_normal': (
            "Дело успешно раскрыто! Ваш счет: {score} очок.\n"
            "Хотя затылок Джо все еще прилично болит после встречи с разводным ключом,\n"
            "а Чет случайно съел слишком много клубники с шоколадом, алмаз спасен, а преступники арестованы!\n"
            "Карибы могут спать спокойно, когда на борту братья Харди!"
        ),
        'final_thanks': "\nСпасибо за игру! Настоящие ценители классического детектива гордились бы вашими действиями."
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
            state.inventory.append('decoder')
            state.inventory.append('flashlight')
            print_slow(loc['act1_out1'])
            break
        elif choice == '2':
            state.route_taken = 'joe'
            state.score += 15
            state.inventory.append('rope')
            state.inventory.append('walkie-talkie')
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
        if state.route_taken == 'frank':
            print("2. " + loc['act2_out2_decoder'].split('\n')[1])
        else:
            print("2. " + loc['act2_out2_slide'].split('\n')[1])
            
        choice = input(loc.get('lang_choice_prompt', '\n-> ')).strip()
        
        if choice == '1':
            state.score += 15
            print_slow(loc['act2_out1'])
            break
        elif choice == '2':
            state.score += 25
            state.stealth_success = True
            if state.route_taken == 'frank':
                print_slow(loc['act2_out2_decoder'])
            else:
                print_slow(loc['act2_out2_slide'])
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
            if not state.stealth_success:
                print_slow(loc['act3_out1_fail'])
                continue
            else:
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
