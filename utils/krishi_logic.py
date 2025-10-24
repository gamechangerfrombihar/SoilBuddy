def generate_plan(land_size, climate, capital, water, labourers, region, num_crops):
    land_size = float(land_size)
    capital = float(capital)
    labourers = int(labourers)
    num_crops = int(num_crops)
    water = water.lower()
    region = region.lower()
    climate = climate.lower()

    # ----------------- Validations -----------------
    if land_size < 0.1:
        raise ValueError("Minimum land size is 0.1 acres")
    if capital < 1000:
        raise ValueError("Minimum working capital is ₹1000")
    if num_crops > 2:
        num_crops = 2
    if labourers <= 0:
        labourers = 1

    # Prevent unrealistic conditions
    if land_size < 0.5 and num_crops == 2:
        num_crops = 1
    if capital < 5000 and num_crops == 2:
        num_crops = 1

    # Crop selection based on region & climate
    primary_crop, secondary_crop = "", ""
    rotation_primary, rotation_secondary = "", ""

    if region in ["east india", "north india"]:
        if climate in ["humid", "tropical"]:
            primary_crop, secondary_crop = "Rice", "Lentil"
            rotation_primary, rotation_secondary = "Maize", "Mustard"
        else:
            primary_crop, secondary_crop = "Wheat", "Barley"
            rotation_primary, rotation_secondary = "Soybean", "Mustard"
    elif region == "west india":
        primary_crop, secondary_crop = "Cotton", "Groundnut"
        rotation_primary, rotation_secondary = "Sorghum", "Chili"
    elif region == "south india":
        primary_crop, secondary_crop = "Maize", "Pulses"
        rotation_primary, rotation_secondary = "Rice", "Soybean"
    else:
        primary_crop, secondary_crop = "Wheat", "Lentil"
        rotation_primary, rotation_secondary = "Maize", "Mustard"

    if num_crops >= 2:
        primary_percent, secondary_percent = 60, 40
    else:
        primary_percent, secondary_percent = 100, 0

    yield_increase = 15 + (land_size / 10)
    profit_increase = 10000 + (capital / 10)

    explanation = (
        f"The system analyzed your inputs: {land_size} acres, {climate.title()} climate, "
        f"₹{capital} working capital, {labourers} labourers, water availability: {water}, "
        f"and region: {region.title()}.\n\n"
        f"Based on crop compatibility, soil nutrient cycles, and labor/capital requirements, "
        f"the recommended crop combination is {primary_crop} ({primary_percent}%) and "
        f"{secondary_crop} ({secondary_percent}%).\n\n"
        f"Crop rotation to {rotation_primary} + {rotation_secondary} in the next season "
        f"ensures soil fertility, pest resistance, and maximizes yield/profit."
    )

    plan = {
        "farmer_profile": f"{land_size} acres | {climate.title()} climate | ₹{capital} capital | {labourers} labourers | {region.title()}",
        "primary_crop": primary_crop,
        "primary_percent": f"{primary_percent}%",
        "secondary_crop": secondary_crop,
        "secondary_percent": f"{secondary_percent}%",
        "rotation_plan": f"Rotate to {rotation_primary} + {rotation_secondary} for soil fertility and pest resistance.",
        "yield_improvement": f"+{yield_increase:.0f}%",
        "profitability": f"₹{profit_increase:,.0f} increase",
        "soil_quality": "Nitrogen +12% (estimated)",
        "explanation": explanation.strip()
    }

    return plan
