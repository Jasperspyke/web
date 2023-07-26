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

@app.route('/search', methods = ['POST', 'GET'])
def search():
    searched = None
    form = SearchForm()
    data = pd.read_csv('databases/Entitled - Sheet1.csv')
    initial_data_html = data.to_html()
    if form.validate_on_submit():
        searched = form.searched.data
        form.searched.data = ''
        new_data = filter_by_keyword(data, searched).to_html()
        return render_template('search.html', searched=searched, form=form, data=new_data)

    return render_template('search.html', searched=searched, form=form, data=initial_data_html)
@app.route('/search', methods = ['POST', 'GET'])
def contact():
    return render_template()

app.run(debug=True)

