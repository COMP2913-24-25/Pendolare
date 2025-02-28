from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/dashboard', methods=['GET', 'POST'])
def dashboard():
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

@app.route('/bookings')
def bookings():
    return render_template('bookings.html')

@app.route('/users')
def users():
    return render_template('users.html')

@app.route('/journey')
def journey():
    return render_template('journey.html')

@app.route('/reports')
def reports():
    return render_template('reports.html')

@app.route('/admin')
def admin():
    return render_template('admin.html')

@app.route('/dispute')
def dispute():
    return render_template('dispute.html')

@app.route('/update_booking_fee', methods=['POST'])
def update_booking_fee():
    booking_fee = request.form['booking_fee']
    # Process the booking fee (e.g., save to database)
    # ...
    return redirect(url_for('dashboard'))

if __name__ == '__main__':
    app.run(debug=True)
