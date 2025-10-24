from flask import Flask, render_template, request, redirect, flash, url_for
from werkzeug.utils import secure_filename
import os

from utils.krishi_logic import generate_plan
from utils.soilscan_logic import analyze_soil  # make sure this exists

app = Flask(__name__)
app.secret_key = 'some_secret_key'

# Folder for uploaded images
UPLOAD_FOLDER = 'static/uploads'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# ----------------- Home & Features -----------------
@app.route('/')
def home():
    return render_template('HomePage.html')

# ----------------- KrishiUdaan -----------------
@app.route('/krishiudaan/desc')
def krishiudaan_desc():
    return render_template('KrishiUdaan.html')

@app.route('/krishiudaan')
def krishiudaan():
    return render_template('KrishiUdaanF.html')

@app.route('/krishiudaan/result', methods=['POST'])
def krishiudaan_result():
    try:
        land_size = request.form['land_size']
        climate = request.form['climate']
        capital = request.form['capital']
        water = request.form['water']
        labourers = request.form['labour']
        region = request.form['region']
        num_crops = request.form['num_crops']

        plan = generate_plan(land_size, climate, capital, water, labourers, region, num_crops)
        return render_template('KrishiUdaanResult.html', plan=plan)

    except ValueError as ve:
        flash(str(ve))
        return redirect('/krishiudaan')

# ----------------- AmritJeevan -----------------
@app.route('/amritjeevan/desc')
def amritjeevan_desc():
    return render_template('AmritJeevan.html')

@app.route('/amritjeevan')
def amritjeevan():
    return render_template('AmritJeevanF.html')

# ----------------- SoilScan -----------------
@app.route('/soilscan/desc')
def soilscan_desc():
    return render_template('SoilScan.html')

@app.route('/soilscan')
def soilscan():
    return render_template('SoilScanF.html')

@app.route('/soilscan/result', methods=['POST'])
def soilscan_result():
    if 'soil_image' not in request.files:
        return "No file uploaded", 400

    file = request.files['soil_image']
    if file.filename == '':
        return "No selected file", 400

    filename = secure_filename(file.filename)
    file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    file.save(file_path)

    # Analyze soil image and generate PDF + plot
    soil_params, plot_path, pdf_path = analyze_soil(image_path=file_path)

    return render_template(
        'SoilScanResult.html',
        soil_params=soil_params,
        plot_path=plot_path,
        pdf_path=pdf_path
    )

# ----------------- Run App -----------------
if __name__ == '__main__':
    app.run(debug=True)
