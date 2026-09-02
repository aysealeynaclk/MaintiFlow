import pandas as pd
import numpy as np
import sklearn
import shap
import matplotlib
import seaborn
import imblearn
import joblib

print("pandas", pd.__version__)
print("numpy", np.__version__)
print("sklearn", sklearn.__version__)
print("shap", shap.__version__)
print("imblearn", imblearn.__version__)

df = pd.read_csv("data/ai4i2020.csv")
print("CSV shape:", df.shape)
print(df.columns.tolist())
