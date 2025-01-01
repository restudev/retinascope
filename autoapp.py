# -*- coding: utf-8 -*-
"""Create an application instance."""
from retinascope.app import create_app

app = create_app()
from flask import Flask, render_template

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)
