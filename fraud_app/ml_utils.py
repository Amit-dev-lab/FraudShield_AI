import pandas as pd
import numpy as np
import os
from datetime import datetime
from django.conf import settings
import warnings

# Compatibility setup
try:
    from numpy.exceptions import VisibleDeprecationWarning
except ImportError:
    try:
        from numpy import VisibleDeprecationWarning
    except ImportError:
        VisibleDeprecationWarning = UserWarning

warnings.filterwarnings("ignore")

# City coordinates mapping
CITY_COORDINATES = {
    'Columbia': (34.0007, -81.0348),
    'Altonah': (40.5944, -110.3737),
    'Bellmore': (40.6687, -73.5271),
    'Titusville': (28.6122, -80.8075),
    'Falmouth': (41.5515, -70.6148),
    'Breesport': (42.1645, -77.0441),
    'Carlotta': (40.5282, -124.0581),
    'Spencer': (42.2459, -71.9928),
    'Morrisdale': (40.9009, -78.1336),
    'Prairie Hill': (31.7354, -96.3419),
    'Westport': (41.1415, -73.3579),
    'Fort Washakie': (43.0138, -108.8998),
    'Loxahatchee': (26.6834, -80.2506),
    'Rock Tavern': (41.4709, -74.1968),
    'Jones': (35.4651, -82.5376),
    'Deltona': (28.9005, -81.2637),
    'Key West': (24.5551, -81.7800),
    'Grandview': (38.8859, -94.5333),
    'Saint Amant': (30.2277, -90.8245),
    'Clarks Mills': (41.2376, -80.3473),
    'Alpharetta': (34.0754, -84.2941),
    'Colorado Springs': (38.8339, -104.8214),
    'Greenville': (34.8526, -82.3940),
    'New York City': (40.7128, -74.0060),
    'Los Angeles': (34.0522, -118.2437),
    'Chicago': (41.8781, -87.6298),
    'Houston': (29.7604, -95.3698),
    'Phoenix': (33.4484, -112.0740),
    'Philadelphia': (39.9526, -75.1652),
    'San Antonio': (29.4241, -98.4936),
    'San Diego': (32.7157, -117.1611),
    'Dallas': (32.7767, -96.7970),
    'San Jose': (37.3382, -121.8863),
    'Birmingham': (33.5207, -86.8025),
    'Baton Rouge': (30.4515, -91.1871),
    'Miami': (25.7617, -80.1918),
    'Atlanta': (33.7490, -84.3880),
    'Boston': (42.3601, -71.0589),
    'Seattle': (47.6062, -122.3321),
    'Denver': (39.7392, -104.9903),
    'Las Vegas': (36.1699, -115.1398),
}

CITY_POPULATION = {
    'Columbia': 133358,
    'Altonah': 106,
    'Bellmore': 16218,
    'Titusville': 47513,
    'Falmouth': 31531,
    'Breesport': 1023,
    'Carlotta': 1200,
    'Spencer': 11688,
    'Morrisdale': 800,
    'Prairie Hill': 147,
    'Westport': 28043,
    'Fort Washakie': 1781,
    'Loxahatchee': 3000,
    'Rock Tavern': 3500,
    'Jones': 1987,
    'Deltona': 91847,
    'Key West': 24649,
    'Grandview': 24475,
    'Saint Amant': 4500,
    'Clarks Mills': 150,
    'Alpharetta': 65818,
    'Colorado Springs': 478221,
    'Greenville': 70720,
    'New York City': 8336817,
    'Los Angeles': 3979576,
    'Chicago': 2693976,
    'Houston': 2320268,
    'Phoenix': 1680992,
    'Philadelphia': 1584064,
    'San Antonio': 1547253,
    'San Diego': 1423851,
    'Dallas': 1343573,
    'San Jose': 1021795,
    'Birmingham': 200733,
    'Baton Rouge': 227470,
    'Miami': 442241,
    'Atlanta': 498715,
    'Boston': 685094,
    'Seattle': 753675,
    'Denver': 715522,
    'Las Vegas': 641903,
}

CITIES = list(CITY_COORDINATES.keys())
CATEGORIES = ['grocery_pos', 'grocery_net', 'shopping_pos', 'shopping_net', 'gas_transport', 'home', 'kids_pets',
              'travel', 'entertainment', 'food_dining', 'health_fitness', 'misc_pos', 'misc_net', 'personal_care']

def haversine_distance(lat1, lon1, lat2, lon2):
    R = 6371.0
    lat1, lon1, lat2, lon2 = map(np.radians, [lat1, lon1, lat2, lon2])
    dlat = lat2 - lat1
    dlon = lon2 - lon1
    a = np.sin(dlat/2.0)**2 + np.cos(lat1)*np.cos(lat2)*np.sin(dlon/2.0)**2
    return R * 2 * np.arcsin(np.sqrt(a))

def load_model():
    model_path = os.path.join(settings.BASE_DIR, 'ml_models', 'fraud_model2.pkl')
    if not os.path.exists(model_path):
        raise FileNotFoundError(f"Model not found at {model_path}")
    try:
        import joblib
        return joblib.load(model_path)
    except Exception as e:
        raise RuntimeError(f"Model loading failed: {e}")

def preprocess_transaction_data(form_data):
    features = {f'city_{city}': 0 for city in CITIES}
    features.update({f'category_{cat}': 0 for cat in CATEGORIES})

    sender_coords = CITY_COORDINATES.get(form_data['sender_city'], (40.7128, -74.0060))
    receiver_coords = CITY_COORDINATES.get(form_data['receiver_city'], (34.0522, -118.2437))
    distance_km = haversine_distance(*sender_coords, *receiver_coords)
    city_pop = CITY_POPULATION.get(form_data['sender_city'], 100000)
    trans_date = form_data['trans_date_trans_time']
    dob = form_data['date_of_birth']
    age = max(18, min(80, (trans_date.date() - dob).days // 365))

    hour = trans_date.hour
    weekday = trans_date.weekday()
    day = trans_date.day
    month = trans_date.month
    is_night = 1 if hour < 6 or hour > 22 else 0

    secs_since_last = 0
    if form_data['has_previous_transaction'] and form_data['previous_transaction_date']:
        time_diff = trans_date - form_data['previous_transaction_date']
        secs_since_last = max(0, time_diff.total_seconds())

    features.update({
        'distance_km': float(distance_km),
        'amt_inr': float(form_data['amount_inr']),
        'city_pop': int(city_pop),
        'age': int(age),
        'hour': int(hour),
        'weekday': int(weekday),
        'day': int(day),
        'month': int(month),
        'is_night': int(is_night),
        'secs_since_last': float(secs_since_last),
    })

    if form_data['sender_city'] in CITIES:
        features[f'city_{form_data['sender_city']}'] = 1
    if form_data['category'] in CATEGORIES:
        features[f'category_{form_data['category']}'] = 1

    
    return features

def safe_predict(model, df):
    try:
        prediction = model.predict(df)[0]
        probability = model.predict_proba(df)[0][1]
        return int(prediction), float(probability)
    except Exception as e:
        print(f"Prediction error: {e}")
        return None, None

def calculate_rule_based_probability(form_data, features):
    risk_score = 0.0
    amount = form_data['amount_inr']
    if amount > 100000:
        risk_score += 0.4
    elif amount > 50000:
        risk_score += 0.25
    elif amount > 20000:
        risk_score += 0.15
    elif amount > 10000:
        risk_score += 0.1

    hour = form_data['trans_date_trans_time'].hour
    if hour < 6 or hour > 22:
        risk_score += 0.2
    elif hour < 8 or hour > 20:
        risk_score += 0.1

    if features and 'distance_km' in features:
        distance = features['distance_km']
        if distance > 3000:
            risk_score += 0.3
        elif distance > 1500:
            risk_score += 0.2
        elif distance > 500:
            risk_score += 0.1

    if form_data['date_of_birth']:
        age = (form_data['trans_date_trans_time'].date() - form_data['date_of_birth']).days // 365
        if age < 18 or age > 75:
            risk_score += 0.15

    if form_data['category'] in ['misc_net', 'misc_pos', 'travel']:
        risk_score += 0.1

    return min(risk_score, 0.85)

def predict_fraud(form_data):
    try:
        features = preprocess_transaction_data(form_data)
        model = load_model()
        df = pd.DataFrame([features])
        shape_f = df.shape
        for col in df.columns:
            df[col] = pd.to_numeric(df[col], errors='coerce').fillna(0)
        prediction, probability = safe_predict(model, df)
        if prediction is None:
            raise Exception("ML failed")
    except Exception as e:
        print(f"ML prediction failed: {e}, falling back to rule-based")
        probability = calculate_rule_based_probability(form_data, features)
        prediction = 1 if probability > 0.5 else 0

    risk_score = probability * 100
    confidence_score = max(probability, 1 - probability) * 100

    if probability > 0.8:
        status = 'declined'
        recommendation = 'decline'
    elif probability > 0.3:
        status = 'pending'
        recommendation = 'review'
    else:
        status = 'approved'
        recommendation = 'approve'

    return {
        'is_fraud': bool(prediction),
        'fraud_probability': float(probability),
        'risk_score': float(risk_score),
        'confidence_score': float(confidence_score),
        'status': status,
        'recommendation': recommendation,
        'processing_time': 150.0,
        'features': features,
    }