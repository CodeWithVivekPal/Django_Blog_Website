from django.urls import path
from .views import *
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path("", home, name="home_page"),
    path("addblog/", addBlog, name="addBlog"),
    path("<int:id>/", post, name="post_id"),
    path("login/", login_page, name="login"),
    path("register/", register_page, name="register"),
    path("logout/", logout_page, name="logout"),
    path("contact/", contact_page, name="contact"),
    path('view_blogs/', view_blogs, name='view_blogs'),
    path('post/<int:id>/', post, name='post'),
    path('publish_blog/<int:blog_id>/', publish_blog, name='publish_blog'),
    path('toggle_publish_status/<int:blog_id>/', toggle_publish_status, name='toggle_publish_status'),
   
]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
