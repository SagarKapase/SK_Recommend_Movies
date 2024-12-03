from flask import Flask, request, jsonify, render_template
import pickle
import difflib

# Initialize the Flask app
app = Flask(__name__)

# Load the trained recommendation model
with open("movie_recommendation_system.pkl", "rb") as file:
    model = pickle.load(file)

# Extract movies_data and similarity from the loaded model
movies_data = model['movies_data']
similarity = model['similarity']

def recommend_movies(user_input):
    # List of all movie titles
    list_of_all_titles = movies_data['title'].tolist()
    
    # Find close match for user input
    find_close_match = difflib.get_close_matches(user_input, list_of_all_titles)
    if not find_close_match:
        return ["No close match found. Please try another movie."]
    
    close_match = find_close_match[0]
    
    # Find the index of the selected movie
    index_of_the_movie = movies_data[movies_data.title == close_match]['index'].values[0]
    
    # Get similarity scores for the selected movie
    similarity_score = list(enumerate(similarity[index_of_the_movie]))
    
    # Sort movies based on similarity scores
    sorted_similar_movies = sorted(similarity_score, key=lambda x: x[1], reverse=True)
    
    # Retrieve top 10 similar movies
    recommended_movies = []
    for movie in sorted_similar_movies[0:11]:  # Skip the first movie (itself)
        index = movie[0]
        title_from_index = movies_data[movies_data.index == index]['title'].values[0]
        recommended_movies.append(title_from_index)
    
    return recommended_movies

# Route to render the HTML page
@app.route("/", methods=["GET"])
def home():
    return render_template("index.html")

# API route for movie recommendations
@app.route("/recommend", methods=["POST"])
def recommend():
    data = request.get_json()
    movie_name = data.get("movie_name", None)
    
    if not movie_name:
        return jsonify({"error": "Please provide a movie_name"}), 400
    
    recommendations = recommend_movies(movie_name)
    return jsonify({"recommendations": recommendations})

# Run the Flask app
if __name__ == "__main__":
    app.run(debug=True)
