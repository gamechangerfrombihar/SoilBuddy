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
        # Homepage
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
        "launch_btn": "Launch",

        # AmritJeevan page
        "amrit_welcome_title": "AmritJeevan",
        "amrit_what_title": "What is AmritJeevan?",
        "amrit_what_desc1": "AmritJeevan is an advanced irrigation and water management system designed to help farmers achieve maximum water efficiency, crop health, and sustainability. It gathers essential farm-specific inputs such as location, total field area, soil type, crop variety, and climate data directly from farmers. Based on this data, AmritJeevan calculates the exact daily water requirement for each field, ensuring precise irrigation with minimal wastage.",
        "amrit_what_desc2": "The system promotes smart water use by integrating rainfall prediction, soil moisture sensing, and crop water demand analytics—making irrigation both sustainable and cost-effective.",

        "amrit_who_title": "Who is it for?",
        "amrit_who_list": [
            "Farmers aiming to optimize water use and reduce irrigation costs.",
            "Agricultural planners and consultants developing efficient irrigation models.",
            "Government and NGOs working on water conservation initiatives.",
            "Researchers studying crop-water relationships and soil hydration levels.",
            "Agri-tech startups building sustainable smart farming systems."
        ],

        "amrit_where_title": "Where can it be applied?",
        "amrit_where_list": [
            "Regions facing irregular rainfall or limited water resources.",
            "Areas where over-irrigation leads to soil erosion or nutrient loss.",
            "Farms using traditional irrigation systems seeking modernization.",
            "Smart farming setups using IoT-based sensors and water automation tools."
        ],

        "amrit_why_title": "Why use AmritJeevan?",
        "amrit_why_list": [
            "Water Conservation: Prevents water wastage by calculating exact crop-wise needs.",
            "Cost Efficiency: Reduces unnecessary irrigation expenses.",
            "Climate Adaptation: Adjusts recommendations as per seasonal and regional variations.",
            "Healthy Crops: Maintains ideal moisture levels for maximum yield.",
            "Automation Ready: Can integrate with IoT irrigation systems for auto-scheduling.",
            "Data-Driven: Replaces guesswork with accurate analytics and smart insights."
        ],

        "amrit_features_title": "Key Features",
        "amrit_features_list": [
            "Real-time water need estimation using farm data and weather info.",
            "Soil moisture-based irrigation recommendation engine.",
            "Integration with rainfall prediction APIs for automatic adjustments.",
            "Custom alerts for under or over-irrigation detection.",
            "Water usage dashboard showing daily, weekly, and monthly statistics.",
            "Region-wise comparison for better water resource planning.",
            "Smart irrigation planning compatible with all crop types."
        ],

        "amrit_innovation_title": "Innovation & USP",
        "amrit_innovation_desc": "AmritJeevan combines meteorological data and soil science to deliver intelligent irrigation insights. Its precision-based approach reduces water wastage up to 40% and boosts yield through efficient hydration cycles. The system’s USP lies in its ability to continuously learn from field data and refine future irrigation schedules automatically.",

        "amrit_impact_title": "Impact",
        "amrit_impact_list": [
            "Reduces irrigation water use by up to 30–40%.",
            "Improves overall soil fertility and crop consistency.",
            "Minimizes manual effort and dependency on weather guesswork.",
            "Empowers farmers with accurate, actionable water insights.",
            "Promotes long-term sustainable water resource management."
        ],

        "amrit_vision_title": "Vision",
        "amrit_vision_desc": "To revolutionize Indian agriculture by enabling smart, data-driven water management—ensuring every drop counts and every farm thrives sustainably with balanced irrigation and higher productivity."
    },
    "hi": {
        # Homepage
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
        "launch_btn": "शुरू करें",

        # AmritJeevan page
        "amrit_welcome_title": "अमृतजीवन",
        "amrit_what_title": "अमृतजीवन क्या है?",
        "amrit_what_desc1": "अमृतजीवन एक उन्नत सिंचाई और जल प्रबंधन प्रणाली है जो किसानों को अधिकतम जल दक्षता, फसल स्वास्थ्य और स्थिरता प्राप्त करने में मदद करती है। यह किसानों से स्थान, कुल क्षेत्रफल, मिट्टी का प्रकार, फसल की किस्म और जलवायु डेटा जैसे आवश्यक इनपुट सीधे प्राप्त करती है। इसके आधार पर अमृतजीवन प्रत्येक खेत के लिए सटीक दैनिक जल आवश्यकता की गणना करता है, जिससे न्यूनतम अपव्यय के साथ सटीक सिंचाई सुनिश्चित होती है।",
        "amrit_what_desc2": "यह प्रणाली स्मार्ट जल उपयोग को बढ़ावा देती है, जिसमें वर्षा पूर्वानुमान, मिट्टी की नमी सेंसर और फसल की जल आवश्यकता विश्लेषण को एकीकृत किया गया है—जिससे सिंचाई स्थायी और लागत-कुशल बनती है।",

        "amrit_who_title": "यह किसके लिए है?",
        "amrit_who_list": [
            "किसान जो जल उपयोग को अनुकूलित करना और सिंचाई लागत कम करना चाहते हैं।",
            "कृषि योजनाकार और सलाहकार जो कुशल सिंचाई मॉडल विकसित कर रहे हैं।",
            "सरकार और एनजीओ जो जल संरक्षण पहलों पर काम कर रहे हैं।",
            "शोधकर्ता जो फसल-जल संबंध और मिट्टी की नमी स्तर का अध्ययन कर रहे हैं।",
            "एग्री-टेक स्टार्टअप जो टिकाऊ स्मार्ट खेती प्रणाली बना रहे हैं।"
        ],

        "amrit_where_title": "यह कहाँ लागू हो सकता है?",
        "amrit_where_list": [
            "ऐसी क्षेत्र जहाँ वर्षा अनियमित या जल स्रोत सीमित हैं।",
            "ऐसी क्षेत्र जहाँ अधिक सिंचाई से मिट्टी का कटाव या पोषक तत्वों की हानि होती है।",
            "पारंपरिक सिंचाई प्रणाली वाले खेत जो आधुनिकीकरण चाहते हैं।",
            "स्मार्ट खेती सेटअप जो आईओटी आधारित सेंसर और जल स्वचालन उपकरण का उपयोग करते हैं।"
        ],

        "amrit_why_title": "अमृतजीवन क्यों इस्तेमाल करें?",
        "amrit_why_list": [
            "जल संरक्षण: सटीक फसल-वार आवश्यकता की गणना करके जल अपव्यय रोकता है।",
            "लागत दक्षता: अनावश्यक सिंचाई खर्च को कम करता है।",
            "जलवायु अनुकूलन: मौसमी और क्षेत्रीय भिन्नताओं के अनुसार सिफारिशों को समायोजित करता है।",
            "स्वस्थ फसल: अधिकतम उपज के लिए आदर्श नमी स्तर बनाए रखता है।",
            "स्वचालन के लिए तैयार: ऑटो-शेड्यूलिंग के लिए आईओटी सिंचाई सिस्टम के साथ एकीकृत हो सकता है।",
            "डेटा-प्रेरित: सटीक विश्लेषण और स्मार्ट इनसाइट के साथ अनुमान को बदलता है।"
        ],

        "amrit_features_title": "मुख्य विशेषताएँ",
        "amrit_features_list": [
            "खेत डेटा और मौसम जानकारी का उपयोग करके वास्तविक समय में जल आवश्यकता का अनुमान।",
            "मिट्टी की नमी आधारित सिंचाई सिफारिश इंजन।",
            "स्वचालित समायोजन के लिए वर्षा पूर्वानुमान API के साथ एकीकरण।",
            "अल्प या अधिक सिंचाई का पता लगाने के लिए कस्टम अलर्ट।",
            "दैनिक, साप्ताहिक और मासिक आँकड़े दिखाने वाला जल उपयोग डैशबोर्ड।",
            "बेहतर जल संसाधन योजना के लिए क्षेत्रवार तुलना।",
            "सभी फसल प्रकारों के लिए संगत स्मार्ट सिंचाई योजना।"
        ],

        "amrit_innovation_title": "नवाचार और यूएसपी",
        "amrit_innovation_desc": "अमृतजीवन मौसमीय डेटा और मिट्टी विज्ञान को जोड़कर बुद्धिमान सिंचाई इनसाइट प्रदान करता है। इसकी सटीकता आधारित विधि 40% तक जल अपव्यय कम करती है और कुशल हाइड्रेशन चक्र के माध्यम से उपज बढ़ाती है। प्रणाली की यूएसपी इसकी क्षमता में निहित है कि यह लगातार क्षेत्र डेटा से सीखती है और भविष्य की सिंचाई अनुसूचियों को स्वचालित रूप से सुधारती है।",

        "amrit_impact_title": "प्रभाव",
        "amrit_impact_list": [
            "सिंचाई जल उपयोग को 30–40% तक कम करता है।",
            "कुल मिट्टी की उर्वरता और फसल स्थिरता में सुधार करता है।",
            "मैनुअल प्रयास और मौसम अनुमान पर निर्भरता को कम करता है।",
            "किसानों को सटीक, कार्रवाई योग्य जल इनसाइट प्रदान करता है।",
            "दीर्घकालिक स्थायी जल संसाधन प्रबंधन को बढ़ावा देता है।"
        ],

        "amrit_vision_title": "दृष्टि",
        "amrit_vision_desc": "भारतीय कृषि को स्मार्ट, डेटा-आधारित जल प्रबंधन सक्षम करके क्रांतिकारी बदलाव लाना—सुनिश्चित करना कि हर बूँद मायने रखे और हर खेत संतुलित सिंचाई और उच्च उत्पादन के साथ स्थायी रूप से फल-फूल सके।"
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
