# train_classfier.py

import pickle

from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score
import numpy as np


data_dict = pickle.load(open('./data.pickle', 'rb'))
for i, sample in enumerate(data_dict['data']):
    print(f"Sample {i} shape: {len(sample)}")
data_cleaned = [sample for sample in data_dict['data'] if len(sample) == 42]
labels_cleaned = [label for i, label in enumerate(data_dict['labels']) if len(data_dict['data'][i]) == 42]

data = np.asarray(data_cleaned)
labels = np.asarray(labels_cleaned)

x_train, x_test, y_train, y_test = train_test_split(data, labels, test_size=0.2, shuffle=True, stratify=labels)

model = RandomForestClassifier()

model.fit(x_train, y_train)

y_predict = model.predict(x_test)

score = accuracy_score(y_predict, y_test)

print('{}% of samples were classified correctly !'.format(score * 100))

f = open('model.p', 'wb')
pickle.dump({'model': model}, f)
f.close()
