import unittest
import os

os.environ["TESTING"] = "true"
from app import app, init_db, mydb, TimelinePost


class AppTestCase(unittest.TestCase):
    def setUp(self):
        self.client = app.test_client()
        # Ensure database is properly initialized for each test
        try:
            # Close any existing connection
            if not mydb.is_closed():
                mydb.close()
            # Connect and create tables
            mydb.connect()
            mydb.create_tables([TimelinePost], safe=True)
            print("Database connected and tables created successfully")
        except Exception as e:
            print(f"Database setup error: {e}")
            raise

    def tearDown(self):
        # Clean up database after each test
        try:
            # Drop all tables to ensure clean state
            mydb.drop_tables([TimelinePost], safe=True)
            # Close connection
            if not mydb.is_closed():
                mydb.close()
        except Exception as e:
            print(f"Database teardown error: {e}")

    def test_home(self):
        response = self.client.get("/")
        assert response.status_code == 200
        html = response.get_data(as_text=True)

        # Test page title
        assert "<title>Home - Ishar Ghura</title>" in html

        # Test main content
        assert "Welcome to my Portfolio!" in html
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
