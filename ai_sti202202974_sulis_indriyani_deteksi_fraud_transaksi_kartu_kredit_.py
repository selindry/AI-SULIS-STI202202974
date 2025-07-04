# -*- coding: utf-8 -*-
"""AI-STI202202974-Sulis Indriyani-Deteksi Fraud Transaksi Kartu Kredit-.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1cerEoQWFWQtE88sIv-VepW39IoeYY583
"""

# 1. IMPORT LIBRARY
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.ensemble import RandomForestClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import classification_report, confusion_matrix, accuracy_score
from imblearn.over_sampling import SMOTE
from sklearn.model_selection import cross_val_score
from sklearn.metrics import roc_curve, auc

# 2. BACA DATA
from google.colab import drive
drive.mount('/content/drive')

file_path = '/content/drive/MyDrive/dataset uas/creditcard_2023.csv'
import pandas as pd
df = pd.read_csv(file_path)

# 3. CEK NILAI YANG HILANG
print("\nMissing values:\n", df.isnull().sum())

# 4. DISTRIBUSI DATA KELAS
print("\nDistribusi Kelas (0: Non-Fraud, 1: Fraud):")
print(df['Class'].value_counts())

sns.countplot(x='Class', data=df)
plt.title('Distribusi Kelas')
plt.show()

# 5. PISAH FITUR DAN LABEL
X = df.drop(['Class'], axis=1)
y = df['Class']

# 6. NORMALISASI FITUR
scaler = StandardScaler()
X_scaled = scaler.fit_transform(X)

# 7. SPLIT DATA
X_train, X_test, y_train, y_test = train_test_split(
    X_scaled, y, test_size=0.3, random_state=42, stratify=y
)

# 8. PENANGANAN IMBALANCED DATA MENGGUNAKAN SMOTE
smote = SMOTE(random_state=42)
X_train_res, y_train_res = smote.fit_resample(X_train, y_train)

# 9 LOGISTIC REGRESSION

model_lr = LogisticRegression(max_iter=1000)
model_lr.fit(X_train_res, y_train_res)

y_pred_lr = model_lr.predict(X_test)

print("\n=== Logistic Regression ===")
print("Akurasi:", accuracy_score(y_test, y_pred_lr))
print("Confusion Matrix:\n", confusion_matrix(y_test, y_pred_lr))
print("Classification Report:\n", classification_report(y_test, y_pred_lr))

# Train vs Test Accuracy
print("Train Accuracy:", model_lr.score(X_train_res, y_train_res))
print("Test Accuracy:", model_lr.score(X_test, y_test))

# Cross-validation
cv_scores = cross_val_score(model_lr, X_scaled, y, cv=5, scoring='accuracy')
print("Cross-validation Akurasi (5-fold):", cv_scores)
print("Rata-rata:", cv_scores.mean())

# ROC Curve
y_prob_lr = model_lr.predict_proba(X_test)[:, 1]
fpr, tpr, _ = roc_curve(y_test, y_prob_lr)
roc_auc = auc(fpr, tpr)

plt.figure()
plt.plot(fpr, tpr, label=f'LogReg ROC curve (AUC = {roc_auc:.2f})')
plt.plot([0, 1], [0, 1], 'k--')
plt.xlabel('False Positive Rate')
plt.ylabel('True Positive Rate')
plt.title('ROC Curve - Logistic Regression')
plt.legend(loc='lower right')
plt.grid()
plt.show()

#10 RANDOM FOREST (PEMBANDING)

model_rf = RandomForestClassifier(n_estimators=100, random_state=42)
model_rf.fit(X_train_res, y_train_res)
y_pred_rf = model_rf.predict(X_test)

print("\n=== Random Forest ===")
print("Akurasi:", accuracy_score(y_test, y_pred_rf))
print("Confusion Matrix:\n", confusion_matrix(y_test, y_pred_rf))
print("Classification Report:\n", classification_report(y_test, y_pred_rf))
print("Train Accuracy:", model_rf.score(X_train_res, y_train_res))
print("Test Accuracy:", model_rf.score(X_test, y_test))

# ROC Curve Random Forest
y_prob_rf = model_rf.predict_proba(X_test)[:, 1]
fpr_rf, tpr_rf, _ = roc_curve(y_test, y_prob_rf)
roc_auc_rf = auc(fpr_rf, tpr_rf)

plt.figure()
plt.plot(fpr_rf, tpr_rf, label=f'Random Forest ROC curve (AUC = {roc_auc_rf:.2f})')
plt.plot([0, 1], [0, 1], 'k--')
plt.xlabel('False Positive Rate')
plt.ylabel('True Positive Rate')
plt.title('ROC Curve - Random Forest')
plt.legend(loc='lower right')
plt.grid()
plt.show()