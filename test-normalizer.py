from hazm import *
import time

st = time.process_time()

normalizer = Normalizer()
#n = normalizer.normalize("سلاممممممها")

output = []

with open("input.txt", encoding='utf-8') as file:
    while (sentence := file.readline().rstrip()):
        output.append(normalizer.normalize(sentence))

with open("output.txt", "w", encoding="utf-8") as file:
    file.write("\n".join(output))

et = time.process_time()
res = et - st
print('Execution time:', res, 'seconds')