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

# Recommendations functions
def truncate(text, length):
    if len(text) > length:
        return text[:length] + "..."
    else:
        return text

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

# API Endpoints
class RecommendationAPI(Resource):
    def post(self):
        data = request.get_json()
        prod = data.get('prod')
        nbr = data.get('nbr')
        if not prod or not nbr:
            return {"message": "Invalid input"}, 400

        content_based_rec = content_based_recommendations(train_data, prod, top_n=nbr)
        if content_based_rec.empty:
            return {"message": "No recommendations available for this product."}, 404
        
        rec_list = content_based_rec.to_dict(orient='records')
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
        for item in rec_list:
            item['ImageURL'] = random.choice(random_image_urls)
            item['Price'] = random.choice([40, 50, 60, 70, 100, 122, 106, 50, 30, 50])
        return jsonify(rec_list)

# Adding the endpoints
api.add_resource(RecommendationAPI, '/recommendations')

if __name__ == '__main__':
    app.run(debug=True)
