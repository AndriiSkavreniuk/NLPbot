import nltk

search_structure = {}  # {word: [(q, a), (q, a), ...], ...}
to_del = []
dialogues_filtered = []
alphabet = '1234567890- абвгдеёжзийклмнопрстуфхцчшщъыьэюяqwertyuiopasdfghjklzxcvbnm'

with open('dialogues.txt') as f:
    dialogues_data = f.read()
dialogues = [dialogue.split('\n')[:2] for dialogue in dialogues_data.split('\n\n')]
dialogues = [dialogue for dialogue in dialogues if len(dialogue) == 2]

for dialogue in dialogues:
    question = dialogue[0][2:].lower()
    question = ''.join(char for char in question if char in alphabet)
    question = question.strip()
    answer = dialogue[1][2:].strip()
    if question and answer:
        dialogues_filtered.append((question, answer))

dialogues_filtered = list(set(dialogues_filtered))

for question, answer in dialogues_filtered:
    words = question.split(' ')
    for word in words:
        if word not in search_structure:
            search_structure[word] = []
        search_structure[word].append((question, answer))


for word in search_structure:
    if len(search_structure[word]) > 10000:
        to_del.append(word)

for word in to_del:
    search_structure.pop(word)


def get_generative_response(text):
    text = text.lower()
    text = ''.join(char for char in text if char in alphabet)
    text = text.strip()
    words = text.split(' ')

    qas = []
    for word in words:
        if word in search_structure:
            qas += search_structure[word]

    for question, answer in qas:
        if abs(len(text) - len(question)) < len(question) * 0.20:
            edit_distance = nltk.edit_distance(text, question)
            if edit_distance / len(question) < 0.20:
                return answer


print(get_generative_response('ты мальчик или девочка'))