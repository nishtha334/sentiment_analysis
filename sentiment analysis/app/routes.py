from flask import Blueprint, render_template, redirect, url_for, flash, request
from app.forms import CSVUploadForm, RegistrationForm, LoginForm, ReviewForm
from app.models import User
from app import db
from flask_login import login_user, logout_user, current_user, login_required
import pickle
import pandas as pd
import os
import joblib
import pandas as pd
import matplotlib.pyplot as plt
from io import BytesIO
import base64
from datetime import datetime
from flask import render_template, flash, redirect, url_for

main = Blueprint('main', __name__)  # Blueprint name should match with the one used in create_app

# Load the trained model
MODEL_PATH = os.path.join(os.path.dirname(__file__), '..', 'models', 'sentiment_model.pkl')
model = joblib.load(MODEL_PATH)

@main.route('/', methods=['GET', 'POST'])
@login_required
def sentiment():
    form = ReviewForm()
    sentiment = None
    if form.validate_on_submit():
        review = form.review.data
        sentiment = model.predict([review])[0]
        if sentiment==1:
            sentiment='Positive'
        else:
            sentiment='Negative'
    return render_template("sentiment.html", form=form, sentiment=sentiment)

@main.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('main.sentiment'))  # Corrected blueprint reference
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(username=form.username.data, email=form.email.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('Account created! You can now log in.', 'success')
        return redirect(url_for('main.login'))  # Corrected blueprint reference
    return render_template('register.html', form=form, title='Register')

@main.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('main.sentiment'))  # Always redirect to '/sentiment' if logged in
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user and user.check_password(form.password.data):
            login_user(user)
            return redirect(url_for('main.sentiment'))  # Always redirect to '/sentiment' after login
        flash('Login failed. Check credentials.', 'danger')
    return render_template('auth.html', form=form, title='Login')


@main.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('main.login'))  


@main.route('/analyze_reviews', methods=['GET', 'POST'])
@login_required
def analyze_reviews():
    form = CSVUploadForm()
    plot_url = None
    sentiment_results = None
    time_analysis = None
    rating_stats = None
    
    if form.validate_on_submit():
        try:
            # Read and prepare data
            df = pd.read_csv(form.csv_file.data)
            
            # Check required columns
            if 'reviews.text' not in df.columns:
                flash("CSV must contain 'reviews.text' column", 'danger')
                return redirect(url_for('main.analyze_reviews'))
            
            # Clean data
            df = df.dropna(subset=['reviews.text'])
            df = df[df['reviews.text'].str.strip() != '']
            
            # Sentiment analysis - MODIFIED SECTION
            if 'reviews.rating' in df.columns:
                # Use rating-based sentiment
                df['sentiment'] = df['reviews.rating'].apply(
                    lambda x: 1 if x >= 4 else (0 if x <= 2 else 0.5)  # 1=Positive, 0=Negative, 0.5=Neutral
                )
                df['sentiment_label'] = df['reviews.rating'].apply(
                    lambda x: 'Positive' if x >= 4 else ('Negative' if x <= 2 else 'Neutral')
                )
            else:
                # Fall back to model prediction
                df['sentiment'] = df['reviews.text'].apply(lambda x: model.predict([x])[0])
                df['sentiment_label'] = df['sentiment'].map({1: 'Positive', 0: 'Negative'})
            
            # Calculate statistics - UPDATED FOR 3 CATEGORIES
            total_reviews = len(df)
            positive = len(df[df['sentiment'] == 1])
            negative = len(df[df['sentiment'] == 0])
            neutral = len(df[df['sentiment'] == 0.5])
            
            positive_percent = round((positive / total_reviews * 100), 1)
            negative_percent = round((negative / total_reviews * 100), 1)
            neutral_percent = round((neutral / total_reviews * 100), 1)
            
            sentiment_results = {
                'total': total_reviews,
                'positive': positive,
                'negative': negative,
                'neutral': neutral,
                'positive_percent': positive_percent,
                'negative_percent': negative_percent,
                'neutral_percent': neutral_percent,
                'sample_positive': df[df['sentiment'] == 1]['reviews.text'].sample(min(3, positive)).tolist(),
                'sample_negative': df[df['sentiment'] == 0]['reviews.text'].sample(min(3, negative)).tolist(),
                'sample_neutral': df[df['sentiment'] == 0.5]['reviews.text'].sample(min(3, neutral)).tolist(),
                'using_ratings': 'reviews.rating' in df.columns
            }
            
            # Time analysis if date column exists
            if 'reviews.date' in df.columns:
                try:
                    df['date'] = pd.to_datetime(df['reviews.date'])
                    df.set_index('date', inplace=True)
                    
                    # Daily sentiment
                    daily_sentiment = df['sentiment'].resample('D').mean()
                    
                    # Weekly rolling average for smoother trend
                    weekly_avg = daily_sentiment.rolling(7, min_periods=1).mean()
                    
                    # Plotting
                    plt.figure(figsize=(12, 6))
                    weekly_avg.plot(color='#4CAF50', linewidth=2.5, label='7-day Avg')
                    daily_sentiment.plot(marker='o', linestyle='', alpha=0.3, color='#8BC34A', label='Daily')
                    
                    plt.title('Sentiment Trend Over Time', pad=20)
                    plt.ylabel('Positive Sentiment Ratio')
                    plt.xlabel('Date')
                    plt.ylim(0, 1)
                    plt.legend()
                    plt.grid(True, alpha=0.3)
                    
                    # Save plot
                    img = BytesIO()
                    plt.savefig(img, format='png', bbox_inches='tight', dpi=100)
                    img.seek(0)
                    plot_url = base64.b64encode(img.getvalue()).decode('utf8')
                    plt.close()
                    
                    # Time-based stats - FIXED ROUNDING HERE TOO
                    recent_positive = df.last('30D')['sentiment'].mean()
                    time_analysis = {
                        'time_period': f"{df.index.min().strftime('%b %Y')} to {df.index.max().strftime('%b %Y')}",
                        'period_weeks': int((df.index.max() - df.index.min()).days / 7),
                        'recent_positive': round(recent_positive, 3) if not pd.isna(recent_positive) else 0
                    }
                    
                except Exception as e:
                    print(f"Error in time analysis: {e}")
                    plot_url = None
            
        except Exception as e:
            flash(f"Error processing file: {str(e)}", 'danger')
            return redirect(url_for('main.analyze_reviews'))
    
        except Exception as e:
            flash(f"Error processing file: {str(e)}", 'danger')
            return redirect(url_for('main.analyze_reviews'))
    
    return render_template(
        "analyze_reviews.html",
        form=form,
        plot_url=plot_url,
        sentiment=sentiment_results,
        time_analysis=time_analysis,
        rating_stats=rating_stats
    )