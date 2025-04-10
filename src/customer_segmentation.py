import pickle

def load_model(model_path):
    with open(model_path, 'rb') as file:
        model = pickle.load(file)
    return model

def segment_customers(df, model, features):
    print('features', features)
    churn_proba = model.predict_proba(df[features])[:, 1]
    df['churn_probability'] = churn_proba
    
    high_risk = df[df['churn_probability'] > 0.7]
    medium_risk = df[(df['churn_probability'] > 0.4) & (df['churn_probability'] <= 0.7)]
    low_risk = df[df['churn_probability'] <= 0.4]
    
    return {
        'high_risk': high_risk,
        'medium_risk': medium_risk,
        'low_risk': low_risk
    }
