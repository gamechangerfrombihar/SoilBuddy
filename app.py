# app.py

from flask import Flask, render_template, request
from utils.krishi_logic import generate_plan

app = Flask(__name__)

# 🔹 Route: Home page
@app.route('/')
def home():
    return render_template('HomePage.html')


# 🔹 Route: Krishi Udaan input form
@app.route('/krishiudaan')
def krishiudaan():
    return render_template('KrishiUdaanF.html')


# 🔹 Route: Process form and show personalized result
@app.route('/krishiudaan/result', methods=['POST'])
def krishiudaan_result():
    # Get form data
    land_size = request.form.get('land_size')
    climate = request.form.get('climate')
    capital = request.form.get('capital')
    water = request.form.get('water')
    labourers = request.form.get('labour')  # matches your form
    region = request.form.get('region')
    num_crops = request.form.get('num_crops')

    # Generate plan
    plan = generate_plan(land_size, climate, capital, water, labourers, region, num_crops)

    # Render result template
    return render_template('KrishiUdaanResult.html', plan=plan)


    # Render result page with personalized plan
    return render_template('KrishiUdaanResult.html', plan=plan)


if __name__ == '__main__':
    app.run(debug=True)
