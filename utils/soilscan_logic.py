# utils/soilscan_logic.py
import numpy as np
from tensorflow.keras.preprocessing import image

# Example soil classes
CLASS_NAMES = ['Alluvial Soil', 'Black Soil', 'Clay Soil', 'Red Soil']

# Recommendations for each soil type
RECOMMENDATIONS = {
    'Alluvial Soil': "Rich in minerals — good for wheat, rice, sugarcane.",
    'Black Soil': "High moisture retention — ideal for cotton, soybean.",
    'Clay Soil': "Heavy and wet — suited for paddy and water-loving crops.",
    'Red Soil': "Low fertility — best for pulses, millet, and groundnut."
}

def analyze_soil(image_path, model):
    """
    Takes an uploaded soil image and the loaded model,
    returns:
    - soil_params (dict): optional details like type, confidence
    - plot_path: optional path if you generate plots
    - pdf_path: optional path if you generate PDF reports
    - recommendation: a simple recommendation string
    - message: optional message string
    """

    # Load and preprocess the image
    img = image.load_img(image_path, target_size=(224, 224))
    img_array = image.img_to_array(img) / 255.0
    img_array = np.expand_dims(img_array, axis=0)

    # Predict soil type
    preds = model.predict(img_array)
    idx = np.argmax(preds[0])
    soil_type = CLASS_NAMES[idx]
    confidence = float(np.max(preds[0])) * 100

    # Recommendation
    recommendation = RECOMMENDATIONS.get(soil_type, "Suitable for multiple crops.")

    # Optional: soil_params dictionary
    soil_params = {
        "type": soil_type,
        "confidence": round(confidence, 2)
    }

    # Optional placeholders (you can generate plots/PDF later)
    plot_path = None
    pdf_path = None
    message = f"Predicted soil type: {soil_type} ({round(confidence, 2)}% confidence)"

    return soil_params, plot_path, pdf_path, recommendation, message
