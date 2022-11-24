from hazm import *

# Testing normalizer

normalizer = Normalizer(affix_spacing=True)

worked_as_expected = []

with open("normalizer-test-cases.txt", encoding='utf-8') as file:
    while (line := file.readline().rstrip()):
        splitted = line.split('#')
        input = splitted[0]
        expected = splitted[1]
        normal = normalizer.normalize(input)
        if normal == expected:
            worked_as_expected.append(line)

with open("worked_as_expected.txt", "w", encoding="utf-8") as outfile:
    outfile.write("\n".join(worked_as_expected))
