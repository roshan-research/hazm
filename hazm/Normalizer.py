# coding: utf-8

"""این ماژول شامل کلاس‌ها و توابعی برای نرمال‌سازی متن است.
"""

from __future__ import unicode_literals
import re
from .Lemmatizer import Lemmatizer
from .WordTokenizer import WordTokenizer
from .utils import maketrans, regex_replace


class Normalizer(object):
    """این کلاس شامل توابعی برای نرمال‌سازی متن است.

    Args:
        correct_spacing (bool, optional): اگر `True‍` فاصله‌گذاری‌ها را در متن، نشانه‌های سجاوندی و پیشوندها و پسوندها اصلاح می‌کند.
        remove_diacritics (bool, optional): اگر `True` باشد اعرابِ حروف را حذف می‌کند.
        remove_specials_chars (bool, optional): اگر `True` باشد برخی از کاراکترها و نشانه‌های خاص را که کاربردی در پردازش متن ندارند حذف می‌کند.
        decrease_repeated_chars (bool, optional): اگر `True` باشد تکرارهای بیش از ۲ بار را به ۲ بار کاهش می‌دهد. مثلاً «سلاممم» را به «سلامم» تبدیل می‌کند.
        persian_style (bool, optional): اگر `True` باشد اصلاحات مخصوص زبان فارسی را انجام می‌دهد؛ مثلاً جایگزین‌کردن کوتیشن با گیومه.
        persian_numbers (bool, optional): اگر `True` باشد ارقام انگلیسی را با فارسی جایگزین می‌کند.
        unicodes_replacement (bool, optional): اگر `True` باشد برخی از کاراکترهای یونیکد را با معادل نرمال‌شدهٔ آن جایگزین می‌کند.
        seperate_mi (bool, optional): اگر `True` باشد پیشوند «می» و «نمی» را در افعال جدا می‌کند.
    """

    def __init__(
        self,
        correct_spacing=True,
        remove_diacritics=True,
        remove_specials_chars=True,
        decrease_repeated_chars=True,
        persian_style=True,
        persian_numbers=True,
        unicodes_replacement=True,
        seperate_mi=True,
    ):
        self._correct_spacing = correct_spacing
        self._remove_diacritics = remove_diacritics
        self._remove_specials_chars = remove_specials_chars
        self._decrease_repeated_chars = decrease_repeated_chars
        self._persian_style = persian_style
        self._persian_number = persian_numbers
        self._unicodes_replacement = unicodes_replacement
        self._seperate_mi = seperate_mi

        self.translation_src = "ؠػػؽؾؿكيٮٯٷٸٹٺٻټٽٿڀځٵٶٷٸٹٺٻټٽٿڀځڂڅڇڈډڊڋڌڍڎڏڐڑڒړڔڕږڗڙښڛڜڝڞڟڠڡڢڣڤڥڦڧڨڪګڬڭڮڰڱڲڳڴڵڶڷڸڹںڻڼڽھڿہۂۃۄۅۆۇۈۉۊۋۏۍێېۑےۓەۮۯۺۻۼۿݐݑݒݓݔݕݖݗݘݙݚݛݜݝݞݟݠݡݢݣݤݥݦݧݨݩݪݫݬݭݮݯݰݱݲݳݴݵݶݷݸݹݺݻݼݽݾݿࢠࢡࢢࢣࢤࢥࢦࢧࢨࢩࢪࢫࢮࢯࢰࢱࢬࢲࢳࢴࢶࢷࢸࢹࢺࢻࢼࢽﭐﭑﭒﭓﭔﭕﭖﭗﭘﭙﭚﭛﭜﭝﭞﭟﭠﭡﭢﭣﭤﭥﭦﭧﭨﭩﭮﭯﭰﭱﭲﭳﭴﭵﭶﭷﭸﭹﭺﭻﭼﭽﭾﭿﮀﮁﮂﮃﮄﮅﮆﮇﮈﮉﮊﮋﮌﮍﮎﮏﮐﮑﮒﮓﮔﮕﮖﮗﮘﮙﮚﮛﮜﮝﮞﮟﮠﮡﮢﮣﮤﮥﮦﮧﮨﮩﮪﮫﮬﮭﮮﮯﮰﮱﺀﺁﺃﺄﺅﺆﺇﺈﺉﺊﺋﺌﺍﺎﺏﺐﺑﺒﺕﺖﺗﺘﺙﺚﺛﺜﺝﺞﺟﺠﺡﺢﺣﺤﺥﺦﺧﺨﺩﺪﺫﺬﺭﺮﺯﺰﺱﺲﺳﺴﺵﺶﺷﺸﺹﺺﺻﺼﺽﺾﺿﻀﻁﻂﻃﻄﻅﻆﻇﻈﻉﻊﻋﻌﻍﻎﻏﻐﻑﻒﻓﻔﻕﻖﻗﻘﻙﻚﻛﻜﻝﻞﻟﻠﻡﻢﻣﻤﻥﻦﻧﻨﻩﻪﻫﻬﻭﻮﻯﻰﻱﻲﻳﻴىكي“” "
        self.translation_dst = 'یککیییکیبقویتتبتتتبحاوویتتبتتتبحححچدددددددددررررررررسسسصصطعففففففققکککککگگگگگللللنننننهچهههوووووووووییییییهدرشضغهبببببببححددرسعععففکککممنننلررسححسرحاایییووییحسسکببجطفقلمییرودصگویزعکبپتریفقنااببببپپپپببببتتتتتتتتتتتتففففححححححححچچچچچچچچددددددددژژررککککگگگگگگگگگگگگننننننههههههههههییییءاااووااییییااببببتتتتثثثثججججححححخخخخددذذررززسسسسششششصصصصضضضضططططظظظظععععغغغغففففققققککککللللممممننننههههوویییییییکی"" '

        if self._correct_spacing or sel._decrease_repeated_chars:
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
                    "([" + punc_after[:3] + "])([^ " + punc_after + "\d۰۱۲۳۴۵۶۷۸۹])",
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
                ("(\d)([آابپتثجچحخدذرزژسشصضطظعغفقکگلمنوهی])", r"\1 \2"),
                # put space after number; e.g., به طول۹ -> به طول ۹
                ("([آابپتثجچحخدذرزژسشصضطظعغفقکگلمنوهی])(\d)", r"\1 \2"),
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
                ("([\d+])\.([\d+])", r"\1٫\2"),  # replace dot with momayez
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
                ("[\u064B\u064C\u064D\u064E\u064F\u0650\u0651\u0652]", ""),
            ]

        if self._remove_specials_chars:
            self.specials_chars_patterns = [
                # Remove almoast all arabic unicode superscript and subscript characters in the ranges of 00600-06FF, 08A0-08FF, FB50-FDFF, and FE70-FEFF
                (
                    "[\u0605\u0653\u0654\u0655\u0656\u0657\u0658\u0659\u065A\u065B\u065C\u065D\u065E\u065F\u0670\u0610\u0611\u0612\u0613\u0614\u0615\u0616\u0618\u0619\u061A\u061E\u06D4\u06D6\u06D7\u06D8\u06D9\u06DA\u06DB\u06DC\u06DD\u06DE\u06DF\u06E0\u06E1\u06E2\u06E3\u06E4\u06E5\u06E6\u06E7\u06E8\u06E9\u06EA\u06EB\u06EC\u06ED\u06FD\u06FE\u08AD\u08D4\u08D5\u08D6\u08D7\u08D8\u08D9\u08DA\u08DB\u08DC\u08DD\u08DE\u08DF\u08E0\u08E1\u08E2\u08E3\u08E4\u08E5\u08E6\u08E7\u08E8\u08E9\u08EA\u08EB\u08EC\u08ED\u08EE\u08EF\u08F0\u08F1\u08F2\u08F3\u08F4\u08F5\u08F6\u08F7\u08F8\u08F9\u08FA\u08FB\u08FC\u08FD\u08FE\u08FF\uFBB2\uFBB3\uFBB4\uFBB5\uFBB6\uFBB7\uFBB8\uFBB9\uFBBA\uFBBB\uFBBC\uFBBD\uFBBE\uFBBF\uFBC0\uFBC1\uFC5E\uFC5F\uFC60\uFC61\uFC62\uFC63\uFCF2\uFCF3\uFCF4\uFD3E\uFD3F\uFE70\uFE71\uFE72\uFE76\uFE77\uFE78\uFE79\uFE7A\uFE7B\uFE7C\uFE7D\uFE7E\uFE7F\uFDFA\uFDFB]",
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

    def normalize(self, text):
        """متن را نرمال‌سازی می‌کند.

        Examples:
            >>> normalizer = Normalizer()
            >>> normalizer.normalize('اِعلام کَرد : « زمین لرزه ای به بُزرگیِ 6 دهم ریشتر ...»')
            'اعلام کرد: «زمین‌لرزه‌ای به بزرگی ۶ دهم ریشتر…»'

        Args:
            text (str): متنی که باید نرمال‌سازی شود.

        Returns:
            (str): متنِ نرمال‌سازی‌شده.
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

    def correct_spacing(self, text):
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

    def remove_diacritics(self, text):
        """اِعراب را از متن حذف می‌کند.

        Examples:
            >>> normalizer = Normalizer()
            >>> normalizer.remove_diacritics('حَذفِ اِعراب')
            'حذف اعراب'

        Args:
            text (str): متنی که باید اعراب آن حذف شود.

        Returns:
            (str): متنی بدون اعراب.
        """
        return regex_replace(self.diacritics_patterns, text)

    def remove_specials_chars(self, text):
        """برخی از کاراکترها و نشانه‌های خاص را که کاربردی در پردازش متن ندارند حذف می‌کند.

        Examples:
            >>> normalizer = Normalizer()
            >>> normalizer.remove_specials_chars('پیامبر اکرم ﷺ')
            'پیامبر اکرم'
        Args:
            text (str): متنی که باید کاراکترها و نشانه‌های اضافهٔ آن حذف شود.

        Returns:
            (str): متنی بدون کاراکترها و نشانه‌های اضافه.
        """
        return regex_replace(self.specials_chars_patterns, text)

    def decrease_repeated_chars(self, text):
        """تکرارهای زائد حروف را در کلماتی مثل سلامممممم حذف می‌کند و در مواردی که نمی‌تواند تشخیص دهد دست کم به دو تکرار کاهش می‌دهد.

        Examples:
            >>> normalizer = Normalizer()
            >>> normalizer.decrease_repeated_chars('سلامممم به همه')
            'سلام به همه'
        Args:
            text (str): متنی که باید تکرارهای زائد آن حذف شود.

        Returns:
            (str): متنی بدون کاراکترهای زائد یا حداقل با دو تکرار.
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

    def persian_style(self, text):
        """برخی از حروف و نشانه‌ها را با حروف و نشانه‌های فارسی جایگزین می‌کند.

        Examples:
            >>> normalizer = Normalizer()
            >>> normalizer.persian_style('"نرمال‌سازی"')
            '«نرمال‌سازی»'

        Args:
            text (str): متنی که باید حروف و نشانه‌های آن با حروف و نشانه‌های فارسی جایگزین شود.

        Returns:
            (str): متنی با حروف و نشانه‌های فارسی‌سازی شده.
        """
        return regex_replace(self.persian_style_patterns, text)

    def persian_number(self, text):
        """اعداد لاتین و علامت % را با معادل فارسی آن جایگزین می‌کند

        Examples:
            >>> normalizer = Normalizer()
            >>> normalizer.persian_number('5% رشد داشته است.')
            '۵٪ رشد داشته است.'

        Args:
            text (str): متنی که باید اعداد لاتین و علامت % آن با معادل فارسی جایگزین شود.

        Returns:
            (str): متنی با اعداد و علامت ٪ فارسی.
        """
        translations = maketrans(
            self.number_translation_src, self.number_translation_dst
        )
        return text.translate(translations)

    def unicodes_replacement(self, text):
        """برخی از کاراکترهای خاص یونیکد را با معادلِ نرمال آن جایگزین می‌کند. غالباً این کار فقط در مواردی صورت می‌گیرد که یک کلمه در قالب یک کاراکتر یونیکد تعریف شده است.

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
            >>> normalizer.unicodes_replacement('حضرت ﷴ صلوات الله علیه)')
            'حضرت محمد صلوات الله علیه'

        Args:
            text (str): متنی که باید برخی از کاراکترهای یونیکد آن (جدول بالا)، با شکل استاندارد، جایگزین شود.

        Returns:
            (str): متنی که برخی از کاراکترهای یونیکد آن با شکل استاندارد جایگزین شده است.
        """

        for old, new in self.replacements:
            text = re.sub(old, new, text)

        return text

    def seperate_mi(self, text):
        """پیشوند «می» و «نمی» را در افعال جدا کرده و با نیم‌فاصله می‌چسباند.

        Examples:
            >>> normalizer = Normalizer()
            >>> normalizer.seperate_mi('نمیدانم چه میگفت')
            'نمی‌دانم چه می‌گفت'
        Args:
            text (str): متنی که باید پیشوند «می» و «نمی» در آن جدا شود.

        Returns:
            (str): متنی با «می» و «نمی» جدا شده.
        """
        matches = re.findall(r"\bن?می[آابپتثجچحخدذرزژسشصضطظعغفقکگلمنوهی]+", text)
        for m in matches:
            r = re.sub("^(ن?می)", r"\1‌", m)
            if r in self.verbs:
                text = text.replace(m, r)

        return text

    def token_spacing(self, tokens):
        """توکن‌های ورودی را به فهرستی از توکن‌های نرمال‌سازی شده تبدیل می‌کند.
        در این فرایند ممکن است برخی از توکن‌ها به یکدیگر بچسبند؛
        برای مثال: `['زمین', 'لرزه', 'ای']` تبدیل می‌شود به: `['زمین‌لرزه‌ای']`
        Examples:
                        >>> normalizer = Normalizer(token_based=True)
                        >>> normalizer.token_spacing(['کتاب', 'ها'])
                        ['کتاب‌ها']
                        >>> normalizer.token_spacing(['او', 'می', 'رود'])
                        ['او', 'می‌رود']
                        >>> normalizer.token_spacing(['ماه', 'می', 'سال', 'جدید'])
                        ['ماه', 'می', 'سال', 'جدید']
                        >>> normalizer.token_spacing(['اخلال', 'گر'])
                        ['اخلال‌گر']
                        >>> normalizer.token_spacing(['پرداخت', 'شده', 'است'])
                        ['پرداخت', 'شده', 'است']
                        >>> normalizer.token_spacing(['زمین', 'لرزه', 'ای'])
                        ['زمین‌لرزه‌ای']
                Args:
                        tokens (List[str]): توکن‌هایی که باید نرمال‌سازی شود.

                Returns:
                        (List[str]): لیستی از توکن‌های نرمال‌سازی شده به شکل `[token1, token2, ...]`.
        """

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
