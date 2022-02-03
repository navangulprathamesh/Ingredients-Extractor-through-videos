from googletrans import Translator

translator = Translator()

f1 = open('program.txt', 'r')
if f1.mode == 'r':
    contents = f1.read()
    print(contents)
result1=translator.detect(contents)
print(result1)
result = translator.translate(contents, dest='en')
print(result.text)
f2= open("program1.txt","w+")
f2.write(result.text)
f2.close()
