document.addEventListener("DOMContentLoaded", () => {
    let start = 0;
    const count = 10;
    const feedContainer = document.getElementById("post-feed");

    async function fetchImageForPost() {
        return `https://picsum.photos/seed/${Math.random().toString(36).substr(2, 9)}/600`;
    }

    async function fetchFeed() {
        fetch(`/get_feed?start=${start}&count=${count}`)
            .then((response) => response.json())
            .then(async (posts) => {
                if (posts.length === 0) return;
                
                for (const post of posts) {
                    const postElement = document.createElement("div");
                    postElement.classList.add("post-card");

                    const imageUrl = await fetchImageForPost();

                    postElement.innerHTML = `
                        <img src="${imageUrl}" alt="Post Image" class="post-image">
                        <button class="like-button" data-id="${post.id}">Like</button>
                        <h3>${post.caption}</h3>
                        <div class="hashtags">${cleanHashtags(post.hashtags)}</div>
                    `;
                    feedContainer.appendChild(postElement);
                }
                start += count;
                addLikeButtonListeners();
            })
            .catch((err) => console.error("Error fetching feed:", err));
    }

    function cleanHashtags(rawHashtags) {
        return rawHashtags
            .split('#')
            .filter(tag => tag.trim() && !tag.includes('�'))
            .map(tag => `<span class="hashtag">#${tag.trim()}</span>`)
            .join('');
    }

    function addLikeButtonListeners() {
        const likeButtons = document.querySelectorAll(".like-button");
        likeButtons.forEach(button => {
            button.addEventListener("click", (event) => {
                const button = event.target;
                button.classList.toggle("liked");
                button.innerText = button.classList.contains("liked") ? "Liked" : "Like";
                button.classList.add("like-animation");
                setTimeout(() => button.classList.remove("like-animation"), 300);
            });
        });
    }

    function sharePost() {
        const githubRepoUrl = 'https://github.com/torinriley/SocialEngine';
        window.open(githubRepoUrl, '_blank');
    }
    
    window.addEventListener("scroll", () => {
        if (window.innerHeight + window.scrollY >= document.body.offsetHeight - 100) {
            fetchFeed();
        }
    });

    fetchFeed();
});
