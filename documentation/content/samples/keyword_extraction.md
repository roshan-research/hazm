وقتی در حال پیمایش لیست پیام‌ها، توییت‌ها، خبرها و ... هستید در واقع مشغول استخراج کلمات کلیدی هستید. شما براساس برخی از کلمات کلیدی تصمیم می‌گیرید که متنی را بخوانید یا نه. الگوریتم‌های استخراج کلمات کلیدی در NLP نیز هر کدام به روشی سعی دارند این رفتار انسان را تقلید کنند. استخراج کلمات کلیدی، رویکردی تحلیل‌گرانه برای شناسایی پرکاربردترین و ضروری‌ترین واژه‌ها و عباراتِ یک متن است. این کار برای شناسایی مفهوم اصلی متن ضروری است.

در این مثال قصد داریم با کمک هضم و برخی از کتابخانه‌های پردازش زبان، کلمات کلیدی یک متن را استخراج کنیم. در تمام الگوریتم‌های استخراج کلمات کلیدی، ابتدا باید متن خام
ورودی نرمال‌سازی، توکنایز و برچسب‌گذاری شود که انجام این کارها به سادگی توسط کتابخانهٔ هضم میسر است.

الگوریتم‌های مختلفی برای استخراج کلمات کلیدی وجود دارد. ما در این مقاله از روش Text Rank استفاده کرده‌ایم. در روش Text Rank متن ورودی ابتدا به جملات و کلمات شکسته می‌شود و سپس گراف معنایی آن ایجاد می‌شود. در این گراف، هر کلمه یا جمله نقش یک گره را بازی می‌کند و یال‌های بین گره‌ها، روابط معنایی بین آن‌هاست. اهمیت هر گره به این صورت مشخص می‌شود که اگر گره‌ای (یعنی کلمه یا جمله‌ای) با کلمات و جملات همجوار، همبستگی بیشتری داشت اهمیت بیشتری دارد.

بیایید جزئیات بیشتر را از طریق کد بررسی کنیم.

!!! info ""

    [سورس این مثال](https://github.com/roshan-research/hazm/blob/master/samples/keyword_extraction.py)

ابتدا آخرین نسخهٔ هضم را نصب کنید.

```python
pip install hazm
```

```python
import numpy as np
import nltk
import re
import string
import warnings
import gensim
from sklearn.metrics.pairwise import cosine_similarity
from configparser import ConfigParser
from functools import reduce
from gensim.models import Doc2Vec
from hazm.Embedding import SentEmbedding
from hazm import *
```

متنی را برای استخراج کلمات کلیدی آن در نظر بگیرید.

```python
text = 'سفارت ایران در مادرید درباره فیلم منتشرشده از «حسن قشقاوی» در مراسم سال نو در کاخ سلطنتی اسپانیا و حاشیه‌سازی‌ها در فضای مجازی اعلام کرد: به تشریفات دربار کتباً اعلام شد سفیر بدون همراه در مراسم حضور خواهد داشت و همچون قبل به دلایل تشریفاتی نمی‌تواند با ملکه دست بدهد. همان‌گونه که کارشناس رسمی تشریفات در توضیحات خود به یک نشریه اسپانیایی گفت این موضوع توضیح مذهبی داشته و هرگز به معنی بی‌احترامی به مقام و شخصیت زن آن هم در سطح ملکه محترمه یک کشور نیست.'

keyword_count = 10
```

## نرمال‌سازی متن و استخراج توکن‌ها توسط هضم

متن ورودی را با کمک [نرمالایزر هضم](../hazm/normalizer.md) نرمال‌سازی می‌کنیم و پس از آن با کمک توکنایزر به [جملات](../hazm/sentence_tokenizer.md) و در نهایت به [کلمات](../hazm/word_tokenizer.md) می‌شکنیم.

```python
normalizer = Normalizer()
normalize_text = normalizer.normalize(text)
tokenize_text = [word_tokenize(txt) for txt in sent_tokenize(normalize_text)]
tokenize_text
```

    [['سفارت',
      'ایران',
      'در',
      'مادرید',
      'درباره',
      'فیلم',
      'منتشرشده',
      ...]]

## استخراج تگ POS برای هر یک از کلمات

بعد از لودکردن مدل POS، هر یک از کلمات را با ماژول [POSTagger](../hazm/pos_tagger.md) هضم برچسب‌گذاری می‌کنیم.

```python
model_path = 'pos_tagger.model'
tagger = POSTagger(model = model_path)
token_tag_list = tagger.tag_sents(tokenize_text)
token_tag_list
```

    [[('سفارت', 'NOUN,EZ'),
      ('ایران', 'NOUN'),
      ('در', 'ADP'),
      ('مادرید', 'NOUN'),
      ('درباره', 'ADP,EZ'),
      ('فیلم', 'NOUN,EZ'),
      ('منتشرشده', 'ADJ'),
      ...]]

## استخراج کاندیداها

با استفاده از چند گرامر، کاندیداها را پیدا می‌کنیم.

```python
grammers = [
"""
NP:
        {<NOUN,EZ>?<NOUN.*>}    # Noun(s) + Noun(optional)

""",

"""
NP:
        {<NOUN.*><ADJ.*>?}    # Noun(s) + Adjective(optional)

"""
]
## you can also add your own grammer to be extracted from the text...
```

```python
def extract_candidates(tagged, grammer):
    keyphrase_candidate = set()
    np_parser = nltk.RegexpParser(grammer)
    trees = np_parser.parse_sents(tagged)
    for tree in trees:
        for subtree in tree.subtrees(filter=lambda t: t.label() == 'NP'):  # For each nounphrase
            # Concatenate the token with a space
            keyphrase_candidate.add(' '.join(word for word, tag in subtree.leaves()))
    keyphrase_candidate = {kp for kp in keyphrase_candidate if len(kp.split()) <= 5}
    keyphrase_candidate = list(keyphrase_candidate)
    return keyphrase_candidate

all_candidates = set()
for grammer in grammers:
    all_candidates.update(extract_candidates(token_tag_list, grammer))


all_candidates = np.array(list(all_candidates))


print(np.array(list(all_candidates)))

```

    ['مقام' 'توضیح' 'اسپانیا' 'ملکه محترمه' 'توضیح مذهبی' 'ملکه'
     'تشریفات دربار' 'معنی بی‌احترامی' 'توضیحات' 'دلایل' 'سفارت' 'کشور'
     'فضای' 'مراسم' 'موضوع' 'سفارت ایران' 'حاشیه‌سازی‌ها' 'ایران'
     'شخصیت زن' 'بی‌احترامی' 'سطح' 'حضور' 'سال نو' 'دست' 'دلایل تشریفاتی'
     'نشریه اسپانیایی' 'سفیر' 'حسن' 'کارشناس رسمی' 'فیلم' 'کارشناس'
     'مراسم سال' 'مادرید' 'تشریفات' 'کاخ' 'معنی' 'فیلم منتشرشده' 'سطح ملکه'
     'کاخ سلطنتی' 'همان‌گونه' 'دربار' 'اعلام' 'زن' 'حسن قشقاوی' 'نشریه'
     'قشقاوی' 'فضای مجازی' 'همراه' 'شخصیت']

## لودکردن مدل Sent2Vec

مدل sent2vec را لود می‌کنیم.

```python
sent2vec_model_path = 'sent2vec.model'
sent2vec_model = SentEmbedding(sent2vec_model_path)
```

## استخراج وکتور برای هر یک از کاندیداها و کل متن

با کمک مدلی که در مرحله قبل لود شد هر یک از کاندیداها را به وکتور متناظر تبدیل می‌کنیم و همانند آن یکبار هم با ترکیب تمام کاندیداهای یک وکتور، به عنوان وکتور نمایندهٔ متن تعیین می‌کنیم.

```python
all_candidates_vectors = [sent2vec_model[candidate] for candidate in all_candidates]
all_candidates_vectors[0:2]
```

    [array([-0.01188162, -0.01629335, -0.02919522, -0.00783677, -0.00102758,
            -0.03208233, -0.01709846,  0.0117062 ,  0.03449516,  0.07738346,
            ...],dtype=float32),
     array([ 1.61259193e-02, -2.24474519e-02, -3.80111709e-02,  2.28938404e-02,
             1.09725883e-02,  3.17719281e-02,  6.31656572e-02,  8.05895310e-03,
            ...],dtype=float32)]

```python

candidates_concatinate = ' '.join(all_candidates)
whole_text_vector = sent2vec_model[candidates_concatinate]
whole_text_vector
```

    array([ 4.67376083e-01,  1.41185641e-01, -4.01345827e-02,  8.06454271e-02,
            2.87257284e-01, -1.73859105e-01,  2.10984781e-01, -4.19053972e-01,
            ...], dtype=float32)

## یافتن شباهت کسینوسی کاندیداها و کل متن

شباهت کسینوسی بین هریک از کاندیداها و وکتور نمایندهٔ متن را محاسبه می‌کنیم.

```python
candidates_sim_whole = cosine_similarity(all_candidates_vectors, whole_text_vector.reshape(1,-1))
candidates_sim_whole.reshape(1,-1)
```

    array([[ 1.19351953e-01,  1.23398483e-01,  1.25267982e-01,
             1.78353339e-02,  2.34080136e-01, -1.43648628e-02,
            ...]], dtype=float32)

## یافتن شباهت کسینوسی کاندیداها به یکدیگر

ماتریسی ایجاد می‌کنیم که هر درایهٔ آن با اندیس آی و جی، بیانگر شباهت کسینوسی کاندیدای آی با کاندیدای جی است.

```python
candidate_sim_candidate = cosine_similarity(all_candidates_vectors)
candidate_sim_candidate
```

    array([[0.9999997 , 0.14587443, 0.20270647, ..., 0.42830434, 0.27730745,
            0.30513293],
           [0.14587443, 0.9999996 , 0.10514447, ..., 0.48333895, 0.3179143 ,
            0.19037738],
           [0.20270647, 0.10514447, 1.        , ..., 0.47220594, 0.24125722,
            0.18565692],
           ...,
           [0.42830434, 0.48333895, 0.47220594, ..., 0.9999998 , 0.52577287,
            0.50683355],
           [0.27730745, 0.3179143 , 0.24125722, ..., 0.52577287, 0.99999964,
            0.40011758],
           [0.30513293, 0.19037738, 0.18565692, ..., 0.50683355, 0.40011758,
            0.9999996 ]], dtype=float32)

## نرمال‌سازی مقادیر مربوط به شباهت‌های کسینوسی

دو مقدار بالا را برای استفاده در مراحل بعد نرمال‌سازی می‌کنیم.

```python
candidates_sim_whole_norm = candidates_sim_whole / np.max(candidates_sim_whole)
candidates_sim_whole_norm = 0.5 + (candidates_sim_whole_norm - np.average(candidates_sim_whole_norm)) / np.std(candidates_sim_whole_norm)
candidates_sim_whole_norm
```

    array([[ 0.9393711 ],
           [ 0.979393  ],
           [ 0.9978831 ],
           [-0.06467056],
           [ 2.0740807 ],
           ...], dtype=float32)

```python
np.fill_diagonal(candidate_sim_candidate, np.NaN)
candidate_sim_candidate_norm = candidate_sim_candidate / np.nanmax(candidate_sim_candidate, axis=0)
candidate_sim_candidate_norm = 0.5 + (candidate_sim_candidate_norm - np.nanmean(candidate_sim_candidate_norm, axis=0)) / np.nanstd(candidate_sim_candidate_norm, axis=0)
candidate_sim_candidate_norm
```

    array([[nan, -3.5498703e-01,  3.2357961e-02, ...,
             1.8948689e-01,  3.9502221e-01,  6.2098056e-01],
           [-5.2607918e-01,            nan, -7.2487104e-01, ...,
             4.3979204e-01,  6.8422610e-01, -9.5400155e-02],
           [-1.7625093e-02, -6.8133366e-01,            nan, ...,
             3.8915750e-01,  1.3827083e-01, -1.2486839e-01],
           ...,
           [ 2.0007110e+00,  2.3489289e+00,  2.1240823e+00, ...,
                       nan,  2.1646044e+00,  1.8801302e+00],
           [ 6.4980078e-01,  1.0234730e+00,  3.3157024e-01, ...,
             6.3278729e-01,            nan,  1.2139380e+00],
           [ 8.9874434e-01,  1.5904903e-03, -9.9972427e-02, ...,
             5.4664868e-01,  1.2696817e+00,nan]], dtype=float32)

## استخراج کلمات کلیدی از روی شباهت‌های کسینوسی

با استفاده از روش امبدرنک در یک الگوریتم تکرارشونده، در هر مرحله با یک فرمول، یک کاندیدا به عنوان کلمهٔ کلیدی انتخاب می‌شود.
کاندیدایی انتخاب می‌شود که در درجهٔ اول بیشترین شباهت را با کل متن دارد و در درجهٔ دوم کمترین شباهت را با کاندیداهای انتخاب‌شده دارد.
میزان اثرگذاری این دو فاکتور را می‌توان با درنظرگرفتن عوامل مختلفی مثل طول و محتوای متن تغییر داد.
(beta)

```python
beta = 0.82
N = min(len(all_candidates), keyword_count)

selected_candidates = []
unselected_candidates = [i for i in range(len(all_candidates))]
best_candidate = np.argmax(candidates_sim_whole_norm)
selected_candidates.append(best_candidate)
unselected_candidates.remove(best_candidate)


for i in range(N-1):
    selected_vec = np.array(selected_candidates)
    unselected_vec = np.array(unselected_candidates)

    unselected_candidate_sim_whole_norm = candidates_sim_whole_norm[unselected_vec, :]

    dist_between = candidate_sim_candidate_norm[unselected_vec][:, selected_vec]

    if dist_between.ndim == 1:
        dist_between = dist_between[:, np.newaxis]

    best_candidate = np.argmax(beta * unselected_candidate_sim_whole_norm - (1 - beta) * np.max(dist_between, axis = 1).reshape(-1,1))
    best_index = unselected_candidates[best_candidate]
    selected_candidates.append(best_index)
    unselected_candidates.remove(best_index)
all_candidates[selected_candidates].tolist()
```

    ['معنی بی‌احترامی',
     'دلایل تشریفاتی',
     'سطح ملکه',
     'توضیح مذهبی',
     'نشریه اسپانیایی',
     'زن',
     'مراسم سال',
     'فیلم',
     'کارشناس رسمی',
     'کشور']
