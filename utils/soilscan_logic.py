import os
import requests
import numpy as np
from PIL import Image
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

# --- Plot NASA Data ---
def plot_nasa_data(nasa_data):
    daily_data = nasa_data.get('properties', {}).get('parameter', {})
    if not daily_data:
        return None

    dates = list(daily_data[list(daily_data.keys())[0]].keys())
    fig, axs = plt.subplots(len(daily_data), 1, figsize=(10, 4*len(daily_data)))
    if len(daily_data) == 1:
        axs = [axs]

    for i, param in enumerate(daily_data):
        values = [daily_data[param][d] for d in dates]
        axs[i].plot(dates, values, marker='o')
        axs[i].set_title(param)
        axs[i].set_xticks(range(0, len(dates), max(1, len(dates)//10)))
        axs[i].set_xticklabels(dates[::max(1, len(dates)//10)], rotation=45)
        axs[i].set_ylabel(param)
        axs[i].grid(True)

    plt.tight_layout()
    os.makedirs("static", exist_ok=True)
    plot_path = os.path.join("static", "nasa_data_plot.png")
    plt.savefig(plot_path)
    plt.close()
    return plot_path

# --- Main analysis ---
def analyze_soil(image_path, lat=None, lon=None, start_date=None, end_date=None):
    soil_params = approximate_soil_from_image(image_path)
    nasa_data = None
    plot_path = None
    if all([lat, lon, start_date, end_date]):
        nasa_data = fetch_nasa_power_data(lat, lon, start_date, end_date)
        if nasa_data:
            plot_path = plot_nasa_data(nasa_data)
    return soil_params, plot_path
