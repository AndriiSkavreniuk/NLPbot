import big_config
from sklearn.linear_model import LogisticRegression
from sklearn.feature_extraction.text import CountVectorizer

BOT_CONFIG = big_config.BOT_CONFIG

dataset = []

for intent, intent_data in BOT_CONFIG['intents'].items():
    for example in intent_data['examples']:
        dataset.append([example, intent])

X_text = [x for x, y in dataset]
y = [y for x, y in dataset]

vectorizer = CountVectorizer(analyzer='char', ngram_range=(1, 3))
X = vectorizer.fit_transform(X_text)

clf = LogisticRegression()
clf.fit(X, y)


def get_intent(text):
    probas = clf.predict_proba(vectorizer.transform([text]))[0]
    proba = max(probas)
    if proba > 0.3:
        index = list(probas).index(proba)
        return clf.classes_[index]

print(get_intent('что послушать'))