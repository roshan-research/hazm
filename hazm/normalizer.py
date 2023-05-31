"""این ماژول شامل کلاس‌ها و توابعی برای نرمال‌سازی متن است."""


import re
from typing import List

from hazm import Lemmatizer
from hazm import WordTokenizer
from hazm import maketrans
from hazm import regex_replace


class Normalizer:
    """این کلاس شامل توابعی برای نرمال‌سازی متن است.

    Args:
        correct_spacing: اگر `True‍` فاصله‌گذاری‌ها را در متن، نشانه‌های سجاوندی و پیشوندها و پسوندها اصلاح می‌کند.
        remove_diacritics: اگر `True` باشد اعرابِ حروف را حذف می‌کند.
        remove_specials_chars: اگر `True` باشد برخی از کاراکترها و نشانه‌های خاص را که کاربردی در پردازش متن ندارند حذف می‌کند.
        decrease_repeated_chars: اگر `True` باشد تکرارهای بیش از ۲ بار را به ۲ بار کاهش می‌دهد. مثلاً «سلاممم» را به «سلامم» تبدیل می‌کند.
        persian_style: اگر `True` باشد اصلاحات مخصوص زبان فارسی را انجام می‌دهد؛ مثلاً جایگزین‌کردن کوتیشن با گیومه.
        persian_numbers: اگر `True` باشد ارقام انگلیسی را با فارسی جایگزین می‌کند.
        unicodes_replacement: اگر `True` باشد برخی از کاراکترهای یونیکد را با معادل نرمال‌شدهٔ آن جایگزین می‌کند.
        seperate_mi: اگر `True` باشد پیشوند «می» و «نمی» را در افعال جدا می‌کند.

    """

    def __init__(
        self: "Normalizer",
        correct_spacing: bool = True,
        remove_diacritics: bool = True,
        remove_specials_chars: bool = True,
        decrease_repeated_chars: bool = True,
        persian_style: bool = True,
        persian_numbers: bool = True,
        unicodes_replacement: bool = True,
        seperate_mi: bool = True,
    ) -> None:
        self._correct_spacing = correct_spacing
        self._remove_diacritics = remove_diacritics
        self._remove_specials_chars = remove_specials_chars
        self._decrease_repeated_chars = decrease_repeated_chars
        self._persian_style = persian_style
        self._persian_number = persian_numbers
        self._unicodes_replacement = unicodes_replacement
        self._seperate_mi = seperate_mi

        self.translation_src = "ؠػػؽؾؿكيٮٯٷٸٹٺٻټٽٿڀځٵٶٷٸٹٺٻټٽٿڀځڂڅڇڈډڊڋڌڍڎڏڐڑڒړڔڕږڗڙښڛڜڝڞڟڠڡڢڣڤڥڦڧڨڪګڬڭڮڰڱڲڳڴڵڶڷڸڹںڻڼڽھڿہۂۃۄۅۆۇۈۉۊۋۏۍێېۑےۓەۮۯۺۻۼۿݐݑݒݓݔݕݖݗݘݙݚݛݜݝݞݟݠݡݢݣݤݥݦݧݨݩݪݫݬݭݮݯݰݱݲݳݴݵݶݷݸݹݺݻݼݽݾݿࢠࢡࢢࢣࢤࢥࢦࢧࢨࢩࢪࢫࢮࢯࢰࢱࢬࢲࢳࢴࢶࢷࢸࢹࢺࢻࢼࢽﭐﭑﭒﭓﭔﭕﭖﭗﭘﭙﭚﭛﭜﭝﭞﭟﭠﭡﭢﭣﭤﭥﭦﭧﭨﭩﭮﭯﭰﭱﭲﭳﭴﭵﭶﭷﭸﭹﭺﭻﭼﭽﭾﭿﮀﮁﮂﮃﮄﮅﮆﮇﮈﮉﮊﮋﮌﮍﮎﮏﮐﮑﮒﮓﮔﮕﮖﮗﮘﮙﮚﮛﮜﮝﮞﮟﮠﮡﮢﮣﮤﮥﮦﮧﮨﮩﮪﮫﮬﮭﮮﮯﮰﮱﺀﺁﺃﺄﺅﺆﺇﺈﺉﺊﺋﺌﺍﺎﺏﺐﺑﺒﺕﺖﺗﺘﺙﺚﺛﺜﺝﺞﺟﺠﺡﺢﺣﺤﺥﺦﺧﺨﺩﺪﺫﺬﺭﺮﺯﺰﺱﺲﺳﺴﺵﺶﺷﺸﺹﺺﺻﺼﺽﺾﺿﻀﻁﻂﻃﻄﻅﻆﻇﻈﻉﻊﻋﻌﻍﻎﻏﻐﻑﻒﻓﻔﻕﻖﻗﻘﻙﻚﻛﻜﻝﻞﻟﻠﻡﻢﻣﻤﻥﻦﻧﻨﻩﻪﻫﻬﻭﻮﻯﻰﻱﻲﻳﻴىكي“” "
        self.translation_dst = (
            'یککیییکیبقویتتبتتتبحاوویتتبتتتبحححچدددددددددررررررررسسسصصطعففففففققکککککگگگگگللللنننننهچهههوووووووووییییییهدرشضغهبببببببححددرسعععففکککممنننلررسححسرحاایییووییحسسکببجطفقلمییرودصگویزعکبپتریفقنااببببپپپپببببتتتتتتتتتتتتففففححححححححچچچچچچچچددددددددژژررککککگگگگگگگگگگگگننننننههههههههههییییءاااووااییییااببببتتتتثثثثججججححححخخخخددذذررززسسسسششششصصصصضضضضططططظظظظععععغغغغففففققققککککللللممممننننههههوویییییییکی"" '
        )

        if self._correct_spacing or self._decrease_repeated_chars:
            self.tokenizer = WordTokenizer(join_verb_parts=False)
            self.words = self.tokenizer.words

        if self._persian_number:
            self.number_translation_src = "0123456789%٠١٢٣٤٥٦٧٨٩"
            self.number_translation_dst = "۰۱۲۳۴۵۶۷۸۹٪۰۱۲۳۴۵۶۷۸۹"

        if self._correct_spacing:
            self.suffixes = {
                "ی",
                "ای",
                "ها",
                "های",
                "تر",
                "تری",
                "ترین",
                "گر",
                "گری",
                "ام",
                "ات",
                "اش",
            }

            self.extra_space_patterns = [
                (r" {2,}", " "),  # remove extra spaces
                (r"\n{3,}", "\n\n"),  # remove extra newlines
                (r"\u200c{2,}", "\u200c"),  # remove extra ZWNJs
                (r"\u200c{1,} ", " "),  # remove unneded ZWNJs before space
                (r" \u200c{1,}", " "),  # remove unneded ZWNJs after space
                (r"\b\u200c*\B", ""),  # remove unneded ZWNJs at the beginning of words
                (r"\B\u200c*\b", ""),  # remove unneded ZWNJs at the end of words
                (r"[ـ\r]", ""),  # remove keshide, carriage returns
            ]

            punc_after, punc_before = r"\.:!،؛؟»\]\)\}", r"«\[\(\{"

            self.punctuation_spacing_patterns = [
                # remove space before and after quotation
                ('" ([^\n"]+) "', r'"\1"'),
                (" ([" + punc_after + "])", r"\1"),  # remove space before
                ("([" + punc_before + "]) ", r"\1"),  # remove space after
                # put space after . and :
                (
                    "([" + punc_after[:3] + "])([^ " + punc_after + r"\d۰۱۲۳۴۵۶۷۸۹])",
                    r"\1 \2",
                ),
                (
                    "([" + punc_after[3:] + "])([^ " + punc_after + "])",
                    r"\1 \2",
                ),  # put space after
                (
                    "([^ " + punc_before + "])([" + punc_before + "])",
                    r"\1 \2",
                ),  # put space before
                # put space after number; e.g., به طول ۹متر -> به طول ۹ متر
                (r"(\d)([آابپتثجچحخدذرزژسشصضطظعغفقکگلمنوهی])", r"\1 \2"),
                # put space after number; e.g., به طول۹ -> به طول ۹
                (r"([آابپتثجچحخدذرزژسشصضطظعغفقکگلمنوهی])(\d)", r"\1 \2"),
            ]

            self.affix_spacing_patterns = [
                (r"([^ ]ه) ی ", r"\1‌ی "),  # fix ی space
                (r"(^| )(ن?می) ", r"\1\2‌"),  # put zwnj after می, نمی
                # put zwnj before تر, تری, ترین, گر, گری, ها, های
                (
                    r"(?<=[^\n\d "
                    + punc_after
                    + punc_before
                    + "]{2}) (تر(ین?)?|گری?|های?)(?=[ \n"
                    + punc_after
                    + punc_before
                    + "]|$)",
                    r"‌\1",
                ),
                # join ام, ایم, اش, اند, ای, اید, ات
                (
                    r"([^ ]ه) (ا(م|یم|ش|ند|ی|ید|ت))(?=[ \n" + punc_after + "]|$)",
                    r"\1‌\2",
                ),
                # شنبهها => شنبه‌ها
                ("(ه)(ها)", r"\1‌\2"),
            ]

        if self._persian_style:
            self.persian_style_patterns = [
                ('"([^\n"]+)"', r"«\1»"),  # replace quotation with gyoome
                (r"([\d+])\.([\d+])", r"\1٫\2"),  # replace dot with momayez
                (r" ?\.\.\.", " …"),  # replace 3 dots
            ]

        if self._decrease_repeated_chars:
            self.more_than_two_repeat_pattern = (
                r"([آابپتثجچحخدذرزژسشصضطظعغفقکگلمنوهی])\1{2,}"
            )
            self.repeated_chars_pattern = (
                r"[آابپتثجچحخدذرزژسشصضطظعغفقکگلمنوهی]*"
                + self.more_than_two_repeat_pattern
                + "[آابپتثجچحخدذرزژسشصضطظعغفقکگلمنوهی]*"
            )

        if self._remove_diacritics:
            self.diacritics_patterns = [
                # remove FATHATAN, DAMMATAN, KASRATAN, FATHA, DAMMA, KASRA, SHADDA, SUKUN
                ("[\u064b\u064c\u064d\u064e\u064f\u0650\u0651\u0652]", ""),
            ]

        if self._remove_specials_chars:
            self.specials_chars_patterns = [
                # Remove almoast all arabic unicode superscript and subscript characters in the ranges of 00600-06FF, 08A0-08FF, FB50-FDFF, and FE70-FEFF
                (
                    "[\u0605\u0653\u0654\u0655\u0656\u0657\u0658\u0659\u065a\u065b\u065c\u065d\u065e\u065f\u0670\u0610\u0611\u0612\u0613\u0614\u0615\u0616\u0618\u0619\u061a\u061e\u06d4\u06d6\u06d7\u06d8\u06d9\u06da\u06db\u06dc\u06dd\u06de\u06df\u06e0\u06e1\u06e2\u06e3\u06e4\u06e5\u06e6\u06e7\u06e8\u06e9\u06ea\u06eb\u06ec\u06ed\u06fd\u06fe\u08ad\u08d4\u08d5\u08d6\u08d7\u08d8\u08d9\u08da\u08db\u08dc\u08dd\u08de\u08df\u08e0\u08e1\u08e2\u08e3\u08e4\u08e5\u08e6\u08e7\u08e8\u08e9\u08ea\u08eb\u08ec\u08ed\u08ee\u08ef\u08f0\u08f1\u08f2\u08f3\u08f4\u08f5\u08f6\u08f7\u08f8\u08f9\u08fa\u08fb\u08fc\u08fd\u08fe\u08ff\ufbb2\ufbb3\ufbb4\ufbb5\ufbb6\ufbb7\ufbb8\ufbb9\ufbba\ufbbb\ufbbc\ufbbd\ufbbe\ufbbf\ufbc0\ufbc1\ufc5e\ufc5f\ufc60\ufc61\ufc62\ufc63\ufcf2\ufcf3\ufcf4\ufd3e\ufd3f\ufe70\ufe71\ufe72\ufe76\ufe77\ufe78\ufe79\ufe7a\ufe7b\ufe7c\ufe7d\ufe7e\ufe7f\ufdfa\ufdfb]",
                    "",
                ),
            ]

        if self._seperate_mi:
            self.verbs = Lemmatizer(joined_verb_parts=False).verbs
            self.joint_mi_patterns = r"\bن?می[آابپتثجچحخدذرزژسشصضطظعغفقکگلمنوهی]+"

        if self._unicodes_replacement:
            self.replacements = [
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

    def normalize(self: "Normalizer", text: str) -> str:
        """متن را نرمال‌سازی می‌کند.

        Examples:
            >>> normalizer = Normalizer()
            >>> normalizer.normalize('اِعلاممممم کَرد : « زمین لرزه ای به بُزرگیِ 6 دهم ریشتر ...»')
            'اعلام کرد: «زمین‌لرزه‌ای به بزرگی ۶ دهم ریشتر …»'
            >>> normalizer.normalize('')
            ''

        Args:
            text: متنی که باید نرمال‌سازی شود.

        Returns:
            متنِ نرمال‌سازی‌شده.

        """
        translations = maketrans(self.translation_src, self.translation_dst)
        text = text.translate(translations)

        if self._persian_style:
            text = self.persian_style(text)

        if self._persian_number:
            text = self.persian_number(text)

        if self._remove_diacritics:
            text = self.remove_diacritics(text)

        if self._correct_spacing:
            text = self.correct_spacing(text)

        if self._unicodes_replacement:
            text = self.unicodes_replacement(text)

        if self._remove_specials_chars:
            text = self.remove_specials_chars(text)

        if self._decrease_repeated_chars:
            text = self.decrease_repeated_chars(text)

        if self._seperate_mi:
            text = self.seperate_mi(text)

        return text

    def correct_spacing(self: "Normalizer", text: str) -> str:
        """فاصله‌گذاری‌ها را در پیشوندها و پسوندها اصلاح می‌کند.

        Examples:
            >>> normalizer = Normalizer()
            >>> normalizer.correct_spacing("سلام   دنیا")
            'سلام دنیا'
            >>> normalizer.correct_spacing("به طول ۹متر و عرض۶")
            'به طول ۹ متر و عرض ۶'
            >>> normalizer.correct_spacing("کاروان‌‌سرا")
            'کاروان‌سرا'
            >>> normalizer.correct_spacing("‌سلام‌ به ‌همه‌")
            'سلام به همه'
            >>> normalizer.correct_spacing("سلام دنیـــا")
            'سلام دنیا'
            >>> normalizer.correct_spacing("جمعهها که کار نمی کنم مطالعه می کنم")
            'جمعه‌ها که کار نمی‌کنم مطالعه می‌کنم'
            >>> normalizer.correct_spacing(' "سلام به همه"   ')
            '"سلام به همه"'
            >>> normalizer.correct_spacing('')
            ''

        Args:
            text (str): متنی که باید فاصله‌گذاری‌های آن اصلاح شود.

        Returns:
            (str): متنی با فاصله‌گذاری‌های اصلاح‌شده.


        """
        text = regex_replace(self.extra_space_patterns, text)

        lines = text.split("\n")
        result = []
        for line in lines:
            tokens = self.tokenizer.tokenize(line)
            spaced_tokens = self.token_spacing(tokens)
            line = " ".join(spaced_tokens)
            result.append(line)

        text = "\n".join(result)

        text = regex_replace(self.affix_spacing_patterns, text)
        text = regex_replace(self.punctuation_spacing_patterns, text)

        return text

    def remove_diacritics(self: "Normalizer", text: str) -> str:
        """اِعراب را از متن حذف می‌کند.

        Examples:
            >>> normalizer = Normalizer()
            >>> normalizer.remove_diacritics('حَذفِ اِعراب')
            'حذف اعراب'
            >>> normalizer.remove_diacritics('آمدند')
            'آمدند'
            >>> normalizer.remove_diacritics('متن بدون اعراب')
            'متن بدون اعراب'
            >>> normalizer.remove_diacritics('')
            ''

        Args:
            text: متنی که باید اعراب آن حذف شود.

        Returns:
            متنی بدون اعراب.

        """
        return regex_replace(self.diacritics_patterns, text)

    def remove_specials_chars(self: "Normalizer", text: str) -> str:
        """برخی از کاراکترها و نشانه‌های خاص را که کاربردی در پردازش متن ندارند حذف
        می‌کند.

        Examples:
            >>> normalizer = Normalizer()
            >>> normalizer.remove_specials_chars('پیامبر اکرم ﷺ')
            'پیامبر اکرم '

        Args:
            text: متنی که باید کاراکترها و نشانه‌های اضافهٔ آن حذف شود.

        Returns:
            متنی بدون کاراکترها و نشانه‌های اضافه.

        """
        return regex_replace(self.specials_chars_patterns, text)

    def decrease_repeated_chars(self: "Normalizer", text: str) -> str:
        """تکرارهای زائد حروف را در کلماتی مثل سلامممممم حذف می‌کند و در مواردی که
        نمی‌تواند تشخیص دهد دست کم به دو تکرار کاهش می‌دهد.

        Examples:
            >>> normalizer = Normalizer()
            >>> normalizer.decrease_repeated_chars('سلامممم به همه')
            'سلام به همه'
            >>> normalizer.decrease_repeated_chars('سلامم به همه')
            'سلامم به همه'
            >>> normalizer.decrease_repeated_chars('سلامم را برسان')
            'سلامم را برسان'
            >>> normalizer.decrease_repeated_chars('سلاممم را برسان')
            'سلام را برسان'
            >>> normalizer.decrease_repeated_chars('')
            ''

        Args:
            text: متنی که باید تکرارهای زائد آن حذف شود.

        Returns:
            متنی بدون کاراکترهای زائد یا حداقل با دو تکرار.

        """
        matches = re.finditer(self.repeated_chars_pattern, text)

        for m in matches:
            word = m.group()
            if word not in self.words:
                no_repeat = re.sub(self.more_than_two_repeat_pattern, r"\1", word)
                two_repeat = re.sub(self.more_than_two_repeat_pattern, r"\1\1", word)

                if (no_repeat in self.words) != (two_repeat in self.words):
                    r = no_repeat if no_repeat in self.words else two_repeat
                    text = text.replace(word, r)
                else:
                    text = text.replace(word, two_repeat)

        return text

    def persian_style(self: "Normalizer", text: str) -> str:
        """برخی از حروف و نشانه‌ها را با حروف و نشانه‌های فارسی جایگزین می‌کند.

        Examples:
            >>> normalizer = Normalizer()
            >>> normalizer.persian_style('"نرمال‌سازی"')
            '«نرمال‌سازی»'
            >>> normalizer.persian_style('و ...')
            'و …'
            >>> normalizer.persian_style('10.450')
            '10٫450'
            >>> normalizer.persian_style('')
            ''

        Args:
            text: متنی که باید حروف و نشانه‌های آن با حروف و نشانه‌های فارسی جایگزین شود.

        Returns:
            متنی با حروف و نشانه‌های فارسی‌سازی شده.

        """
        return regex_replace(self.persian_style_patterns, text)

    def persian_number(self: "Normalizer", text: str) -> str:
        """اعداد لاتین و علامت % را با معادل فارسی آن جایگزین می‌کند.

        Examples:
            >>> normalizer = Normalizer()
            >>> normalizer.persian_number('5 درصد')
            '۵ درصد'
            >>> normalizer.persian_number('۵ درصد')
            '۵ درصد'
            >>> normalizer.persian_number('')
            ''

        Args:
            text: متنی که باید اعداد لاتین و علامت % آن با معادل فارسی جایگزین شود.

        Returns:
            متنی با اعداد و علامت ٪ فارسی.

        """
        translations = maketrans(
            self.number_translation_src,
            self.number_translation_dst,
        )
        return text.translate(translations)

    def unicodes_replacement(self: "Normalizer", text: str) -> str:
        """برخی از کاراکترهای خاص یونیکد را با معادلِ نرمال آن جایگزین می‌کند. غالباً
        این کار فقط در مواردی صورت می‌گیرد که یک کلمه در قالب یک کاراکتر یونیکد تعریف
        شده است.

        **فهرست این کاراکترها و نسخهٔ جایگزین آن:**

        |کاراکتر|نسخهٔ جایگزین|
        |--------|------------------|
        |﷽|بسم الله الرحمن الرحیم|
        |﷼|ریال|
        |ﷰ، ﷹ|صلی|
        |ﷲ|الله|
        |ﷳ|اکبر|
        |ﷴ|محمد|
        |ﷵ|صلعم|
        |ﷶ|رسول|
        |ﷷ|علیه|
        |ﷸ|وسلم|
        |ﻵ، ﻶ، ﻷ، ﻸ، ﻹ، ﻺ، ﻻ، ﻼ|لا|

        Examples:
            >>> normalizer = Normalizer()
            >>> normalizer.remove_specials_chars('پیامبر اکرم ﷺ')
            'پیامبر اکرم '
            >>> normalizer.remove_specials_chars('')
            ''

        Args:
            text: متنی که باید برخی از کاراکترهای یونیکد آن (جدول بالا)، با شکل استاندارد، جایگزین شود.

        Returns:
            متنی که برخی از کاراکترهای یونیکد آن با شکل استاندارد جایگزین شده است.

        """
        for old, new in self.replacements:
            text = re.sub(old, new, text)

        return text

    def seperate_mi(self: "Normalizer", text: str) -> str:
        """پیشوند «می» و «نمی» را در افعال جدا کرده و با نیم‌فاصله می‌چسباند.

        Examples:
            >>> normalizer = Normalizer()
            >>> normalizer.seperate_mi('نمیدانم چه میگفت')
            'نمی‌دانم چه می‌گفت'
            >>> normalizer.seperate_mi('میز')
            'میز'
            >>> normalizer.seperate_mi('')
            ''


        Args:
            text: متنی که باید پیشوند «می» و «نمی» در آن جدا شود.

        Returns:
            متنی با «می» و «نمی» جدا شده.

        """
        matches = re.findall(r"\bن?می[آابپتثجچحخدذرزژسشصضطظعغفقکگلمنوهی]+", text)
        for m in matches:
            r = re.sub("^(ن?می)", r"\1‌", m)
            if r in self.verbs:
                text = text.replace(m, r)

        return text

    def token_spacing(self: "Normalizer", tokens: List[str]) -> List[str]:
        """توکن‌های ورودی را به فهرستی از توکن‌های نرمال‌سازی شده تبدیل می‌کند.
        در این فرایند ممکن است برخی از توکن‌ها به یکدیگر بچسبند؛
        برای مثال: `['زمین', 'لرزه', 'ای']` تبدیل می‌شود به: `['زمین‌لرزه‌ای']`.

        Examples:
            >>> normalizer = Normalizer()
            >>> normalizer.token_spacing(['کتاب', 'ها'])
            ['کتاب‌ها']
            >>> normalizer.token_spacing(['او', 'می', 'رود'])
            ['او', 'می‌رود']
            >>> normalizer.token_spacing(['ماه', 'می', 'سال', 'جدید'])
            ['ماه', 'می', 'سال', 'جدید']
            >>> normalizer.token_spacing(['اخلال', 'گر'])
            ['اخلال‌گر']
            >>> normalizer.token_spacing(['زمین', 'لرزه', 'ای'])
            ['زمین‌لرزه‌ای']
            >>> normalizer.token_spacing([])
            []

        Args:
            tokens: توکن‌هایی که باید نرمال‌سازی شود.

        Returns:
            لیستی از توکن‌های نرمال‌سازی شده به شکل `[token1, token2, ...]`.

        """
        # >>> normalizer.token_spacing(['پرداخت', 'شده', 'است'])

        result = []
        for t, token in enumerate(tokens):
            joined = False

            if result:
                token_pair = result[-1] + "‌" + token
                if (
                    token_pair in self.verbs
                    or token_pair in self.words
                    and self.words[token_pair][0] > 0
                ):
                    joined = True

                    if (
                        t < len(tokens) - 1
                        and token + "_" + tokens[t + 1] in self.verbs
                    ):
                        joined = False

                elif token in self.suffixes and result[-1] in self.words:
                    joined = True

            if joined:
                result.pop()
                result.append(token_pair)
            else:
                result.append(token)

        return result
