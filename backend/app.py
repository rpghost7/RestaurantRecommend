from flask import Flask, request, jsonify
from flask_cors import CORS
import pandas as pd

from model import prepare_recommender_data, recommend_top_restaurant_names

# Init Flask app
app = Flask(__name__)
CORS(app)

# Load data and model
final_data = pd.read_csv('enhanced_zomato_dataset_clean.csv')
final_data = final_data[['Restaurant_Name', 'City', 'Cuisine', 'Average_Rating', 'Prices', 'Place_Name', 'Item_Name']]
model = prepare_recommender_data(final_data)

@app.route('/recommend', methods=['POST'])
def recommend():
    data = request.get_json()
    
    user_cuisine = data.get('place_cuisine')
    user_city = data.get('place_city')

    user_rating = float(data.get('rating', 4.0))
    user_price = float(data.get('price', 300))
    
    try:
        top_k = recommend_top_restaurant_names(
            model,
            user_cuisine=user_cuisine,
            user_city=user_city,
            user_rating=user_rating,
            user_price=user_price,
            top_k=5
        )

        # Convert to JSON-serializable format
        recommendations = top_k[['Restaurant_Name', 'Item_Name', 'Average_Rating', 'Prices', 'Place_Name','City']].to_dict(orient='records')
        return jsonify({"results": recommendations})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(debug=True)
    
    # made these changes to as backend is deployed
