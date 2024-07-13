from flask import Flask, request, jsonify
import pandas as pd
import random
from flask_restful import Api, Resource
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

app = Flask(__name__)
api = Api(app)

# Load files
trending_products = pd.read_csv("models/trending_products.csv")
train_data = pd.read_csv("models/clean_data.csv")

# Utility function to truncate text
def truncate(text, length):
    if len(text) > length:
        return text[:length] + "..."
    else:
        return text

# Content-based recommendation function
def content_based_recommendations(train_data, item_name, top_n=10):
    if item_name not in train_data['Name'].values:
        return pd.DataFrame()

    tfidf_vectorizer = TfidfVectorizer(stop_words='english')
    tfidf_matrix_content = tfidf_vectorizer.fit_transform(train_data['Tags'])
    cosine_similarities_content = cosine_similarity(tfidf_matrix_content, tfidf_matrix_content)
    item_index = train_data[train_data['Name'] == item_name].index[0]
    similar_items = list(enumerate(cosine_similarities_content[item_index]))
    similar_items = sorted(similar_items, key=lambda x: x[1], reverse=True)
    top_similar_items = similar_items[1:top_n+1]
    recommended_item_indices = [x[0] for x in top_similar_items]
    recommended_items_details = train_data.iloc[recommended_item_indices][['Name', 'ReviewCount', 'Brand', 'ImageURL', 'Rating']]
    return recommended_items_details

# User-based recommendation function
def user_based_recommendations(train_data, liked_products, top_n=10):
    liked_data = train_data[train_data['Name'].isin(liked_products)]

    if liked_data.empty:
        return pd.DataFrame()

    aggregated_tags = ' '.join(liked_data['Tags'])
    tfidf_vectorizer = TfidfVectorizer(stop_words='english')
    all_tags = train_data['Tags'].tolist() + [aggregated_tags]
    tfidf_matrix_content = tfidf_vectorizer.fit_transform(all_tags)
    cosine_similarities_content = cosine_similarity(tfidf_matrix_content[-1], tfidf_matrix_content[:-1])
    similar_items = list(enumerate(cosine_similarities_content[0]))
    similar_items = sorted(similar_items, key=lambda x: x[1], reverse=True)
    top_similar_items = similar_items[:top_n]
    recommended_item_indices = [x[0] for x in top_similar_items]
    recommended_items_details = train_data.iloc[recommended_item_indices][['Name', 'ReviewCount', 'Brand', 'ImageURL', 'Rating']]
    return recommended_items_details

# Wishlist-based recommendation function
def wishlist_based_recommendations(train_data, wishlist, top_n=10):
    liked_data = train_data[train_data['Name'].isin(wishlist)]

    if liked_data.empty:
        return pd.DataFrame()

    aggregated_tags = ' '.join(liked_data['Tags'])
    tfidf_vectorizer = TfidfVectorizer(stop_words='english')
    all_tags = train_data['Tags'].tolist() + [aggregated_tags]
    tfidf_matrix_content = tfidf_vectorizer.fit_transform(all_tags)
    cosine_similarities_content = cosine_similarity(tfidf_matrix_content[-1], tfidf_matrix_content[:-1])
    similar_items = list(enumerate(cosine_similarities_content[0]))
    similar_items = sorted(similar_items, key=lambda x: x[1], reverse=True)
    top_similar_items = similar_items[:top_n]
    recommended_item_indices = [x[0] for x in top_similar_items]
    recommended_items_details = train_data.iloc[recommended_item_indices][['Name', 'ReviewCount', 'Brand', 'ImageURL', 'Rating']]
    return recommended_items_details

# API Endpoints
class RecommendationAPI(Resource):
    def post(self):
        data = request.get_json()
        prod = data.get('prod')
        nbr = data.get('nbr')
        wishlist = data.get('wishlist')  # New parameter for wishlist

        if not prod or not nbr:
            return {"message": "Invalid input"}, 400

        # Content-based recommendations
        content_based_rec = content_based_recommendations(train_data, prod, top_n=nbr)
        if content_based_rec.empty:
            content_based_rec = []

        # User-based recommendations (example list of liked products)
        liked_products = [
            "Nicole by OPI Nail Lacquer, Next Stop the Bikini Zone A59, .5 fl oz",
            "ReNew Life CleanseMore, Veggie Caps, 60 ea",
            "Alba Botanica Very Emollient Herbal Healing Body Lotion, 32 oz."
        ]
        user_based_rec = user_based_recommendations(train_data, liked_products, top_n=nbr)
        if user_based_rec.empty:
            user_based_rec = []

        # Wishlist-based recommendations
        wishlist_rec = wishlist_based_recommendations(train_data, wishlist, top_n=nbr)
        if wishlist_rec.empty:
            wishlist_rec = []

        # Combine recommendations
        combined_recommendations = {
            "content_based": content_based_rec.to_dict(orient='records'),
            "user_based": user_based_rec.to_dict(orient='records'),
            "wishlist_based": wishlist_rec.to_dict(orient='records')
        }

        # Simulate random image URLs and prices
        random_image_urls = [
            "static/img/img_1.png",
            "static/img/img_2.png",
            "static/img/img_3.png",
            "static/img/img_4.png",
            "static/img/img_5.png",
            "static/img/img_6.png",
            "static/img/img_7.png",
            "static/img/img_8.png",
        ]
        for rec_type in combined_recommendations:
            for item in combined_recommendations[rec_type]:
                item['ImageURL'] = random.choice(random_image_urls)
                item['Price'] = random.choice([40, 50, 60, 70, 100, 122, 106, 50, 30, 50])

        return jsonify(combined_recommendations)

# Adding the endpoints
api.add_resource(RecommendationAPI, '/recommendations')

if __name__ == '__main__':
    app.run(debug=True)
