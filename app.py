from flask import Flask, render_template, request, redirect, flash, url_for, session
from werkzeug.utils import secure_filename
import os

from utils.krishi_logic import generate_plan
from utils.soilscan_logic import analyze_soil

app = Flask(__name__)
app.secret_key = 'some_secret_key'

# Folder for uploaded images
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
translations = {
    "en": {
        "welcome_title": "Welcome to SoilBuddy",
        "welcome_desc": "Empowering farmers with technology for a sustainable future. Explore the tools below to access live features:",
        "krishi_title": "KrishiUdaan",
        "krishi_desc": "Live crop transport tracking system for farmers and distributors.",
        "amrit_title": "AmritJeevan",
        "amrit_desc": "Monitor and manage soil moisture in real-time using IoT sensors.",
        "bharatbot_title": "BharatBot",
        "bharatbot_desc": "AI-powered chatbot to assist farmers with agriculture-related queries.",
        "soilscan_title": "SoilScan",
        "soilscan_desc": "Upload soil images and receive AI-based quality analysis instantly.",
        "launch_btn": "Launch"
    },
    "hi": {
        "welcome_title": "सोइलबड्डी में आपका स्वागत है",
        "welcome_desc": "किसानों को टिकाऊ भविष्य के लिए तकनीक से सशक्त बनाना। नीचे दिए गए टूल्स के माध्यम से लाइव फीचर्स एक्सेस करें:",
        "krishi_title": "कृषिउड़ान",
        "krishi_desc": "किसानों और वितरकों के लिए लाइव फसल ट्रैकिंग सिस्टम।",
        "amrit_title": "अमृतजीवन",
        "amrit_desc": "आईओटी सेंसर का उपयोग करके मिट्टी की नमी को वास्तविक समय में मॉनिटर और प्रबंधित करें।",
        "bharatbot_title": "भारतबोट",
        "bharatbot_desc": "कृषि से संबंधित प्रश्नों में किसानों की सहायता के लिए एआई चैटबॉट।",
        "soilscan_title": "सोइलस्कैन",
        "soilscan_desc": "मिट्टी की तस्वीरें अपलोड करें और तुरंत एआई आधारित गुणवत्ता विश्लेषण प्राप्त करें।",
        "launch_btn": "शुरू करें"
    }
}

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
        lang = get_lang()
        texts = translations[lang]
        return render_template('KrishiUdaanResult.html', plan=plan, texts=texts, lang=lang)

    except ValueError as ve:
        flash(str(ve))
        return redirect('/krishiudaan')

# ----------------- AmritJeevan -----------------
@app.route('/amritjeevan/desc')
def amritjeevan_desc():
    lang = get_lang()
    texts = translations[lang]
    return render_template('AmritJeevan.html', texts=texts, lang=lang)

@app.route('/amritjeevan')
def amritjeevan():
    lang = get_lang()
    texts = translations[lang]
    return render_template('AmritJeevanF.html', texts=texts, lang=lang)

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

    soil_params, plot_path, pdf_path, recommendation, message = analyze_soil(image_path=file_path)
    lang = get_lang()
    texts = translations[lang]
    return render_template(
        'SoilScanResult.html',
        soil_params=soil_params,
        plot_path=plot_path,
        pdf_path=pdf_path,
        recommendation=recommendation,
        message=message,
        texts=texts,
        lang=lang
    )

# ----------------- BharatBot -----------------
@app.route('/bharatbot/desc')
def bharatbot_desc():
    lang = get_lang()
    texts = translations[lang]
    return render_template('BharatBot.html', texts=texts, lang=lang)

# ----------------- Run App -----------------
if __name__ == '__main__':
    app.run(debug=True)
