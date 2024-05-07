import pytest


class TestLemmatizer:

    @pytest.mark.parametrize(
        ("word", "expected"),
        [
            ("کتاب‌ها", "کتاب"),
            ("آتشفشان", "آتشفشان"),
            ("می‌روم", "رفت#رو"),
            ("گفته_شده_است", "گفت#گو"),
            ("نچشیده_است", "چشید#چش"),
            ("می‌روم", "رفت#رو"),
        ],
    )
    def test_lemmatize(self: "TestLemmatizer", lemmatizer, word, expected):
        assert lemmatizer.lemmatize(word) == expected

    @pytest.mark.parametrize(
        ("word", "pos", "expected"),
        [
            ("مردم", "N", "مردم"),
            ("اجتماعی", "AJ", "اجتماعی"),
        ],
    )
    def test_lemmatize_with_pos(self: "TestLemmatizer", lemmatizer, word, pos, expected):
        assert lemmatizer.lemmatize(word, pos) == expected


class TestConjugation:
    # ri: بن ماضی
    # rii: بن مضارع

    def test_perfective_past(self: "TestConjugation", conjugation):
        actual = conjugation.perfective_past("دید")
        expected = ["دیدم", "دیدی", "دید", "دیدیم", "دیدید", "دیدند"]
        assert actual == expected

    def test_negative_perfective_past(self: "TestConjugation", conjugation):
        actual = conjugation.negative_perfective_past("دید")
        expected = ["ندیدم", "ندیدی", "ندید", "ندیدیم", "ندیدید", "ندیدند"]
        assert actual == expected

    def test_passive_perfective_past(self: "TestConjugation", conjugation):
        actual = conjugation.passive_perfective_past("دید")
        expected = [
            "دیده شدم",
            "دیده شدی",
            "دیده شد",
            "دیده شدیم",
            "دیده شدید",
            "دیده شدند",
        ]
        assert actual == expected

    def test_negative_passive_perfective_past(self: "TestConjugation", conjugation):
        actual = conjugation.negative_passive_perfective_past("دید")
        expected = [
            "دیده نشدم",
            "دیده نشدی",
            "دیده نشد",
            "دیده نشدیم",
            "دیده نشدید",
            "دیده نشدند",
        ]
        assert actual == expected

    def test_imperfective_past(self: "TestConjugation", conjugation):
        actual = conjugation.imperfective_past("دید")
        expected = ["می‌دیدم", "می‌دیدی", "می‌دید", "می‌دیدیم", "می‌دیدید", "می‌دیدند"]
        assert actual == expected

    def test_negative_imperfective_past(self: "TestConjugation", conjugation):
        actual = conjugation.negative_imperfective_past("دید")
        expected = ["نمی‌دیدم", "نمی‌دیدی", "نمی‌دید", "نمی‌دیدیم", "نمی‌دیدید", "نمی‌دیدند"]
        assert actual == expected

    def test_passive_imperfective_past(self: "TestConjugation", conjugation):
        actual = conjugation.passive_imperfective_past("دید")
        expected = [
            "دیده می‌شدم",
            "دیده می‌شدی",
            "دیده می‌شد",
            "دیده می‌شدیم",
            "دیده می‌شدید",
            "دیده می‌شدند",
        ]
        assert actual == expected

    def test_negative_passive_imperfective_past(self: "TestConjugation", conjugation):
        actual = conjugation.negative_passive_imperfective_past("دید")
        expected = [
            "دیده نمی‌شدم",
            "دیده نمی‌شدی",
            "دیده نمی‌شد",
            "دیده نمی‌شدیم",
            "دیده نمی‌شدید",
            "دیده نمی‌شدند",
        ]
        assert actual == expected

    def test_past_progresive(self: "TestConjugation", conjugation):
        actual = conjugation.past_progresive("دید")
        expected = [
            "داشتم می‌دیدم",
            "داشتی می‌دیدی",
            "داشت می‌دید",
            "داشتیم می‌دیدیم",
            "داشتید می‌دیدید",
            "داشتند می‌دیدند",
        ]
        assert actual == expected

    def test_passive_past_progresive(self: "TestConjugation", conjugation):
        actual = conjugation.passive_past_progresive("دید")
        expected = [
            "داشتم دیده می‌شدم",
            "داشتی دیده می‌شدی",
            "داشت دیده می‌شد",
            "داشتیم دیده می‌شدیم",
            "داشتید دیده می‌شدید",
            "داشتند دیده می‌شدند",
        ]
        assert actual == expected

    def test_present_perfect(self: "TestConjugation", conjugation):
        actual = conjugation.present_perfect("دید")
        expected = [
            "دیده‌ام",
            "دیده‌ای",
            "دیده است",
            "دیده",
            "دیده‌ایم",
            "دیده‌اید",
            "دیده‌اند",
        ]
        assert actual == expected

    def test_negative_present_perfect(self: "TestConjugation", conjugation):
        actual = conjugation.negative_present_perfect("دید")
        expected = [
            "ندیده‌ام",
            "ندیده‌ای",
            "ندیده است",
            "ندیده",
            "ندیده‌ایم",
            "ندیده‌اید",
            "ندیده‌اند",
        ]
        assert actual == expected

    def test_subjunctive_present_perfect(self: "TestConjugation", conjugation):
        actual = conjugation.subjunctive_present_perfect("دید")
        expected = [
            "دیده باشم",
            "دیده باشی",
            "دیده باشد",
            "دیده باشیم",
            "دیده باشید",
            "دیده باشند",
        ]
        assert actual == expected

    def test_negative_subjunctive_present_perfect(self: "TestConjugation", conjugation):
        actual = conjugation.negative_subjunctive_present_perfect("دید")
        expected = [
            "ندیده باشم",
            "ندیده باشی",
            "ندیده باشد",
            "ندیده باشیم",
            "ندیده باشید",
            "ندیده باشند",
        ]
        assert actual == expected

    def test_grammatical_present_perfect(self: "TestConjugation", conjugation):
        actual = conjugation.grammatical_present_perfect("دید")
        expected = [
            "دیده باشم",
            "دیده باش",
            "دیده باشد",
            "دیده باشیم",
            "دیده باشید",
            "دیده باشند",
        ]
        assert actual == expected

    def test_negative_grammatical_present_perfect(self: "TestConjugation", conjugation):
        actual = conjugation.negative_grammatical_present_perfect("دید")
        expected = [
            "ندیده باشم",
            "ندیده باش",
            "ندیده باشد",
            "ندیده باشیم",
            "ندیده باشید",
            "ندیده باشند",
        ]
        assert actual == expected

    def test_passive_present_perfect(self: "TestConjugation", conjugation):
        actual = conjugation.passive_present_perfect("دید")
        expected = [
            "دیده شده‌ام",
            "دیده شده‌ای",
            "دیده شده است",
            "دیده شده",
            "دیده شده‌ایم",
            "دیده شده‌اید",
            "دیده شده‌اند",
        ]
        assert actual == expected

    def test_negative_passive_present_perfect(self: "TestConjugation", conjugation):
        actual = conjugation.negative_passive_present_perfect("دید")
        expected = [
            "دیده نشده‌ام",
            "دیده نشده‌ای",
            "دیده نشده است",
            "دیده نشده",
            "دیده نشده‌ایم",
            "دیده نشده‌اید",
            "دیده نشده‌اند",
        ]
        assert actual == expected

    def test_passive_subjunctive_present_perfect(self: "TestConjugation", conjugation):
        actual = conjugation.passive_subjunctive_present_perfect("دید")
        expected = [
            "دیده شده باشم",
            "دیده شده باشی",
            "دیده شده باشد",
            "دیده شده باشیم",
            "دیده شده باشید",
            "دیده شده باشند",
        ]
        assert actual == expected

    def test_negative_passive_subjunctive_present_perfect(self: "TestConjugation", conjugation):
        actual = conjugation.negative_passive_subjunctive_present_perfect("دید")
        expected = [
            "دیده نشده باشم",
            "دیده نشده باشی",
            "دیده نشده باشد",
            "دیده نشده باشیم",
            "دیده نشده باشید",
            "دیده نشده باشند",
        ]
        assert actual == expected

    def test_passive_grammatical_present_perfect(self: "TestConjugation", conjugation):
        actual = conjugation.passive_grammatical_present_perfect("دید")
        expected = [
            "دیده شده باشم",
            "دیده شده باش",
            "دیده شده باشد",
            "دیده شده باشیم",
            "دیده شده باشید",
            "دیده شده باشند",
        ]
        assert actual == expected

    def test_negative_passive_grammatical_present_perfect(self: "TestConjugation", conjugation):
        actual = conjugation.negative_passive_grammatical_present_perfect("دید")
        expected = [
            "دیده نشده باشم",
            "دیده نشده باش",
            "دیده نشده باشد",
            "دیده نشده باشیم",
            "دیده نشده باشید",
            "دیده نشده باشند",
        ]
        assert actual == expected

    def test_imperfective_present_perfect(self: "TestConjugation", conjugation):
        actual = conjugation.imperfective_present_perfect("دید")
        expected = [
            "می‌دیده‌ام",
            "می‌دیده‌ای",
            "می‌دیده است",
            "می‌دیده",
            "می‌دیده‌ایم",
            "می‌دیده‌اید",
            "می‌دیده‌اند",
        ]
        assert actual == expected

    def test_negative_imperfective_present_perfect(self: "TestConjugation", conjugation):
        actual = conjugation.negative_imperfective_present_perfect("دید")
        expected = [
            "نمی‌دیده‌ام",
            "نمی‌دیده‌ای",
            "نمی‌دیده است",
            "نمی‌دیده",
            "نمی‌دیده‌ایم",
            "نمی‌دیده‌اید",
            "نمی‌دیده‌اند",
        ]
        assert actual == expected

    def test_subjunctive_imperfective_present_perfect(self: "TestConjugation", conjugation):
        actual = conjugation.subjunctive_imperfective_present_perfect("دید")
        expected = [
            "می‌دیده باشم",
            "می‌دیده باشی",
            "می‌دیده باشد",
            "می‌دیده باشیم",
            "می‌دیده باشید",
            "می‌دیده باشند",
        ]
        assert actual == expected

    def test_negative_subjunctive_imperfective_present_perfect(self: "TestConjugation", conjugation):
        actual = conjugation.negative_subjunctive_imperfective_present_perfect("دید")
        expected = [
            "نمی‌دیده باشم",
            "نمی‌دیده باشی",
            "نمی‌دیده باشد",
            "نمی‌دیده باشیم",
            "نمی‌دیده باشید",
            "نمی‌دیده باشند",
        ]
        assert actual == expected

    def test_passive_imperfective_present_perfect(self: "TestConjugation", conjugation):
        actual = conjugation.passive_imperfective_present_perfect("دید")
        expected = [
            "دیده می‌شده‌ام",
            "دیده می‌شده‌ای",
            "دیده می‌شده است",
            "دیده می‌شده",
            "دیده می‌شده‌ایم",
            "دیده می‌شده‌اید",
            "دیده می‌شده‌اند",
        ]
        assert actual == expected

    def test_negative_passive_imperfective_present_perfect(self: "TestConjugation", conjugation):
        actual = conjugation.negative_passive_imperfective_present_perfect("دید")
        expected = [
            "دیده نمی‌شده‌ام",
            "دیده نمی‌شده‌ای",
            "دیده نمی‌شده است",
            "دیده نمی‌شده",
            "دیده نمی‌شده‌ایم",
            "دیده نمی‌شده‌اید",
            "دیده نمی‌شده‌اند",
        ]
        assert actual == expected

    def test_passive_subjunctive_imperfective_present_perfect(self: "TestConjugation", conjugation):
        actual = conjugation.passive_subjunctive_imperfective_present_perfect("دید")
        expected = [
            "دیده می‌شده باشم",
            "دیده می‌شده باشی",
            "دیده می‌شده باشد",
            "دیده می‌شده باشیم",
            "دیده می‌شده باشید",
            "دیده می‌شده باشند",
        ]
        assert actual == expected

    def test_negative_passive_subjunctive_imperfective_present_perfect(
        self: "TestConjugation", conjugation,
    ):
        actual = conjugation.negative_passive_subjunctive_imperfective_present_perfect(
            "دید",
        )
        expected = [
            "دیده نمی‌شده باشم",
            "دیده نمی‌شده باشی",
            "دیده نمی‌شده باشد",
            "دیده نمی‌شده باشیم",
            "دیده نمی‌شده باشید",
            "دیده نمی‌شده باشند",
        ]
        assert actual == expected

    def test_present_perfect_progressive(self: "TestConjugation", conjugation):
        actual = conjugation.present_perfect_progressive("دید")
        expected = [
            "داشته‌ام می‌دیده‌ام",
            "داشته‌ای می‌دیده‌ای",
            "داشته است می‌دیده است",
            "داشته می‌دیده",
            "داشته‌ایم می‌دیده‌ایم",
            "داشته‌اید می‌دیده‌اید",
            "داشته‌اند می‌دیده‌اند",
        ]
        assert actual == expected

    def test_passive_present_perfect_progressive(self: "TestConjugation", conjugation):
        actual = conjugation.passive_present_perfect_progressive("دید")
        expected = [
            "داشته‌ام دیده می‌شده‌ام",
            "داشته‌ای دیده می‌شده‌ای",
            "داشته است دیده می‌شده است",
            "داشته دیده می‌شده",
            "داشته‌ایم دیده می‌شده‌ایم",
            "داشته‌اید دیده می‌شده‌اید",
            "داشته‌اند دیده می‌شده‌اند",
        ]
        assert actual == expected

    def test_past_precedent(self: "TestConjugation", conjugation):
        actual = conjugation.past_precedent("دید")
        expected = [
            "دیده بودم",
            "دیده بودی",
            "دیده بود",
            "دیده بودیم",
            "دیده بودید",
            "دیده بودند",
        ]
        assert actual == expected

    def test_negative_past_precedent(self: "TestConjugation", conjugation):
        actual = conjugation.negative_past_precedent("دید")
        expected = [
            "ندیده بودم",
            "ندیده بودی",
            "ندیده بود",
            "ندیده بودیم",
            "ندیده بودید",
            "ندیده بودند",
        ]
        assert actual == expected

    def test_passive_past_precedent(self: "TestConjugation", conjugation):
        actual = conjugation.passive_past_precedent("دید")
        expected = [
            "دیده شده بودم",
            "دیده شده بودی",
            "دیده شده بود",
            "دیده شده بودیم",
            "دیده شده بودید",
            "دیده شده بودند",
        ]
        assert actual == expected

    def test_negative_passive_past_precedent(self: "TestConjugation", conjugation):
        actual = conjugation.negative_passive_past_precedent("دید")
        expected = [
            "دیده نشده بودم",
            "دیده نشده بودی",
            "دیده نشده بود",
            "دیده نشده بودیم",
            "دیده نشده بودید",
            "دیده نشده بودند",
        ]
        assert actual == expected

    def test_imperfective_past_precedent(self: "TestConjugation", conjugation):
        actual = conjugation.imperfective_past_precedent("دید")
        expected = [
            "می‌دیده بودم",
            "می‌دیده بودی",
            "می‌دیده بود",
            "می‌دیده بودیم",
            "می‌دیده بودید",
            "می‌دیده بودند",
        ]
        assert actual == expected

    def test_negative_imperfective_past_precedent(self: "TestConjugation", conjugation):
        actual = conjugation.negative_imperfective_past_precedent("دید")
        expected = [
            "نمی‌دیده بودم",
            "نمی‌دیده بودی",
            "نمی‌دیده بود",
            "نمی‌دیده بودیم",
            "نمی‌دیده بودید",
            "نمی‌دیده بودند",
        ]
        assert actual == expected

    def test_passive_imperfective_past_precedent(self: "TestConjugation", conjugation):
        actual = conjugation.passive_imperfective_past_precedent("دید")
        expected = [
            "دیده می‌شده بودم",
            "دیده می‌شده بودی",
            "دیده می‌شده بود",
            "دیده می‌شده بودیم",
            "دیده می‌شده بودید",
            "دیده می‌شده بودند",
        ]
        assert actual == expected

    def test_negative_passive_imperfective_past_precedent(self: "TestConjugation", conjugation):
        actual = conjugation.negative_passive_imperfective_past_precedent("دید")
        expected = [
            "دیده نمی‌شده بودم",
            "دیده نمی‌شده بودی",
            "دیده نمی‌شده بود",
            "دیده نمی‌شده بودیم",
            "دیده نمی‌شده بودید",
            "دیده نمی‌شده بودند",
        ]
        assert actual == expected

    def test_past_precedent_progressive(self: "TestConjugation", conjugation):
        actual = conjugation.past_precedent_progressive("دید")
        expected = [
            "داشتم می‌دیده بودم",
            "داشتی می‌دیده بودی",
            "داشت می‌دیده بود",
            "داشتیم می‌دیده بودیم",
            "داشتید می‌دیده بودید",
            "داشتند می‌دیده بودند",
        ]
        assert actual == expected

    def test_passive_past_precedent_progressive(self: "TestConjugation", conjugation):
        actual = conjugation.passive_past_precedent_progressive("دید")
        expected = [
            "داشتم دیده می‌شده بودم",
            "داشتی دیده می‌شده بودی",
            "داشت دیده می‌شده بود",
            "داشتیم دیده می‌شده بودیم",
            "داشتید دیده می‌شده بودید",
            "داشتند دیده می‌شده بودند",
        ]
        assert actual == expected

    def test_past_precedent_perfect(self: "TestConjugation", conjugation):
        actual = conjugation.past_precedent_perfect("دید")
        expected = [
            "دیده بوده‌ام",
            "دیده بوده‌ای",
            "دیده بوده است",
            "دیده بوده",
            "دیده بوده‌ایم",
            "دیده بوده‌اید",
            "دیده بوده‌اند",
        ]
        assert actual == expected

    def test_negative_past_precedent_perfect(self: "TestConjugation", conjugation):
        actual = conjugation.negative_past_precedent_perfect("دید")
        expected = [
            "ندیده بوده‌ام",
            "ندیده بوده‌ای",
            "ندیده بوده است",
            "ندیده بوده",
            "ندیده بوده‌ایم",
            "ندیده بوده‌اید",
            "ندیده بوده‌اند",
        ]
        assert actual == expected

    def test_subjunctive_past_precedent_perfect(self: "TestConjugation", conjugation):
        actual = conjugation.subjunctive_past_precedent_perfect("دید")
        expected = [
            "دیده بوده باشم",
            "دیده بوده باشی",
            "دیده بوده باشد",
            "دیده بوده باشیم",
            "دیده بوده باشید",
            "دیده بوده باشند",
        ]
        assert actual == expected

    def test_negative_subjunctive_past_precedent_perfect(self: "TestConjugation", conjugation):
        actual = conjugation.negative_subjunctive_past_precedent_perfect("دید")
        expected = [
            "ندیده بوده باشم",
            "ندیده بوده باشی",
            "ندیده بوده باشد",
            "ندیده بوده باشیم",
            "ندیده بوده باشید",
            "ندیده بوده باشند",
        ]
        assert actual == expected

    def test_grammatical_past_precedent_perfect(self: "TestConjugation", conjugation):
        actual = conjugation.grammatical_past_precedent_perfect("دید")
        expected = [
            "دیده بوده باشم",
            "دیده بوده باش",
            "دیده بوده باشد",
            "دیده بوده باشیم",
            "دیده بوده باشید",
            "دیده بوده باشند",
        ]
        assert actual == expected

    def test_negative_grammatical_past_precedent_perfect(self: "TestConjugation", conjugation):
        actual = conjugation.negative_grammatical_past_precedent_perfect("دید")
        expected = [
            "ندیده بوده باشم",
            "ندیده بوده باش",
            "ندیده بوده باشد",
            "ندیده بوده باشیم",
            "ندیده بوده باشید",
            "ندیده بوده باشند",
        ]
        assert actual == expected

    def test_passive_past_precedent_perfect(self: "TestConjugation", conjugation):
        actual = conjugation.passive_past_precedent_perfect("دید")
        expected = [
            "دیده شده بوده‌ام",
            "دیده شده بوده‌ای",
            "دیده شده بوده است",
            "دیده شده بوده",
            "دیده شده بوده‌ایم",
            "دیده شده بوده‌اید",
            "دیده شده بوده‌اند",
        ]
        assert actual == expected

    def test_negative_passive_past_precedent_perfect(self: "TestConjugation", conjugation):
        actual = conjugation.negative_passive_past_precedent_perfect("دید")
        expected = [
            "دیده نشده بوده‌ام",
            "دیده نشده بوده‌ای",
            "دیده نشده بوده است",
            "دیده نشده بوده",
            "دیده نشده بوده‌ایم",
            "دیده نشده بوده‌اید",
            "دیده نشده بوده‌اند",
        ]
        assert actual == expected

    def test_passive_subjunctive_past_precedent_perfect(self: "TestConjugation", conjugation):
        actual = conjugation.passive_subjunctive_past_precedent_perfect("دید")
        expected = [
            "دیده شده بوده باشم",
            "دیده شده بوده باشی",
            "دیده شده بوده باشد",
            "دیده شده بوده باشیم",
            "دیده شده بوده باشید",
            "دیده شده بوده باشند",
        ]
        assert actual == expected

    def test_negative_passive_subjunctive_past_precedent_perfect(self: "TestConjugation", conjugation):
        actual = conjugation.negative_passive_subjunctive_past_precedent_perfect("دید")
        expected = [
            "دیده نشده بوده باشم",
            "دیده نشده بوده باشی",
            "دیده نشده بوده باشد",
            "دیده نشده بوده باشیم",
            "دیده نشده بوده باشید",
            "دیده نشده بوده باشند",
        ]
        assert actual == expected

    def test_passive_grammatical_past_precedent_perfect(self: "TestConjugation", conjugation):
        actual = conjugation.passive_grammatical_past_precedent_perfect("دید")
        expected = [
            "دیده شده بوده باشم",
            "دیده شده بوده باش",
            "دیده شده بوده باشد",
            "دیده شده بوده باشیم",
            "دیده شده بوده باشید",
            "دیده شده بوده باشند",
        ]
        assert actual == expected

    def test_negative_passive_grammatical_past_precedent_perfect(self: "TestConjugation", conjugation):
        actual = conjugation.negative_passive_grammatical_past_precedent_perfect("دید")
        expected = [
            "دیده نشده بوده باشم",
            "دیده نشده بوده باش",
            "دیده نشده بوده باشد",
            "دیده نشده بوده باشیم",
            "دیده نشده بوده باشید",
            "دیده نشده بوده باشند",
        ]
        assert actual == expected

    def test_imperfective_past_precedent_perfect(self: "TestConjugation", conjugation):
        actual = conjugation.imperfective_past_precedent_perfect("دید")
        expected = [
            "می‌دیده بوده‌ام",
            "می‌دیده بوده‌ای",
            "می‌دیده بوده است",
            "می‌دیده بوده",
            "می‌دیده بوده‌ایم",
            "می‌دیده بوده‌اید",
            "می‌دیده بوده‌اند",
        ]
        assert actual == expected

    def test_negative_imperfective_past_precedent_perfect(self: "TestConjugation", conjugation):
        actual = conjugation.negative_imperfective_past_precedent_perfect("دید")
        expected = [
            "نمی‌دیده بوده‌ام",
            "نمی‌دیده بوده‌ای",
            "نمی‌دیده بوده است",
            "نمی‌دیده بوده",
            "نمی‌دیده بوده‌ایم",
            "نمی‌دیده بوده‌اید",
            "نمی‌دیده بوده‌اند",
        ]
        assert actual == expected

    def test_subjunctive_imperfective_past_precedent_perfect(self: "TestConjugation", conjugation):
        actual = conjugation.subjunctive_imperfective_past_precedent_perfect("دید")
        expected = [
            "می‌دیده بوده باشم",
            "می‌دیده بوده باشی",
            "می‌دیده بوده باشد",
            "می‌دیده بوده باشیم",
            "می‌دیده بوده باشید",
            "می‌دیده بوده باشند",
        ]
        assert actual == expected

    def test_negative_subjunctive_imperfective_past_precedent_perfect(
        self: "TestConjugation", conjugation,
    ):
        actual = conjugation.negative_subjunctive_imperfective_past_precedent_perfect(
            "دید",
        )
        expected = [
            "نمی‌دیده بوده باشم",
            "نمی‌دیده بوده باشی",
            "نمی‌دیده بوده باشد",
            "نمی‌دیده بوده باشیم",
            "نمی‌دیده بوده باشید",
            "نمی‌دیده بوده باشند",
        ]
        assert actual == expected

    def test_passive_imperfective_past_precedent_perfect(self: "TestConjugation", conjugation):
        actual = conjugation.passive_imperfective_past_precedent_perfect("دید")
        expected = [
            "دیده می‌شده بوده‌ام",
            "دیده می‌شده بوده‌ای",
            "دیده می‌شده بوده است",
            "دیده می‌شده بوده",
            "دیده می‌شده بوده‌ایم",
            "دیده می‌شده بوده‌اید",
            "دیده می‌شده بوده‌اند",
        ]
        assert actual == expected

    def test_negative_passive_imperfective_past_precedent_perfect(self: "TestConjugation", conjugation):
        actual = conjugation.negative_passive_imperfective_past_precedent_perfect("دید")
        expected = [
            "دیده نمی‌شده بوده‌ام",
            "دیده نمی‌شده بوده‌ای",
            "دیده نمی‌شده بوده است",
            "دیده نمی‌شده بوده",
            "دیده نمی‌شده بوده‌ایم",
            "دیده نمی‌شده بوده‌اید",
            "دیده نمی‌شده بوده‌اند",
        ]
        assert actual == expected

    def test_passive_subjunctive_imperfective_past_precedent_perfect(self: "TestConjugation", conjugation):
        actual = conjugation.passive_subjunctive_imperfective_past_precedent_perfect(
            "دید",
        )
        expected = [
            "دیده می‌شده بوده باشم",
            "دیده می‌شده بوده باشی",
            "دیده می‌شده بوده باشد",
            "دیده می‌شده بوده باشیم",
            "دیده می‌شده بوده باشید",
            "دیده می‌شده بوده باشند",
        ]
        assert actual == expected

    def test_negative_passive_subjunctive_imperfective_past_precedent_perfect(
        self: "TestConjugation", conjugation,
    ):
        actual = conjugation.negative_passive_subjunctive_imperfective_past_precedent_perfect(
            "دید",
        )
        expected = [
            "دیده نمی‌شده بوده باشم",
            "دیده نمی‌شده بوده باشی",
            "دیده نمی‌شده بوده باشد",
            "دیده نمی‌شده بوده باشیم",
            "دیده نمی‌شده بوده باشید",
            "دیده نمی‌شده بوده باشند",
        ]
        assert actual == expected

    def test_past_precedent_perfect_progressive(self: "TestConjugation", conjugation):
        actual = conjugation.past_precedent_perfect_progressive("دید")
        expected = [
            "داشته‌ام می‌دیده بوده‌ام",
            "داشته‌ای می‌دیده بوده‌ای",
            "داشته است می‌دیده بوده است",
            "داشته می‌دیده بوده",
            "داشته‌ایم می‌دیده بوده‌ایم",
            "داشته‌اید می‌دیده بوده‌اید",
            "داشته‌اند می‌دیده بوده‌اند",
        ]
        assert actual == expected

    def test_passive_past_precedent_perfect_progressive(self: "TestConjugation", conjugation):
        actual = conjugation.passive_past_precedent_perfect_progressive("دید")
        expected = [
            "داشته‌ام دیده می‌شده بوده‌ام",
            "داشته‌ای دیده می‌شده بوده‌ای",
            "داشته است دیده می‌شده بوده است",
            "داشته دیده می‌شده بوده",
            "داشته‌ایم دیده می‌شده بوده‌ایم",
            "داشته‌اید دیده می‌شده بوده‌اید",
            "داشته‌اند دیده می‌شده بوده‌اند",
        ]
        assert actual == expected

    def test_perfective_present(self: "TestConjugation", conjugation):
        actual = conjugation.perfective_present("بین")
        expected = ["بینم", "بینی", "بیند", "بینیم", "بینید", "بینند"]
        assert actual == expected

    def test_negative_perfective_present(self: "TestConjugation", conjugation):
        actual = conjugation.negative_perfective_present("بین")
        expected = ["نبینم", "نبینی", "نبیند", "نبینیم", "نبینید", "نبینند"]
        assert actual == expected

    def test_subjunctive_perfective_present(self: "TestConjugation", conjugation):
        actual = conjugation.subjunctive_perfective_present("بین")
        expected = ["ببینم", "ببینی", "ببیند", "ببینیم", "ببینید", "ببینند"]
        assert actual == expected

    def test_negative_subjunctive_perfective_present(self: "TestConjugation", conjugation):
        actual = conjugation.negative_subjunctive_perfective_present("بین")
        expected = ["نبینم", "نبینی", "نبیند", "نبینیم", "نبینید", "نبینند"]
        assert actual == expected

    def test_grammatical_perfective_present(self: "TestConjugation", conjugation):
        actual = conjugation.grammatical_perfective_present("بین")
        expected = ["ببینم", "ببین", "ببیند", "ببینیم", "ببینید", "ببینند"]
        assert actual == expected

    def test_negative_grammatical_perfective_present(self: "TestConjugation", conjugation):
        actual = conjugation.negative_grammatical_perfective_present("بین")
        expected = ["نبینم", "نبین", "نبیند", "نبینیم", "نبینید", "نبینند"]
        assert actual == expected

    def test_passive_perfective_present(self: "TestConjugation", conjugation):
        actual = conjugation.passive_perfective_present("دید")
        expected = [
            "دیده شوم",
            "دیده شوی",
            "دیده شود",
            "دیده شویم",
            "دیده شوید",
            "دیده شوند",
        ]
        assert actual == expected

    def test_negative_passive_perfective_present(self: "TestConjugation", conjugation):
        actual = conjugation.negative_passive_perfective_present("دید")
        expected = [
            "دیده نشوم",
            "دیده نشوی",
            "دیده نشود",
            "دیده نشویم",
            "دیده نشوید",
            "دیده نشوند",
        ]
        assert actual == expected

    def test_passive_subjunctive_perfective_present(self: "TestConjugation", conjugation):
        actual = conjugation.passive_subjunctive_perfective_present("دید")
        expected = [
            "دیده بشوم",
            "دیده بشوی",
            "دیده بشود",
            "دیده بشویم",
            "دیده بشوید",
            "دیده بشوند",
        ]
        assert actual == expected

    def test_negative_passive_subjunctive_perfective_present(self: "TestConjugation", conjugation):
        actual = conjugation.negative_passive_subjunctive_perfective_present("دید")
        expected = [
            "دیده نشوم",
            "دیده نشوی",
            "دیده نشود",
            "دیده نشویم",
            "دیده نشوید",
            "دیده نشوند",
        ]
        assert actual == expected

    def test_passive_grammatical_perfective_present(self: "TestConjugation", conjugation):
        actual = conjugation.passive_grammatical_perfective_present("دید")
        expected = [
            "دیده بشوم",
            "دیده بشو",
            "دیده بشود",
            "دیده بشویم",
            "دیده بشوید",
            "دیده بشوند",
        ]
        assert actual == expected

    def test_negative_passive_grammatical_perfective_present(self: "TestConjugation", conjugation):
        actual = conjugation.negative_passive_grammatical_perfective_present("دید")
        expected = [
            "دیده نشوم",
            "دیده نشو",
            "دیده نشود",
            "دیده نشویم",
            "دیده نشوید",
            "دیده نشوند",
        ]
        assert actual == expected

    def test_imperfective_present(self: "TestConjugation", conjugation):
        actual = conjugation.imperfective_present("بین")
        expected = ["می‌بینم", "می‌بینی", "می‌بیند", "می‌بینیم", "می‌بینید", "می‌بینند"]
        assert actual == expected

    def test_negative_imperfective_present(self: "TestConjugation", conjugation):
        actual = conjugation.negative_imperfective_present("بین")
        expected = ["نمی‌بینم", "نمی‌بینی", "نمی‌بیند", "نمی‌بینیم", "نمی‌بینید", "نمی‌بینند"]
        assert actual == expected

    def test_passive_imperfective_present(self: "TestConjugation", conjugation):
        actual = conjugation.passive_imperfective_present("دید")
        expected = [
            "دیده می‌شوم",
            "دیده می‌شوی",
            "دیده می‌شود",
            "دیده می‌شویم",
            "دیده می‌شوید",
            "دیده می‌شوند",
        ]
        assert actual == expected

    def test_negative_passive_imperfective_present(self: "TestConjugation", conjugation):
        actual = conjugation.negative_passive_imperfective_present("دید")
        expected = [
            "دیده نمی‌شوم",
            "دیده نمی‌شوی",
            "دیده نمی‌شود",
            "دیده نمی‌شویم",
            "دیده نمی‌شوید",
            "دیده نمی‌شوند",
        ]
        assert actual == expected

    def test_present_progressive(self: "TestConjugation", conjugation):
        actual = conjugation.present_progressive("بین")
        expected = [
            "دارم می‌بینم",
            "داری می‌بینی",
            "دارد می‌بیند",
            "داریم می‌بینیم",
            "دارید می‌بینید",
            "دارند می‌بینند",
        ]
        assert actual == expected

    def test_passive_present_progressive(self: "TestConjugation", conjugation):
        actual = conjugation.passive_present_progressive("دید")
        expected = [
            "دارم دیده می‌شوم",
            "داری دیده می‌شوی",
            "دارد دیده می‌شود",
            "داریم دیده می‌شویم",
            "دارید دیده می‌شوید",
            "دارند دیده می‌شوند",
        ]
        assert actual == expected

    def test_perfective_future(self: "TestConjugation", conjugation):
        actual = conjugation.perfective_future("دید")
        expected = [
            "خواهم دید",
            "خواهی دید",
            "خواهد دید",
            "خواهیم دید",
            "خواهید دید",
            "خواهند دید",
        ]
        assert actual == expected

    def test_negative_perfective_future(self: "TestConjugation", conjugation):
        actual = conjugation.negative_perfective_future("دید")
        expected = [
            "نخواهم دید",
            "نخواهی دید",
            "نخواهد دید",
            "نخواهیم دید",
            "نخواهید دید",
            "نخواهند دید",
        ]
        assert actual == expected

    def test_passive_perfective_future(self: "TestConjugation", conjugation):
        actual = conjugation.passive_perfective_future("دید")
        expected = [
            "دیده خواهم شد",
            "دیده خواهی شد",
            "دیده خواهد شد",
            "دیده خواهیم شد",
            "دیده خواهید شد",
            "دیده خواهند شد",
        ]
        assert actual == expected

    def test_negative_passive_perfective_future(self: "TestConjugation", conjugation):
        actual = conjugation.negative_passive_perfective_future("دید")
        expected = [
            "دیده نخواهم شد",
            "دیده نخواهی شد",
            "دیده نخواهد شد",
            "دیده نخواهیم شد",
            "دیده نخواهید شد",
            "دیده نخواهند شد",
        ]
        assert actual == expected

    def test_imperfective_future(self: "TestConjugation", conjugation):
        actual = conjugation.imperfective_future("دید")
        expected = [
            "می‌خواهم دید",
            "می‌خواهی دید",
            "می‌خواهد دید",
            "می‌خواهیم دید",
            "می‌خواهید دید",
            "می‌خواهند دید",
        ]
        assert actual == expected

    def test_negative_imperfective_future(self: "TestConjugation", conjugation):
        actual = conjugation.negative_imperfective_future("دید")
        expected = [
            "نمی‌خواهم دید",
            "نمی‌خواهی دید",
            "نمی‌خواهد دید",
            "نمی‌خواهیم دید",
            "نمی‌خواهید دید",
            "نمی‌خواهند دید",
        ]
        assert actual == expected

    def test_passive_imperfective_future(self: "TestConjugation", conjugation):
        actual = conjugation.passive_imperfective_future("دید")
        expected = [
            "دیده می‌خواهم شد",
            "دیده می‌خواهی شد",
            "دیده می‌خواهد شد",
            "دیده می‌خواهیم شد",
            "دیده می‌خواهید شد",
            "دیده می‌خواهند شد",
        ]
        assert actual == expected

    def test_negative_passive_imperfective_future(self: "TestConjugation", conjugation):
        actual = conjugation.negative_passive_imperfective_future("دید")
        expected = [
            "دیده نمی‌خواهم شد",
            "دیده نمی‌خواهی شد",
            "دیده نمی‌خواهد شد",
            "دیده نمی‌خواهیم شد",
            "دیده نمی‌خواهید شد",
            "دیده نمی‌خواهند شد",
        ]
        assert actual == expected

    def test_future_precedent(self: "TestConjugation", conjugation):
        actual = conjugation.future_precedent("دید")
        expected = [
            "دیده خواهم بود",
            "دیده خواهی بود",
            "دیده خواهد بود",
            "دیده خواهیم بود",
            "دیده خواهید بود",
            "دیده خواهند بود",
        ]
        assert actual == expected

    def test_negative_future_precedent(self: "TestConjugation", conjugation):
        actual = conjugation.negative_future_precedent("دید")
        expected = [
            "ندیده خواهم بود",
            "ندیده خواهی بود",
            "ندیده خواهد بود",
            "ندیده خواهیم بود",
            "ندیده خواهید بود",
            "ندیده خواهند بود",
        ]
        assert actual == expected

    def test_passive_future_precedent(self: "TestConjugation", conjugation):
        actual = conjugation.passive_future_precedent("دید")
        expected = [
            "دیده شده خواهم بود",
            "دیده شده خواهی بود",
            "دیده شده خواهد بود",
            "دیده شده خواهیم بود",
            "دیده شده خواهید بود",
            "دیده شده خواهند بود",
        ]
        assert actual == expected

    def test_negative_passive_future_precedent(self: "TestConjugation", conjugation):
        actual = conjugation.negative_passive_future_precedent("دید")
        expected = [
            "دیده نشده خواهم بود",
            "دیده نشده خواهی بود",
            "دیده نشده خواهد بود",
            "دیده نشده خواهیم بود",
            "دیده نشده خواهید بود",
            "دیده نشده خواهند بود",
        ]
        assert actual == expected

    def test_future_precedent_imperfective(self: "TestConjugation", conjugation):
        actual = conjugation.future_precedent_imperfective("دید")
        expected = [
            "می‌دیده خواهم بود",
            "می‌دیده خواهی بود",
            "می‌دیده خواهد بود",
            "می‌دیده خواهیم بود",
            "می‌دیده خواهید بود",
            "می‌دیده خواهند بود",
        ]
        assert actual == expected

    def test_negative_future_precedent_imperfective(self: "TestConjugation", conjugation):
        actual = conjugation.negative_future_precedent_imperfective("دید")
        expected = [
            "نمی‌دیده خواهم بود",
            "نمی‌دیده خواهی بود",
            "نمی‌دیده خواهد بود",
            "نمی‌دیده خواهیم بود",
            "نمی‌دیده خواهید بود",
            "نمی‌دیده خواهند بود",
        ]
        assert actual == expected

    def test_passive_future_precedent_imperfective(self: "TestConjugation", conjugation):
        actual = conjugation.passive_future_precedent_imperfective("دید")
        expected = [
            "دیده می‌شده خواهم بود",
            "دیده می‌شده خواهی بود",
            "دیده می‌شده خواهد بود",
            "دیده می‌شده خواهیم بود",
            "دیده می‌شده خواهید بود",
            "دیده می‌شده خواهند بود",
        ]
        assert actual == expected

    def test_negative_passive_future_precedent_imperfective(self: "TestConjugation", conjugation):
        actual = conjugation.negative_passive_future_precedent_imperfective("دید")
        expected = [
            "دیده نمی‌شده خواهم بود",
            "دیده نمی‌شده خواهی بود",
            "دیده نمی‌شده خواهد بود",
            "دیده نمی‌شده خواهیم بود",
            "دیده نمی‌شده خواهید بود",
            "دیده نمی‌شده خواهند بود",
        ]
        assert actual == expected
