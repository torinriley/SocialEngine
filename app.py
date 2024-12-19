from flask import Flask, request, jsonify, render_template
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

app = Flask(__name__)

# Load posts from CSV and calculate engagement metrics
def load_posts():
    df = pd.read_csv("data.csv")
    df["Engagement"] = df["Likes"] + df["Comments"] + df["Shares"] + df["Saves"]
    posts = []
    for idx, row in df.iterrows():
        posts.append({
            "id": idx,
            "caption": row["Caption"],
            "engagement": row["Engagement"],
            "hashtags": row["Hashtags"],
        })
    return posts

all_posts = load_posts()
liked_posts = []
tfidf_vectorizer = None
tfidf_matrix = None

# Precompute TF-IDF matrix for captions and hashtags
def compute_similarity_matrix(posts):
    global tfidf_vectorizer, tfidf_matrix
    captions_and_hashtags = [
        f"{post['caption']} {post['hashtags']}" for post in posts
    ]
    tfidf_vectorizer = TfidfVectorizer(stop_words="english")
    tfidf_matrix = tfidf_vectorizer.fit_transform(captions_and_hashtags)

compute_similarity_matrix(all_posts)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/get_feed', methods=['GET'])
def get_feed():
    start = int(request.args.get('start', 0))
    count = int(request.args.get('count', 10))

    # Generate feed based on liked posts or high engagement posts
    if not liked_posts:
        curated_feed = sorted(all_posts, key=lambda x: x["engagement"], reverse=True)
    else:
        liked_posts_data = [post for post in all_posts if post["id"] in liked_posts]
        recommendations = recommend_posts(liked_posts_data, all_posts)
        curated_feed = recommendations

    next_posts = curated_feed[start:start + count]
    return jsonify(next_posts)

@app.route('/like_post', methods=['POST'])
def like_post():
    data = request.get_json()
    post_id = data.get("post_id")

    # Validate post_id and update liked posts
    if not post_id or not str(post_id).isdigit():
        return jsonify({"error": "Invalid post ID"}), 400

    post_id = int(post_id)
    if post_id not in liked_posts:
        liked_posts.append(post_id)

    return jsonify({"status": "success", "liked_post_id": post_id})

def recommend_posts(liked_posts, all_posts):
    """
    Generate recommendations based on liked posts using content-based filtering.
    """
    global tfidf_matrix
    liked_indices = [post["id"] for post in liked_posts]

    # Compute similarity scores for all posts
    liked_vectors = tfidf_matrix[liked_indices]
    similarity_scores = cosine_similarity(liked_vectors, tfidf_matrix).mean(axis=0)

    # Rank posts by similarity scores and engagement
    recommendations = []
    for idx, post in enumerate(all_posts):
        if post["id"] not in liked_indices:
            score = similarity_scores[idx] * 0.7 + (post["engagement"] / 1000) * 0.3
            recommendations.append((score, post))

    recommendations.sort(reverse=True, key=lambda x: x[0])
    return [rec[1] for rec in recommendations]

if __name__ == '__main__':
    app.run(debug=True)
