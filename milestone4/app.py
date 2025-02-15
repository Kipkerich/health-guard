from flask import Flask, render_template, request, jsonify
import joblib
import mysql.connector
import numpy as np
import pandas as pd
from flask_cors import CORS
from sklearn.metrics.pairwise import cosine_similarity
app = Flask(__name__)
CORS(app)
DB_CONFIG = {
    'host': 'localhost',
    'user': 'root',
    'password': '',
    'database': 'hospital',
}

df = pd.read_csv("data.csv")
symptoms_columns = df.drop('STI_Type', axis=1).columns.tolist()
# Load the pre-trained model
model = joblib.load('sti_prediction_model.joblib')  # Replace with your actual filename

# Endpoint for predicting STI
model = joblib.load('sti_prediction_model.joblib')  # Replace with your actual filename

# Read the dataset for feature names
df = pd.read_csv('data.csv')  # Replace with the actual filename
feature_names = df.drop('STI_Type', axis=1).columns.tolist()

# Endpoint for predicting STI
@app.route('/predict_sti', methods=['POST'])
def predict_sti():
    try:
        # Get symptoms from the request
        data = request.get_json()
        symptoms = data['symptoms']
        print(data['user'])
        # Prepare data for prediction
        symptom_array = prepare_data(symptoms, feature_names)
        res=compare_symptoms_percentage(symptom_array)
        # Make prediction
        predicted_sti = model.predict([symptom_array])[0]
        print(predicted_sti)
        save_to_database(symptoms, predicted_sti,data['user'])
        return jsonify({'predicted_sti': str(res),'model_prediction':predicted_sti})

    except Exception as e:
        return jsonify({'error': str(e)}), 500

def prepare_data(symptoms, feature_names):
    # Convert symptoms to a binary array (0s and 1s)
    symptom_array = np.zeros(len(feature_names))
    # Use a while loop to iterate through symptoms
    i = 0
    while i < len(symptoms):
        symptom = symptoms[i]
        if symptom in feature_names:
            index = feature_names.index(symptom)
            symptom_array[index] = 1
        i += 1

    return symptom_array.tolist()  # Convert to list for better JSON serialization

def save_to_database(symptoms, predicted_sti,user):
    try:
        # Connect to the MySQL database
        conn = mysql.connector.connect(**DB_CONFIG)
        cursor = conn.cursor()

        # Insert data into the 'predictions' table
        cursor.execute("INSERT INTO predictions (symptoms, predictedDisease,patient_id) VALUES (%s, %s,%s)",
                       (','.join(symptoms), predicted_sti,user))

        # Commit the changes and close the connection
        conn.commit()
        conn.close()

    except Exception as e:
        print(f"Error saving to database: {e}")

def compare_symptoms_percentage(user_symptoms):
    try:
        # Create a DataFrame for user symptoms
        user_df = pd.DataFrame([user_symptoms], columns=feature_names)
        
        # Calculate cosine similarity
        similarity_matrix = cosine_similarity(df.drop('STI_Type', axis=1), user_df)
        
        # Get the similarity level for each row
        similarity_levels = pd.Series(similarity_matrix.flatten(), index=df['STI_Type'])
        
        # Sort the results by similarity level
        sorted_results = similarity_levels.sort_values(ascending=False)
        
        # Convert to percentage
        similarity_percentage = (sorted_results * 100).round(2).astype(str) + '%'
        print("Similarity Percentage:", similarity_percentage)
        return similarity_percentage

    except Exception as e:
        print("Error in compare_symptoms_percentage:", e)
        return str(e)
@app.route('/')
def index():
    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)
