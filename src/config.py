MISTRAL_API_ENDPOINT = "https://api.mistral.ai/v1/chat/completions"
MISTRAL_MODEL = "mistral-large-latest"
TEMPERATURE = 0.7
MAX_TOKENS = 1500

MODEL_PATH = "./models/model.pkl"
DATA_PATH = "./Vodafone_Customer_Churn_Sample_Dataset.csv"

EMAIL_SETTINGS = {
    "high_risk": {
        "subject_prefix": "Special Offer Just for You: ",
        "offer_strength": "strong"
    },
    "medium_risk": {
        "subject_prefix": "We Value Your Loyalty: ",
        "offer_strength": "medium"
    },
    "low_risk": {
        "subject_prefix": "Exclusive Vodafone Benefits: ",
        "offer_strength": "light"
    }
}
