# Social Media Recommendation Engine

This project focuses on building a recommendation engine using social media data, specifically Instagram data.

## Dataset

The dataset used for this analysis can be found on Kaggle: [Instagram Data](https://www.kaggle.com/datasets/amirmotefaker/instagram-data)

## Project Structure

- `data/`: Contains the dataset and any data preprocessing scripts.
- `src/`: Source code for data processing and model training.
- `static/`: Static files such as images and JavaScript.
- `templates/`: HTML templates for the Flask app.

## Installation

To install the required dependencies, run:

```bash
pip install -r requirements.txt
```


## Flask Application
This is a Flask application that serves a social media recommendation engine.

### Content-Based Filtering
The algorithm uses TF-IDF (Term Frequency-Inverse Document Frequency) to vectorize the captions and hashtags of the posts.

- `compute_similarity_matrix(posts)`: Creates a TF-IDF matrix from the captions and hashtags of all posts.
- `recommend_posts(liked_posts, all_posts)`: Generates recommendations based on the posts that the user has liked.

