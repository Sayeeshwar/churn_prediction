import requests
import json
from src.config import MISTRAL_API_ENDPOINT, MISTRAL_MODEL, TEMPERATURE, MAX_TOKENS

def create_retention_email_prompt(customer, risk_level):
    contract_type = customer.get('Contract', 'Unknown')
    internet_service = customer.get('InternetService', 'Unknown')
    tenure = customer.get('tenure', 0)
    monthly_charges = customer.get('MonthlyCharges', 0)
    
    # Identify likely churn factors based on the dataset
    churn_factors = []
    if contract_type == 'Month-to-month':
        churn_factors.append("month-to-month contract")
    if customer.get('TechSupport') == 'No':
        churn_factors.append("no tech support")
    if customer.get('OnlineSecurity') == 'No':
        churn_factors.append("no online security")
    
    # Create tailored offers based on risk level and churn factors
    offers = []
    if "month-to-month contract" in churn_factors:
        offers.append("special discount on annual contracts")
    if "no tech support" in churn_factors:
        offers.append("complimentary tech support for 3 months")
    if "no online security" in churn_factors:
        offers.append("free security package for 6 months")
    
    prompt = f"""
    Create a personalized retention email for a Vodafone customer with {risk_level} churn risk.
    
    CUSTOMER PROFILE:
    - Contract type: {contract_type}
    - Internet service: {internet_service}
    - Tenure: {tenure} months
    - Monthly charges: ${monthly_charges}
    - Churn risk factors: {', '.join(churn_factors) if churn_factors else 'None identified'}
    
    SPECIAL OFFERS TO INCLUDE:
    {', '.join(offers) if offers else 'General loyalty discount'}
    
    FOLLOW THESE VODAFONE TONE GUIDELINES:
    1. Friendly and approachable: Use warm conversational language
    2. Clear and concise: Ensure messages are straightforward
    3. Positive and reassuring: Highlight benefits and positive outcomes
    4. Professional and trustworthy: Maintain a respectful tone
    
    EMAIL STRUCTURE:
    - Subject line: Engaging and relevant
    - Greeting: Personalized
    - Introduction: Brief appreciation for their business
    - Body: Highlight offers addressing their specific churn factors
    - Call to action: Clear next steps
    - Closing: Warm and appreciative
    
    The date today is April 10, 2025. Make sure the email feels personalized and not generic.
    """
    return prompt

def generate_email(prompt, api_key=None):
    try:
        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {api_key}"
        }
        
        # Create payload according to Mistral API format
        payload = {
            "model": MISTRAL_MODEL,
            "messages": [{"role": "user", "content": prompt}],
            "temperature": TEMPERATURE,
            "max_tokens": MAX_TOKENS
        }
        
        # Make API request to Mistral
        response = requests.post(
            MISTRAL_API_ENDPOINT,
            headers=headers,
            data=json.dumps(payload)
        )
        
        if response.status_code == 200:
            return response.json()["choices"][0]["message"]["content"]
        else:
            return f"Error generating email: {response.status_code} - {response.text}"
            
    except Exception as e:
        return f"Error generating email: {str(e)}"
