import numpy as np
import pandas as pd
import streamlit as st
from pathlib import Path
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split, GridSearchCV
from sklearn.tree import DecisionTreeRegressor, DecisionTreeClassifier


st.title("Machine Learning!🤖")
st.subheader("By: Bridget Selna 💓")
st.write(
    "Upload a dataset, pick a target, train a model, and see how well it performs."
)
st.header("1. Choose your data")

data_source = st.radio(
    "Where should the data come from?",
    ["Use the sample Spotify dataset", "Upload my own CSV"]
)
#had to look up Path because the file was too big for importing the file normally
if data_source == "Use the sample Spotify dataset":
    df = pd.read_csv(Path(__file__).parent / "spotify_small.csv")
else:
    uploaded_file = st.file_uploader("Upload a CSV file", type="csv")
    if uploaded_file is None:
        st.info("Please upload a CSV file to continue.")
        st.stop()
    df = pd.read_csv(uploaded_file)

st.dataframe(df.head())

#choosing target - but also having popularity as the default
st.header("2. Choose your target")

target = st.selectbox(
    "Which column do you want to predict?",
    df.columns,
    index=list(df.columns).index("popularity") if "popularity" in df.columns else 0
)

st.write(f"You chose **{target}** as the target. All other columns will be used as features.")


st.header("3. Train a Model")

# If the target is text/True-False, or has only a few unique values, treat it as dummies
if df[target].dtype == "object" or df[target].dtype == "bool" or df[target].nunique() <= 10:
    task = "classification"
else:
    task = "regression"

    st.write(f"Since **{target}** looks like {'categories' if task == 'classification' else 'a number'}, this is a **{task}** problem.")

#Separate features from target and clean up
X = df.drop(columns=[target])
X = X.drop(columns=["Unnamed: 0"], errors="ignore")

# Keep text columns only if they have 5 or fewer unique values
text_cols = X.select_dtypes(exclude="number").columns
too_many = [c for c in text_cols if X[c].nunique() > 5]
X = X.drop(columns=too_many)

X = pd.get_dummies(X, drop_first=True)
y = df[target]

#remove rows with missing values
data = pd.concat([X, y], axis=1).dropna()
X = data.drop(columns=[target])
y = data[target]

st.write(f"The model will use these **{X.shape[1]} features**: {', '.join(X.columns)}")

#split the data and train

X_train, X_test, y_train, y_test = train_test_split(X, y,
                                                    test_size=0.2,
                                                    random_state=42)

#Grid Search to suggest the hyperparameter
st.subheader("❓Not sure what to pick❓")

if st.button("Find suggested settings!"):
    if task == "regression":
        base_model = DecisionTreeRegressor(random_state=42)
    else:
        base_model = DecisionTreeClassifier(random_state=42)

    param_grid = {
    'max_depth': [None, 5, 10, 15, 20],
    'min_samples_split': [2, 5, 10],
    'min_samples_leaf': [1, 2, 4],
    'max_features': [None, 'sqrt', 'log2'],
    'criterion': ['squared_error', 'friedman_mse', 'absolute_error']
    }

    grid_search = GridSearchCV(
        estimator=DecisionTreeRegressor(random_state=42),
        param_grid=param_grid,
        cv=5,
        scoring='r2',
        n_jobs=-1
    )

    grid_search.fit(X_train, y_train)

    best = grid_search.best_params_
    st.info(
        f"Suggested settings: max_depth = {best['max_depth']}, "
        f"min_samples_split = {best['min_samples_split']}. "
        f"Set the sliders below to these values to try them!😀"
    )

#slider for hyperparameter 
st.subheader("Adjust the model's settings")

max_depth = st.slider(
    "max_depth (how many questions in a row the tree can ask)",
    min_value=1, max_value=20, value=5
)
min_samples_split = st.slider(
    "min_samples_split (minimum rows needed to split a group)",
    min_value=2, max_value=50, value=10
)



if task == "regression":
    model = DecisionTreeRegressor(
        max_depth=max_depth,
        min_samples_split=min_samples_split,
        random_state=42
    )
else:
    model = DecisionTreeClassifier(
        max_depth=max_depth,
        min_samples_split=min_samples_split,
        random_state=42
    )

model.fit(X_train, y_train)

#2 performance metrics on the test data R2, MAE, accuraccy, precision, recall
from sklearn.metrics import (
    r2_score, mean_absolute_error,
    accuracy_score, precision_score, recall_score,
    ConfusionMatrixDisplay
)
st.header("4. Results")

#model's guesses
y_train_pred = model.predict(X_train)
y_test_pred = model.predict(X_test)

st.subheader("Performance Metrics:")
if task == "regression":
    train_r2 = r2_score(y_train, y_train_pred)
    test_r2 = r2_score(y_test, y_test_pred)
    mae = mean_absolute_error(y_test, y_test_pred)
    col1, col2, col3 = st.columns(3)
    st.write("R² (test): It shows how much better the model is than just guessing the average every time, where 1.0 is perfect, 0 is no better than guessing, and negative is worse. It’s calculated on test songs the model never saw, so it’s the score that counts")
    st.write("R² (train): It’s the same score on the songs the model studied, and if it’s much higher than the test R², the model is overfitting (memorizing instead of learning).")
    st.write( "MAE: It’s the average number of points the model’s guesses are off by, in the same units as your target, so lower is better.")
    col1.metric("R² (test)", f"{test_r2}")
    col2.metric("MAE (test)", f"{mae}")
    col3.metric("R² (train)", f"{train_r2}")
else:
    train_acc = accuracy_score(y_train, y_train_pred)
    test_acc = accuracy_score(y_test, y_test_pred)
    precision = precision_score(y_test, y_test_pred, average="weighted", zero_division=0)
    recall = recall_score(y_test, y_test_pred, average="weighted", zero_division=0)
    st.write("Accuracy (test): The share of test rows the model got right, calculated on rows it never saw during training.")
    st.write("Precision (test): When the model predicts a category (like “explicit”), this is how often it’s correct.")
    st.write("Recall (test): Of all the rows that truly belong to a category, this is how many the model managed to find.")
    st.write("Accuracy (train): The share of training rows the model got right, which is only useful for comparing to the test accuracy, since a much higher train score means overfitting.")
    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Accuracy (test)", f"{test_acc}")
    col2.metric("Precision (test)", f"{precision}")
    col3.metric("Recall (test)", f"{recall}")
    col4.metric("Accuracy (train)", f"{train_acc}")

#CONFUSION MATRIX
st.subheader("Chart")

fig, ax = plt.subplots()

if task == "regression":   #make residual plot for this one
    residuals = y_test - y_test_pred
    ax.scatter(y_test_pred, residuals, alpha=0.4)
    ax.axhline(0, color="red", linestyle="--")
    ax.set_xlabel("Predicted value")
    ax.set_ylabel("Residual (actual - predicted)")
    ax.set_title("Residual Plot (test data)")
    st.caption("Each dot is one test row. The red line is zero error. Dots above the line mean the model guessed too low, and dots below mean it guessed too high. The farther a dot is from the line, the bigger the mistake.")
    st.write("This chart shows how wrong the model’s guesses were. Each dot is one test song. The red line means “no error,” so dots on the line were guessed perfectly, dots above it were guessed too low, and dots below it were guessed too high. The farther a dot is from the line, the bigger the mistake.")
else:
    ConfusionMatrixDisplay.from_predictions(y_test, y_test_pred, ax=ax)
    ax.set_title("Confusion Matrix (test data)")
    st.caption("Each row is the real category, and each column is what the model predicted. Numbers on the diagonal (top-left to bottom-right) are correct guesses. Numbers off the diagonal are mistakes.")
    st.write("This chart is a scoreboard of the model’s guesses. Each row is the real answer and each column is what the model predicted. The boxes on the diagonal (top-left to bottom-right) are correct guesses, and every other box is a mistake. The bigger the numbers on the diagonal, the better the model.")
st.pyplot(fig)