# 🤖 Machine Learning Explorer!!

## Overview 🎯📋
An interactive Streamlit app where you upload a dataset (or use the sample Spotify data), pick a target column, train a decision tree, adjust its settings, and see how well it performs.
1. **Choose your data** Use the built-in Spotify track dataset or upload your own CSV file.
2. **Choose your target** Pick a column you want the model to predict. The app defaults to "popularity" for the Spotify dataset, but any column works great. All other columns become the *features*, the clues the model uses.
3. **Train a model** The app splits your data into a training set (80%), which the model learns from, and a test set (20%), which is held back to check how well the model does on rows it has never seen.
4. **Adjust Hyperparameters** Sliders change the model's hyperparameters, and the model retrains every time you move one.
5. **Look at the Decision Tree** Each box is a yes/no question about one feature. The boxes at the bottom are the model's guesses.
6. **Results are displayed** The app shows scores and a chart (either a confusion matrix or residual chart), all explained in plain language.

## 🔗🔗🔗A link to my deployed app!🔗🔗🔗
<<https://bselna-lab-selna-data-science-portfo-mlstreamlitappmyapp-csgkef.streamlit.app/>>

## Instructions for running the app locally📌📌
1. Clone the repo: `git clone https://github.com/bselna-lab/Selna-Data-Science-Portfolio.git`
2. Go to the folder: `cd Selna-Data-Science-Portfolio/MLStreamlitApp`
3. Install libraries: `pip install -r requirements.txt`
4. Run: `streamlit run myapp.py`

## Libraries Needed(with versions) 📚📖
streamlit 1.67.0, pandas 3.1.1, numpy 2.5.5, matplotlib 3.11.2, scikit-learn 1.9.1

## Models Used and How Hyperparameters Can Be Adjusted 💻
The app uses a 'DecisionTreeRegressor' or 'DecisionTreeClassifier', depending on the target chosen by the user. 

- **`DecisionTreeRegressor`** if the target is a number (like `popularity`). This is called *regression*.
- **`DecisionTreeClassifier`** if the target is categories (like `explicit`). This is called *classification*. The app treats a column as categories if it is text, True/False, or has 10 or fewer unique values.

Both have 2 sliders indicating their hyperparameters:
- **max_depth**: the most questions in a row the tree can ask. A small value makes a simple tree that may miss patterns. A large value makes a tree that memorizes the training data, contributing to overfitting.
- **min_samples_split**: the minimum number of rows a group needs before the tree is allowed to split it further. Higher values make a simpler tree.

**Metrics:** R² and MAE for regression, and accuracy, precision, and recall for classification. Charts are a residual plot (regression) and a confusion matrix (classification).

**Regression**
- **R²:** how much better the model is than always guessing the average. 1.0 is perfect, 0 means no better than guessing, and negative means worse.
- **MAE (Mean Absolute Error):** how far off the guesses are on average, in the same units as the target. Lower is better.
- **Chart, residual plot:** each dot is one test row. The red line means no error. Dots above it were guessed too low, and dots below it were guessed too high.

**Classification**🏷️ 🔡 ✅
- **Accuracy:** the share of test rows the model got right.
- **Precision:** when the model predicts a category, how often it is correct.
- **Recall:** of all the rows that truly belong to a category, how many the model found.
- **Chart, confusion matrix:** a grid of real answers (rows) versus the model's guesses (columns). The diagonal boxes are correct guesses, and every other box is a mistake.


<img width="844" height="538" alt="Screenshot 2026-11-15 at 10 34 30 PM" src="https://github.com/user-attachments/assets/83baad73-1ab6-4f01-bc0c-38bd3299bed7" />

**References**
- <https://scikit-learn.org/stable/modules/tree.html>
- <https://pandas.pydata.org/docs/reference/api/pandas.DataFrame.sample.html>
- **DATASET LINK** <https://www.kaggle.com/datasets/maharshipandya/-spotify-tracks-dataset>
