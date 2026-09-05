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
        'uk': "          БРАТИ ХАРДІ ТА ЗОЛОТИЙ ІДОЛ КОСТА-РИКИ (ЧАСТИНА XVII)        ",
        'en': "      THE HARDY BOYS AND THE GOLDEN IDOL OF COSTA RICA (PART XVII)     ",
        'ru': "          БРАТЬЯ ХАРДИ И ЗОЛОТОЙ ИДОЛ КОСТА-РИКИ (ЧАСТЬ XVII)         "
    }
    subtitle_text = {
        'uk': "                 Інтерактивний текстовий квест                 ",
        'en': "                 Interactive Text-Based Quest                  ",
        'ru': "                 Интерактивный текстовый квест                 "
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
        self.route_taken = None  # 'frank' (decode/museum) or 'joe' (atv/mud)
        self.stealth_success = False
        self.score = 0

# Localization dictionary
LOCALIZATION = {
    'uk': {
        'select_lang': "Оберіть мову / Select Language / Выберите язык:\\n1. Українська\\n2. English\\n3. Русский",
        'lang_choice_prompt': "Ваш вибір (1-3): ",
        'press_enter': "Натисніть ENTER, щоб розпочати пригоду...",
        'invalid_input': "Будь ласка, введіть 1 або 2.",
        'intro_text': (
            "Ви граєте за відомих братів-детективів Френка та Джо Харді.\\n\"\n"
            "\"Після гучного розкриття справи на Карибському лайнері, ваше судно робить тривалу\\n\"\n"
            "\"зупинку в порту Лимон, Коста-Рика. Навколо розкинулися дикі, вічно оповиті туманом\\n\"\n"
            "\"тропічні ліси, де за легендами приховане стародавнє місто золотого племені Ягуара.\\n\"\n"
            "\"Але де є легенди про золото, там завжди з'являються небезпечні шукачі наживи!"
        ),
        'act1_title': "\n--- АКТ I: ГАЛЛО ПІНТО ТА ТАЄМНИЧИЙ АМУЛЕТ ---",
        'act1_text': (
            "Ви сидите на затишній відкритій терасі автентичного кафе «Ель Тукан».\\n\"\n"
            "\"Перед вами на столі — справжній флоридсько-карибський бенкет: традиційне галло пінто\\n\"\n"
            "\"(ніжний чорний бобовий рис з кокосовим молоком та прянощами), солодкі смажені банани платано,\\n\"\n"
            "\"свіжоспечена кукурудзяна коржі тортильяс, ароматні скибочки стиглого манго, папайї та гуави,\\n\"\n"
            "\"а також великі чашки міцної, щойно звареної костариканської кави. Чет Мортон уже доїдає\\n\"\n"
            "\"другу порцію платано з вершками.\\n\\n\"\n"
            "\"Раптом до вашого столика підбігає схвильований хлопчик-місцевий провідник Мануель.\\n\"\n"
            "\"Він кидає на стіл старовинний глиняний амулет у вигляді голови ягуара і задихано каже:\\n\"\n"
            "\"— Сеньйори! Мого батька, археолога доктора Альвареса, викрали озброєні люди у джунглях!\\n\"\n"
            "\"Вони вимагають карту золотого ідола, яку він сховав у таємному форпості Ягуара!\""
        ),
        'act1_q': "Як ви розпочнете рятувальну місію?",
        'act1_opt1': "1. [Шлях Френка] Вивчити амулет, дослідити мікрогліфи та розшифрувати старовинний щоденник батька Мануеля, щоб знайти безпечну стежку.",
        'act1_opt2': "2. [Шлях Джо] Орендувати потужні позашляхові квадроцикли (ATV) та негайно мчати по гарячих слідах коліс викрадачів углиб сельви.",
        'act1_out1': (
            "\nВи залишаєтеся в номері готелю. Френк під лупою вивчає глиняний амулет.\\n\"\n"
            "\"На задній стороні ви виявляєте приховані географічні координати та напис на латині.\\n\"\n"
            "\"Завдяки знанням історії, ви вираховуєте безпечний шлях в обхід смертоносних боліт.\\n\"\n"
            "\"Ви берете з собою мапу, супутниковий навігатор, альпіністську мотузку та вирушаєте в ліс."
        ),
        'act1_out2': (
            "\nРевіння моторів квадроциклів розриває тишу джунглів! Ви вирішуєте діяти миттєво.\\n\"\n"
            "\"Ви летите через густі хащі, розбризкуючи червону багнюку з-под коліс.\\n\"\n"
            "\"Чет Мортон міцно тримається ззаду, благаючи їхати повільніше.\\n\"\n"
            "\"Ви швидко наздоганяєте сліди важких шин викрадачів, які ведуть до гірського укосу."
        ),
        'act2_title': "\n--- АКТ II: СМЕРТОНОСНІ ТУМАННІ ДЖУНГЛІ ---",
        'act2_text': (
            "Ви заглиблюєтеся у туманний хмарний ліс Монтеверде. Величезні папороті та ліани\\n\"\n"
            "\"утворюють щільну стіну. Раптом попереду ви помічаєте табір викрадачів.\\n\"\n"
            "\"Вони тримають зв'язаного доктора Альвареса біля входу до занедбаної кам'яної шахти.\\n\"\n"
            "\"Територія навколо табору всіяна сигнальними пастками-розтяжками."
        ),
        'act2_q': "Як ви проберетеся повз охорону?",
        'act2_opt1': "1. Спробувати непомітно обійти табір по деревах, використовуючи ліани та міцну мотузку (тихий варіант).",
        'act2_opt2': "2. Влаштувати диверсію (запустити квадроцикл на автопілоті у протилежний бік, щоб виманити бандитів).",
        'act2_out1': (
            "\nВи спритно підіймаєтесь на товсте гілля віковічного фікуса.\\n\"\n"
            "\"Джо та Френк, мов справжні тарзани, за допомогою мотузки перелітають через сигнальну лінію\\n\"\n"
            "\"і безшумно приземляються на м'який мох прямо за спиною вартового. Шлях вільний!"
        ),
        'act2_out2': (
            "\nВи затискаєте акселератор одного з квадроциклів гілкою і спрямовуєте його в хащі.\\n\"\n"
            "\"Двигун реве, машина з тріском ламає кущі. Бандити з криками біжать з'ясовувати ситуацію!\\n\"\n"
            "\"Ви користуєтеся метушнею і проникаєте безпосередньо в шахту."
        ),
        'act3_title': "\n--- АКТ III: ТАЄМНИЧА ШАХТА ТА МІЦНА ГОЛОВА JOE ---",
        'act3_text': (
            "Кам'яні тунелі шахти дихають сирістю та стародавнім мороком.\\n\"\n"
            "\"Ви прокрадаєтеся всередину, але раптом лунає металевий щиголь.\\n\"\n"
            "\"Ви наступили на приховану плиту-пастку! Важка кам'яна колона з барельєфом ягуара\\n\"\n"
            "\"зривається зі стелі та летить прямо на Френка!\\n\"\n"
            "\"Джо блискавично штовхає брата вбік, приймаючи ковзний удар каменю на власну потилицю!\\n\"\n"
            "\"Джо падає на землю непритомним. Бандити, що повернулися, миттєво зачиняють вас\\n\"\n"
            "\"у стародавній залізній клітці конкістадорів, яка підвішена над глибоким колодязем.\\n\\n\"\n"
            "\"За кілька хвилин Джо розплющує очі й потирає потилицю:\\n\"\n"
            "\"— Ох, моя бідна голова... Наче по ній проїхала вантажівка з кокосами. Але не хвилюйтеся,\\n\"\n"
            "\"у мене міцний череп! Бувало й гірше! (Класичний троп нашої родини!)\\n\"\n"
            "\"Клітка починає повільно опускатися вниз на старих іржавих ланцюгах!"
        ),
        'act3_q': "Як ви врятуєтеся з пастки?",
        'act3_opt1': "1. [Дія Джо] Використати важкий металевий уламок лат на підлозі клітки, щоб протаранити кріплення замка грат.",
        'act3_opt2': "2. [Дія Френка] Використати акустичний сканер та шпильку, щоб закоротити електронну лебідку підйомника.",
        'act3_out1_success': (
            "\nДжо хапає залізний уламок і з силою таранного удару б'є по іржавому замку клітки.\\n\"\n"
            "\"Метал не витримує і з брязкотом розлітається! Ви вистрибуєте на уступ колодязя якраз вчасно!"
        ),
        'act3_out1_fail': (
            "\nВи б'єте залізякою по замку, але стародавня ковка тримається напрочуд міцно.\\n\"\n"
            "\"Ви лише набиваєте руки, а клітка опускається все нижче! Спробуйте інший варіант!"
        ),
        'act3_out2_success': (
            "\nФренк дістає свій кишеньковий мультитул і дотягується через грати до кабелю живлення лебідки.\\n\"\n"
            "\"Він спритно перерізає ізоляцію та закорочує контакти. Лебідка з іскрами зупиняється і починає\\n\"\n"
            "\"обертатися у зворотний бік, піднімаючи клітку вгору! Ви вільні!"
        ),
        'act4_title': "\n--- АКТ IV: ФІНАЛЬНИЙ ПРОРИВ КРІЗЬ ВОДОСПАД ---",
        'act4_text': (
            "Ви вибираєтеся назовні і бачите, що лідер викрадачів на прізвисько «Ягуар»\\n\"\n"
            "\"вже тримає в руках золотого ідола і намагається втекти на потужному моторному човні\\n\"\n"
            "\"по бурхливій річці, яка веде безпосередньо до гігантського водоспаду «Глотка Диявола».\\n\"\n"
            "\"Доктор Альварес врятований Четом, але якщо бандит втече з ідолом — реліквія зникне назавжди!"
        ),
        'act4_q': "Як зупинити човен Ягуара перед водоспадом?",
        'act4_opt1': "1. [Шлях Джо] Здійснити екстремальний стрибок з ліани прямо на палубу човна і вступити у відкритий бій.",
        'act4_opt2': "2. [Шлях Френка] Використати важку колоду біля берега та звалити її у воду за допомогою лебідки квадроцикла, перекривши шлях.",
        'act4_out1': (
            "\nДжо розбігається, хапає міцну ліану і здійснює шалений стрибок прямо на борт човна!\\n\"\n"
            "\"Він вибиває штурвал з рук Ягуара. Френк миттєво стрибає слідом, допомагаючи зв'язати лиходія.\\n\"\n"
            "\"Човен успішно зупинено за метр від урвища!"
        ),
        'act4_out2': (
            "\nФренк швидко чіпляє сталевий трос лебідки квадроцикла до сухої колоди та вмикає реверс.\\n\"\n"
            "\"Колода з гуркотом падає у воду, утворюючи надійний бар'єр. Човен Ягуара з силою врізається\\n\"\n"
            "\"в дерево і глухне. Бандита затримано, ідола врятовано!"
        ),
        'final_header': "                 ФІНАЛ                       ",
        'final_high': (
            "Вітаємо! Ви блискуче розкрили справу! Ваш рахунок: {score} очок.\\n\"\n"
            "\"Золотого ідола Коста-Рики повернуто у національний музей, а доктора Альвареса врятовано!\\n\"\n"
            "\"Вдячний археолог влаштовує на вашу честь розкішний костариканський обід з неймовірними\\n\"\n"
            "\"емпанадас та солодким пирогом з ананасами, а Чет Мортон уже придивляється до місцевих десертів!\\n\"\n"
            "\"Бейпортські детективи знову довели свій світовий клас!"
        ),
        'final_normal': (
            "Справу успішно закрито! Ваш рахунок: {score} очок.\\n\"\n"
            "\"Хоча подорож через джунглі була надзвичайно небезпечною, а голова Джо все ще трохи\\n\"\n"
            "\"гуде від зустрічі з колоною, ви врятували доктора і зберегли історичну спадщину!\\n\"\n"
            "\"Попереду на вас чекають нові пригоди!"
        ),
        'final_thanks': "\nДякуємо за гру! Френк та Джо пишалися б вашим детективним талантом."
    },
    'en': {
        'select_lang': "Select Language / Оберіть мову / Выберите язык:\n1. Українська\n2. English\n3. Русский",
        'lang_choice_prompt': "Your choice (1-3): ",
        'press_enter': "Press ENTER to start the adventure...",
        'invalid_input': "Please enter 1 or 2.",
        'intro_text': (
            "You are playing as the famous detective brothers, Frank and Joe Hardy.\n"
            "After solving the Caribbean cruise ship mystery, your ship makes a long stop\n"
            "at Port Limon, Costa Rica. Around you are dark, foggy tropical rainforests,\n"
            "where legends say a golden city of the Jaguar tribe is hidden.\n"
            "But wherever there are treasures, dangerous criminals are sure to follow!"
        ),
        'act1_title': "\n--- ACT I: GALLO PINTO AND THE MYSTERIOUS AMULET ---",
        'act1_text': (
            "You are sitting on a cozy open terrace of the authentic 'El Tucan' cafe.\n"
            "On the table before you is a real tropical feast: traditional gallo pinto\n"
            "(savory black bean rice with coconut milk and spices), sweet fried plantains,\n"
            "freshly baked corn tortillas, ripe slices of mango, papaya, and guava,\n"
            "and huge mugs of strong, freshly brewed Costa Rican coffee. Chet Morton is already\n"
            "finishing his second portion of plantains with heavy cream.\n\n"
            "Suddenly, a local guide boy named Manuel runs up to your table.\n"
            "He throws an ancient clay amulet shaped like a jaguar's head on the table:\n"
            "— Senors! My father, archaeologist Dr. Alvarez, has been kidnapped in the jungle!\n"
            "The kidnappers demand the map of the golden idol hidden in the secret Jaguar outpost!"
        ),
        'act1_q': "How will you start your rescue mission?",
        'act1_opt1': "1. [Frank's Path] Examine the amulet, research micro-glyphs and decode Dr. Alvarez's diary to find a safe path.",
        'act1_opt2': "2. [Joe's Path] Rent powerful off-road ATVs and immediately chase the kidnappers' tire tracks into the jungle.",
        'act1_out1': (
            "\nYou stay at the hotel. Frank studies the clay amulet under a magnifying glass.\n"
            "On the reverse side, you find hidden geographic coordinates and a Latin inscription.\n"
            "Relying on your history knowledge, you calculate a safe path around the deadly swamps.\n"
            "You pack a map, a satellite navigator, a climbing rope, and set off into the forest."
        ),
        'act1_out2': (
            "\nThe roar of ATV engines shatters the silence of the jungle! You decide to act instantly.\n"
            "You speed through the dense thickets, splashing red mud from under the wheels.\n"
            "Chet Morton holds on tight behind you, begging to slow down.\n"
            "You quickly catch up with the heavy tire tracks leading to a mountain slope."
        ),
        'act2_title': "\n--- ACT II: THE DEADLY FOGGY JUNGLE ---",
        'act2_text': (
            "You venture deep into the foggy Monteverde cloud forest. Huge ferns and vines\n"
            "form a solid green wall. Suddenly, you spot the kidnappers' camp ahead.\n"
            "They are holding a tied Dr. Alvarez near the entrance to an abandoned stone mine.\n"
            "The area around the camp is heavily rigged with tripwire alarm traps."
        ),
        'act2_q': "How will you slip past the guard?",
        'act2_opt1': "1. Quietly bypass the camp through the trees, using vines and a strong climbing rope.",
        'act2_opt2': "2. Create a distraction (launch one ATV on autopilot in the opposite direction to lure them away).",
        'act2_out1': (
            "\nYou quickly climb onto a thick branch of an ancient wild fig tree.\n"
            "Joe and Frank swing over the tripwire alarm line like Tarzan using a rope\n"
            "and land silently on the soft moss right behind the guard's back. The way is clear!"
        ),
        'act2_out2': (
            "\nYou jam the accelerator of one ATV with a branch and send it into the thicket.\n"
            "The engine roars, crashing through bushes. The bandits run to investigate the noise!\n"
            "You use the chaos to slip directly into the mine shaft."
        ),
        'act3_title': "\n--- ACT III: THE MYSTERIOUS MINE & JOE'S HARD HEAD ---",
        'act3_text': (
            "The stone tunnels of the mine breathe dampness and ancient darkness.\n"
            "You sneak inside, but suddenly a loud metallic click echoes.\n"
            "You stepped on a hidden trap plate! A heavy stone column with a jaguar relief\n"
            "falls from the ceiling directly towards Frank!\n"
            "Joe instantly shoves his brother aside, taking a glancing blow to his own head!\n"
            "Joe falls unconscious. The returning bandits quickly lock you in an ancient\n"
            "iron conquistador cage suspended over a deep well.\n\n"
            "A few minutes later, Joe opens his eyes and rubs his head:\n"
            "— Ouch, my poor head... Feels like a truck loaded with coconuts hit it. But don't worry,\n"
            "I've got a tough skull! I've had worse! (Classic family trope!)\n"
            "The cage begins to slowly lower down on old rusty chains!"
        ),
        'act3_q': "How will you escape from the lowering cage?",
        'act3_opt1': "1. [Joe's Action] Use a heavy piece of metal armor on the cage floor to ram the rusty lock.",
        'act3_opt2': "2. [Frank's Action] Use an acoustic scanner and a wire to short-circuit the electric winch.",
        'act3_out1_success': (
            "\nJoe grabs the iron plate and rams the rusty lock with full force.\n"
            "The old metal cannot withstand and shatters. You jump to the well ledge just in time!"
        ),
        'act3_out1_fail': (
            "\nYou hit the lock with the metal piece, but the ancient steel holds firm.\n"
            "You only hurt your hands while the cage lowers deeper! Try another option!"
        ),
        'act3_out2_success': (
            "\nFrank pulls out his pocket multitool and reaches through the bars to the winch power cable.\n"
            "He carefully strips the wires and shorts the contacts. The winch stops with sparks\n"
            "and begins to spin in reverse, lifting the cage back up! You are free!"
        ),
        'act4_title': "\n--- ACT IV: THE FINALE AT THE WATERFALL ---",
        'act4_text': (
            "You make your way outside and see the leader of the kidnappers, 'The Jaguar',\n"
            "already holding the golden idol and attempting to escape in a fast motorboat\n"
            "down a wild river leading straight to the massive 'Devil's Throat' waterfall.\n"
            "Dr. Alvarez is saved by Chet, but if the bandit escapes with the idol, it's gone forever!"
        ),
        'act4_q': "How to stop the Jaguar's speedboat before the waterfall?",
        'act4_opt1': "1. [Joe's Action] Make an extreme leap from a vine right onto the boat and engage in a fight.",
        'act4_opt2': "2. [Frank's Action] Use a heavy log on the riverbank, dropping it with the ATV winch to block the river.",
        'act4_out1': (
            "\nJoe runs, grabs a sturdy vine, and swings onto the boat's deck!\n"
            "He knocks the steering wheel out of the Jaguar's hands. Frank jumps right after him,\n"
            "helping to subdue the villain. The boat is successfully stopped a meter from the edge!"
        ),
        'act4_out2': (
            "\nFrank quickly attaches the ATV winch cable to a dry log and activates the reverse.\n"
            "The log crashes into the water, creating a barrier. The speedboat slams into the wood\n"
            "and stalls. The bandit is caught, the golden idol is saved!"
        ),
        'final_header': "                 THE END                     ",
        'final_high': (
            "Congratulations! You solved the case brilliantly! Your score: {score} points.\n"
            "The golden idol of Costa Rica is returned to the museum, and Dr. Alvarez is safe!\n"
            "The grateful archaeologist hosts a magnificent Costa Rican feast in your honor\n"
            "featuring delicious empanadas and pineapple pie, while Chet is already picking dessert!\n"
            "The Bayport detectives have proven their world-class skills once again!"
        ),
        'final_normal': (
            "The case is closed! Your score: {score} points.\n"
            "Although the journey through the jungle was dangerous and Joe's head is still\n"
            "buzzing from the column blow, you saved the doctor and preserved history!\n"
            "More mysteries await you in the future!"
        ),
        'final_thanks': "\nThanks for playing! Frank and Joe would be proud of your detective skills."
    },
    'ru': {
        'select_lang': "Выберите язык / Oберіть мову / Select Language:\n1. Українська\n2. English\n3. Русский",
        'lang_choice_prompt': "Ваш выбор (1-3): ",
        'press_enter': "Нажмите ENTER, чтобы начать приключение...",
        'invalid_input': "Пожалуйста, введите 1 или 2.",
        'intro_text': (
            "Вы играете за известных братьев-детективов Фрэнка и Джо Харди.\n"
            "После раскрытия дела на Карибском лайнере, ваш корабль делает длительную\n"
            "остановку в порту Лимон, Коста-Рика. Вокруг раскинулись дикие, покрытые туманом\n"
            "тропические леса, где по легендам скрыт золотой город племени Ягуара.\n"
            "Но где есть легенды о золоте, там всегда появляются опасные искатели наживы!"
        ),
        'act1_title': "\n--- АКТ I: ГАЛЛО ПИНТО И ТАИНСТВЕННЫЙ АМУЛЕТ ---",
        'act1_text': (
            "Вы сидите на уютной открытой террасе аутентичного кафе «Эль Тукан».\n"
            "Перед вами на столе — настоящий тропический пир: традиционное галло пинто\n"
            "(рис с черной фасолью, кокосовым молоком и специями), сладкие жареные бананы платано,\n"
            "свежевыпеченные кукурузные лепешки тортильяс, ароматные ломтики спелого манго, папайи,\n"
            "а также большие чашки крепкого костариканского кофе. Чет Мортон уже доедает\n"
            "вторую порцию платано со сливками.\n\n"
            "Вдруг к вашему столику подбегает взволнованный местный мальчик-проводник Мануэль.\n"
            "Он бросает на стол старинный глиняный амулет в виде головы ягуара и задыхаясь говорит:\n"
            "— Сеньоры! Моего отца, археолога доктора Альвареса, похитили вооруженные люди в джунглях!\n"
            "Они требуют карту золотого идола, которую он спрятал в тайном форпосте Ягуара!"
        ),
        'act1_q': "Как вы начнете спасательную миссию?",
        'act1_opt1': "1. [Путь Фрэнка] Изучить амулет, исследовать микроглифы и расшифровать дневник доктора, чтобы найти безопасный путь.",
        'act1_opt2': "2. [Путь Джо] Арендовать мощные квадроциклы (ATV) и немедленно броситься в погоню по следам колес похитителей.",
        'act1_out1': (
            "\nВы остаетесь в номере отеля. Фрэнк под лупой изучает глиняный амулет.\n"
            "На обратной стороне вы находите скрытые географические координаты и латинскую надпись.\n"
            "Благодаря знаниям истории, вы вычисляете безопасный путь в обход смертоносных болот.\n"
            "Вы берете карту, спутниковый навигатор, альпинистскую веревку и отправляетесь в лес."
        ),
        'act1_out2': (
            "\nРев моторов квадроциклов разрывает тишину джунглей! Вы решаете действовать мгновенно.\n"
            "Вы летите через густые заросли, разбрызгивая красную грязь из-под колес.\n"
            "Чет Мортон крепко держится сзади, умоляя ехать помедленнее.\n"
            "Вы быстро нагоняете следы тяжелых шин похитителей, ведущие к горному склону."
        ),
        'act2_title': "\n--- АКТ II: СМЕРТОНОСНЫЕ ТУМАННЫЕ ДЖУНГЛИ ---",
        'act2_text': (
            "Вы углубляетесь в туманный облачный лес Монтеверде. Огромные папоротники и лианы\n"
            "образуют сплошную стену. Вдруг впереди вы замечаете лагерь похитителей.\n"
            "Они держат связанного доктора Альвареса у входа в заброшенную каменную шахту.\n"
            "Территория вокруг лагеря усеяна сигнальными растяжками-ловушками."
        ),
        'act2_q': "Как вы проберетесь мимо охраны?",
        'act2_opt1': "1. Попробовать незаметно обойти лагерь по деревьям, используя лианы и прочную веревку (тихий вариант).",
        'act2_opt2': "2. Устроить диверсию (направить один квадроцикл на автопилоте в противоположную сторону, чтобы выманить бандитов).",
        'act2_out1': (
            "\nВы ловко взбираетесь на толстые ветви векового фикуса.\n"
            "Джо и Фрэнк, словно заправские тарзаны, с помощью веревки перелетают через растяжку\n"
            "и бесшумно приземляются на мягкий мох прямо за спиной часового. Путь свободен!"
        ),
        'act2_out2': (
            "\nВы зажимаете педаль газа одного из квадроциклов веткой и направляете его в чащу.\n"
            "Двигатель ревет, круша кусты. Бандиты с криками бегут выяснять, что произошло!\n"
            "Вы пользуетесь суматохой и проникаете непосредственно в шахту."
        ),
        'act3_title': "\n--- АКТ III: ТАИНСТВЕННАЯ ШАХТА И КРЕПКАЯ ГОЛОВА JOE ---",
        'act3_text': (
            "Каменные туннели шахты дышат сыростью и древним мраком.\n"
            "Вы пробираетесь внутрь, но вдруг раздается металлический щелчок.\n"
            "Вы наступили на скрытую плиту-ловушку! Тяжелая каменная колонна с барельефом ягуара\n"
            "срывается с потолка и летит прямо на Фрэнка!\n"
            "Джо молниеносно толкает брата в сторону, принимая скользящий удар камня на свой затылок!\n"
            "Джо падает без чувств. Вернувшиеся бандиты мгновенно запирают вас\n"
            "в древней железной клетке конкистадоров, подвешенной над глубоким колодцем.\n\n"
            "Через несколько минут Джо открывает глаза и потирает затылок:\n"
            "— Ох, моя бедная голова... Как будто по ней грузовик с кокосами проехал. Но не волнуйтесь,\n"
            "у меня крепкий череп! Бывало и хуже! (Классический троп нашей семьи!)\n"
            "Клетка начинает медленно опускаться вниз на старых ржавых цепях!"
        ),
        'act3_q': "Как вы спасетесь из ловушки?",
        'act3_opt1': "1. [Действие Джо] Использовать тяжелый обломок лат на полу клетки, чтобы протаранить замок решетки.",
        'act3_opt2': "2. [Действие Фрэнка] Использовать акустический сканер и проволоку, чтобы закоротить лебедку подъемника.",
        'act3_out1_success': (
            "\nДжо хватает железный облом и со всей силы бьет по ржавому замку клетки.\n"
            "Металл не выдерживает и с дребезгом разлетается! Вы выпрыгиваете на уступ колодца как раз вовремя!"
        ),
        'act3_out1_fail': (
            "\nВы бьете железякой по замку, но древняя ковка держится на удивление крепко.\n"
            "Вы только отбиваете руки, а клетка опускается все ниже! Попробуйте другой вариант!"
        ),
        'act3_out2_success': (
            "\nФрэнк достает свой карманный мультитул и тянется через решетку к кабелю питания лебедки.\n"
            "Он ловко зачищает провода и закорачивает контакты. Лебедка с искрами останавливается\n"
            "и начинает вращаться в обратную сторону, поднимая вас вверх! Вы свободны!"
        ),
        'act4_title': "\n--- АКТ IV: ФИНАЛЬНЫЙ ПРОРЫВ СКВОЗЬ ВОДОПАД ---",
        'act4_text': (
            "Вы выбираетесь наружу и видите, что лидер похитителей по кличке «Ягуар»\n"
            "уже держит в руках золотого идола и пытается сбежать на быстроходной моторной лодке\n"
            "по бурной реке, ведущей прямо к гигантскому водопаду «Глотка Дьявола».\n"
            "Доктор Альварес спасен Четом, но если бандит сбежит с идолом — реликвия исчезнет навсегда!"
        ),
        'act4_q': "Как остановить лодку Ягуара перед водопадом?",
        'act4_opt1': "1. [Путь Джо] Совершить экстремальный прыжок с лианы прямо на палубу лодки и вступить в открытый бой.",
        'act4_opt2': "2. [Путь Фрэнка] Использовать тяжелое бревно у берега и свалить его в воду лебедкой квадроцикла, преградив путь.",
        'act4_out1': (
            "\nДжо разбегается, хватает прочную лиану и совершает безумный прыжок прямо на борт лодки!\n"
            "Он выбивает штурвал из рук Ягуара. Фрэнк мгновенно прыгает следом, помогая связать злодея.\n"
            "Лодка успешно остановлена в метре от обрыва!"
        ),
        'act4_out2': (
            "\nФрэнк быстро цепляет стальной трос лебедки квадроцикла к сухому бревну и включает реверс.\n"
            "Бревно с грохотом падает в воду, образуя барьер. Скоростная лодка Ягуара с силой врезается\n"
            "в дерево и глохнет. Бандит задержан, идол спасен!"
        ),
        'final_header': "                 ФИНАЛ                       ",
        'final_high': (
            "Поздравляем! Вы блестяще раскрыли дело! Ваш счет: {score} очков.\n"
            "Золотой идол Коста-Рики возвращен в музей, а доктор Альварес спасен!\n"
            "Благодарный археолог устраивает в вашу честь роскошный костариканский обед\n"
            "с великолепными эмпанадас и пирогом с ананасами, а Чет уже присматривает десерт!\n"
            "Бейпортские детективы снова доказали свой мировой класс!"
        ),
        'final_normal': (
            "Дело успешно закрыто! Ваш счет: {score} очок.\n"
            "Хотя путешествие по джунглям было смертельно опасным, а голова Джо все еще немного\n"
            "гудит от встречи с колонной, вы спасли доктора и сохранили историческое наследие!\n"
            "Впереди вас ждут новые приключения!"
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
            state.inventory.append('map')
            state.inventory.append('rope')
            print_slow(loc['act1_out1'])
            break
        elif choice == '2':
            state.route_taken = 'joe'
            state.score += 15
            state.inventory.append('atv')
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
            state.stealth_success = True
            state.score += 25
            print_slow(loc['act2_out1'])
            break
        elif choice == '2':
            state.stealth_success = False
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
            if state.route_taken == 'joe' or 'atv' in state.inventory:
                state.score += 20
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
