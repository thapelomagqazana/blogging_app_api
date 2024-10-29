from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from django.contrib.auth.models import User
from blog_app.models import Post

class PostManagementTests(APITestCase):

    def setUp(self):
        # Create an admin user and a non-admin user
                # Create an admin user and a non-admin user
        self.admin_user = User.objects.create_superuser(
            username='adminuser', email='admin@example.com', password='adminpass'
        )
        self.non_admin_user = User.objects.create_user(
            username='regularuser', email='user@example.com', password='userpass'
        )
        # Sample post data
        self.post = Post.objects.create(
            title="Sample Post",
            content="This is a sample post.",
            is_published=True
        )
        # URLs
        self.post_list_create_url = reverse('post-list-create')
        self.post_detail_url = reverse('post-detail', kwargs={'pk': self.post.id})

    def authenticate_admin(self):
        """Helper method to authenticate as the admin user."""
        self.client.force_authenticate(user=self.admin_user)

    def authenticate_non_admin(self):
        """Helper method to authenticate as a non-admin user."""
        self.client.force_authenticate(user=self.non_admin_user)

    # List and Retrieve Posts
    def test_list_posts(self):
        """Test admin can list all posts."""
        self.authenticate_admin()
        response = self.client.get(self.post_list_create_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertGreaterEqual(len(response.data), 1)

    def test_retrieve_post(self):
        """Test admin can retrieve a single post."""
        self.authenticate_admin()
        response = self.client.get(self.post_detail_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['title'], self.post.title)

    # Create Post
    def test_create_post_as_admin(self):
        """Test admin can create a new post."""
        self.authenticate_admin()
        data = {
            "title": "New Post",
            "content": "Content for the new post.",
            "is_published": True
        }
        response = self.client.post(self.post_list_create_url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['title'], data['title'])

    def test_create_post_as_non_admin(self):
        """Test non-admin user cannot create a post."""
        self.authenticate_non_admin()
        data = {
            "title": "Unauthorized Post",
            "content": "Should not be allowed to create this post.",
            "is_published": False
        }
        response = self.client.post(self.post_list_create_url, data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    # Update Post
    def test_update_post_as_admin(self):
        """Test admin can update an existing post."""
        self.authenticate_admin()
        data = {
            "title": "Updated Post Title",
            "content": "Updated content for the post.",
            "is_published": False
        }
        response = self.client.put(self.post_detail_url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['title'], data['title'])

    def test_update_post_as_non_admin(self):
        """Test non-admin user cannot update a post."""
        self.authenticate_non_admin()
        data = {
            "title": "Attempted Update",
            "content": "This update should be forbidden.",
            "is_published": False
        }
        response = self.client.put(self.post_detail_url, data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    # Delete Post
    def test_delete_post_as_admin(self):
        """Test admin can delete a post."""
        self.authenticate_admin()
        response = self.client.delete(self.post_detail_url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(Post.objects.filter(id=self.post.id).exists())

    def test_delete_post_as_non_admin(self):
        """Test non-admin user cannot delete a post."""
        self.authenticate_non_admin()
        response = self.client.delete(self.post_detail_url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertTrue(Post.objects.filter(id=self.post.id).exists())