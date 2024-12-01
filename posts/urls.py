from django.urls import path
from .views import *
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path("", home, name="home_page"),  # Home Page
    path("addblog/", addBlog, name="addBlog"),  # Add Blog
    path("login/", login_page, name="login"),  # Login
    path("register/", register_page, name="register"),  # Register
    path("logout/", logout_page, name="logout"),  # Logout
    path("contact/", contact_page, name="contact"),  # Contact Page
    path("view_blogs/", view_blogs, name="view_blogs"),  # View Blogs

    # Blog Post
    path("post/<int:id>/", post, name="post"),  # View a single blog post
    path("publish_blog/<int:blog_id>/", publish_blog, name="publish_blog"),  # Publish Blog
    path("toggle_publish_status/<int:blog_id>/", toggle_publish_status, name="toggle_publish_status"),  # Toggle Publish/Draft Status

    # Editing and Updating Blogs
    path("edit_blog/", edit_blog, name="edit_blog"),  # Edit Blog (handles modal form submission)
    path("delete_blog/<int:blog_id>/", delete_blog, name="delete_blog"),  # Delete Blog
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
