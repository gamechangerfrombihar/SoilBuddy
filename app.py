from flask import Flask, render_template, request, redirect, flash, url_for, session
from werkzeug.utils import secure_filename
import os

from utils.krishi_logic import generate_plan
from utils.soilscan_logic import analyze_soil

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
        "amrit_vision_desc": "To revolutionize Indian agriculture by enabling smart, data-driven water management—ensuring every drop counts and every farm thrives sustainably with balanced irrigation and higher productivity.",

        # KrishiUdaan page
        "krishi_welcome_title": "KrishiUdaan",
        "krishi_what_title": "What is KrishiUdaan?",
        "krishi_what_desc1": "KrishiUdaan is an advanced AI-powered crop recommendation and farm management system designed to help farmers maximize productivity, profitability, and sustainability. It analyzes multiple farm-specific factors—such as region, area, capital, irrigation system, soil type, climate, and number of crops a farmer intends to grow—to provide precise recommendations on which crops to cultivate and which modern techniques to use for optimum yield.",
        "krishi_what_desc2": "Techniques like multicropping and crop rotation ensure efficient land use and soil health while boosting profitability.",
        "krishi_who_title": "Who is it for?",
        "krishi_who_list": [
            "Small and medium-scale farmers seeking to optimize resources.",
            "Agricultural planners and consultants who advise farmers.",
            "Government agricultural departments aiming to improve regional crop planning.",
            "Agri-tech startups and investors analyzing crop viability in different regions.",
            "Anyone involved in crop cultivation who wants data-driven insights for informed decisions."
        ],
        "krishi_where_title": "Where can it be applied?",
        "krishi_where_list": [
            "Diverse regions with varying climate zones and soil types.",
            "Urban and rural farms, from small kitchen gardens to large agricultural fields.",
            "Areas with irrigation constraints or where capital investment optimization is crucial."
        ],
        "krishi_why_title": "Why use KrishiUdaan?",
        "krishi_why_list": [
            "Maximize Profits: Suggests suitable crops and techniques for higher yield per acre.",
            "Data-Driven Decisions: Eliminates guesswork, adapting to regional conditions and climate patterns.",
            "Sustainable Farming: Promotes crop rotation and multicropping for long-term soil health.",
            "Resource Optimization: Recommends crops based on capital, irrigation, and labor availability.",
            "Comprehensive Planning: End-to-end guidance for sowing, harvesting, and crop cycles.",
            "Scalable & Customizable: Adapts recommendations for 1 or multiple crops."
        ],
        "krishi_features_title": "Key Features",
        "krishi_features_list": [
            "Multi-factor Analysis: region, area, soil, climate, water, and financial resources considered.",
            "Crop Suitability Index: recommends crops with max profit potential and minimal risk.",
            "Technique Suggestions: guides on multicropping, crop rotation, intercropping, and organic methods.",
            "Profit Estimator: predicts potential revenue and ROI.",
            "Seasonal Planning: sowing-to-harvest calendar tailored to local conditions.",
            "Visualization & Reports: easy-to-read charts for farmers and planners.",
            "Decision Support System: helps with capital allocation, irrigation planning, and land management."
        ],
        "krishi_innovation_title": "Innovation & USP",
        "krishi_innovation_desc": "KrishiUdaan is more than a crop suggestion tool—it’s a holistic farm advisor. Its AI-driven recommendations combine agronomy, climate science, and economics to provide actionable insights, personalized for each farmer’s conditions.",
        "krishi_impact_title": "Impact",
        "krishi_impact_list": [
            "Improves farmer income and reduces losses.",
            "Promotes eco-friendly and sustainable farming practices.",
            "Supports planning and policy-making for governments and NGOs.",
            "Ensures food security and resource-efficient agriculture."
        ],
        "krishi_vision_title": "Vision",
        "krishi_vision_desc": "To empower farmers with knowledge, technology, and actionable insights, enabling every farm to achieve maximum growth, sustainability, and profit."
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
        "amrit_vision_desc": "भारतीय कृषि को स्मार्ट, डेटा-आधारित जल प्रबंधन सक्षम करके क्रांतिकारी बदलाव लाना—सुनिश्चित करना कि हर बूँद मायने रखे और हर खेत संतुलित सिंचाई और उच्च उत्पादन के साथ स्थायी रूप से फल-फूल सके।",

        # KrishiUdaan page
        "krishi_welcome_title": "कृषिउड़ान",
        "krishi_what_title": "कृषिउड़ान क्या है?",
        "krishi_what_desc1": "कृषिउड़ान एक उन्नत एआई-आधारित फसल सिफारिश और फार्म प्रबंधन प्रणाली है जो किसानों को अधिकतम उत्पादकता, लाभप्रदता और स्थिरता प्राप्त करने में मदद करती है। यह क्षेत्र, क्षेत्रफल, पूंजी, सिंचाई प्रणाली, मिट्टी का प्रकार, जलवायु और उगाई जाने वाली फसलों की संख्या जैसे कई फॉर्म-विशिष्ट कारकों का विश्लेषण करती है और सही फसल और आधुनिक तकनीकें सुझाती है।",
        "krishi_what_desc2": "मल्टीक्रॉपिंग और फसल चक्रीय तकनीकें जमीन का कुशल उपयोग सुनिश्चित करती हैं और लाभप्रदता बढ़ाती हैं।",
        "krishi_who_title": "यह किसके लिए है?",
        "krishi_who_list": [
            "छोटे और मध्यम स्तर के किसान जो संसाधनों का अनुकूलन करना चाहते हैं।",
            "कृषि योजनाकार और सलाहकार जो किसानों को मार्गदर्शन देते हैं।",
            "सरकारी कृषि विभाग जो क्षेत्रीय फसल योजना सुधारना चाहते हैं।",
            "एग्री-टेक स्टार्टअप और निवेशक जो विभिन्न क्षेत्रों में फसल क्षमता का विश्लेषण करते हैं।",
            "फसल उगाने में शामिल कोई भी व्यक्ति जो डेटा-आधारित निर्णय लेना चाहता है।"
        ],
        "krishi_where_title": "यह कहाँ लागू हो सकता है?",
        "krishi_where_list": [
            "विभिन्न जलवायु क्षेत्रों और मिट्टी के प्रकार वाले क्षेत्र।",
            "शहरी और ग्रामीण खेत, छोटे किचन गार्डन से लेकर बड़े कृषि क्षेत्र तक।",
            "सिंचाई सीमित या पूंजी निवेश अनुकूलन आवश्यक क्षेत्र।"
        ],
        "krishi_why_title": "क्यों उपयोग करें?",
        "krishi_why_list": [
            "लाभ अधिकतम करें: उच्च उत्पादन और लाभ के लिए उपयुक्त फसल और तकनीक सुझाता है।",
            "डेटा-आधारित निर्णय: क्षेत्रीय परिस्थितियों और मौसम पैटर्न के अनुसार अनुमान समाप्त करता है।",
            "सतत खेती: फसल चक्रीय और मल्टीक्रॉपिंग को बढ़ावा देता है।",
            "संसाधन अनुकूलन: पूंजी, सिंचाई और श्रम उपलब्धता के आधार पर फसल सुझाता है।",
            "समग्र योजना: बुवाई, कटाई और फसल चक्र के लिए पूर्ण मार्गदर्शन।",
            "स्केलेबल और अनुकूलनीय: एक या अधिक फसलों के लिए सुझाव देता है।"
        ],
        "krishi_features_title": "मुख्य विशेषताएँ",
        "krishi_features_list": [
            "बहु-कारक विश्लेषण: क्षेत्र, क्षेत्रफल, मिट्टी, जलवायु, पानी और वित्तीय संसाधन विचारित।",
            "फसल उपयुक्तता सूचकांक: अधिकतम लाभ और न्यूनतम जोखिम वाली फसल की सिफारिश।",
            "तकनीक सुझाव: मल्टीक्रॉपिंग, फसल चक्र, इंटरक्रॉपिंग और ऑर्गेनिक विधियों पर मार्गदर्शन।",
            "लाभ अनुमानक: संभावित राजस्व और ROI का पूर्वानुमान।",
            "मौसमी योजना: स्थानीय परिस्थितियों के अनुसार बुवाई-से-कटाई कैलेंडर।",
            "दृश्य और रिपोर्ट: किसानों और योजनाकारों के लिए आसान चार्ट।",
            "निर्णय समर्थन प्रणाली: पूंजी आवंटन, सिंचाई योजना और भूमि प्रबंधन में मदद।"
        ],
        "krishi_innovation_title": "नवाचार और यूएसपी",
        "krishi_innovation_desc": "कृषिउड़ान सिर्फ फसल सिफारिश उपकरण नहीं है—यह एक संपूर्ण फार्म सलाहकार है। इसकी एआई-आधारित सिफारिशें कृषि विज्ञान, जलवायु विज्ञान और अर्थशास्त्र को जोड़ती हैं।",
        "krishi_impact_title": "प्रभाव",
        "krishi_impact_list": [
            "किसानों की आय बढ़ाता है और नुकसान कम करता है।",
            "पर्यावरण-मित्र और स्थायी खेती को बढ़ावा देता है।",
            "सरकार और एनजीओ के लिए योजना और नीति निर्माण का समर्थन करता है।",
            "खाद्य सुरक्षा और संसाधन-कुशल कृषि सुनिश्चित करता है।"
        ],
        "krishi_vision_title": "दृष्टि",
        "krishi_vision_desc": "किसानों को ज्ञान, तकनीक और कार्रवाई योग्य इनसाइट प्रदान करना, जिससे प्रत्येक खेत अधिकतम वृद्धि, स्थिरता और लाभ प्राप्त करे।"
    }
}

# BharatBot
"en": {
    "bharatbot_title": "BharatBot",
    "bharatbot_desc": "BharatBot is an intelligent AI chatbot integrated into SoilBuddy. It acts as a smart digital assistant for farmers, helping them get quick answers to their queries related to crops, soil health, irrigation, and fertilizers — anytime, anywhere.",
    "bharatbot_features_title": "Key Features:",
    "bharatbot_features": [
        "Provides instant AI-based guidance in local languages.",
        "Connects farmers directly with the right knowledge, without waiting for human assistance.",
        "Available 24/7 within the SoilBuddy ecosystem."
    ],
    "bharatbot_impact_title": "Impact:",
    "bharatbot_impact": "BharatBot bridges the gap between modern AI and traditional agriculture. By making expert knowledge easily accessible, it empowers farmers to make informed decisions and improve productivity sustainably.",
    "bharatbot_launch_link": "https://bharatbot-2a7793.zapier.app/"
},
"hi": {
    ...
    "bharatbot_title": "भारतबोट",
    "bharatbot_desc": "भारतबोट SoilBuddy में एक बुद्धिमान एआई चैटबोट है। यह किसानों के लिए एक स्मार्ट डिजिटल सहायक के रूप में कार्य करता है, जो उन्हें फसल, मिट्टी की गुणवत्ता, सिंचाई और उर्वरक से संबंधित प्रश्नों के तुरंत उत्तर प्राप्त करने में मदद करता है।",
    "bharatbot_features_title": "मुख्य विशेषताएँ:",
    "bharatbot_features": [
        "स्थानीय भाषाओं में त्वरित एआई-आधारित मार्गदर्शन प्रदान करता है।",
        "किसानों को सही ज्ञान तक सीधे जोड़ता है, बिना मानव सहायता के इंतजार किए।",
        "SoilBuddy पारिस्थितिकी तंत्र में 24/7 उपलब्ध।"
    ],
    "bharatbot_impact_title": "प्रभाव:",
    "bharatbot_impact": "भारतबोट आधुनिक एआई और पारंपरिक कृषि के बीच की खाई को पाटता है। विशेषज्ञ ज्ञान को आसानी से सुलभ बनाकर, यह किसानों को सूचित निर्णय लेने और उत्पादकता में सुधार करने में सक्षम बनाता है।",
    "bharatbot_launch_link": "https://bharatbot-2a7793.zapier.app/"
}

# SoilScan

"en": {
    ...
    "soilscan_title": "SoilScan",
    "soilscan_desc": "SoilScan is an advanced AI-powered feature within SoilBuddy designed to revolutionize how farmers understand their soil. By simply capturing and sending a clear photo of their soil, farmers can access an in-depth analysis powered by machine learning and computer vision technology. The feature identifies key physical and visual properties of the soil and provides precise insights into its nutrient profile and overall health.",
    "soilscan_features_title": "Key Features:",
    "soilscan_features": [
        "Allows farmers to upload high-resolution soil photos for instant analysis.",
        "AI model evaluates soil color, granularity, texture, and moisture patterns.",
        "Generates comprehensive digital reports including NPK levels, pH, and organic matter content.",
        "Detects nutrient deficiencies and potential disease symptoms in soil composition.",
        "Provides recommendations for fertilizers, crop rotation, and organic enrichment methods."
    ],
    "soilscan_impact_title": "Impact:",
    "soilscan_impact": "SoilScan transforms traditional farming practices by giving farmers instant, data-driven insights about their land. It eliminates expensive lab testing, reduces turnaround time, and helps farmers make informed choices about fertilizer usage, irrigation schedules, and crop selection. This encourages sustainable farming practices and prevents soil depletion."
},
"hi": {
    ...
    "soilscan_title": "सोइलस्कैन",
    "soilscan_desc": "सोइलस्कैन SoilBuddy में एक उन्नत एआई-आधारित फीचर है, जो किसानों को उनकी मिट्टी की समझ को क्रांतिकारी बनाने में मदद करता है। केवल मिट्टी की स्पष्ट फोटो भेजकर, किसान मशीन लर्निंग और कंप्यूटर विज़न तकनीक से गहन विश्लेषण प्राप्त कर सकते हैं। यह फीचर मिट्टी की मुख्य भौतिक और दृश्य विशेषताओं की पहचान करता है और पोषक तत्व प्रोफ़ाइल और कुल स्वास्थ्य में सटीक जानकारी प्रदान करता है।",
    "soilscan_features_title": "मुख्य विशेषताएँ:",
    "soilscan_features": [
        "किसानों को तुरंत विश्लेषण के लिए उच्च-रिज़ॉल्यूशन मिट्टी की तस्वीरें अपलोड करने की अनुमति देता है।",
        "एआई मॉडल मिट्टी के रंग, दानेपन, बनावट और नमी पैटर्न का मूल्यांकन करता है।",
        "एनपीके स्तर, पीएच, और कार्बनिक पदार्थ की सामग्री सहित व्यापक डिजिटल रिपोर्ट तैयार करता है।",
        "मिट्टी की संरचना में पोषक तत्वों की कमी और संभावित रोग लक्षण का पता लगाता है।",
        "उर्वरक, फसल चक्र, और जैविक संवर्धन विधियों के लिए सिफारिशें प्रदान करता है।"
    ],
    "soilscan_impact_title": "प्रभाव:",
    "soilscan_impact": "सोइलस्कैन पारंपरिक खेती के तरीकों को बदल देता है, किसानों को उनकी भूमि के बारे में तुरंत, डेटा-आधारित जानकारी देता है। यह महंगे लैब परीक्षण को समाप्त करता है, समय बचाता है और किसानों को उर्वरक उपयोग, सिंचाई कार्यक्रम और फसल चयन के बारे में सूचित निर्णय लेने में मदद करता है। इससे टिकाऊ खेती को बढ़ावा मिलता है और मिट्टी के अपक्षय को रोका जाता है।"
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
    return render_template('KrishiUdaanF.html', texts=translations[lang], lang=lang)

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
