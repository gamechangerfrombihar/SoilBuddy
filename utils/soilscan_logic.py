import os
import requests
import numpy as np
from PIL import Image
from fpdf import FPDF
import matplotlib.pyplot as plt

# --- Fetch NASA POWER Data ---
def fetch_nasa_power_data(lat, lon, start_date, end_date, parameters=None):
    if parameters is None:
        parameters = ['T2M_MAX', 'T2M_MIN', 'PRECTOT']
    url = f"https://power.larc.nasa.gov/api/temporal/daily/point?parameters={','.join(parameters)}&community=AG&longitude={lon}&latitude={lat}&start={start_date}&end={end_date}&format=JSON"
    try:
        response = requests.get(url, timeout=10)
        if response.status_code == 200:
            return response.json()
        else:
            print("NASA POWER API Error:", response.status_code)
            return None
    except Exception as e:
        print("NASA POWER API request failed:", e)
        return None

# --- Approximate soil composition from image ---
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
        return {'Clay': 30, 'Silt': 40, 'Sand': 30}  # default

# --- Plot NASA Data ---
def plot_nasa_data(nasa_data):
    daily_data = nasa_data.get('properties', {}).get('parameter', {})
    if not daily_data:
        print("NASA data not available or invalid format.")
        return None

    dates = list(daily_data[list(daily_data.keys())[0]].keys())
    if not dates:
        print("No valid date entries found in NASA data.")
        return None

    fig, axs = plt.subplots(len(daily_data), 1, figsize=(10, 4*len(daily_data)))
    if len(daily_data) == 1:
        axs = [axs]

    for i, param in enumerate(daily_data):
        values = [daily_data[param][d] for d in dates]
        axs[i].plot(dates, values, marker='o')
        axs[i].set_title(param)
        axs[i].set_xticks(dates[::max(1, len(dates)//10)])
        axs[i].set_xticklabels(dates[::max(1, len(dates)//10)], rotation=45)
        axs[i].set_ylabel(param)
        axs[i].grid(True)

    plt.tight_layout()
    os.makedirs("static", exist_ok=True)
    plot_path = os.path.join("static", "nasa_data_plot.png")
    plt.savefig(plot_path)
    plt.close()
    return plot_path

# --- Generate PDF Report ---
def generate_pdf_report(soil_params, nasa_data=None, plot_path=None, output_file="static/Soil_Report.pdf", recommendation=None):
    os.makedirs("static", exist_ok=True)
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", 'B', 16)
    pdf.cell(0, 10, "Soil & NASA POWER Report", ln=True, align='C')

    pdf.ln(10)
    pdf.set_font("Arial", '', 12)
    for key, val in soil_params.items():
        pdf.cell(0, 8, f"{key}: {val}%", ln=True)

    if recommendation:
        pdf.ln(10)
        pdf.set_font("Arial", 'B', 14)
        pdf.cell(0, 10, "Recommendation:", ln=True)
        pdf.set_font("Arial", '', 12)
        pdf.multi_cell(0, 8, recommendation)

    if nasa_data and plot_path:
        pdf.ln(10)
        pdf.set_font("Arial", 'B', 14)
        pdf.cell(0, 10, "NASA POWER Graphs:", ln=True)
        pdf.image(plot_path, x=10, w=190)

    pdf.output(output_file)
    return output_file

# --- Soil Type & Crop Recommendation ---
def get_soil_recommendation(soil_params):
    clay, silt, sand = soil_params['Clay'], soil_params['Silt'], soil_params['Sand']
    soil_type = ""
    if sand > silt and sand > clay:
        soil_type = "Sandy"
        crops = "Jowar, Bajra"
    elif silt > clay and silt > sand:
        soil_type = "Silt"
        crops = "Wheat, Rice, Sugarcane"
    elif clay > sand and clay > silt:
        soil_type = "Clayey"
        crops = "Rice, Cauliflower, Potato"
    else:
        soil_type = "Mixed"
        crops = "Maize, Barley, Pulses"

    recommendation = f"Your soil type: {soil_type}\nRecommended crops: {crops}"
    return recommendation

# --- Main Logic for Flask ---
def analyze_soil(lat=None, lon=None, start_date=None, end_date=None, image_path=None):
    # Step 1: NASA data (optional)
    nasa_data = None
    plot_path = None
    nasa_valid = False

    if lat and lon and start_date and end_date:
        nasa_data = fetch_nasa_power_data(lat, lon, start_date, end_date)
        if nasa_data:
            daily_data = nasa_data.get('properties', {}).get('parameter', {})
            if daily_data:
                nasa_valid = True
                plot_path = plot_nasa_data(nasa_data)

    # Step 2: Soil image (or default)
    soil_params = approximate_soil_from_image(image_path) if image_path else {'Clay': 30, 'Silt': 40, 'Sand': 30}

    # Step 3: Generate recommendation
    recommendation = get_soil_recommendation(soil_params)

    # Step 4: Generate PDF report
    pdf_path = generate_pdf_report(soil_params, nasa_data if nasa_valid else None, plot_path, recommendation=recommendation)

    # Step 5: Handle invalid NASA data or wrong image
    if not nasa_valid:
        message = "⚠️ The NASA data could not be fetched properly or does not match expected format.\nIf your image is not of soil, please try again with a clearer soil image."
    else:
        message = "✅ Analysis complete successfully."

    return soil_params, plot_path, pdf_path, recommendation, message
