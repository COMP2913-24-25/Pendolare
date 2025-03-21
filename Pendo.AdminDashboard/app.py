from flask import Flask, render_template, request, redirect, url_for, session, flash, jsonify
import requests
from datetime import timedelta, datetime
from identity_client import IdentityClient
from admin_client import AdminClient
from message_client import MessageClient

app = Flask(__name__)
app.secret_key = 'reallyStrongPwd123'
app.permanent_session_lifetime = timedelta(minutes=30)

api_url = 'https://pendo-gateway.clsolutions.dev'

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
                session['jwt'] = data.get('jwt')
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
    
    admin_client = AdminClient(api_url, app.logger, jwt=session.get('jwt'))
    booking_fee = admin_client.GetBookingFee()
    print("Booking fee:", booking_fee)

    now = datetime.utcnow()
    start_of_week = now - timedelta(days=now.weekday())
    end_of_week = now
    rev_response = admin_client.GetWeeklyRevenue(start_of_week, end_of_week)
    rev_this_week = rev_response.get('total')
    
    messaging_client = MessageClient(f"{api_url}/api/Message", app.logger, jwt=session.get('jwt'))
    user_conversations = messaging_client.get_user_conversations("00000000-0000-0000-0000-000000000000")
    
    return render_template('dashboard.html',
                           booking_fee=booking_fee,
                           rev_this_week=rev_this_week,
                           revenue_date=start_of_week.strftime('%d %B %Y'),
                           conversations=user_conversations)

@app.route('/chat/conversation/<conversation_id>', methods=['GET'])
def chat_conversation(conversation_id):
    messaging_client = MessageClient(f"{api_url}/api/Message", app.logger, jwt=session.get('jwt'))
    conv_response = messaging_client.join_conversation("00000000-0000-0000-0000-000000000000", conversation_id)
    app.logger.info(f"Join conversation returned: {conv_response}")
    print("conv_response:", conv_response)
    return render_template('chat.html',
                           conversation_id=conversation_id,
                           conversation=conv_response)

@app.route('/chat/send', methods=['POST'])
def chat_send():
    data = request.get_json()
    sender = data.get('sender')
    conversation_id = data.get('conversation_id')
    content = data.get('content')
    timestamp = data.get('timestamp')
    
    messaging_client = MessageClient(f"{api_url}/api/Message", app.logger, jwt=session.get('jwt'))
    if not messaging_client.ws or messaging_client.ws.closed:
        messaging_client.join_conversation("00000000-0000-0000-0000-000000000000", conversation_id)
    
    response = messaging_client.send_chat_message(sender, conversation_id, content, timestamp)
    return jsonify(response)

@app.route('/update_booking_fee', methods=['POST'])
def update_booking_fee():
    booking_fee = request.form['booking_fee']
    response = AdminClient(api_url, app.logger, jwt=session.get('jwt')).UpdateBookingFee(booking_fee)
    if response.status_code == 200:
        flash("Booking fee updated successfully.")
    else:
        flash("Failed to update booking fee.")
    return redirect(url_for('dashboard'))

@app.route('/update_discount_offers', methods=['POST'])
def update_discount_offers():
    discounts = request.form.getlist('discounts')
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
