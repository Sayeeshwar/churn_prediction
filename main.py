import pandas as pd
import os
import pickle
from src.customer_segmentation import load_model, segment_customers
from src.email_generator import create_retention_email_prompt, generate_email
from src.utils import preprocess_customer_data
from src.config import MODEL_PATH, DATA_PATH, MISTRAL_API_KEY

def main():
    api_key = input("Please enter your Mistral API key: ")
    os.environ['MISTRAL_API_KEY'] = api_key
    df = pd.read_csv(DATA_PATH)
    df_processed = preprocess_customer_data(df)
    model = load_model(MODEL_PATH)
    
    with open('models/model_features.pkl', 'rb') as f:
        features = pickle.load(f)
    
    segments = segment_customers(df_processed, model, features)
    high_risk_customers = segments['high_risk']
    emails = {}
    
    print(f"Generating emails for {len(high_risk_customers)} high-risk customers...")
    
    # Generate for first 5 customers as a sample
    for i, (idx, customer) in enumerate(high_risk_customers.iloc[:5].iterrows()):
        customer_dict = customer.to_dict()
        prompt = create_retention_email_prompt(customer_dict, 'high')
        email = generate_email(prompt, api_key=MISTRAL_API_KEY)
        emails[idx] = email
        print(f"Generated email for customer {idx}")
    
    if not os.path.exists('outputs'):
        os.makedirs('outputs')
        print("'outputs' directory created.")
    else:
        print("'outputs' directory already exists.")

    with open('outputs/retention_emails.txt', 'w') as f:
        for customer_id, email in emails.items():
            f.write(f"===== EMAIL FOR CUSTOMER {customer_id} =====\n\n")
            f.write(email)
            f.write("\n\n")
    
    print("Email generation complete!")

if __name__ == "__main__":
    main()
