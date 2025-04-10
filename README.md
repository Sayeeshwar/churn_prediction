# Vodafone Customer Churn Prediction & Email Generation

This project implements a machine learning solution to predict which Vodafone customers are likely to churn, coupled with an AI-powered email generation system to create personalized retention emails following brand guidelines.

## Project Structure

```
vodafone-churn-project/
├── Vodafone_Customer_Churn_Sample_Dataset.csv # Telecom customer dataset
├── models/
│   ├── best_logistic_regression_model.pkl            # Trained churn prediction model
│   └── model_features.pkl                            # Features used in model training
├── src/
│   ├── customer_segmentation.py                      # Code to segment customers by churn risk
│   ├── email_generator.py                            # Email generation using Mistral AI
│   ├── utils.py                                      # Preprocessing and utility functions
│   └── config.py                                     # Configuration settings and API keys
├── outputs/
│   └── retention_emails.txt                          # Generated retention emails
├── main.py                                           # Main execution script
└── README.md                                         # This file
```

## Setup Instructions

### Prerequisites

- Python 3.8 or higher
- Mistral AI API key

### Installation

1. Clone this repository:
   ```
   git clone https://github.com/yourusername/vodafone-churn-project.git
   cd vodafone-churn-project
   ```

2. Create and activate a virtual environment:
   ```
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. Install dependencies:
   ```
   pip install -r requirements.txt
   ```

4. Ensure you have an API key for Mistral AI

### Data Preparation

1. Ensure the Vodafone dataset is placed in the `data/` directory:
   ```
   mkdir -p data
   # Copy the dataset to the data directory
   ```

## Model Training (Optional)

The repository includes pre-trained models, but if you want to retrain:

1. Run the Jupyter notebook or script for model training:
   ```
   jupyter notebook model.ipynb
   ```
   
2. This will generate updated model files in the `models/` directory.

## Running the Email Generation System

1. Execute the main script:
   ```
   python main.py
   ```

2. The script will:
   - Load and preprocess the customer data
   - Apply the churn prediction model
   - Segment customers by churn risk
   - Generate personalized retention emails for high-risk customers
   - Save the emails to `outputs/retention_emails.txt`

## Configuration

To customize the system:

1. Edit `src/config.py` to update:
   - API endpoints and parameters
   - Model paths
   - Email settings for different customer segments

2. Modify email generation prompts in `src/email_generator.py` to adjust:
   - Special offers based on customer profile
   - Tone and structure requirements

## Project Approach

1. **Churn Prediction**:
   - Uses logistic regression model
   - Identifies key factors influencing churn: contract type, payment method, service add-ons

2. **Email Generation**:
   - Segments customers based on churn probability
   - Creates personalized prompts based on customer profile and churn factors
   - Generates emails following Vodafone tone guidelines using Mistral AI
   - Ensures content adheres to brand standards and structure requirements

## Notes

- The email generation system requires an active internet connection to access the Mistral AI API