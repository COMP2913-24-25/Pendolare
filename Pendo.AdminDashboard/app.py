from flask import Flask, render_template, request, redirect, url_for, session, flash
import requests

app = Flask(__name__)
app.secret_key = 'reallyStrongPwd123'

api_url = 'http://localhost:8080'

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        identityRequest = {"emailAddress": email}
        response = requests.post(f'{api_url}/api/auth/request-otp', json=identityRequest)
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
        response = requests.post(f'{api_url}/api/auth/verify-otp', json={'email': session['email'], 'otp': otp})
        if response.status_code == 200:
            session['logged_in'] = True
            return redirect(url_for('dashboard'))
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
    return "Chat with {username}"

@app.route('/update_booking_fee', methods=['POST'])
def update_booking_fee():
    booking_fee = request.form['booking_fee']

    # Update the booking fee the database through analytics service
    return redirect(url_for('dashboard'))

if __name__ == '__main__':
    app.run(debug=True)
