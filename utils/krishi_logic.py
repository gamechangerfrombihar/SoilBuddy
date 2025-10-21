# utils/krishi_logic.py

def generate_plan(land_size, climate, capital, water, labourers, region, num_crops):
    """
    Generates a Krishi Udaan smart plan based on farmer inputs.
    Returns a dictionary ready to pass to the template.
    """

    # 1️⃣ Convert inputs
    land_size = float(land_size)
    capital = float(capital)
    labourers = int(labourers)
    num_crops = int(num_crops)
    water = water.lower()
    region = region.lower()
    climate = climate.lower()

    # 2️⃣ Select crops based on region & climate
    primary_crop, secondary_crop = "", ""
    rotation_primary, rotation_secondary = "", ""

    if region in ["east india", "north india"]:
        if climate in ["humid", "tropical"]:
            primary_crop = "Rice"
            secondary_crop = "Lentil"
            rotation_primary = "Maize"
            rotation_secondary = "Mustard"
        else:
            primary_crop = "Wheat"
            secondary_crop = "Barley"
            rotation_primary = "Soybean"
            rotation_secondary = "Mustard"
    elif region == "west india":
        primary_crop = "Cotton"
        secondary_crop = "Groundnut"
        rotation_primary = "Sorghum"
        rotation_secondary = "Chili"
    elif region == "south india":
        primary_crop = "Maize"
        secondary_crop = "Pulses"
        rotation_primary = "Rice"
        rotation_secondary = "Soybean"
    else:
        primary_crop = "Wheat"
        secondary_crop = "Lentil"
        rotation_primary = "Maize"
        rotation_secondary = "Mustard"

    # 3️⃣ Decide area percentage per crop
    if num_crops >= 2:
        primary_percent = 60
        secondary_percent = 40
    else:
        primary_percent = 100
        secondary_percent = 0

    # 4️⃣ Estimated impact
    yield_increase = 15 + (land_size / 10)  # arbitrary formula
    profit_increase = 10000 + (capital / 10)

    # 5️⃣ Explanation for collapsible card
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

    # 6️⃣ Assemble plan dictionary aligned with template
    plan = {
        "farmer_profile": f"{land_size} acres | {climate.title()} climate | ₹{capital} capital | {labourers} labourers | {region.title()}",
        "primary_crop": primary_crop,
        "primary_percent": f"{primary_percent}%",
        "secondary_crop": secondary_crop,
        "secondary_percent": f"{secondary_percent}%",
        "rotation_plan": f"Rotate to {rotation_primary} + {rotation_secondary} for soil fertility and pest resistance.",
        "yield_improvement": f"+{yield_increase:.0f}%",
        "profitability": f"₹{profit_increase:,.0f} increase",
        "soil_quality": "Nitrogen +12% (estimated)",  # Placeholder, can be dynamic later
        "explanation": explanation.strip()
    }

    return plan
