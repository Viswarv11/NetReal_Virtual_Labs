import flash
from flask import flash
from flask import Flask, render_template, request, redirect, url_for, session
import mysql.connector

app = Flask(__name__)

db_config = {
    'host': 'localhost',
    'user': 'root',
    'password': '',
    'database': 'vlabs',
}
app.secret_key = '7PQkX3uRvJb4Gp5Y'


@app.route('/')
def index():
    return render_template("index.html")


@app.route('/logout')
def logout():
    # Clear the user's session data
    session.pop('user_email', None)
    # Redirect to the home page or any other desired page after logging out
    return redirect(url_for('index'))


@app.route('/course')
def course():
    return render_template('Course.html')


@app.route('/sqlinjection')
def sql_injection_page():
    # Your code to render the Sqlinjection.html page here
    return render_template('Sqlinjection.html')


@app.route('/nmap')
def nmap_page():
    # Your code to render the nmap.html page here
    return render_template('nmap.html')


@app.route('/Taskpage1')
def task_page():
    return render_template('TaskPage1.html')


@app.route('/register', methods=['POST'])
def register():
    if request.method == 'POST':
        first_name = request.form['first_name']
        last_name = request.form['last_name']
        mobile = request.form['mobile']
        email = request.form['email']
        password = request.form['password']

        if first_name and last_name and mobile and email and password:
            db = mysql.connector.connect(**db_config)
            cursor = db.cursor()

            try:
                # Insert the new user into the database
                insert_query = "INSERT INTO userstable (FirstName, LastName, Mobile, Email, Password, Admin) " \
                               "VALUES (%s, %s, %s, %s, %s, 0)"  # Assuming Admin is set to 0 for regular users
                cursor.execute(insert_query, (first_name, last_name, mobile, email, password))
                db.commit()

                flash("Registration successful.", "success")

            except mysql.connector.Error as err:
                flash(f"Database Error: {err}", "danger")

            finally:
                cursor.close()
                db.close()
        else:
            flash("All fields are required.", "danger")

    return render_template('LoginReg.html')  # Redirect back to the registration page


@app.route('/profile')
def profile():
    if 'user_email' in session:
        user_email = session['user_email']

        db = mysql.connector.connect(**db_config)
        cursor = db.cursor()

        # Fetch user details from the database
        cursor.execute("SELECT * FROM userstable WHERE Email = %s", (user_email,))
        user_data = cursor.fetchone()

        cursor.close()
        db.close()

        print("User Email:", user_email)
        print("User Data:", user_data)

        if user_data:
            # Pass user data to the profile.html template
            return render_template('profile.html', user_data=user_data)

    return redirect('/login')


# Redirect to login if not logged in


# Route for login
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['subject']

        if email and password:
            db = mysql.connector.connect(**db_config)
            cursor = db.cursor()

            # Check if the user exists in the database
            cursor.execute("SELECT * FROM userstable WHERE Email = %s AND Password = %s", (email, password))
            user = cursor.fetchone()

            cursor.close()
            db.close()

            if user:
                session['user_email'] = email  # Store user email in session
                flash("Login successful.", "success")
                return redirect('/profile')  # Redirect to the profile route

            flash("Invalid email or password. Please try again.", "danger")

    return render_template('LoginReg.html')


@app.route('/cyber')
def cyber_page():
    # You can add any necessary logic here before rendering the template
    return render_template('Cyber.html')


@app.route('/LoginRegister')
def login_register():
    return render_template('LoginReg.html')


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5003, debug=True)
