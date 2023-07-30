## معرفی هضم

[هضم](https://www.roshan-ai.ir/hazm) **کتابخانه‌ای پایتونی برای پردازش زبان
فارسی** است. با هضم می‌توانید متن را نرمال‌سازی کنید. جملات و واژه‌های متن را
استخراج کنید. ریشهٔ کلمات را پیدا کنید. جملات را تحلیل صرفی و نحوی کنید.
وابستگی‌های دستوری را در متن شناسایی کنید و ... .

!!! info "مبتنی بر کتابخانهٔ nltk و سازگار با پایتون +۳.۸"
هضم بر مبنای کتابخانهٔ [NLTK](https://www.nltk.org/) توسعه داده شده و برای
**زبان فارسی** بومی‌سازی شده است. هضم با پایتون ۳.۸ و بالاتر سازگار است.

!!! info "محصولی از تیم روشن"
این کتابخانه در ابتدا به عنوان پروژه‌ای شخصی توسعه داده شد و اکنون زیر چتر
[محصولات روشن](https://www.roshan-ai.ir/) در ادامهٔ مسیر توسعه است.

<figure markdown>
  ![کتابخانهٔ هضم](assets/sample.png){ loading=lazy }
  <figcaption></figcaption>
</figure>

## نصب هضم

ابتدا پکیج هضم را نصب کنید:

```console
$ pip install hazm
```

سپس [منابع موردنظر را دانلود کنید](https://github.com/roshan-research/hazm#pretrained-models) و ترجیحاً در ریشهٔ پروژه اکسترکت کنید.

و در آخر، هضم را را در پروژه خود ایمپورت کنید:

```py
from hazm import *
```

## استفاده از هضم

کد پایین دیدی کلی از کاربردهای هضم نشان می‌دهد:

```py
from hazm import *

# Clean and normalize a text.
print(Normalizer().normalize("چه گل های زیبایی."))
# چه گل‌های زیبایی

# Find the word’s root (faster but less accurate)
print(Stemmer().stem("کتاب‌هایشان"))
# کتاب

# Find the word’s root (More accurate but slower)
print(Lemmatizer().lemmatize("می‌روم"))
# رفت#رو

# Break text into sentences.
print(SentenceTokenizer().tokenize("بسیار خوشحال بود! پرسید، چرا دیروز نیامدی ؟"))
# ['پرسید، چرا دیروز نیامدی ؟','! بسیار خوشحال بود']

# Break text into tokens.
print(WordTokenizer().tokenize("پرسید، چرا دیروز نیامدی؟"))
# ['پرسید', '،', 'چرا', 'دیروز', 'نیامدی', '؟']

# Assigns parts of speech to each word, such as noun, verb, adjective, etc.
tagger = POSTagger(model='pos_tagger.model')
print(tagger.tag(WordTokenizer().tokenize("ما بسیار کتاب می‌خوانیم")))
# [('ما', 'PRO'), ('بسیار', 'ADV'), ('کتاب', 'N'), ('می‌خوانیم', 'V')]

# Labels each word with its part of speech, such as noun, verb, adjective, etc.
chunker = chunker('chunker.model')
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
نسخه‌هایی از این کتابخانه به زبان‌های دیگر [پورت شده است](content/in-other-languages.md).
