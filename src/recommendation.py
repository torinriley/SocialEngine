import pandas as pd
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.preprocessing import MinMaxScaler
from sklearn.metrics.pairwise import cosine_similarity
import random

class SocialMediaRecommendation:
    def __init__(self, file_path):
        """
        Initialize the class with the path to the CSV file.
        :param file_path: Path to the dataset (data.csv).
        """
        self.file_path = file_path
        self.dataset = None
        self.scaler = MinMaxScaler()
        self.tfidf = TfidfVectorizer(stop_words='english')
        self.combined_features = None 

    def load_data(self):
        """
        Loads the dataset from the specified file path.
        """
        try:
            self.dataset = pd.read_csv(self.file_path)
            print(f"Dataset loaded successfully. Total records: {len(self.dataset)}")
        except Exception as e:
            print(f"Error loading dataset: {e}")

    def preprocess_data(self):
        """
        Preprocesses the dataset for further use.
        """
        from preprocessing import preprocess_dataset
        self.dataset = preprocess_dataset(self.dataset)
        
        # Create combined features
        text_features = self.tfidf.fit_transform(self.dataset['Caption'] + " " + self.dataset['Hashtags'])
        self.combined_features = np.hstack([
            text_features.toarray(),
            self.dataset[['Engagement Norm']].to_numpy()
        ])
        print("Data preprocessing complete.")

    def get_random_post(self):
        """
        Get a random post from the dataset.
        """
        return self.dataset.sample(1).iloc[0]

    def recommend_similar_posts(self, post_id, top_n=3):
        """
        Recommends similar posts based on cosine similarity.
        """
        similarities = cosine_similarity(
            [self.combined_features[post_id]],
            self.combined_features
        ).flatten()

        similar_indices = similarities.argsort()[-top_n-1:-1][::-1]
        return self.dataset.iloc[similar_indices]

    def update_user_profile(self, liked_post_ids):
        """
        Updates the user profile based on liked posts.
        """
        liked_features = self.combined_features[liked_post_ids]
        return liked_features.mean(axis=0)

    def recommend_for_user_profile(self, user_profile, top_n=3):
        """
        Recommends posts based on the user's preference profile.
        """
        similarities = cosine_similarity([user_profile], self.combined_features).flatten()
        similar_indices = similarities.argsort()[-top_n:][::-1]
        return self.dataset.iloc[similar_indices]
    