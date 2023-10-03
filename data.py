import subprocess
import random
from collections import Counter
from itertools import islice

from nltk.tag import untag
from sklearn.model_selection import train_test_split

from hazm import (Chunker, InformalNormalizer, Lemmatizer, Normalizer,
                  POSTagger, sent_tokenize)
from hazm.chunker import tree2brackets
from hazm.corpus_readers import (DadeganReader, PeykareReader, SentiPersReader,
                                 TNewsReader, TreebankReader)
from hazm.corpus_readers.peykare_reader import \
    coarse_pos_e as peykare_coarse_pos_e
from hazm.dependency_parser import MaltParser, TurboParser


def create_words_file(dic_file="tests/files/persian.dic", output="hazm/data/words.dat"):
    """prepares list of persian word words from [Virastyar](https://sourceforge.net/projects/virastyar/) dic file."""

    dic_words = [
        line.strip().replace(", ", ",").split("\t")
        for line in open(dic_file, encoding="utf-8")
        if len(line.strip().split("\t")) == 3
    ]
    dic_words = [
        item
        for item in dic_words
        if not item[2].startswith("V") and "NEG" not in item[2]
    ]
    dic_words = [
        "\t".join(item) for item in sorted(dic_words, key=lambda item: item[0])
    ]
    print(*dic_words, sep="\n", file=open(output, "w", "utf-8"))
    print(output, "created")


def evaluate_lemmatizer(
    conll_file="tests/files/train.conll", peykare_root="tests/files/peykare"
):
    lemmatizer = Lemmatizer()

    errors = []
    with open("tests/files/lemmatizer_errors.txt", "w", "utf8") as output:
        dadegan = DadeganReader(conll_file)
        for tree in dadegan.trees():
            for node in tree.nodelist[1:]:
                word, lemma, pos = node["word"], node["lemma"], node["mtag"]
                if lemmatizer.lemmatize(word, pos) != lemma:
                    errors.append((word, lemma, pos, lemmatizer.lemmatize(word, pos)))
        print(len(errors), "errors", file=output)
        counter = Counter(errors)
        for item, count in sorted(
            list(counter.items()), key=lambda t: t[1], reverse=True
        ):
            print(count, *item, file=output)

    missed = []
    with open("tests/files/lemmatizer_missed.txt", "w", "utf8") as output:
        peykare = PeykareReader(peykare_root)
        for sentence in peykare.sents():
            for word in sentence:
                if word[1] == "V":
                    if word[0] == lemmatizer.lemmatize(word[0]):
                        missed.append(word[0])
        print(len(missed), "missed", file=output)
        counter = Counter(missed)
        for item, count in sorted(
            list(counter.items()), key=lambda t: t[1], reverse=True
        ):
            print(count, item, file=output)


def evaluate_normalizer(tnews_root="tests/files/tnews"):
    tnews = TNewsReader(root=tnews_root)
    normalizer = Normalizer(
        persian_style=False,
        persian_numbers=False,
        remove_diacritics=False,
        token_based=False,
        affix_spacing=True,
    )
    token_normalizer = Normalizer(
        persian_style=False,
        persian_numbers=False,
        remove_diacritics=False,
        token_based=True,
        affix_spacing=False,
    )

    with open("tests/files/normalized.txt", "w", "utf8") as output1, open(
        "tests/files/normalized_token_based.txt", "w", "utf8"
    ) as output2:
        random.seed(0)
        for text in tnews.texts():
            if random.randint(0, 100) != 0:
                continue

            for sentence in sent_tokenize(text):
                print(normalizer.normalize(sentence), "\n", file=output1)
                print(token_normalizer.normalize(sentence), "\n", file=output2)


def evaluate_informal_normalizer(sentipars_root="tests/files/sentipers"):
    sentipers = SentiPersReader(root=sentipars_root)
    normalizer = Normalizer()
    informal_normalizer = InformalNormalizer()

    output = open("tests/files/normalized.txt", "w", "utf8")
    for comments in sentipers.comments():
        for comment in comments:
            for sentence in comment:
                print(normalizer.normalize(sentence), file=output)
                sents = informal_normalizer.normalize(sentence)
                sents = [[word[0] for word in sent] for sent in sents]
                sents = [" ".join(sent) for sent in sents]
                text = "\n".join(sents)
                text = normalizer.normalize(text)
                print(text, file=output)
                print(file=output)


def evaluate_chunker(treebank_root="tests/files/treebank"):
    treebank = TreebankReader(treebank_root, join_clitics=True, join_verb_parts=True)
    chunker = Chunker()
    chunked_trees = list(treebank.chunked_trees())

    print(chunker.evaluate(chunked_trees))

    output = open("tests/files/chunker_errors.txt", "w", "utf8")
    for sentence, gold in zip(treebank.sents(), chunked_trees):
        chunked = chunker.parse(sentence)
        if chunked != gold:
            print(tree2brackets(chunked), file=output)
            print(tree2brackets(gold), file=output)
            print(file=output)


def train_postagger(
    peykare_root="tests/files/peykare",
    model_file="tests/files/postagger.model",
    test_size=0.1,
    sents_limit=None,
    pos_map=peykare_coarse_pos_e,
):
    tagger = POSTagger(
        type="crf",
        algo="rprop",
        compact=True,
        patterns=[
            "*",
            "u:wll=%x[-2,0]",
            "u:wl=%x[-1,0]",
            "u:w=%x[0,0]",
            "u:wr=%x[1,0]",
            "u:wrr=%x[2,0]",
            # 'u:w2l=%x[-1,0]/%x[0,0]',
            # 'u:w2r=%x[0,0]/%x[1,0]',
            '*:p1=%m[0,0,"^.?"]',
            '*:p2=%m[0,0,"^.?.?"]',
            '*:p3=%m[0,0,"^.?.?.?"]',
            '*:s1=%m[0,0,".?$"]',
            '*:s2=%m[0,0,".?.?$"]',
            '*:s3=%m[0,0,".?.?.?$"]',
            r'*:p?l=%t[-1,0,"\p"]',
            r'*:p?=%t[0,0,"\p"]',
            r'*:p?r=%t[1,0,"\p"]',
            r'*:p?a=%t[0,0,"^\p*$"]',
            r'*:n?l=%t[-1,0,"\d"]',
            r'*:n?=%t[0,0,"\d"]',
            r'*:n?r=%t[1,0,"\d"]',
            r'*:n?a=%t[0,0,"^\d*$"]',
        ],
    )

    peykare = PeykareReader(peykare_root, pos_map=pos_map)
    train_sents, test_sents = train_test_split(
        list(islice(peykare.sents(), sents_limit)), test_size=test_size, random_state=0
    )

    tagger.train(train_sents)
    tagger.save_model(model_file)

    print(tagger.evaluate(test_sents))


def train_chunker(
    train_file="tests/files/train.conll",
    dev_file="tests/files/dev.conll",
    test_file="tests/files/test.conll",
    model_file="tests/files/chunker.model",
):
    tagger = POSTagger(model="tests/files/postagger.model")
    chunker = Chunker(
        type="crf",
        algo="l-bfgs",
        compact=True,
        patterns=[
            "*",
            "u:wll=%x[-2,0]",
            "u:wl=%x[-1,0]",
            "u:w=%x[0,0]",
            "u:wr=%x[1,0]",
            "u:wrr=%x[2,0]",
            "*:tll=%x[-2,1]",
            "*:tl=%x[-1,1]",
            "*:t=%x[0,1]",
            "*:tr=%x[1,1]",
            "*:trr=%x[2,1]",
        ],
    )

    def retag_trees(trees, sents):
        for tree, sentence in zip(trees, tagger.tag_sents(list(map(untag, sents)))):
            for n, word in zip(tree.treepositions("leaves"), sentence):
                tree[n] = word

    train, test = DadeganReader(train_file), DadeganReader(test_file)
    train_trees = list(train.chunked_trees())
    retag_trees(train_trees, train.sents())
    chunker.train(train_trees)
    chunker.save_model(model_file)

    test_trees = list(test.chunked_trees())
    retag_trees(test_trees, test.sents())
    print(chunker.evaluate(test_trees))


def train_maltparser(
    train_file="tests/files/train.conll",
    dev_file="tests/files/dev.conll",
    test_file="tests/files/test.conll",
    model_file="langModel.mco",
    path_to_jar="tests/files/malt.jar",
    options_file="tests/files/malt-options.xml",
    features_file="tests/files/malt-features.xml",
    memory_min="-Xms7g",
    memory_max="-Xmx8g",
):
    lemmatizer, tagger = Lemmatizer(), POSTagger(model="tests/files/pos_tagger.model")

    train, test = DadeganReader(train_file), DadeganReader(test_file)
    train_data = train_file + ".data"
    with open(train_data, "w", encoding="utf8") as output:
        for tree, sentence in zip(
            train.trees(), tagger.tag_sents(list(map(untag, train.sents())))
        ):
            for i, (node, word) in enumerate(
                zip(list(tree.nodes.values())[1:], sentence), start=1
            ):
                node["mtag"] = word[1]
                node["lemma"] = lemmatizer.lemmatize(node["word"], node["mtag"])
                print(
                    i,
                    node["word"].replace(" ", "_"),
                    node["lemma"].replace(" ", "_"),
                    node["mtag"],
                    node["mtag"],
                    "_",
                    node["head"],
                    node["rel"],
                    "_",
                    "_",
                    sep="\t",
                    file=output,
                )
            print(file=output)

    subprocess.Popen(
        [
            "java",
            memory_min,
            memory_max,
            "-jar",
            path_to_jar,
            "-w",
            "resources",
            "-c",
            model_file,
            "-i",
            train_data,
            "-f",
            options_file,
            "-F",
            features_file,
            "-m",
            "learn",
        ]
    ).wait()

    # evaluation
    parser = MaltParser(tagger=tagger, lemmatizer=lemmatizer, model_file=model_file)
    parsed_trees = parser.parse_sents(list(map(untag, test.sents())))

    test_data, test_results = test_file + ".data", test_file + ".results"
    print(
        "\n".join([tree.to_conll(10) for tree in test.trees()]).strip(),
        file=open(test_data, "w", encoding="utf8"),
    )
    print(
        "\n".join([tree.to_conll(10) for tree in parsed_trees]).strip(),
        file=open(test_results, "w", encoding="utf8"),
    )
    subprocess.Popen(
        ["java", "-jar", "tests/files/MaltEval.jar", "-g", test_data, "-s", test_results]
    ).wait()


def train_turboparser(
    train_file="tests/files/train.conll",
    dev_file="tests/files/dev.conll",
    test_file="tests/files/test.conll",
    model_file="tests/files/turboparser.model",
):
    lemmatizer, tagger = Lemmatizer(), POSTagger(model="tests/files/postagger.model")

    train, test = DadeganReader(train_file), DadeganReader(test_file)
    train_data = train_file + ".data"
    with open(train_data, "w", "utf8") as output:
        for tree, sentence in zip(
            train.trees(), tagger.tag_sents(list(map(untag, train.sents())))
        ):
            for i, (node, word) in enumerate(
                zip(list(tree.nodes.values())[1:], sentence), start=1
            ):
                node["mtag"] = word[1]
                node["lemma"] = lemmatizer.lemmatize(node["word"], node["mtag"])
                print(
                    i,
                    node["word"].replace(" ", "_"),
                    node["lemma"].replace(" ", "_"),
                    node["mtag"],
                    node["mtag"],
                    "_",
                    node["head"],
                    node["rel"],
                    "_",
                    "_",
                    sep="\t",
                    file=output,
                )
            print(file=output)

    subprocess.Popen(
        [
            "./tests/files/TurboParser",
            "--train",
            "--file_train=" + train_data,
            "--file_model=" + model_file,
            "--logtostderr",
        ]
    ).wait()

    # evaluation
    parser = TurboParser(tagger=tagger, lemmatizer=lemmatizer, model_file=model_file)
    parsed_trees = parser.parse_sents(list(map(untag, test.sents())))

    test_data, test_results = test_file + ".data", test_file + ".results"
    print(
        "\n".join([tree.to_conll(10) for tree in test.trees()]).strip(),
        file=open(test_data, "w", "utf8"),
    )
    print(
        "\n".join([tree.to_conll(10) for tree in parsed_trees]).strip(),
        file=open(test_results, "w", "utf8"),
    )
    subprocess.Popen(
        [
            "java",
            "-jar",
            "tests/files/MaltEval.jar",
            "-g",
            test_data,
            "-s",
            test_results,
            "--pattern",
            "0.####",
            "--Metric",
            "LAS;UAS",
        ]
    ).wait()
    
