from flask import Flask, render_template, request, redirect, flash
from utils.krishi_logic import generate_plan

app = Flask(__name__)
app.secret_key = 'some_secret_key'

@app.route('/')
def home():
    return render_template('HomePage.html')

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

if __name__ == '__main__':
    app.run(debug=True)


# SoilScan input page
@app.route('/soilscan')
def soilscan():
    return render_template('soilscanF.html')  # Make sure filename matches

# SoilScan result page
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




    f
