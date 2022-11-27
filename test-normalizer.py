from hazm import *

normalizer = Normalizer()

output = []

with open("input.txt", encoding='utf-8') as file:
    while (sentence := file.readline().rstrip()):
        output.append(normalizer.normalize(sentence))

with open("output.txt", "w", encoding="utf-8") as file:
    file.write("\n".join(output))
