import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, classification_report
import joblib

# Read the dataset
df = pd.read_csv('data.csv')  

X = df.drop('STI_Type', axis=1)
y = df['STI_Type']

# Split the dataset into training and testing sets
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Initialize the Random Forest classifier
model = RandomForestClassifier(random_state=42)

# Train the model
model.fit(X_train, y_train)

# Make predictions on the test set
y_pred = model.predict(X_test)

# Evaluate the accuracy of the model
accuracy = accuracy_score(y_test, y_pred)
print(f'Model Accuracy: {accuracy * 100:.2f}%')

# Print classification report for more detailed evaluation
print('\nClassification Report:\n', classification_report(y_test, y_pred))

# Save the trained model to a file
model_filename = 'sti_prediction_model.joblib'
joblib.dump(model, model_filename)
print(f'Model saved to {model_filename}')
