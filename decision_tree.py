# This is a sample Python script.

import numpy as np
import joblib as jl

from sklearn.model_selection import train_test_split
from sklearn.tree import DecisionTreeClassifier
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.preprocessing import MultiLabelBinarizer
from sklearn import metrics

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.


# process and split the data
def data_process():
    DatContent = []
    for i in open("dialog_acts.dat").readlines():
        DatContent.append(i.strip().split())
    # print(datContent)
    np.random.shuffle(DatContent)
    features = [] # feature
    labels = [] # label
    for dc in DatContent:
        labels.append(dc[:1])
        features.append(dc[1:])

    # split the dataset(using Function train_test_split)
    train_features, test_features, train_labels, test_labels = train_test_split(features, labels, test_size=0.15, random_state=42)
    print(f"Num of train data: {len(train_labels)}")
    print(f"Num of test data: {len(test_labels)}")

    return train_features, test_features, train_labels, test_labels # X_train, X_test, y_train, y_test


# train and test the model DecisionTreeClassifier
def train_test_DTC(train_features, test_features, train_labels, test_labels):
    vectorizer = CountVectorizer()
    label_binarizer = MultiLabelBinarizer()

    # print(feature_matrix)

    clf = DecisionTreeClassifier(criterion="gini", max_depth=256)

    train_text_data = [' '.join(d) for d in train_features]
    test_text_data = [' '.join(d) for d in test_features]

    train_feature_matrix = vectorizer.fit_transform(train_text_data)
    test_feature_matrix = vectorizer.transform(test_text_data)

    # print(train_labels)
    train_labels = label_binarizer.fit_transform(train_labels)
    test_labels = label_binarizer.transform(test_labels)

    # print(train_feature_matrix)
    # print(train_labels)

    clf.fit(train_feature_matrix, train_labels)

    # predict using test data
    # train_accuracy = clf.score(train_feature_matrix, train_labels)
    # test_accuracy = clf.score(test_feature_matrix, test_labels)
    pred = clf.predict(test_feature_matrix)
    # print(pred)
    # evaluation?
    print(f"Test Accuracy: {metrics.accuracy_score(test_labels, pred)}")
    print(f"Test Precision: {metrics.precision_score(test_labels, pred, average='macro')}")
    print(f"Test Recall: {metrics.recall_score(test_labels, pred, average='macro')}")
    print(f"Test F1score: {metrics.f1_score(test_labels, pred, average='macro')}")

    return clf, vectorizer, label_binarizer

# predict using the model
def predict_new(clf, vectorizer, label_binarizer):
    new_message = ["hello hi man", "request can you tell me where is utrecht", "null lol"]
    features = []  # feature
    labels = []  # label
    for nm in new_message:
        messages = nm.split()
        first_m = messages[0]
        remain_m = ' '.join(messages[1:])
        labels.append(first_m)
        features.append(remain_m)
    print(features)

    labels = np.reshape(labels, (-1, 1)).tolist()
    print(labels)

    features_new_message = vectorizer.transform(features)
    labels_new_message = label_binarizer.transform(labels)
    # print(features_new_message)
    # print(labels_new_message)
    pred_m = clf.predict(features_new_message)
    print(pred_m)
    print(f"Predict accuracy: {metrics.accuracy_score(labels_new_message, pred_m)}")

# export the pkl file
def export_model(clf):
    jl.dump(clf, 'DTC.pkl')

# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    # train and test the classifier, then use ex to predict
    train_features, test_features, train_labels, test_labels = data_process()
    clf, vectorizer, label_binarizer = train_test_DTC(train_features, test_features, train_labels, test_labels)
    predict_new(clf, vectorizer, label_binarizer)

