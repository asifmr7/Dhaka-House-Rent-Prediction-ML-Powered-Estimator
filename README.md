
This repository contains a machine learning project designed to predict house rental prices in Dhaka. The model leverages features such as location, area (in square feet), the number of bedrooms, and
the number of bathrooms to provide rental price predictions.

Features of the Project:
Machine Learning Algorithm: Random Forest
Preprocessing Steps: Feature scaling, encoding, and pipeline integration
Backend Framework: Flask
Frontend Technologies: HTML, CSS, JavaScript
Data Source: Kaggle

Files in the Repository:
updated_with_randomforest_final_with_pipeline_and_pickle (1).ipynb.
The main notebook containing the model training code and implementation using Random Forest, integrated with pipeline processing.

Other associated scripts for data preprocessing, API integration, and front-end files.

Prerequisites:
Before using this project, make sure you have the following installed:

Python (>= 3.8).
Required Python Libraries (install using pip install -r requirements.txt):

pandas,
numpy,
matplotlib,
scikit-learn,
flask.


Usage
1. Clone the Repository
git clone https://github.com/asifmr7/HOUSE_PRD.git 
cd HOUSE_PRD
2. Run the Flask Backend
Make sure to update the file paths for the model and pipeline in your backend code. Start the Flask server:



python app.py
3. Access the Frontend
Open a web browser and navigate to:
http://127.0.0.1:5000/

4. Input Data for Prediction
Enter details such as location, area (sq. ft.), the number of bedrooms, and bathrooms.
The system will predict the estimated rental price.

Important Notes
The scaler and pipeline files used during preprocessing are not included in the repository.

How It Works
Input: User fills out the form with property details.
Preprocessing: The input data is scaled and encoded as required.
Prediction: The model predicts the rental price based on the input features.

Output: The prediction is displayed on the frontend.
