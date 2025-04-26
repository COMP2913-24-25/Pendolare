from flask import Flask, render_template, request, redirect, url_for, session, flash, jsonify
import requests
from datetime import timedelta, datetime
from identity_client import IdentityClient
from admin_client import AdminClient
from message_client import MessageClient
from config import app, api_url

def check_inactivity():
    now = datetime.utcnow()  # naive UTC datetime
    last_activity = session.get('last_activity')
    if last_activity:
        # Ensure last_activity is a naive datetime if it's aware.
        if hasattr(last_activity, 'tzinfo') and last_activity.tzinfo is not None:
            last_activity = last_activity.replace(tzinfo=None)
    if last_activity and (now - last_activity).total_seconds() > app.permanent_session_lifetime.total_seconds():
        session.clear()
        flash('You have been logged out due to inactivity.', 'warning')
        return redirect(url_for('login'))
    session['last_activity'] = now

@app.before_request
def before_request():
    """Pre-request hook to check for inactivity.
    
    Checks if the user has exceeded the inactivity timeout and clears the session if so.
    """
    if 'logged_in' in session:
        check_inactivity()

@app.route('/')
def home():
    """Redirect to the login route."""
    return redirect(url_for('login'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    """Handle user login.
    
    GET: Render the login form.
    POST: Process login form, request OTP via IdentityClient.
    
    Returns:
        Flask response object.
    """
    if request.method == 'POST':
        email = request.form['email']
        response = IdentityClient(api_url, app.logger).RequestOtp(email)
        if response.status_code == 200:
            session['email'] = email
            return redirect(url_for('verify_otp'))
        else:
            flash('Failed to request OTP. Are you sure you have an account?', 'danger')
    return render_template('login.html')

@app.route('/verify_otp', methods=['GET', 'POST'])
def verify_otp():
    """Verify OTP for user authentication.
    
    GET: Render the OTP verification form.
    POST: Validate OTP via IdentityClient and, if valid and user is a manager, initiate a session.
    
    Returns:
        Flask response object.
    """
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
                flash('Access denied. You must be a manager to log in to the admin dashboard.', 'danger')
                return redirect(url_for('login'))
        else:
            flash('Invalid OTP. Please try again.', 'danger')
    return render_template('verify_otp.html')

@app.route('/logout')
def logout():
    """Log out the user by clearing the session."""
    session.clear()
    return redirect(url_for('login'))

@app.route('/dashboard', methods=['GET', 'POST'])
def dashboard():
    """Display the admin dashboard.
    
    GET: Retrieve and display booking fee, weekly revenue, discounts, and conversation data.
    POST: Process booking fee update form submissions.
    
    Returns:
        Flask response object.
    """
    if not session.get('logged_in'):
        return redirect(url_for('login'))
    if request.method == 'POST':
        booking_fee = request.form['booking_fee']
        return redirect(url_for('dashboard'))
    
    admin_client = AdminClient(api_url, app.logger, jwt=session.get('jwt'))
    booking_fee = admin_client.GetBookingFee()
    print("Booking fee:", booking_fee)

    now = datetime.utcnow()
    start_of_week = now - timedelta(days=7)
    print("Start of week:", start_of_week)
    rev_response = admin_client.GetWeeklyRevenue(start_of_week, now)
    
    rev_this_week = rev_response.get('total')

    five_weeks_ago = start_of_week - timedelta(weeks=5)
    revenue_response = admin_client.GetWeeklyRevenue(five_weeks_ago, now)
    
    expected_labels = [(five_weeks_ago + timedelta(weeks=i)).strftime('%d %B %Y') for i in range(6)]
    api_labels = revenue_response.get('labels', [])
    api_data = revenue_response.get('data', [])

    chartData = [0] * len(expected_labels)
    for label, data in zip(api_labels, api_data):
        try:
            week_num = int(label.split()[-1])
            index = week_num - 1
            if 0 <= index < len(chartData):
                chartData[index] = data
        except ValueError:
            pass

    chartLabels = expected_labels
    
    discounts = admin_client.GetDiscounts()
    if discounts:
        for discount in discounts:
            discount['DiscountPercentage'] = discount.get('DiscountPercentage', 0) * 100
    app.logger.info("Discounts: %s", discounts)
    
    messaging_client = MessageClient(f"{api_url}/api/Message", app.logger, jwt=session.get('jwt'))
    user_conversations = messaging_client.get_user_conversations("00000000-0000-0000-0000-000000000000")
    
    return render_template('dashboard.html',
                           booking_fee=booking_fee,
                           rev_this_week=rev_this_week,
                           revenue_date=start_of_week.strftime('%d %B %Y'),
                           conversations=user_conversations,
                           discounts=discounts,
                           chartData=chartData,
                           chartLabels=chartLabels)

@app.route('/chat/conversation/<conversation_id>', methods=['GET'])
def chat_conversation(conversation_id):
    """Render a chat conversation page.
    
    Retrieves conversation details based on conversation_id.
    
    Args:
        conversation_id (str): The ID of the conversation.
    
    Returns:
        Flask response object.
    """
    messaging_client = MessageClient(f"{api_url}/api/Message", app.logger, jwt=session.get('jwt'))
    conv_response = messaging_client.join_conversation("00000000-0000-0000-0000-000000000000", conversation_id)
    app.logger.info(f"Join conversation returned: {conv_response}")
    print("conv_response:", conv_response)
    return render_template('chat.html',
                           conversation_id=conversation_id,
                           conversation=conv_response)

@app.route('/chat/send', methods=['POST'])
def chat_send():
    """Send a chat message.
    
    Processes JSON data containing sender, conversation_id, content, and timestamp, sends the chat message via MessageClient, and returns the response as JSON.
    
    Returns:
        Flask JSON response.
    """
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
    """Update the booking fee.
    
    Reads the booking fee from the POST request, updates it through AdminClient, and flashes a success or error message.
    
    Returns:
        Flask redirect response.
    """
    booking_fee = request.form['booking_fee']
    response = AdminClient(api_url, app.logger, jwt=session.get('jwt')).UpdateBookingFee(booking_fee)
    if response.status_code == 200:
        flash("Booking fee updated successfully.", "success")
    else:
        flash("Failed to update booking fee.", "danger")
    return redirect(url_for('dashboard'))

@app.route('/create_discount', methods=['GET', 'POST'])
def create_discount():
    """Create a new discount.
    
    GET: Render the discount creation form.
    POST: Process form data to create a discount via AdminClient and provide a success/error flash message.
    
    Returns:
        Flask response object.
    """
    if not session.get('logged_in'):
        return redirect(url_for('login'))
    if request.method == 'POST':
        weekly_journeys = request.form.get('weekly_journeys')
        discount_percentage = request.form.get('discount_percentage')
        app.logger.info("Attempting to create discount with weekly_journeys: %s, discount_percentage: %s", weekly_journeys, discount_percentage)
        admin_client = AdminClient(api_url, app.logger, jwt=session.get('jwt'))
        result = admin_client.CreateDiscount(weekly_journeys, discount_percentage)
        if result:
            app.logger.info("Discount created successfully: %s", result)
            flash("Discount created successfully.", "success")
        else:
            app.logger.error("Failed to create discount with weekly_journeys: %s, discount_percentage: %s", weekly_journeys, discount_percentage)
            flash("Failed to create discount.", "danger")
        return redirect(url_for('dashboard'))
    return render_template('create_discount.html')

@app.route('/delete_discount/<discount_id>', methods=['POST', 'DELETE'])
def delete_discount(discount_id):
    """Delete an existing discount.
    
    Initiates discount deletion using AdminClient and provides an appropriate flash message.
    
    Args:
        discount_id (str): The ID of the discount to be deleted.
    
    Returns:
        Flask redirect response.
    """
    if not session.get('logged_in'):
        return redirect(url_for('login'))
    app.logger.info("Attempting to delete discount with id: %s", discount_id)
    admin_client = AdminClient(api_url, app.logger, jwt=session.get('jwt'))
    success = admin_client.DeleteDiscount(discount_id)
    if success:
        app.logger.info("Discount deleted successfully: %s", discount_id)
    else:
        app.logger.error("Failed to delete discount: %s", discount_id)
    flash("Discount deleted successfully." if success else "Failed to delete discount. This discount option may be in use by a journey.", "success" if success else "danger")
    return redirect(url_for('dashboard'))

@app.route('/ping')
def ping():
    """Ping the IdentityClient API.
    
    Sends a ping request to the API to verify connectivity and returns the API's status message or an error.
    
    Returns:
        String message with API status.
    """
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
