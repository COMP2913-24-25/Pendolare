from flask import Flask, render_template

app = Flask(__name__)

@app.route('/')
def home():
    return "Hello, World!"

@app.route('/dashboard')
def dashboard():
    total_active_users = 100
    return render_template('dashboard.html', total_active_users=total_active_users)

@app.route('/bookings')
def bookings():
    return "Bookings Management Page"

@app.route('/users')
def users():
    return "Users Management Page"

@app.route('/journey')
def journey():
    return "Journey Monitoring Page"

@app.route('/reports')
def reports():
    return "Financial Reports Page"

@app.route('/admin')
def admin():
    return "Admin Controls Page"

@app.route('/dispute')
def dispute():
    return "Dispute Resolution Page"

if __name__ == '__main__':
    app.run(debug=True)
