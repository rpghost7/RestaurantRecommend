import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd 


final_data = pd.read_csv('enhanced_zomato_dataset_clean.csv')
final_data = final_data[['Restaurant_Name','City','Cuisine','Average_Rating','Prices','Place_Name','Item_Name']]


from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.preprocessing import MinMaxScaler
from sklearn.metrics.pairwise import cosine_similarity
from scipy.sparse import hstack
import pandas as pd

def prepare_recommender_data(final_data):
    final_data['Cuisine'] = final_data['Cuisine'].str.lower().str.strip()
    final_data['City'] = final_data['City'].str.lower().str.strip()
    
    # this is so that all the data is in one single format Mumbai and mumbai is same 

    # Combine textual features
    final_data['Combined'] = final_data['Cuisine'] + ' ' + final_data['City']

    # TF-IDF vectorization
    tfidf = TfidfVectorizer()
    tfidf_matrix = tfidf.fit_transform(final_data['Combined'])
    
    # this is also a sparse matrix
    # this converts it into a matrix of vectors where each row is a document and each column is a word in the document
    # Scale numeric features
    scaler = MinMaxScaler()
    numeric_matrix = scaler.fit_transform(final_data[['Average_Rating', 'Prices']])

    numerical_weight = 0.2  # Here we are reducing the contribution given by average rating and prices
    numeric_matrix = numeric_matrix * numerical_weight

    # Combine all features
    full_matrix = hstack([tfidf_matrix, numeric_matrix])

    return {
        'tfidf': tfidf,
        'scaler': scaler,
        'final_matrix': full_matrix,
        'final_data': final_data
    }

def recommend_top_restaurant_names(model, user_cuisine, user_city, user_rating=4.0, user_price=300, top_k=5):
    user_cuisine = user_cuisine.lower().strip()
    user_city = user_city.lower().strip()
    user_text = user_cuisine + ' ' + user_city

    tfidf = model['tfidf']
    scaler = model['scaler']
    final_matrix = model['final_matrix']
    final_data = model['final_data']

    # Vectorize user input to make a similar vector as the one we did for tfidf of initial data
    user_vec_text = tfidf.transform([user_text])
    

    user_vec_num = scaler.transform(pd.DataFrame([[user_rating, user_price]], columns=['Average_Rating', 'Prices']))

    user_vec = hstack([user_vec_text, user_vec_num])
    # making the final vector

    # Similarity calculation
    similarities = cosine_similarity(user_vec, final_matrix)[0]
    # here it returns an array of 1,N where N is the number of restaurants in the data
    # so 0 here is just converting it back to 1D form
    final_data = final_data.copy()
    final_data['SimilarityScore'] = similarities

    # Sort by similarity and then rating
    top_similar = final_data.sort_values(by='SimilarityScore', ascending=False).head(100)
    top_similar = top_similar.drop_duplicates(subset='Item_Name')
    top_ranked = top_similar.sort_values(by='Average_Rating', ascending=False).head(top_k)

    # Return only unique restaurant names
    return top_ranked


# # Step 1: Prepare the recommender model from your dataset
# model = prepare_recommender_data(final_data)

# # Step 2: Use the recommender
# top_restaurants = recommend_top_restaurant_names(
#     model,
#     user_cuisine='chinese',
#     user_city='mumbai',
#     user_rating=4.5,
#     user_price=200,
#     top_k=5
# )

# print("🍽️ Our Recommendations")

# for i in range(5):
#     row = top_restaurants.iloc[i]
#     print(f"{i+1}. Restaurant Name: {row['Restaurant_Name']},Item:{row['Item_Name']}, Rating: {row['Average_Rating']}, Price: ₹{row['Prices']}")



