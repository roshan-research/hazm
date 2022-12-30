# coding: utf-8

"""این ماژول شامل کلاس‌ها و توابعی برای نرمال‌سازی متن است.
"""

from __future__ import unicode_literals
import re
from .Lemmatizer import Lemmatizer
from .WordTokenizer import WordTokenizer
from .utils import maketrans, past_roots, present_roots


def compile_patterns(patterns): return [
    (re.compile(pattern), repl) for pattern, repl in patterns]


class Normalizer(object):
    """این کلاس شامل توابعی برای نرمال‌سازی متن است. 

    Args:
        remove_extra_spaces (bool, optional): اگر `True‍` باشد فواصل اضافهٔ متن را حذف می‌کند.
        persian_style (bool, optional): اگر `True` باشد اصلاحات مخصوص زبان فارسی را انجام می‌دهد؛ مثلاً جایگزین‌کردن کوتیشن با گیومه.
        persian_numbers (bool, optional): اگر `True` باشد ارقام انگلیسی را با فارسی جایگزین می‌کند.
        remove_diacritics (bool, optional): اگر `True` باشد اعرابِ حروف را حذف می‌کند.
        affix_spacing (bool, optional): اگر `True` باشد فواصل را در پیشوندها و پسوندها اصلاح می‌کند.
        token_based (bool, optional): اگر `True‍` باشد متن به‌شکل توکن‌به‌توکن نرمالایز می‌شود نه یکجا.
        punctuation_spacing (bool, optional): اگر `True` باشد فواصل را در نشانه‌های سجاوندی اصلاح می‌کند.
    """

    def __init__(self, remove_extra_spaces=True, persian_style=True, persian_numbers=True, remove_diacritics=True, affix_spacing=True, token_based=False, punctuation_spacing=True, unicodes_replacement=True, remove_redundant_chars=True):
        self.lemmatizer = Lemmatizer()        
        self._punctuation_spacing = punctuation_spacing
        self._affix_spacing = affix_spacing
        self._token_based = token_based
        self._unicodes_replacement = unicodes_replacement
        self._remove_redundant_chars=remove_redundant_chars

        translation_src = 'ؠػػؽؾؿكيٮٯٷٸٹٺٻټٽٿڀځٵٶٷٸٹٺٻټٽٿڀځڂڅڇڈډڊڋڌڍڎڏڐڑڒړڔڕږڗڙښڛڜڝڞڟڠڡڢڣڤڥڦڧڨڪګڬڭڮڰڱڲڳڴڵڶڷڸڹںڻڼڽھڿہۂۃۄۅۆۇۈۉۊۋۏۍێېۑےۓەۮۯۺۻۼۿݐݑݒݓݔݕݖݗݘݙݚݛݜݝݞݟݠݡݢݣݤݥݦݧݨݩݪݫݬݭݮݯݰݱݲݳݴݵݶݷݸݹݺݻݼݽݾݿࢠࢡࢢࢣࢤࢥࢦࢧࢨࢩࢪࢫࢮࢯࢰࢱࢬࢲࢳࢴࢶࢷࢸࢹࢺࢻࢼࢽﭐﭑﭒﭓﭔﭕﭖﭗﭘﭙﭚﭛﭜﭝﭞﭟﭠﭡﭢﭣﭤﭥﭦﭧﭨﭩﭮﭯﭰﭱﭲﭳﭴﭵﭶﭷﭸﭹﭺﭻﭼﭽﭾﭿﮀﮁﮂﮃﮄﮅﮆﮇﮈﮉﮊﮋﮌﮍﮎﮏﮐﮑﮒﮓﮔﮕﮖﮗﮘﮙﮚﮛﮜﮝﮞﮟﮠﮡﮢﮣﮤﮥﮦﮧﮨﮩﮪﮫﮬﮭﮮﮯﮰﮱﺀﺁﺃﺄﺅﺆﺇﺈﺉﺊﺋﺌﺍﺎﺏﺐﺑﺒﺕﺖﺗﺘﺙﺚﺛﺜﺝﺞﺟﺠﺡﺢﺣﺤﺥﺦﺧﺨﺩﺪﺫﺬﺭﺮﺯﺰﺱﺲﺳﺴﺵﺶﺷﺸﺹﺺﺻﺼﺽﺾﺿﻀﻁﻂﻃﻄﻅﻆﻇﻈﻉﻊﻋﻌﻍﻎﻏﻐﻑﻒﻓﻔﻕﻖﻗﻘﻙﻚﻛﻜﻝﻞﻟﻠﻡﻢﻣﻤﻥﻦﻧﻨﻩﻪﻫﻬﻭﻮﻯﻰﻱﻲﻳﻴىكي“” '
        translation_dst = 'یککیییکیبقویتتبتتتبحاوویتتبتتتبحححچدددددددددررررررررسسسصصطعففففففققکککککگگگگگللللنننننهچهههوووووووووییییییهدرشضغهبببببببححددرسعععففکککممنننلررسححسرحاایییووییحسسکببجطفقلمییرودصگویزعکبپتریفقنااببببپپپپببببتتتتتتتتتتتتففففححححححححچچچچچچچچددددددددژژررککککگگگگگگگگگگگگننننننههههههههههییییءاااووااییییااببببتتتتثثثثججججححححخخخخددذذررززسسسسششششصصصصضضضضططططظظظظععععغغغغففففققققککککللللممممننننههههوویییییییکی"" '

        if persian_numbers:
            translation_src += '0123456789%٠١٢٣٤٥٦٧٨٩'
            translation_dst += '۰۱۲۳۴۵۶۷۸۹٪۰۱۲۳۴۵۶۷۸۹'

        self.translations = maketrans(translation_src, translation_dst)

        if self._token_based:
            self.words = self.lemmatizer.words
            self.verbs = self.lemmatizer.verbs
            self.tokenizer = WordTokenizer(join_verb_parts=False)
            self.suffixes = {'ی', 'ای', 'ها', 'های', 'تر',
                             'تری', 'ترین', 'گر', 'گری', 'ام', 'ات', 'اش'}

        if self.remove_redundant_chars:
            self.tokenizer = WordTokenizer(join_verb_parts=False)
            self.words = self.lemmatizer.words
            self.redundant_chars_pattern = re.compile(r'([آابپتثجچحخدذرزژسشصضطظعغفقکگلمنوهی])\1{1,}')

        self.character_refinement_patterns = []

        if remove_extra_spaces:
            self.character_refinement_patterns.extend([
                (r' {2,}', ' '),  # remove extra spaces
                (r'\n{3,}', '\n\n'),  # remove extra newlines
                (r'\u200c{2,}', '\u200c'),  # remove extra ZWNJs
                (r'\u200c{1,} ', ' '),  # remove unneded ZWNJs before space
                (r' \u200c{1,}', ' '),  # remove unneded ZWNJs after space
                (r'[ـ\r]', ''),  # remove keshide, carriage returns
            ])

        if persian_style:
            self.character_refinement_patterns.extend([
                ('"([^\n"]+)"', r'«\1»'),  # replace quotation with gyoome
                ('([\d+])\.([\d+])', r'\1٫\2'),  # replace dot with momayez
                (r' ?\.\.\.', ' …'),  # replace 3 dots
            ])

        if remove_diacritics:
            self.character_refinement_patterns.append(
                # Remove almoast all arabic unicode superscript and subscript characters in the ranges of 00600-06FF, 08A0-08FF, FB50-FDFF, and FE70-FEFF
                ('[\u064B\u064C\u064D\u064E\u064F\u0650\u0651\u0652\u0605\u0653\u0654\u0655\u0656\u0657\u0658\u0659\u065A\u065B\u065C\u065D\u065E\u065F\u0670\u0610\u0611\u0612\u0613\u0614\u0615\u0616\u0618\u0619\u061A\u061E\u06D4\u06D6\u06D7\u06D8\u06D9\u06DA\u06DB\u06DC\u06DD\u06DE\u06DF\u06E0\u06E1\u06E2\u06E3\u06E4\u06E5\u06E6\u06E7\u06E8\u06E9\u06EA\u06EB\u06EC\u06ED\u06FD\u06FE\u08AD\u08D4\u08D5\u08D6\u08D7\u08D8\u08D9\u08DA\u08DB\u08DC\u08DD\u08DE\u08DF\u08E0\u08E1\u08E2\u08E3\u08E4\u08E5\u08E6\u08E7\u08E8\u08E9\u08EA\u08EB\u08EC\u08ED\u08EE\u08EF\u08F0\u08F1\u08F2\u08F3\u08F4\u08F5\u08F6\u08F7\u08F8\u08F9\u08FA\u08FB\u08FC\u08FD\u08FE\u08FF\uFBB2\uFBB3\uFBB4\uFBB5\uFBB6\uFBB7\uFBB8\uFBB9\uFBBA\uFBBB\uFBBC\uFBBD\uFBBE\uFBBF\uFBC0\uFBC1\uFC5E\uFC5F\uFC60\uFC61\uFC62\uFC63\uFCF2\uFCF3\uFCF4\uFD3E\uFD3F\uFE70\uFE71\uFE72\uFE76\uFE77\uFE78\uFE79\uFE7A\uFE7B\uFE7C\uFE7D\uFE7E\uFE7F\uFDFA\uFDFB]', ''),
            )

        self.character_refinement_patterns = compile_patterns(
            self.character_refinement_patterns)

        punc_after, punc_before = r'\.:!،؛؟»\]\)\}', r'«\[\(\{'
        if punctuation_spacing:
            self.punctuation_spacing_patterns = compile_patterns([
                # remove space before and after quotation
                ('" ([^\n"]+) "', r'"\1"'),
                (' ([' + punc_after + '])', r'\1'),  # remove space before
                ('([' + punc_before + ']) ', r'\1'),  # remove space after
                # put space after . and :
                ('([' + punc_after[:3] + '])([^ ' + \
                 punc_after + '\d۰۱۲۳۴۵۶۷۸۹])', r'\1 \2'),
                ('([' + punc_after[3:] + '])([^ ' + punc_after + '])',
                 r'\1 \2'),  # put space after
                ('([^ ' + punc_before + '])([' + punc_before + '])',
                 r'\1 \2'),  # put space before
                # put space after number; e.g., به طول ۹متر -> به طول ۹ متر
                ('(\d)([آابپتثجچحخدذرزژسشصضطظعغفقکگلمنوهی])', r'\1 \2'),
                # put space after number; e.g., به طول۹ -> به طول ۹
                ('([آابپتثجچحخدذرزژسشصضطظعغفقکگلمنوهی])(\d)', r'\1 \2'),
            ])

        if affix_spacing:
            self.affix_spacing_patterns = compile_patterns([
                (r'([^ ]ه) ی ', r'\1‌ی '),  # fix ی space
                (r'(^| )(ن?می) ', r'\1\2‌'),  # put zwnj after می, نمی
                # put zwnj before تر, تری, ترین, گر, گری, ها, های
                (r'(?<=[^\n\d ' + punc_after + punc_before + \
                 ']{2}) (تر(ین?)?|گری?|های?)(?=[ \n' + punc_after + punc_before + ']|$)', r'‌\1'),
                # join ام, ایم, اش, اند, ای, اید, ات
                (r'([^ ]ه) (ا(م|یم|ش|ند|ی|ید|ت))(?=[ \n' + \
                 punc_after + ']|$)', r'\1‌\2'),

                # شنبهها => شنبه‌ها
                ('(ه)(ها)', r'\1‌\2')
            ])
            self.is_verb = re.compile(r'^.+#.+$')
            self.joint_mi = re.compile(r'ن?می[آابپتثجچحخدذرزژسشصضطظعغفقکگلمنوهی]+')

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

        text = self.character_refinement(text)
        if self._affix_spacing:
            text = self.affix_spacing(text)

        
        tokens = list(set(self.tokenizer.tokenize(text.translate(self.translations))))

        for token in tokens:
            if re.search(self.redundant_chars_pattern,token):
                no_redundant=self.remove_redundant_chars(token)
                if token!=no_redundant:
                    text = text.replace(token,no_redundant)     

        if self._token_based:
            tokens = self.tokenizer.tokenize(text.translate(self.translations))
            tokens = self.token_spacing(tokens)
            text = ' '.join(self.repeated_chars(tokens))

        if self._punctuation_spacing:
            text = self.punctuation_spacing(text)

        if self._unicodes_replacement:
            text = self.unicodes_replacement(text)

        return text

    def remove_redundant_chars(self, word):
        result = word

        if len(set(word))==len(word): return word
        if word in self.words: return word
        
        refined_unichar = re.sub(self.redundant_chars_pattern, r'\1', word)
        refined_bichar = re.sub(self.redundant_chars_pattern, r'\1\1', word)
        
        if (refined_unichar in self.words) != (refined_bichar in self.words):                    
            return refined_unichar if refined_unichar in self.words else refined_bichar
                
        return word

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
        replacements = [
            ('﷽', 'بسم الله الرحمن الرحیم'),
            ('﷼', 'ریال'),
            ('(ﷰ|ﷹ)', 'صلی'),
            ('ﷲ', 'الله'),
            ('ﷳ', 'اکبر'),
            ('ﷴ', 'محمد'),
            ('ﷵ', 'صلعم'),
            ('ﷶ', 'رسول'),
            ('ﷷ', 'علیه'),
            ('ﷸ', 'وسلم'),
            ('ﻵ|ﻶ|ﻷ|ﻸ|ﻹ|ﻺ|ﻻ|ﻼ', 'لا'),
        ]

        for old, new in replacements:
            text = re.sub(old, new, text)

        return text

    def character_refinement(self, text):
        """حروف متن را به حروف استاندارد فارسی تبدیل می‌کند.

        Examples:
            >>> normalizer = Normalizer()
            >>> normalizer.character_refinement('اصلاح كاف و ياي عربي')
            'اصلاح کاف و یای عربی'

            >>> normalizer.character_refinement('عراق سال 2012 قراردادی به ارزش "4.2 میلیارد دلار" برای خرید تجهیزات نظامی با روسیه امضا  کرد.')
            'عراق سال ۲۰۱۲ قراردادی به ارزش «۴٫۲ میلیارد دلار» برای خرید تجهیزات نظامی با روسیه امضا کرد.'

            >>> normalizer.character_refinement('رمــــان')
            'رمان'

            >>> normalizer.character_refinement('بُشقابِ مَن را بِگیر')
            'بشقاب من را بگیر'

        Args:
            text (str): متنی که باید حروف آن استانداردسازی شود.

        Returns:
            (str): متنی با حروف استاندارد فارسی.
        """

        text = text.translate(self.translations)
        for pattern, repl in self.character_refinement_patterns:
            text = pattern.sub(repl, text)
        return text

    def punctuation_spacing(self, text):
        """فاصله‌گذاری‌های اشتباه را در نشانه‌های سجاوندی اصلاح می‌کند. 

        Examples:
            >>> normalizer = Normalizer()
            >>> normalizer.punctuation_spacing('اصلاح ( پرانتزها ) در متن .')
            'اصلاح (پرانتزها) در متن.'

            >>> normalizer.punctuation_spacing('نسخه 0.5 در ساعت 22:00 تهران،1396')
            'نسخه 0.5 در ساعت 22:00 تهران، 1396'

            >>> normalizer.punctuation_spacing('اتریش ۷.۹ میلیون.')
            'اتریش ۷.۹ میلیون.'

        Args:
            text (str): متنی که باید فاصله‌گذاری‌های اشتباه آن در نشانه‌های سجاوندی اصلاح شود.

        Returns:
            (str): متنی با فاصله‌گذاری صحیحِ‌ نشانه‌های سجاوندی.
        """

        for pattern, repl in self.punctuation_spacing_patterns:
            text = pattern.sub(repl, text)
        return text

    def affix_spacing(self, text):
        """فاصله‌گذاری‌های اشتباه را در پسوندها و پیشوندها اصلاح می‌کند.

        Examples:
            >>> normalizer = Normalizer()
            >>> normalizer.affix_spacing('خانه ی پدری')
            'خانه‌ی پدری'

            >>> normalizer.affix_spacing('فاصله میان پیشوند ها و پسوند ها را اصلاح می کند.')
            'فاصله میان پیشوند‌ها و پسوند‌ها را اصلاح می‌کند.'

            >>> normalizer.affix_spacing('می روم')
            'می‌روم'

            >>> normalizer.affix_spacing('حرفه ای')
            'حرفه‌ای'

            >>> normalizer.affix_spacing('محبوب ترین ها')
            'محبوب‌ترین‌ها'

        Args:
            text (str): متنی که باید فاصله‌گذاری‌های اشتباهِ آن در پسوندها و پیشوندها اصلاح شود.

        Returns:
            (str): متنی با فاصله‌گذاری صحیحِ پیشوندها و پسوندها.
        """

        for pattern, repl in self.affix_spacing_patterns:
            text = pattern.sub(repl, text)
        
        matches = re.findall(self.joint_mi, text)
        for m in matches:
            r = re.sub("^می", "می‌", m)
            if re.match(self.is_verb , self.lemmatizer.lemmatize(r)):
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
                token_pair = result[-1]+'‌'+token
                if token_pair in self.verbs or token_pair in self.words and self.words[token_pair][0] > 0:
                    joined = True

                    if t < len(tokens)-1 and token+'_'+tokens[t+1] in self.verbs:
                        joined = False

                elif token in self.suffixes and result[-1] in self.words:
                    joined = True

            if joined:
                result.pop()
                result.append(token_pair)
            else:
                result.append(token)

        return result
    

    def repeated_chars(self, tokens):
        result = []
        for token in tokens:
            if token not in self.words:
                refined_unichar = re.sub(self.repeated_chars_pattern, r'\1', token)
                refined_bichar = re.sub(self.repeated_chars_pattern, r'\1\1', token)
                
                if (refined_unichar in self.words) != (refined_bichar in self.words):                    
                    token = refined_unichar if refined_unichar in self.words else refined_bichar
                    
            result.append(token)
        
        return result
