from hazm import *
import time, re

st = time.process_time()

#normalizer = Normalizer().normalize("میدانم میخواهم مینویسم میرفت")

normalizer = Normalizer()

output = ""

with open("input.txt", encoding='utf-8') as file:    
    output=normalizer.normalize(file.read())

with open("output.txt", "w", encoding="utf-8") as file:
    file.write(output)

et = time.process_time()
res = et - st
print('Execution time:', res, 'seconds')