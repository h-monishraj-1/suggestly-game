from flask import Flask, request, jsonify, render_template
from game_recommendation import GameRecommender
import pandas as pd

app = Flask(__name__)

# Initialize game recommender
game_recommender = GameRecommender()

games_df = pd.read_pickle("game_data.pkl")

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/recommend_games", methods=["POST"])
def recommend_games():
    data = request.json
    game_title = data.get("game_title", "")
    recommendations = game_recommender.recommend(game_title)
    # Adding images to the response
    recommendation_details = [
        {"title": game['name'], "image": game['image']} for game in recommendations
    ]

    return jsonify({"recommendations": recommendation_details})

@app.route("/get_titles", methods=["GET"])
def get_titles():
    query = request.args.get("q", "").lower()
    if not query:
        return jsonify({"titles": []})
    
    matching_titles = games_df[games_df['Name'].str.lower().str.contains(query, na=False)]['Name'].head(10).tolist()
    return jsonify({"titles": matching_titles})

if __name__ == "__main__":
    app.run(debug=True)
