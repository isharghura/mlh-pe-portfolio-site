import unittest
import os

os.environ["TESTING"] = "true"
from app import app, mydb, TimelinePost


class AppTestCase(unittest.TestCase):
    def setUp(self):
        self.client = app.test_client()

    def test_home(self):
        response = self.client.get("/")
        assert response.status_code == 200
        html = response.get_data(as_text=True)

        # Test page title
        assert "<title>Home - Ishar Ghura</title>" in html

        # Test main content
        assert "my name is Ishar Ghura!" in html

        # Test navigation elements
        assert "Ishar Ghura" in html
        assert "navbar" in html
        assert "Home" in html
        assert "About" in html
        assert "Work" in html
        assert "Hobbies" in html
        assert "Education" in html
        assert "Travel" in html
        assert "Timeline" in html

        # Test Bootstrap integration
        assert "bootstrap" in html.lower()
        assert "container" in html

        # Test meta tags
        assert 'charset="utf-8"' in html
        assert "viewport" in html

        # Test that it's a proper HTML document
        assert html.strip().startswith("<!DOCTYPE html>")
        assert "</html>" in html

    def test_timeline_get_empty(self):
        response = self.client.get("/api/timeline_post")
        assert response.status_code == 200
        assert response.is_json
        json = response.get_json()
        assert "timeline_posts" in json
        assert len(json["timeline_posts"]) == 0

    def test_timeline_post_create(self):
        post_data = {
            "name": "Test User",
            "email": "test@example.com",
            "content": "This is a test post",
        }
        response = self.client.post(
            "/api/timeline_post",
            data=post_data,
        )
        assert response.status_code == 200
        assert response.is_json

        created_post = response.get_json()
        assert "name" in created_post
        assert "email" in created_post
        assert "content" in created_post
        assert "created_at" in created_post
        assert created_post["name"] == post_data["name"]
        assert created_post["email"] == post_data["email"]
        assert created_post["content"] == post_data["content"]

    def test_timeline_multiple_posts(self):
        # Create first post
        post1_data = {
            "name": "User 1",
            "email": "user1@example.com",
            "content": "First post",
        }
        response1 = self.client.post("/api/timeline_post", data=post1_data)
        assert response1.status_code == 200

        # Create second post
        post2_data = {
            "name": "User 2",
            "email": "user2@example.com",
            "content": "Second post",
        }
        response2 = self.client.post("/api/timeline_post", data=post2_data)
        assert response2.status_code == 200

        # Create third post
        post3_data = {
            "name": "User 3",
            "email": "user3@example.com",
            "content": "Third post",
        }
        response3 = self.client.post("/api/timeline_post", data=post3_data)
        assert response3.status_code == 200

        # Get all posts
        response = self.client.get("/api/timeline_post")
        assert response.status_code == 200
        assert response.is_json

        json = response.get_json()
        assert "timeline_posts" in json
        assert len(json["timeline_posts"]) == 3

        # Verify all posts are present
        posts = json["timeline_posts"]
        names = [post["name"] for post in posts]
        assert "User 1" in names
        assert "User 2" in names
        assert "User 3" in names

        # Verify posts are ordered by created_at desc (newest first)
        assert posts[0]["name"] == "User 3"  # Most recent
        assert posts[1]["name"] == "User 2"  # Middle
        assert posts[2]["name"] == "User 1"  # Oldest

    def test_timeline_page(self):
        """Test the timeline page rendering"""
        response = self.client.get("/timeline")
        assert response.status_code == 200

        html = response.get_data(as_text=True)

        # Test page title
        assert "<title>Timeline</title>" in html

        # Test main content
        assert "<h1>Timeline</h1>" in html
        assert "<h2>Create Post</h2>" in html
        assert "<h2>Posts</h2>" in html

        # Test form elements
        assert 'id="postForm"' in html
        assert 'id="name"' in html
        assert 'id="email"' in html
        assert 'id="content"' in html
        assert 'type="text"' in html
        assert 'type="email"' in html
        assert 'placeholder="Name"' in html
        assert 'placeholder="Email"' in html
        assert 'placeholder="Your post"' in html
        assert 'type="submit"' in html

        # Test JavaScript functionality
        assert "loadPosts()" in html
        assert "fetch('/api/timeline_post')" in html
        assert "POST" in html
        assert "FormData" in html

        # Test posts container
        assert 'id="posts"' in html
        assert "Loading..." in html

    def test_malformed_timeline_post(self):
        # POST request missing name
        response = self.client.post(
            "/api/timeline_post",
            data={"email": "john@example.com", "content": "Hello world, I'm John!"},
        )
        assert response.status_code == 400
        html = response.get_data(as_text=True)
        assert "Invalid name" in html

        # POST request with empty content
        response = self.client.post(
            "/api/timeline_post",
            data={"name": "John Doe", "email": "john@example.com", "content": ""},
        )
        assert response.status_code == 400
        html = response.get_data(as_text=True)
        assert "Invalid content" in html

        # POST request with malformed email
        response = self.client.post(
            "/api/timeline_post",
            data={
                "name": "John Doe",
                "email": "not-an-email",
                "content": "Hello world, I'm John!",
            },
        )
        assert response.status_code == 400
        html = response.get_data(as_text=True)
        assert "Invalid email" in html
