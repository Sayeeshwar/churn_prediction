import pandas as pd
import pickle
from sklearn.preprocessing import StandardScaler

def preprocess_customer_data(df):
    df['TotalCharges'] = pd.to_numeric(df['TotalCharges'], errors='coerce')
    df = df.dropna()
    
    # Binary encoding for Yes/No variables
    binary_cols = ['Partner', 'Dependents', 'PhoneService', 'PaperlessBilling', 'Churn']
    for col in binary_cols:
        if col in df.columns:
            df[f'has_{col.lower()}'] = df[col].map({'Yes': 1, 'No': 0})
    
    # Handle gender
    if 'gender' in df.columns:
        df['is_male'] = df['gender'].map({'Male': 1, 'Female': 0})
    
    if 'SeniorCitizen' in df.columns:
        df['is_senior_citizen'] = df['SeniorCitizen']
    
    # Handle internet-dependent services
    internet_services = ['OnlineSecurity', 'OnlineBackup', 'DeviceProtection', 
                        'TechSupport', 'StreamingTV', 'StreamingMovies']
    for service in internet_services:
        if service in df.columns:
            df[f'has_{service.lower()}'] = df[service].map({'Yes': 1, 'No': 0, 'No internet service': 0})
    
    # Handle MultipleLines
    if 'MultipleLines' in df.columns:
        df['has_multiple_lines'] = df['MultipleLines'].map({'Yes': 1, 'No': 0, 'No phone service': 0})
    
    # One-hot encode multi-category variables
    multi_cat_cols = [col for col in ['InternetService', 'Contract', 'PaymentMethod'] if col in df.columns]
    if multi_cat_cols:
        df = pd.get_dummies(df, columns=multi_cat_cols, drop_first=False)
    
    # Create internet_services_count feature
    if all(f'has_{service.lower()}' in df.columns for service in internet_services):
        internet_service_cols = [f'has_{service.lower()}' for service in internet_services]
        df['internet_services_count'] = df[internet_service_cols].sum(axis=1)
    
    # Drop original categorical columns that have been encoded
    original_cols_to_drop = [
        'customerID',
        'gender',    
        'SeniorCitizen',
        'Partner',   
        'Dependents',
        'PhoneService',
        'MultipleLines',
        'OnlineSecurity',
        'OnlineBackup',
        'DeviceProtection',
        'TechSupport',
        'StreamingTV',
        'StreamingMovies',
        'PaperlessBilling',
        'Churn'      
    ]
    
    df = df.drop(columns=[col for col in original_cols_to_drop if col in df.columns], errors='ignore')
    
    numerical_features = ['tenure', 'MonthlyCharges', 'TotalCharges']
    features_present = [col for col in numerical_features if col in df.columns]
    
    if features_present:
        scaler = StandardScaler()
        df[features_present] = scaler.fit_transform(df[features_present])
    
    return df

def scale_features(df, scaler=None):
    numerical_features = ['tenure', 'MonthlyCharges', 'TotalCharges']
    features_present = [col for col in numerical_features if col in df.columns]
    
    if not features_present:
        return df, scaler
    
    if scaler is None:
        scaler = StandardScaler()
        scaler.fit(df[features_present])
    
    df[features_present] = scaler.transform(df[features_present])
    return df, scaler

def load_model(model_path):
    with open(model_path, 'rb') as file:
        model = pickle.load(file)
    return model

def save_model(model, model_path):
    with open(model_path, 'wb') as file:
        pickle.dump(model, file)
    print(f"Model saved as {model_path}")

def get_churn_factors(customer, model_coefficients, feature_names):
    feature_impacts = []
    for i, feature in enumerate(feature_names):
        if feature in customer:
            impact = float(customer[feature]) * model_coefficients[i]
            feature_impacts.append((feature, impact, model_coefficients[i]))
    
    # Sort by absolute impact value (highest first)
    feature_impacts.sort(key=lambda x: abs(x[1]), reverse=True)
    
    # Return the top 3 factors
    return feature_impacts[:3]

def identify_retention_offers(churn_factors):
    offers = []
    
    for factor, _, coefficient in churn_factors:
        if coefficient > 0:  # This factor increases churn probability
            if "Contract_Month-to-month" in factor:
                offers.append("Special discount on a one-year contract")
            elif "InternetService_Fiber" in factor:
                offers.append("Enhanced stability for your Fiber optic connection")
            elif "has_techsupport" in factor and factor == 0:
                offers.append("Complimentary Tech Support for 3 months")
            elif "has_onlinesecurity" in factor and factor == 0:
                offers.append("Free Online Security package for 6 months")
            elif "MonthlyCharges" in factor:
                offers.append("Loyalty discount on your monthly bill")
            elif "PaymentMethod_Electronic" in factor:
                offers.append("10% discount for switching to automatic payment")
            else:
                offers.append("Exclusive loyalty reward for valued customers")
    
    if not offers:
        offers.append("Special loyalty discount as a valued Vodafone customer")
    
    return offers[:2]
