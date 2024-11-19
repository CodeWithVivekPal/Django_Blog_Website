from django.db import models
from accounts.models import CustomUser
from django.utils import timezone


class Category(models.Model):
    cat_name = models.CharField(max_length=100)

    def __str__(self):
        return self.cat_name


class Blog(models.Model):
  
    blog_cat = models.ForeignKey(
        Category, on_delete=models.SET_NULL, null=True, blank=True
    )

    blog_title = models.CharField(max_length=100)
    blog_content = models.TextField()
    blog_image = models.ImageField(upload_to="Posts", null=True, blank=True)
    submitted_at = models.DateTimeField(auto_now_add=True, null=True, blank=True)

    def __str__(self):
        return self.blog_title


class UserBlogs(models.Model):
    user = models.ForeignKey(
        CustomUser, on_delete=models.CASCADE
    )
    blog = models.ForeignKey(
        Blog,
        on_delete=models.CASCADE
    )
    is_published = models.BooleanField(
        default=False,
    )  # Indicates if the blog is published
    published_date = models.DateTimeField(
        null=True, blank=True,
    )  # Date when published

    def publish(self):
        """Method to publish the blog."""
        if not self.is_published:
            self.is_published = True
            self.published_date = timezone.now()
            self.save()

    def save_as_draft(self):
        """Method to save the blog as a draft."""
        self.is_published = False
        self.published_date = None
        self.save()

    def __str__(self):
        status = "Published" if self.is_published else "Draft"
        return f"{self.blog.blog_title} - {status}"
