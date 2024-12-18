import tkinter as tk
from tkinter import messagebox
from recommendation import SocialMediaRecommendation


class SocialMediaGUI:
    def __init__(self, master):
        self.master = master
        self.master.title("Social Media Feed Simulation")
        self.master.configure(bg="#2C2F33")

        self.recommendation_system = SocialMediaRecommendation("data/data.csv")
        self.recommendation_system.load_data()
        self.recommendation_system.preprocess_data()

        self.user_liked_posts = []
        self.user_profile = None

        self.post_frame = tk.Frame(self.master, bg="#2C2F33", padx=20, pady=20)
        self.post_frame.pack(fill="both", expand=True)

        self.caption_label = tk.Label(
            self.post_frame,
            text="",
            wraplength=700,
            justify="center",
            fg="white",
            bg="#2C2F33",
            font=("Arial", 14, "bold"),
        )
        self.caption_label.pack(pady=10)

        self.hashtags_label = tk.Label(
            self.post_frame,
            text="",
            wraplength=700,
            justify="center",
            fg="#7289DA",  # Blue color
            bg="#2C2F33",
            font=("Arial", 12, "italic"),
        )
        self.hashtags_label.pack(pady=10)

        self.engagement_label = tk.Label(
            self.post_frame,
            text="",
            fg="#43B581",  # Green color
            bg="#2C2F33",
            font=("Arial", 12, "bold"),
        )
        self.engagement_label.pack(pady=10)

        # Action buttons with styles
        button_frame = tk.Frame(self.master, bg="#2C2F33")
        button_frame.pack(pady=20)

        self.like_button = tk.Button(
            button_frame,
            text="👍 Like",
            command=self.like_post,
            bg="#4CAF50",
            fg="white",
            font=("Arial", 12, "bold"),
            padx=10,
            pady=5,
        )
        self.like_button.grid(row=0, column=0, padx=10)

        self.scroll_button = tk.Button(
            button_frame,
            text="➡️ Scroll",
            command=self.scroll_post,
            bg="#2196F3",
            fg="white",
            font=("Arial", 12, "bold"),
            padx=10,
            pady=5,
        )
        self.scroll_button.grid(row=0, column=1, padx=10)

        self.exit_button = tk.Button(
            button_frame,
            text="❌ Exit",
            command=self.master.quit,
            bg="#FF5555",
            fg="white",
            font=("Arial", 12, "bold"),
            padx=10,
            pady=5,
        )
        self.exit_button.grid(row=0, column=2, padx=10)

        # Load the first post
        self.random_post = None
        self.load_new_post()

    def load_new_post(self):
        """
        Load a random post to display in the GUI.
        """
        self.random_post = self.recommendation_system.get_random_post()
        self.caption_label.config(text=f"{self.random_post['Caption']}")
        self.hashtags_label.config(text=f"Hashtags: {self.random_post['Hashtags']}")
        self.engagement_label.config(text=f"Engagement: {self.random_post['Engagement']:.2f}")

    def like_post(self):
        """
        Handle the action when the user likes a post.
        """
        self.user_liked_posts.append(self.random_post.name)
        self.user_profile = self.recommendation_system.update_user_profile(self.user_liked_posts)
        messagebox.showinfo("Post Liked", "You liked this post!")
        self.show_recommendations()
        self.load_new_post()

    def scroll_post(self):
        """
        Handle the action when the user scrolls past a post.
        """
        messagebox.showinfo("Post Scrolled", "You scrolled past this post.")
        self.load_new_post()

    def show_recommendations(self):
        """
        Show recommendations based on the user's liked posts.
        """
        if self.user_profile is not None:
            recommendations = self.recommendation_system.recommend_for_user_profile(self.user_profile, top_n=3)
            rec_text = "\n".join(
                [f"Caption: {post['Caption']}\nHashtags: {post['Hashtags']}\nEngagement: {post['Engagement']:.2f}"
                 for _, post in recommendations.iterrows()]
            )
            messagebox.showinfo("Recommendations", f"Recommended Posts:\n\n{rec_text}")


if __name__ == "__main__":
    root = tk.Tk()
    app = SocialMediaGUI(root)
    root.mainloop()