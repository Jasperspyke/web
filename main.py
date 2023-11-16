from flask import Flask, render_template, request, redirect, url_for, flash
import flask_wtf
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired
import pandas as pd
app = Flask(__name__)
app.config['SECRET_KEY'] = 'my_secret'

class SearchForm(flask_wtf.FlaskForm):
    searched = StringField('Enter a keyword for an article', validators=[DataRequired()])
    submit = SubmitField('Submit')

@app.get('/')
def home():
    return render_template('index.html')

def filter_by_keyword(df, keyword):
    return df[df['keyword'].str.contains(keyword)]

@app.route('/contact', methods=['GET', 'POST'])
def contact():
    if request.method == 'POST':
        # Form submitted, handle the data
        full_name = request.form.get('full_name')
        email = request.form.get('email')
        message = request.form.get('message')

        # Process the form data (for demonstration, just print to console)
        print(f"Full Name: {full_name}, Email: {email}, Message: {message}")

        # Send a response message back to the frontend
        response_message = "Message received! We will respond and get back to you shortly."

        # Redirect to a new page with the response message
        return redirect(url_for('response', response_message=response_message))

    # If it's a GET request, render the contact form
    return render_template('contact.html', form_submitted=False)

@app.route('/response')
def response():
    response_message = request.args.get('response_message', '')
    return render_template('response.html', response_message=response_message)


def send_email(full_name, email, message):
    # Configure your SMTP server details
    smtp_server = 'your_smtp_server.com'
    smtp_port = 587
    smtp_username = 'your_email@example.com'
    smtp_password = 'your_email_password'

    # Create the email content
    subject = 'New Contact Form Submission'
    body = f'Full Name: {full_name}\nEmail: {email}\nMessage:\n{message}'

    # Send the email
    with smtplib.SMTP(smtp_server, smtp_port) as server:
        server.starttls()
        server.login(smtp_username, smtp_password)

        msg = MIMEText(body)
        msg['Subject'] = subject
        msg['From'] = smtp_username
        msg['To'] = 'tomhilliard@example.com'  # Replace with your actual email

        server.sendmail(smtp_username, ['tomhilliard@example.com'], msg.as_string())

@app.route('/search', methods = ['POST', 'GET'])
def search():
    searched = None
    form = SearchForm()
    data = pd.read_csv('databases/Entitled - Sheet1.csv')
    initial_data_html = data
    if form.validate_on_submit():
        searched = form.searched.data
        form.searched.data = ''
        new_data = filter_by_keyword(data, searched)
        return render_template('search.html', searched=searched, form=form, data=new_data)

    return render_template('search.html', searched=searched, form=form, data=initial_data_html)

@app.route('/process_data', methods=['POST'])
def process_data():
    form = SearchForm()
    data = pd.read_csv('databases/Entitled - Sheet1.csv')
    searched = request.form['searched']
    new_data = filter_by_keyword(data, searched)
    print(new_data)
    return render_template('search.html', form=form, searched=searched, data=new_data)

@app.route('/contact', methods = ['POST', 'GET'])
def test():
    return render_template('test.html')

app.run(debug=True)

