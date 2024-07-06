import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.naive_bayes import GaussianNB
from sklearn.metrics import accuracy_score, classification_report
import matplotlib.pyplot as plt
import seaborn as sns
data = pd.read_csv("/content/OSID.csv")
print(data.head())
numerical_columns = ['Administrative', 'Informational', 'ProductRelated']
for column in numerical_columns:
 plt.figure(figsize=(8, 6))
 sns.histplot(data[column], bins=20, kde=True)
 plt.title(f'Histogram of {column}')
 plt.xlabel(column)
 plt.ylabel('Frequency')
 plt.show()
plt.figure(figsize=(8, 6))
sns.countplot(data['Revenue'])
plt.title('Histogram of Revenue')
plt.xlabel('Revenue')
plt.ylabel('Count')
plt.show()
data = data.dropna()
# Encode categorical variables if any
data = pd.get_dummies(data)
X = data.drop('Revenue', axis=1) # Assuming 'Revenue' is the target variable
y = data['Revenue']
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
nb_classifier = GaussianNB()
nb_classifier.fit(X_train, y_train)
y_pred = nb_classifier.predict(X_test)
accuracy = accuracy_score(y_test, y_pred)
report_dict = classification_report(y_test, y_pred, output_dict=True)
report_df = pd.DataFrame(report_dict)
print("Accuracy:", accuracy)
print("Classification Report:")
print(report_df)