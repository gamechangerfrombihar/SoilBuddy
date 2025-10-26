import os
import numpy as np
from PIL import Image

# --- Soil analysis from image ---
def approximate_soil_from_image(image_path):
    try:
        img = Image.open(image_path).convert('RGB')
        img = img.resize((100, 100))
        arr = np.array(img)
        mean_color = arr.mean(axis=(0, 1))
        clay = round(mean_color[0]/255 * 40 + 10, 1)
        silt = round(mean_color[1]/255 * 40 + 20, 1)
        sand = round(mean_color[2]/255 * 50 + 20, 1)
        return {'Clay': clay, 'Silt': silt, 'Sand': sand}
    except Exception as e:
        print("Error reading image:", e)
        return {'Clay': 30, 'Silt': 40, 'Sand': 30}

# --- Main analysis ---
def analyze_soil(image_path):
    """
    Analyze soil from image only.
    NASA POWER data is completely removed.
    """
    soil_params = approximate_soil_from_image(image_path)
    
    # --- Recommended crops logic ---
    crops = []
    clay_high = soil_params['Clay'] > 40
    silt_high = soil_params['Silt'] > 40
    sand_high = soil_params['Sand'] > 40

    if clay_high and not (silt_high or sand_high):
        crops = ['Broccoli', 'Cabbage', 'Rice']
    elif silt_high and not (clay_high or sand_high):
        crops = ['Pea', 'Wheat', 'Potato']
    elif sand_high and not (clay_high or silt_high):
        crops = ['Jowar', 'Bajra', 'Maize']
    elif clay_high and silt_high:
        crops = ['Rice', 'Potato', 'Wheat']
    elif silt_high and sand_high:
        crops = ['Potato', 'Jowar', 'Bajra']
    elif clay_high and sand_high:
        crops = ['Jowar', 'Bajra', 'Wheat']
    else:
        crops = ['Pea', 'Wheat', 'Potato', 'Broccoli', 'Cabbage', 'Rice', 'Jowar', 'Bajra', 'Maize']  # fallback mix

    return soil_params, crops  # return crops along with soil params
