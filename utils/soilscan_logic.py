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
    return soil_params, None  # No plot
