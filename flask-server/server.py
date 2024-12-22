from flask import Flask, jsonify
import requests



# Updated Recommended Daily Amounts (RDA) for a 2000 Calorie Diet
rda = {
    "calories_100g": 2000,
    "proteins_100g": 50,
    "fat_100g": 70,
    "sat_fat_100g": 20,
    "insat_fat_100g": 40,
    "carbs_100g": 300,
    "sugars_100g": 25,
    "fibers_100g": 30,
    "cholesterol_100g": 300,
    "iron_100g": 18,
    "calcium_100g": 1000,
    "vitamin_c_100g": 90,
    "vitamin_b9_100g": 400,
    "omega_3_100g": 1.6,
    "omega_6_100g": 17,
    "sodium_100g": 2300,
    "magnesium_100g": 400,
    "vitamin_a_retinol_100g": 900,
    "vitamin_d_100g": 20,
    "vitamin_e_100g": 15,
    "vitamin_k1_100g": 120,
    "zinc_100g": 11,
    "copper_100g": 0.9,
    "manganese_100g": 2.3,
    "selenium_100g": 55,
    "iodine_100g": 150,
    "chromium_100g": 35,
    "molybdenum_100g": 45,
}

url = "https://vision.foodvisor.io/api/1.0/en/analysis/"
headers = {"Authorization": "Api-Key JI7Zs8Gl.k3ATixoz6OeIxvDgtJAhsw1LueTwgS98"}
with open("burger.jpg", "rb") as image:
  response = requests.post(url, headers=headers, files={"image": image})
  response.raise_for_status()
data = response.json()
# print(data)

# Process each item and access the first food possibility
food = data['items'][0]['food'][0]
food_name = food['food_info']['display_name']
food_nut = food['food_info']['nutrition']
# print (food_nut)

# Nutritional data for the food item
nutritional_data = {
    "calories_100g": food_nut.get('calories_100g'),
    "proteins_100g": food_nut.get('proteins_100g'),
    "fat_100g": food_nut.get('fat_100g'),
    "sat_fat_100g": food_nut.get('sat_fat_100g'),
    "insat_fat_100g": food.get('insat_fat_100g'),
    "carbs_100g": food.get('carbs_100g'),
    "sugars_100g": food.get('sugars_100g'),
    "fibers_100g": food.get('fibers_100g'),
    "cholesterol_100g": food.get('cholesterol_100g'),
    "iron_100g": food.get('iron_100g'),
    "calcium_100g": food.get('calcium_100g'),
    "vitamin_c_100g": food.get('vitamin_c_100g'),
    "vitamin_b9_100g": food.get('vitamin_b9_100g'),
    "omega_3_100g": food.get('omega_3_100g'),
    "omega_6_100g": food.get('omega_6_100g'),
    "sodium_100g": food.get('sodium_100g'),
}

# for key, value in nutritional_data.items():
#    print(f"Key: {key}, Value: {value}")


# Normalize and calculate the score using updated RDA values


def calculate_nutritional_score(data, weights, rda):
    score = 0
    recommendations = ""
    for nutrient, weight in weights.items():
        value = data.get(nutrient, None)
        if value == None:
           value = 0
        recommended = rda.get(nutrient, 1)  # Avoid division by zero
        normalized = value / recommended
        score += weight * normalized
    
    if score < 0:
        recommendations += "Your nutritional intake is needs to be improved. Consider having a more balanced diet."
    elif 0 <= score < 1:
        recommendations += "Your diet may need improvement. Focus on increasing beneficial nutrients."
    elif 1 <= score < 2:
        recommendations += "Your diet is balanced, however there's room for improvement."
    elif 2 <= score < 3:
        recommendations += "Good job! You're on the right track with your nutritional choices."
    else:
        recommendations += "Excellent! Your dietary choices are very healthy. "

    sodium = nutritional_data.get("sodium_100g")
    if sodium is None:
        sodium = 0
    if sodium > 2300:
        recommendations += ("This food is high in sodium. Consider reducing intake.")
    
    fibers = nutritional_data.get("fibers_100g", None)
    if fibers is None:
        fibers = 0
    if fibers < 30:
        recommendations += ("This food is low in fiber. Try pairing it with fiber-rich foods.")

    sugars = nutritional_data.get("sugars_100g", None)
    if sugars is None:
        sugars = 0
    if sugars > 25:
        recommendations += ("This food has high sugar content. Aim to reduce added sugars.")

    vitamin_c = nutritional_data.get("vitamin_c_100g", None)
    if vitamin_c is None:
        vitamin_c = 0
        recommendations += ("This food lacks vitamin C. Consider adding fruits or vegetables rich in vitamin C.")

    calcium = nutritional_data.get("calcium_100g", None)
    if calcium is None:
        calcium = 0
    if calcium < 100:
        recommendations += ("This food is low in calcium. Include dairy or fortified alternatives in your diet.")


    return score, recommendations

# Define nutrient weights (for example, positive and negative weightings)
weights = {
    "calories_100g": 0.2,
    "proteins_100g": 0.3,
    "fat_100g": -0.2,
    "sat_fat_100g": -0.3,
    "insat_fat_100g": 0.1,
    "carbs_100g": 0.1,
    "sugars_100g": -0.4,
    "fibers_100g": 0.3,
    "cholesterol_100g": -0.2,
    "iron_100g": 0.2,
    "calcium_100g": 0.2,
    "vitamin_c_100g": 0.15,
    "vitamin_b9_100g": 0.1,
    "omega_3_100g": 0.2,
    "omega_6_100g": 0.1,
    "sodium_100g": -0.3,
}


print(f"Evaluating food: {food_name}")

# Extract the nutritional data for the first food possibility
# nutrients = food['food_info']['nutrition']

# Calculate the nutritional score for this food item
# food_score = calculate_nutritional_score(nutrients, weights, rda)

# Print the result for this food item
# print(f"Food: {food_name} | Nutritional Score: {food_score:.2f}")
print("-" * 40)

# Compute the score
nutritional_score = calculate_nutritional_score(nutritional_data, weights, rda)
print(f"Nutritional Score: {nutritional_score}")


app = Flask(__name__)

@app.route("/members")
def members():
    return {
        "foodname": food_name, 
        "score": nutritional_score
        }

if __name__ == "__main__":
    app.run(debug=True)
