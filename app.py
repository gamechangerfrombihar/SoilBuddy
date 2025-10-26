from flask import Flask, render_template, request, redirect, flash, url_for, session
from werkzeug.utils import secure_filename
import os

from utils.krishi_logic import generate_plan
from utils.soilscan_logic import analyze_soil  # only one argument

app = Flask(__name__)
app.secret_key = 'some_secret_key'

# ----------------- File Upload -----------------
UPLOAD_FOLDER = 'static/uploads'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# ----------------- Language Logic -----------------
@app.route('/set_language/<lang>')
def set_language(lang):
    session['lang'] = lang
    next_page = request.args.get('next') or url_for('home')
    return redirect(next_page)

def get_lang():
    return session.get('lang', 'en')

# ----------------- Translations Dictionary -----------------
from translations import translations

# ----------------- Home & Features -----------------
@app.route('/')
def home():
    lang = get_lang()
    texts = translations[lang]
    return render_template('HomePage.html', texts=texts, lang=lang)

# ----------------- KrishiUdaan -----------------
@app.route('/krishiudaan/desc')
def krishiudaan_desc():
    lang = get_lang()
    texts = translations[lang]
    return render_template('KrishiUdaan.html', texts=texts, lang=lang)

@app.route('/krishiudaan')
def krishiudaan():
    lang = get_lang()
    texts = translations[lang]
    return render_template('KrishiUdaanF.html', texts=texts, lang=lang)

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
        texts = translations[get_lang()]
        return render_template('KrishiUdaanResult.html', plan=plan, texts=texts, lang=get_lang())

    except ValueError as ve:
        flash(str(ve))
        return redirect('/krishiudaan')

# ----------------- AmritJeevan -----------------
@app.route('/amritjeevan/desc')
def amritjeevan_desc():
    texts = translations[get_lang()]
    return render_template('AmritJeevan.html', texts=texts, lang=get_lang())

@app.route('/amritjeevan')
def amritjeevan():
    texts = translations[get_lang()]
    return render_template('AmritJeevanF.html', texts=texts, lang=get_lang())

# ----------------- SoilScan -----------------
@app.route('/soilscan/desc')
def soilscan_desc():
    lang = get_lang()
    texts = translations[lang]
    return render_template('SoilScan.html', texts=texts, lang=lang)

@app.route('/soilscan')
def soilscan():
    lang = get_lang()
    texts = translations[lang]
    return render_template('SoilScanF.html', texts=texts, lang=lang)

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

    # ✅ Correct: only one argument
    soil_params, _ = analyze_soil(file_path)

    lang = get_lang()
    texts = translations[lang]

    return render_template(
        'SoilScanResult.html',
        soil_params=soil_params,
        plot_path=None,
        texts=texts,
        lang=lang
    )

# ----------------- BharatBot -----------------
@app.route('/bharatbot/desc')
def bharatbot_desc():
    lang = get_lang()
    texts = translations[lang]
    return render_template('BharatBot.html', texts=texts, lang=lang)

# ----------------- AgriConnect -----------------
@app.route('/agriconnect')
def agric_connect():
    lang = get_lang()
    texts = translations[lang]
    return render_template('Subsidiaries.html', texts=texts, lang=lang)


# ----------------- Logo -----------------
from flask import send_from_directory
@app.route('/templates/<path:filename>')
def serve_template_file(filename):
    return send_from_directory('templates', filename)

# ------------AgriRates----------------------    
@app.route('/agrirates')
def agrirates():
    return render_template('AgriRates.html')


# ----------------- Run App -----------------
if __name__ == '__main__':
    app.run(debug=True)
