TRANSLATION_SRC = "ؠػػؽؾؿكيٮٯٷٸٹٺٻټٽٿڀځٵٶٷٸٹٺٻټٽٿڀځڂڅڇڈډڊڋڌڍڎڏڐڑڒړڔڕږڗڙښڛڜڝڞڟڠڡڢڣڤڥڦڧڨڪګڬڭڮڰڱڲڳڴڵڶڷڸڹںڻڼڽھڿہۂۃۄۅۆۇۈۉۊۋۏۍێېۑےۓەۮۯۺۻۼۿݐݑݒݓݔݕݖݗݘݙݚݛݜݝݞݟݠݡݢݣݤݥݦݧݨݩݪݫݬݭݮݯݰݱݲݳݴݵݶݷݸݹݺݻݼݽݾݿࢠࢡࢢࢣࢤࢥࢦࢧࢨࢩࢪࢫࢮࢯࢰࢱࢬࢲࢳࢴࢶࢷࢸࢹࢺࢻࢼࢽﭐﭑﭒﭓﭔﭕﭖﭗﭘﭙﭚﭛﭜﭝﭞﭟﭠﭡﭢﭣﭤﭥﭦﭧﭨﭩﭮﭯﭰﭱﭲﭳﭴﭵﭶﭷﭸﭹﭺﭻﭼﭽﭾﭿﮀﮁﮂﮃﮄﮅﮆﮇﮈﮉﮊﮋﮌﮍﮎﮏﮐﮑﮒﮓﮔﮕﮖﮗﮘﮙﮚﮛﮜﮝﮞﮟﮠﮡﮢﮣﮤﮥﮦﮧﮨﮩﮪﮫﮬﮭﮮﮯﮰﮱﺀﺁﺃﺄﺅﺆﺇﺈﺉﺊﺋﺌﺍﺎﺏﺐﺑﺒﺕﺖﺗﺘﺙﺚﺛﺜﺝﺞﺟﺠﺡﺢﺣﺤﺥﺦﺧﺨﺩﺪﺫﺬﺭﺮﺯﺰﺱﺲﺳﺴﺵﺶﺷﺸﺹﺺﺻﺼﺽﺾﺿﻀﻁﻂﻃﻄﻅﻆﻇﻈﻉﻊﻋﻌﻍﻎﻏﻐﻑﻒﻓﻔﻕﻖﻗﻘﻙﻚﻛﻜﻝﻞﻟﻠﻡﻢﻣﻤﻥﻦﻧﻨﻩﻪﻫﻬﻭﻮﻯﻰﻱﻲﻳﻴىكيﺂﯽﯼ“” "
TRANSLATION_DST = 'یککیییکیبقویتتبتتتبحاوویتتبتتتبحححچدددددددددررررررررسسسصصطعففففففققکککککگگگگگللللنننننهچهههوووووووووییییییهدرشضغهبببببببححددرسعععففکککممنننلررسححسرحاایییووییحسسکببجطفقلمییرودصگویزعکبپتریفقنااببببپپپپببببتتتتتتتتتتتتففففححححححححچچچچچچچچددددددددژژررککککگگگگگگگگگگگگننننننههههههههههییییءاااووااییییااببببتتتتثثثثججججححححخخخخددذذررززسسسسششششصصصصضضضضططططظظظظععععغغغغففففققققککککللللممممننننههههوویییییییکیایی"" '

NUMBERS_SRC = "0123456789%٠١٢٣٤٥٦٧٨٩"
NUMBERS_DST = "۰۱۲۳۴۵۶۷۸۹٪۰۱۲۳۴۵۶۷۸۹"

PUNC_AFTER = r"\.:!،؛؟»\]\)\}"
PUNC_BEFORE = r"«\[\(\{"

EXTRA_SPACE_PATTERNS = [
    (r"^ +| +$", ""),
    (r" {2,}", " "),  # remove extra spaces
    (r"\n{3,}", "\n\n"),  # remove extra newlines
    (r"\u200c{2,}", "\u200c"),  # remove extra ZWNJs
    (r"\u200c{1,} ", " "),  # remove unneded ZWNJs before space
    (r" \u200c{1,}", " "),  # remove unneded ZWNJs after space
    (r"\b\u200c*\B", ""),  # remove unneded ZWNJs at the beginning of words
    (r"\B\u200c*\b", ""),  # remove unneded ZWNJs at the end of words
    (r"[ـ\r]", ""),  # remove keshide, carriage returns
]

PUNCTUATION_SPACING_PATTERNS = [
    # remove space before and after quotation
    (r'" ([^\n"]+) "', r'"\1"'),
    (f" ([{PUNC_AFTER}])", r"\1"),  # remove space before
    (f"([{PUNC_BEFORE}]) ", r"\1"),  # remove space after
    # put space after . and :
    (f"([{PUNC_AFTER[:3]}])([^ {PUNC_AFTER}" + r"\d۰۱۲۳۴۵۶۷۸۹])", r"\1 \2"),
    (f"([{PUNC_AFTER[3:]}])([^ {PUNC_AFTER}])", r"\1 \2"),  # put space after
    (f"([^ {PUNC_BEFORE}])([{PUNC_BEFORE}])", r"\1 \2"),  # put space before
    # put space after number
    (r"(\d)([آابپتثجچحخدذرزژسشصضطظعغفقکگلمنوهی])", r"\1 \2"),
    (r"([آابپتثجچحخدذرزژسشصضطظعغفقکگلمنوهی])(\d)", r"\1 \2"),
]

AFFIX_SPACING_PATTERNS = [
    (r"([^ ]ه) ی ", r"\1‌ی "),  # fix ی space
    (r"(^| )(ن?می) ", r"\1\2‌"),  # put zwnj after می, نمی
    (
        r"(?<=[^\n\d "
        + PUNC_AFTER
        + PUNC_BEFORE
        + r"]{2}) (تر(ین?)?|گری?|های?)(?=[ \n"
        + PUNC_AFTER
        + PUNC_BEFORE
        + r"]|$)",
        r"‌\1",
    ),
    (
        r"([^ ]ه) (ا(م|یم|ش|ند|ی|ید|ت))(?=[ \n" + PUNC_AFTER + r"]|$)",
        r"\1‌\2",
    ),
    (r"(ه)(ها)", r"\1‌\2"),
]

PERSIAN_STYLE_PATTERNS = [
    (r'"([^\n"]+)"', r"«\1»"),
    (r"(\d+)\.(\d+)", r"\1٫\2"),
    (r" ?\.\.\.", " …"),
]

DIACRITICS_PATTERNS = [
    (r"[\u064b\u064c\u064d\u064e\u064f\u0650\u0651\u0652]", ""),
]

SPECIAL_CHARS_PATTERNS = [
    (r"[\u0605\u0653\u0654\u0655\u0656\u0657\u0658\u0659\u065a\u065b\u065c\u065d\u065e\u065f\u0670\u0610\u0611\u0612\u0613\u0614\u0615\u0616\u0618\u0619\u061a\u061e\u06d4\u06d6\u06d7\u06d8\u06d9\u06da\u06db\u06dc\u06dd\u06de\u06df\u06e0\u06e1\u06e2\u06e3\u06e4\u06e5\u06e6\u06e7\u06e8\u06e9\u06ea\u06eb\u06ec\u06ed\u06fd\u06fe\u08ad\u08d4\u08d5\u08d6\u08d7\u08d8\u08d9\u08da\u08db\u08dc\u08dd\u08de\u08df\u08e0\u08e1\u08e2\u08e3\u08e4\u08e5\u08e6\u08e7\u08e8\u08e9\u08ea\u08eb\u08ec\u08ed\u08ee\u08ef\u08f0\u08f1\u08f2\u08f3\u08f4\u08f5\u08f6\u08f7\u08f8\u08f9\u08fa\u08fb\u08fc\u08fd\u08fe\u08ff\ufbb2\ufbb3\ufbb4\ufbb5\ufbb6\ufbb7\ufbb8\ufbb9\ufbba\ufbbb\ufbbc\ufbbd\ufbbe\ufbbf\ufbc0\ufbc1\ufc5e\ufc5f\ufc60\ufc61\ufc62\ufc63\ufcf2\ufcf3\ufcf4\ufd3e\ufd3f\ufe70\ufe71\ufe72\ufe76\ufe77\ufe78\ufe79\ufe7a\ufe7b\ufe7c\ufe7d\ufe7e\ufe7f\ufdfa\ufdfb]", ""),
]

UNICODE_REPLACEMENTS = [
    ("﷽", "بسم الله الرحمن الرحیم"),
    ("﷼", "ریال"),
    ("(ﷰ|ﷹ)", "صلی"),
    ("ﷲ", "الله"),
    ("ﷳ", "اکبر"),
    ("ﷴ", "محمد"),
    ("ﷵ", "صلعم"),
    ("ﷶ", "رسول"),
    ("ﷷ", "علیه"),
    ("ﷸ", "وسلم"),
    ("ﻵ|ﻶ|ﻷ|ﻸ|ﻹ|ﻺ|ﻻ|ﻼ", "لا"),
]

SUFFIXES = {
    "ی", "ای", "ها", "های", "هایی", "تر", "تری", "ترین", "گر", "گری",
    "ام", "ات", "اش", "یم", "ید", "ند", "مان", "تان", "شان",
    "هایمان", "هایتان", "هایشان", "ان", "ین",
    "م", "ت", "ش",
}

