import json

with open('questions.json') as json_file:
    dump_data = json.load(json_file)


#codigo para exportacao de questoes em csv
csv = "question, A, B, C, D\n"
for line in dump_data:
    if line['text'] is None:
        line['text'] = ''
    question = str(line['text']).strip()
    question = question.replace('\n', ' ')
    csv += f'"{question}", {line["options"][0]}, {line["options"][1]}, {line["options"][2]}, {line["options"][3]}\n'
print(csv)

f = open("questions.csv", "w")
f.write(csv)
f.close()
