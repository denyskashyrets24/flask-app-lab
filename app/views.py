from flask import request, render_template
from . import app

@app.route('/')
@app.route('/resume')
def resume():
    return render_template('resume.html', title="Resume")

@app.route('/contacts')
def contacts():
    return render_template('contacts.html', title="Contacts")

@app.route('/homepage')
def home():
    agent = request.user_agent
    return render_template('homepage.html', agent=agent, title="Homepage")