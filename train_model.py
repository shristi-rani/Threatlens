import pandas as pd
import pickle

from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score

# LOAD DATASET

df = pd.read_csv("new_data_urls.csv")

print(df.shape)

# SPLIT

x_train, x_test, y_train, y_test = train_test_split(
    df["url"],
    df["status"],
    test_size=0.25,
    random_state=42
)

# VECTORIZER

vectorizer = TfidfVectorizer()

xv_train = vectorizer.fit_transform(x_train)

xv_test = vectorizer.transform(x_test)

# MODEL

model = LogisticRegression(max_iter=1000)

model.fit(xv_train, y_train)

# ACCURACY

y_pred = model.predict(xv_test)

acc = accuracy_score(y_test, y_pred)

print("Accuracy =", acc)

# SAVE MODEL

pickle.dump(
    model,
    open("model.pkl", "wb")
)

pickle.dump(
    vectorizer,
    open("vectorizer.pkl", "wb")
)

print("Model Saved Successfully")
