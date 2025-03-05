from flask import Flask, render_template, request, redirect, url_for, session, flash
import requests
from datetime import timedelta, datetime
from identity_client import IdentityClient

app = Flask(__name__)
app.secret_key = 'reallyStrongPwd123'
app.permanent_session_lifetime = timedelta(minutes=30)

api_url = 'http://localhost:8080'

def check_inactivity():
    now = datetime.now().replace(tzinfo=None)
    last_activity = session.get('last_activity')
    if last_activity:
        last_activity = last_activity.replace(tzinfo=None)
    if last_activity and (now - last_activity).total_seconds() > app.permanent_session_lifetime.total_seconds():
        session.clear()
        flash('You have been logged out due to inactivity.')
        return redirect(url_for('login'))
    session['last_activity'] = now

@app.before_request
def before_request():
    if 'logged_in' in session:
        check_inactivity()

@app.route('/')
def home():
    return redirect(url_for('login'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        response = IdentityClient(api_url, app.logger).RequestOtp(email)

        if response.status_code == 200:
            session['email'] = email
            return redirect(url_for('verify_otp'))
        else:
            flash('Failed to request OTP. Are you sure you have an account?')
    return render_template('login.html')

@app.route('/verify_otp', methods=['GET', 'POST'])
def verify_otp():
    if request.method == 'POST':
        session.get('email')
        otp = request.form['otp']

        response = IdentityClient(api_url, app.logger).VerifyOtp(session['email'], otp)

        if response.status_code == 200:
            data = response.json()
            if data.get('isManager'):
                session['logged_in'] = True
                session['last_activity'] = datetime.utcnow().replace(tzinfo=None)
                return redirect(url_for('dashboard'))
            else:
                flash('Access denied. You must be a manager to log in to the admin dashboard.')
                return redirect(url_for('login'))
        else:
            flash('Invalid OTP. Please try again.')
    return render_template('verify_otp.html')

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('login'))

@app.route('/dashboard', methods=['GET', 'POST'])
def dashboard():
    if not session.get('logged_in'):
        return redirect(url_for('login'))
    if request.method == 'POST':
        booking_fee = request.form['booking_fee']
        return redirect(url_for('dashboard'))
    
    booking_fee = 5
    weekly_revenue = 1435
    revenue_date = '2021-09-01'
    customer_disputes = [
        {'username': 'user1', 'message': 'Dispute message 1'},
        {'username': 'user2', 'message': 'Dispute message 2'},
        {'username': 'user3', 'message': 'Lorem ipsum dorlor sit amet, consectetur adipiscing elit. Nullam'},
    ]
    return render_template('dashboard.html', booking_fee=booking_fee, weekly_revenue=weekly_revenue, revenue_date=revenue_date, customer_disputes=customer_disputes)

@app.route('/chat/<username>')
def chat(username):
    return f"Chat with {username}"

@app.route('/update_booking_fee', methods=['POST'])
def update_booking_fee():
    booking_fee = request.form['booking_fee']

    # update the booking fee the database through analytics service
    return redirect(url_for('dashboard'))

@app.route('/ping')
def ping():
    try:
        response = IdentityClient(api_url, app.logger).Ping()
        if response.status_code == 200:
            data = response.json()
            return f"API is reachable: {data['message']} at {data['timeSent']}"
        else:
            return f"Failed to reach API: {response.status_code}"
    except Exception as e:
        return f"Error: {str(e)}"

if __name__ == '__main__':
    app.run(debug=True)
