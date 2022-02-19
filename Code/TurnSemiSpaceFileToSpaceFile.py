# sourceFileAddress = "./output-test-formal.txt"
# destinationFileAddress = "./output-test-formal-space.txt"
sourceFileAddress = "./shekasteh-test.tok.formal"
destinationFileAddress = "./shekasteh-test-space.tok.formal"

def main(sourceAddress,destinationAddress):
    with open(sourceAddress, "r", encoding='utf-8') as readFile, open(destinationAddress, "w", encoding='utf-8') as writeFile:
        while True:
            line = readFile.readline().strip()
            if not line:
                break
            line = line.replace('‌', ' ')
            line = line.replace('‎', ' ')
            line = line.replace('.', '')
            line = line.replace('؟', '')
            line = line.replace('!', '')
            writeFile.write(line + "\n")


main(sourceFileAddress,destinationFileAddress)