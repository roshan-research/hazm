"""این ماژول شامل کلاس‌ها و توابعی برای خواندن پیکرهٔ بی‌جن‌خان است.

[پیکرهٔ
بی‌جن‌خان](https://www.peykaregan.ir/dataset/%D9%BE%DB%8C%DA%A9%D8%B1%D9%87-
%D8%A8%DB%8C%E2%80%8C%D8%AC%D9%86%E2%80%8C%D8%AE%D8%A7%D9%86) مجموعه‌ای
است از متون فارسی شامل بیش از ۲ میلیون و ۶۰۰ هزار کلمه که با ۵۵۰ نوع برچسب POS
برچسب‌گذاری شده‌اند. این پیکره که در پژوهشکدهٔ پردازش هوشمند علائم تهیه شده است
همچنین شامل بیش از ۴۳۰۰ تگ موضوعی چون سیاسی، تاریخی و ... برای متون است.

"""

import re
from pathlib import Path
from typing import Iterator
from typing import List
from typing import Optional
from typing import Tuple

from hazm import Normalizer

from .peykare_reader import join_verb_parts

default_pos_map = {
    "ADJ": "ADJ",
    "ADJ_CMPR": "ADJ",
    "ADJ_INO": "ADJ",
    "ADJ_ORD": "ADJ",
    "ADJ_SIM": "ADJ",
    "ADJ_SUP": "ADJ",
    "ADV": "ADV",
    "ADV_EXM": "ADV",
    "ADV_I": "ADV",
    "ADV_NEGG": "ADV",
    "ADV_NI": "ADV",
    "ADV_TIME": "ADV",
    "AR": "AR",
    "CON": "CONJ",
    "DEFAULT": "DEFAULT",
    "DELM": "PUNC",
    "DET": "PREP",
    "IF": "IF",
    "INT": "INT",
    "MORP": "MORP",
    "MQUA": "MQUA",
    "MS": "MS",
    "N_PL": "N",
    "N_SING": "N",
    "NN": "NN",
    "NP": "NP",
    "OH": "OH",
    "OHH": "OHH",
    "P": "PREP",
    "PP": "PP",
    "PRO": "PR",
    "PS": "PS",
    "QUA": "QUA",
    "SPEC": "SPEC",
    "V_AUX": "V",
    "V_IMP": "V",
    "V_PA": "V",
    "V_PRE": "V",
    "V_PRS": "V",
    "V_SUB": "V",
}


class BijankhanReader:
    """این کلاس شامل توابعی برای خواندن پیکرهٔ بی‌جن‌خان است.

    Args:
        bijankhan_file: مسیر فایلِ پیکره.
        joined_verb_parts: اگر `True‍` باشد افعال چندبخشی را با _ به‌هم می‌چسباند.
        pos_map: دیکشنری مبدل برچسب‌های ریز به درشت.

    """

    def __init__(
        self: "BijankhanReader",
        bijankhan_file: str,
        joined_verb_parts: bool = True,
        pos_map: Optional[str] = None,
    ) -> None:
        if pos_map is None:
            pos_map = default_pos_map
        self._bijankhan_file = bijankhan_file
        self._joined_verb_parts = joined_verb_parts
        self._pos_map = pos_map
        self._normalizer = Normalizer(correct_spacing=False)

    def _sentences(self: "BijankhanReader") -> Iterator[List[Tuple[str, str]]]:
        """جملات پیکره را به شکل متن خام برمی‌گرداند.

        Yields:
            جملهٔ بعدی.

        """
        sentence = []
        with Path(self._bijankhan_file).open(encoding="utf-8") as f:
            length = 2
            for line in f:
                parts = re.split("  +", line.strip())
                if len(parts) == length:
                    word, tag = parts
                    if word not in ("#", "*"):
                        word = self._normalizer.normalize(word)
                        sentence.append((word if word else "_", tag))
                    if (
                        tag == "DELM"
                        and word in ("#", "*", ".", "؟", "!")
                        and len(sentence)
                    ):
                        yield sentence
                        sentence = []

    def sents(self: "BijankhanReader") -> Iterator[List[Tuple[str, str]]]:
        """جملات پیکره را به شکل لیستی از `(توکن،برچسب)`ها برمی‌گرداند..

        Examples:
            >>> bijankhan = BijankhanReader(bijankhan_file='bijankhan.txt')
            >>> next(bijankhan.sents())
            [('اولین', 'ADJ'), ('سیاره', 'N'), ('خارج', 'ADJ'), ('از', 'PREP'), ('منظومه', 'N'), ('شمسی', 'ADJ'), ('دیده_شد', 'V'), ('.', 'PUNC')]

        Yields:
            جملهٔ بعدی در قالب لیستی از `(توکن،برچسب)`ها.

        """

        def map_poses(item: Tuple[str, str]) -> Tuple[str, str]:
            return (item[0], self._pos_map.get(item[1], item[1]))

        for sentence in self._sentences():
            if self._joined_verb_parts:
                sentence = join_verb_parts(sentence)
            yield list(map(map_poses, sentence))
