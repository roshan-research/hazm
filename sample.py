from hazm import *

#normalizer = Normalizer().normalize("سلامممممم می خواهم")

normalizer = Normalizer()

output = ""

with open("input.txt", encoding='utf-8') as file:    
    output=normalizer.normalize(file.read())

with open("output.txt", "w", encoding="utf-8") as file:
    file.write(output)