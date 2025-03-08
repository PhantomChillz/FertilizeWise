import pandas as pd
import numpy as np
from sklearn.preprocessing import StandardScaler, OneHotEncoder, LabelEncoder
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.tree import DecisionTreeClassifier
import joblib

def analyze_nutrients(input_data):
    """
    Analyze nutrient levels and determine deficiencies.
    
    Nutrient Levels (mg/kg):
    - Nitrogen (N):  Low < 30, Medium 30-60, High > 60
    - Phosphorous (P): Low < 10, Medium 10-20, High > 20
    - Potassium (K): Low < 20, Medium 20-40, High > 40
    """
    nutrient_levels = {
        'Nitrogen': {
            'value': input_data['Nitrogen'],
            'low': 30,
            'medium': 60,
            'status': None
        },
        'Phosphorous': {
            'value': input_data['Phosphorous'],
            'low': 10,
            'medium': 20,
            'status': None
        },
        'Potassium': {
            'value': input_data['Potassium'],
            'low': 20,
            'medium': 40,
            'status': None
        }
    }

    # Determine status for each nutrient
    for nutrient, data in nutrient_levels.items():
        if data['value'] < data['low']:
            data['status'] = 'Low'
        elif data['value'] < data['medium']:
            data['status'] = 'Medium'
        else:
            data['status'] = 'High'

    # Sort nutrients by severity (Low > Medium > High)
    severity_order = {'Low': 3, 'Medium': 2, 'High': 1}
    sorted_nutrients = sorted(
        nutrient_levels.items(),
        key=lambda x: (severity_order[x[1]['status']], -x[1]['value']),
        reverse=True
    )

    return sorted_nutrients

def get_fertilizer_recommendation(nutrients, soil_type, crop_type):
    """
    Get fertilizer recommendation based on nutrient analysis and crop/soil type.
    Returns tuple of (fertilizer, explanation)
    """
    most_deficient = nutrients[0][0]
    deficiency_level = nutrients[0][1]['status']
    
    # Fertilizer recommendations based on primary deficiency
    recommendations = {
        'Nitrogen': {
            'Low': 'Urea',
            'Medium': 'NPK',
            'High': 'DAP'
        },
        'Phosphorous': {
            'Low': 'DAP',
            'Medium': 'NPK',
            'High': 'Urea'
        },
        'Potassium': {
            'Low': 'MOP',
            'Medium': 'NPK',
            'High': 'Urea'
        }
    }
    
    return recommendations[most_deficient][deficiency_level]

# Load the trained model and preprocessor
try:
    model = joblib.load('trained_model.joblib')
    le = joblib.load('label_encoder.joblib')
except:
    # If model doesn't exist, train it
    
    df = pd.read_csv("C:\\Users\\rushi\\Desktop\\FertilizeWIseDjagno\\FertWiseMergedMain.csv")

    categorical_columns = ['Soil_Type', 'Crop_Type']
    numerical_columns = ['Temparature', 'Humidity', 'Moisture', 'Nitrogen', 'Potassium', 'Phosphorous']

    preprocessor = ColumnTransformer(
        transformers=[
            ('num', StandardScaler(), numerical_columns),
            ('cat', OneHotEncoder(drop='first', sparse_output=False), categorical_columns)
        ])

    le = LabelEncoder()
    y = le.fit_transform(df['Fertilizer'])
    X = df[numerical_columns + categorical_columns]

    model = Pipeline([
        ('preprocessor', preprocessor),
        ('classifier', DecisionTreeClassifier(
            random_state=42,
            class_weight='balanced',
            max_depth=10,
            min_samples_split=5,
            min_samples_leaf=2
        ))
    ])

    model.fit(X, y)
    joblib.dump(model, 'trained_model.joblib')
    joblib.dump(le, 'label_encoder.joblib')

def predict_fertilizer(input_data):
    """
    Make predictions with nutrient analysis.
    
    Parameters:
    input_data (dict): Dictionary containing soil and crop parameters
    
    Returns:
    tuple: (predicted_fertilizer, confidence_score, explanation)
    """
    try:
        # Analyze nutrients first
        nutrient_analysis = analyze_nutrients(input_data)
        
        # Get recommendation based on nutrient analysis
        nutrient_based_recommendation = get_fertilizer_recommendation(
            nutrient_analysis,
            input_data['Soil_Type'],
            input_data['Crop_Type']
        )

        # Get model prediction
        df_new = pd.DataFrame([input_data])
        probabilities = model.predict_proba(df_new)
        predicted_class_idx = np.argmax(probabilities[0])
        confidence_score = probabilities[0][predicted_class_idx]
        model_prediction = le.inverse_transform([predicted_class_idx])[0]

        # Create explanation
        explanation = {
            'nutrient_analysis': [
                {
                    'nutrient': nutrient,
                    'value': data['value'],
                    'status': data['status']
                }
                for nutrient, data in nutrient_analysis
            ],
            'model_prediction': model_prediction,
            'nutrient_recommendation': nutrient_based_recommendation
        }

        # Use nutrient-based recommendation if confidence is low
        final_prediction = (
            nutrient_based_recommendation 
            if confidence_score < 0.7 
            else model_prediction
        )

        return final_prediction, confidence_score, explanation

    except Exception as e:
        print(f"Error in prediction: {str(e)}")
        return "Error in prediction", 0.0, {}