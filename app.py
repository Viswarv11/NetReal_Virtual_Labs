import base64
import hashlib
import hmac
import time
import urllib
import uuid

import flash
from flask import flash, json
from flask import Flask, render_template, request, redirect, url_for, session
import mysql.connector
from flask import Flask, request, jsonify
from flask_cors import CORS
from flask import request as reqf

app = Flask(__name__)
CORS(app, resources={r"/api/*": {"origins": "http://127.0.0.1:5003"}})

baseurl = 'http://172.16.23.5:8080/client/api?'
secretkey = 'dmKJEDmijUYC6V53mpQZzNipzPryi0lizIYx9dvCepifE4XhcwkLX7W7txruiRaXkPHwadnl4lFGSVTUD7Ho_w'
api_key = 'CN9MeFkRSP09yNJ8d4W1GxLrBJEvGUATpipIpzu9GA6MC6SxNI-1ixRLjX2eANF6znPzZ1n0Unzc5OjqHEwRZA'

db_config = {
    'host': 'localhost',
    'user': 'root',
    'password': '',
    'database': 'vlabs',
}
app.secret_key = '7PQkX3uRvJb4Gp5Y'


def send_api_request(request):
    request_str = urllib.parse.urlencode(request)

    sig_str = '&'.join(['='.join([k.lower(), urllib.parse.quote_plus(request[k].lower().replace('+', '%20'))]) for k in
                        sorted(request.keys())])
    sig = base64.b64encode(hmac.new(secretkey.encode('utf-8'), sig_str.encode('utf-8'), hashlib.sha1).digest()).decode(
        'utf-8')
    req = baseurl + request_str + '&signature=' + urllib.parse.quote_plus(sig)
    with urllib.request.urlopen(req) as response:
        res = response.read().decode('utf-8')
    return res


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

@app.route('/Taskpage2')
def task_page1():
    return render_template('TaskPage2.html')

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

@app.errorhandler(Exception)
def handle_error(e):
    return jsonify({'error': str(e)}), 500


@app.route('/LoginRegister')
def login_register():
    return render_template('LoginReg.html')


@app.route('/api/deploy-vm', methods=['POST'])
def api_deploy_vm():
    try:
        # Access the data sent in the request body
        os_name = request.form.get('name')  # Change from reqf.form to request.form
        print(os_name)

        os_id = '1021daf6-f543-46db-a38a-5534c6a51ad6'

        # Generate a random VM name using uuid

        vm_name = 'vm'
        print(vm_name)
        request_data = {
            'command': 'deployVirtualMachine',
            'response': 'json',
            'apikey': api_key,  # Assuming 'api_key' is defined somewhere in your code
            'serviceofferingid': '38f991e6-0519-4d53-8f1b-2d3fb057332a',
            'templateid': os_id,
            'zoneid': 'ebeae8ad-582c-4ea7-9012-52238084af64',
            'name': 'nmap',
            'networkids': '886043f1-4289-4897-8e0e-0881b8182ec8',
            'rootdisksize': '10',
        }

        res = send_api_request(request_data)

        # Check if response is valid
        try:
            job_id = json.loads(res)['deployvirtualmachineresponse']['jobid']
            session['jobid'] = job_id
        except KeyError:
            return jsonify({'error': 'Invalid response from API'})

        # Wait for the IP address with a timeout
        timeout = 15  # Set your desired timeout in seconds
        start_time = time.time()

        while True:
            # Query for the IP address using the job_id
            ip_request_data = {
                'command': 'queryAsyncJobResult',
                'response': 'json',
                'apikey': api_key,
                'jobid': job_id,
            }

            ip_res = send_api_request(ip_request_data)

            # Extract the IP address from the response
            try:
                ip_address = json.loads(ip_res)['queryasyncjobresultresponse']['jobresult']['virtualmachine']['nic'][0][
                    'ipaddress']
                return jsonify({'success': True, 'message': 'VM deployment initiated successfully', 'vm_name': vm_name,
                                'ip_address': ip_address})
            except KeyError:
                pass  # Continue the loop if the IP address is not available yet

            if time.time() - start_time > timeout:
                return jsonify({'error': 'Timeout waiting for the IP address'}), 500

            time.sleep(2)  # Adjust the sleep interval as needed

    except Exception as e:
        return jsonify({'error': f'An error occurred: {str(e)}'}), 500

@app.route('/api/deploy-vm2', methods=['POST'])
def api_deploy_vm2():
    try:
        # Access the data sent in the request body
        # os_name = request.form.get('name')  # Change from reqf.form to request.form
        # print(os_name)

        os_id = '5fbb05fd-43b3-4f50-b483-b0564d15f77a'

        # Generate a random VM name using uuid

        vm_name = 'Sql'
        print(vm_name)
        request_data = {
            'command': 'deployVirtualMachine',
            'response': 'json',
            'apikey': api_key,  # Assuming 'api_key' is defined somewhere in your code
            'serviceofferingid': 'c7069951-3349-4f48-b9c6-48b76a1da15a',
            'templateid': '5fbb05fd-43b3-4f50-b483-b0564d15f77a',
            'zoneid': 'ebeae8ad-582c-4ea7-9012-52238084af64',
            'name': 'sql',
            'networkids': '886043f1-4289-4897-8e0e-0881b8182ec8',
            'diskofferingid': 'd753d61a-7dfa-4ac7-9df4-105538929d46'
        }

        res = send_api_request(request_data)

        # Check if response is valid
        try:
            job_id = json.loads(res)['deployvirtualmachineresponse']['jobid']
            session['jobid'] = job_id
        except KeyError:
            return jsonify({'error': 'Invalid response from API'})

        # Wait for the IP address with a timeout
        timeout = 15  # Set your desired timeout in seconds
        start_time = time.time()

        while True:
            # Query for the IP address using the job_id
            ip_request_data = {
                'command': 'queryAsyncJobResult',
                'response': 'json',
                'apikey': api_key,
                'jobid': job_id,
            }

            ip_res = send_api_request(ip_request_data)

            # Extract the IP address from the response
            try:
                ip_address = json.loads(ip_res)['queryasyncjobresultresponse']['jobresult']['virtualmachine']['nic'][0][
                    'ipaddress']
                return jsonify({'success': True, 'message': 'VM deployment initiated successfully', 'vm_name': vm_name,
                                'ip_address': ip_address})
            except KeyError:
                pass  # Continue the loop if the IP address is not available yet

            if time.time() - start_time > timeout:
                return jsonify({'error': 'Timeout waiting for the IP address'}), 500

            time.sleep(2)  # Adjust the sleep interval as needed

    except Exception as e:
        return jsonify({'error': f'An error occurred: {str(e)}'}), 500
# Run the Flask app
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5003, debug=True)

