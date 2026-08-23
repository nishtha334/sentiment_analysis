# Sentiment Analysis Web App

A full-stack Flask web application for performing sentiment analysis on product reviews. This project includes a machine learning model trained on the Datafiniti Amazon Consumer Reviews dataset, along with a web interface that allows users to analyze individual text inputs or upload CSV files for bulk review analysis.

## Features
* **User Authentication:** Secure user registration and login system.
* **Single Text Analysis:** Enter a sentence or review to instantly get its sentiment (Positive/Negative).
* **Bulk Review Analysis:** Upload a CSV of reviews to analyze them in batches.
* **Custom Machine Learning Model:** Includes a pre-trained model (`sentiment_model.pkl`) and the script (`train_model.py`) used to train it.
* **Data Cleaning Utility:** Built-in text preprocessing to ensure clean data for accurate model predictions.

## Project Structure
```text
sentiment analysis/
├── app/
│   ├── static/             # CSS styling (styles.css)
│   ├── templates/          # HTML templates (base.html, auth.html, sentiment.html, etc.)
│   ├── utils/              # Helper scripts (text_cleaner.py)
│   ├── __init__.py         # Flask app initialization
│   ├── forms.py            # WTForms for user input/auth
│   ├── models.py           # Database models (User, etc.)
│   └── routes.py           # Application routes and views
├── instance/
│   └── site.db             # SQLite database for storing user data
├── models/
│   └── sentiment_model.pkl # Pickled machine learning model
├── Datafiniti_Amazon_Consumer_Reviews_of_Amazon_Products.csv # Training dataset
├── app.py                  # Entry point to run the Flask server
├── csv generator from dataset.py # Script for processing the raw dataset
├── requirements.txt        # Python dependencies
└── train_model.py          # Script to train and save the ML model

Installation & Setup
Clone the repository:

Bash
git clone [https://github.com/yourusername/your-repo-name.git](https://github.com/yourusername/your-repo-name.git)
cd your-repo-name
Create a Virtual Environment (Optional but recommended):

Bash
python -m venv venv
source venv/bin/activate  # On Windows use: venv\Scripts\activate
Install dependencies:

Bash
pip install -r requirements.txt
Run the application:

Bash
python app.py
The app will typically be accessible at http://127.0.0.1:5000/.

Model Training
If you want to retrain the machine learning model using the provided Amazon dataset or your own data:

Ensure the dataset CSV is in the root directory.

Run the training script:

Bash
python train_model.py
The new model will be saved as sentiment_model.pkl in the models/ directory.

Technologies Used
Backend: Python, Flask, SQLAlchemy

Frontend: HTML, CSS, Jinja2

Machine Learning: Scikit-Learn, Pandas, NLTK (or relevant NLP libraries)

License
[Add your license here, e.g., MIT License]


### Next Steps:
You might want to tweak the **Technologies Used** or **Prerequisites** sections if you used specific libraries (like TensorFlow or NLTK) that require extra setup steps (like downloading NLTK corpora). Do you need any help writing the code for those specific setup instructions?
