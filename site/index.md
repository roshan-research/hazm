## معرفی هضم
[هضم](https://www.roshan-ai.ir/hazm) **کتابخانه‌ای پایتونی برای پردازش زبان
فارسی** است. با هضم می‌توانید متن را نرمال‌سازی کنید. جملات و واژه‌های متن را
استخراج کنید. ریشهٔ کلمات را پیدا کنید. جملات را تحلیل صرفی و نحوی کنید.
وابستگی‌های دستوری را در متن شناسایی کنید و ... .


!!! info "مبتنی بر کتابخانهٔ nltk و سازگار با پایتون +۲.۷"
      هضم بر مبنای کتابخانهٔ [NLTK](https://www.nltk.org/) توسعه داده شده و برای
      **زبان فارسی** بومی‌سازی شده است. هضم با پایتون ۲.۷ و بالاتر سازگار است.

!!! info "محصولی از تیم روشن"
      این کتابخانه در ابتدا به عنوان پروژه‌ای شخصی توسعه داده شد و اکنون زیر چتر
      [محصولات روشن](https://www.roshan-ai.ir/) در ادامهٔ مسیر توسعه است.

!!! info "در حال توسعه"
      با وجود وقفهٔ طولانی و پیشروی کُند در توسعهٔ هضم، همچنان در حال توسعه و
      بهبود آن هستیم. امیدواریم در نسخه‌های بعدی بتوانیم با عرضهٔ قابلیت‌های
      جدید، کم‌کاری این چند سال را جبران کنیم.

<figure markdown>
  ![کتابخانهٔ هضم](assets/sample.png){ loading=lazy }
  <figcaption></figcaption>
</figure>

## نصب هضم
ابتدا پکیج هضم را نصب کنید:

``` console 
$ pip install hazm
```

!!! warning "قابل توجه کاربران ویندوز"
      برخی از قابلیت‌های هضم وابسته به کتابخانه‌ای است که متأسفانه با ویندوز
      سازگار نیست! بنابراین تا زمانی که این وابستگی وجود دارد کاربران ویندوز
      باید از طریق wsl و زیرسیستم لینوکس از تمام امکانات هضم استفاده کنند.
      <br><br>
      **در ویدیوی زیر مراحل نصب در ویندوز آموزش داده شده است.**

<video controls>
  <source src="content/Guide-to-use-hazm-on-windows.mp4" type="video/mp4">
مرورگر شما قادر به پخش این ویدیو نیست. لطفاً آن را بروزرسانی کنید.
</video>

سپس [منابع هضم را دانلود
کنید](https://github.com/sobhe/hazm/releases/download/v0.5/resources-0.5.zip) و
در فولدری تحت عنوان resources در پروژهٔ خود قرار دهید.

!!! note ""
      فایل‌ها را در فولدری به جز resource هم می‌توانید قرار دهید ولی در این حالت
      باید مسیر فولدر حاوی فایل‌های منبع را در هنگام نمونه‌سازی کلاس‌ها معرفی
      کنید.

و در آخر، هضم را را در پروژه خود ایمپورت کنید:
``` py 
from hazm import *
```

## استفاده از هضم

کد پایین دیدی کلی از کاربردهای هضم نشان می‌دهد:

``` py
from hazm import *

# Transform a text into a standard form.
print(Normalizer().normalize("چه گل های زیبایی."))
# چه گل‌های زیبایی

# Extract the root of word (more speed, less accuracy).
print(Stemmer().stem("کتاب‌هایشان"))
# کتاب

# Extract the root of word (more accuracy, less speed).
print(Lemmatizer().lemmatize("می‌روم"))
# رفت#رو

# Split text into individual sentences.
print(SentenceTokenizer().tokenize("بسیار خوشحال بود! پرسید، چرا دیروز نیامدی ؟"))
# ['پرسید، چرا دیروز نیامدی ؟','! بسیار خوشحال بود']

# Split text into individual words.
print(WordTokenizer().tokenize("پرسید، چرا دیروز نیامدی؟"))
# ['پرسید', '،', 'چرا', 'دیروز', 'نیامدی', '؟']

# Assigns parts of speech to each word, such as noun, verb, adjective, etc.
tagger = POSTagger(model='resources/postagger.model')
print(tagger.tag(WordTokenizer().tokenize("ما بسیار کتاب می‌خوانیم")))
# [('ما', 'PRO'), ('بسیار', 'ADV'), ('کتاب', 'N'), ('می‌خوانیم', 'V')]

# Segments a sentence into its subconstituents, such as noun (NP), verb (VP), etc.
chunker = Chunker(model='resources/chunker.model')
tagged = tagger.tag(word_tokenize('کتاب خواندن را دوست داریم'))
tree2brackets(chunker.parse(tagged))
# '[کتاب خواندن NP] [را POSTP] [دوست داریم VP]'

# Identify semantic relations between words in a sentence.
parser = DependencyParser(tagger=tagger, lemmatizer=lemmatizer)
parser.parse(word_tokenize('زنگ‌ها برای که به صدا درمی‌آید؟'))
# <DependencyGraph with 8 nodes>
```

جزئیات بیشترِ این توابع را در بخش [کلاس‌ها و توابع](content/modules) پی بگیرید.
هضم علاوه بر کلاس‌ها و توابع مختص خود، کلاس‌ها و توابعی نیز برای خواندن
پیکره‌های مشهور دارد که می‌توانید توضیحات هریک از آن‌ها را در بخش
[پیکره‌خوان‌ها ](content/readers)بخوانید. هضم مبتنی بر پایتون است؛ با این حال
قبل از اینکه ناامید شوید سری به [نسخه‌های پورت‌شدهٔ هضم در زبان‌های
دیگر](content/in-other-languages) بیندازید.