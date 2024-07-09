from flask import Flask, request, jsonify
from flask_cors import CORS, cross_origin
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from dotenv import load_dotenv
import os

load_dotenv()  # Load environment variables from .env file

app = Flask(__name__)
CORS(app, resources={r"/send-email": {"origins": "*"}})

@app.route('/send-email', methods=['POST'])
@cross_origin(origin='localhost', headers=['Content-Type', 'Authorization'])
def send_email():
    data = request.get_json()
    name = data.get('name')
    sender_email = data.get('email')
    message = data.get('message')

    # Create the email content
    email_message = MIMEMultipart()
    email_message['From'] = sender_email
    email_message['To'] = os.getenv('EMAIL_USER')
    email_message['Subject'] = f'Contact Us Form Submission from {name}'
    
    email_message.attach(MIMEText(f'Name: {name}\nEmail: {sender_email}\nMessage: {message}', 'plain'))

    # Send the email
    try:
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        server.login(os.getenv('EMAIL_USER'), os.getenv('EMAIL_PASS'))
        server.send_message(email_message)
        server.quit()
        return jsonify({'message': 'Email sent successfully'}), 200
    except smtplib.SMTPException as e:
        return jsonify({'message': f'Failed to send email: {str(e)}'}), 500
    except Exception as e:
        return jsonify({'message': f'An error occurred: {str(e)}'}), 500

if __name__ == '__main__':
    app.run(debug=True)