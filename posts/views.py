from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import (
    HttpResponse,
    HttpResponseRedirect,
)
from django.urls import reverse
from .models import *


def helloWorld(request):
    return HttpResponse("HELLO WORLD !")


def home(request):
    # Fetch published blogs via the UserBlogs model (only published blogs)
    posts = Blog.objects.filter(userblogs__is_published=True)
    page_name = "Home Page"
    categories = Category.objects.all()

    if request.GET.get("search"):
        posts = posts.filter(blog_title__icontains=request.GET.get("search"))

    return render(
        request,
        "posts/home.html",
        {"posts": posts, "categories": categories, "page_name": page_name},
    )


@login_required(login_url="/login/")
def post(request, id):
    try:
        # Fetch the blog using UserBlogs to ensure the user can view it
        user_blog = UserBlogs.objects.get(blog_id=id, user=request.user)
        queryset = user_blog.blog  # Get the associated Blog object

        return render(
            request,
            "posts/post.html",
            {"queryset": queryset, "page_name": "Post Page"},
        )

    except UserBlogs.DoesNotExist:
        messages.error(request, "You do not have access to this blog.")
        return redirect(reverse("home"))



def direct_id(request, id):
    url = reverse("post_id", args=[id])
    return HttpResponseRedirect(url)


@login_required(login_url="/login/")
def addBlog(request):
    url = reverse("view_blogs")  # Redirect to the page where users can manage their drafts
    categories = Category.objects.all()

    if request.method == "POST":
        data = request.POST
        blog_title = data.get("blog_title")
        blog_content = data.get("blog_content")
        blog_image = request.FILES.get("blog_image")

        blog_cat_id = data.get("blog_cat")
        if blog_cat_id != "Null":
            try:
                blog_cat = Category.objects.get(id=blog_cat_id)
            except Category.DoesNotExist:
                blog_cat = None
        else:
            blog_cat = None

        # Save the blog as a draft by default
        blog = Blog.objects.create(
            blog_title=blog_title,
            blog_content=blog_content,
            blog_image=blog_image,
            blog_cat=blog_cat,
        )

        # Link the blog to the user and mark it as a draft
        user_blog = UserBlogs.objects.create(
            user=request.user,
            blog=blog,
            is_published=False,  # Default as draft
        )

        messages.success(request, "Blog saved as draft!")
        return redirect(url)  # Redirect to the user's blog management page

    return render(
        request,
        "posts/addBlog.html",
        {
            "categories": categories,
            "page_name": "Add Blog",
        },
    )


@login_required(login_url="/login/")
def publish_blog(request, blog_id):
    try:
        # Fetch the UserBlogs object for the specific blog and user
        user_blog = UserBlogs.objects.get(blog_id=blog_id, user=request.user)

        # Check if the blog is already published, if not, publish it
        if not user_blog.is_published:
            user_blog.publish()
            messages.success(request, "Blog published successfully!")
        else:
            messages.info(request, "This blog is already published.")

        return redirect(reverse("view_blogs"))

    except UserBlogs.DoesNotExist:
        messages.error(request, "Blog not found or you do not have permission to publish it.")
        return redirect(reverse("addBlog"))

@login_required(login_url="/login/")
def view_blogs(request):
    # Fetch all blogs related to the current user, whether published or draft
    user_blogs = UserBlogs.objects.filter(user=request.user)

    published_blogs = user_blogs.filter(is_published=True)
    draft_blogs = user_blogs.filter(is_published=False)

    # Handle editing a blog
    if request.method == "POST" and 'edit_blog_id' in request.POST:
        blog_id = request.POST.get('edit_blog_id')
        
        try:
            # Fetch the UserBlogs object for the specific blog and user
            user_blog = UserBlogs.objects.get(blog_id=blog_id, user=request.user)
            blog_to_edit = user_blog.blog  # Access the related Blog object
            
            blog_title = request.POST.get('blog_title')
            blog_content = request.POST.get('blog_content')
            blog_cat_id = request.POST.get('blog_cat')
            blog_image = request.FILES.get('blog_image')
            
            # Update the blog details
            blog_to_edit.blog_title = blog_title
            blog_to_edit.blog_content = blog_content
            blog_to_edit.blog_cat_id = blog_cat_id
            if blog_image:
                blog_to_edit.blog_image = blog_image
            blog_to_edit.save()

            messages.success(request, "Blog updated successfully!")
            return redirect(reverse("view_blogs"))
        except UserBlogs.DoesNotExist:
            messages.error(request, "Blog not found or you do not have permission to edit it.")
            return redirect(reverse("view_blogs"))

    return render(
        request,
        "posts/view_blogs.html",
        {"published_blogs": published_blogs, "draft_blogs": draft_blogs, "page_name": "Your Blogs"},
    )
@login_required(login_url="/login/")
def toggle_publish_status(request, blog_id):
    try:
        # Fetch the UserBlogs object for the specific blog and user
        user_blog = UserBlogs.objects.get(blog_id=blog_id, user=request.user)

        # Toggle the is_published field
        if user_blog.is_published:
            user_blog.is_published = False  # Move to draft
            messages.success(request, "Blog moved to draft successfully!")
        else:
            user_blog.is_published = True  # Publish the blog
            messages.success(request, "Blog published successfully!")

        # Save the changes
        user_blog.save()

        return redirect(reverse("view_blogs"))

    except UserBlogs.DoesNotExist:
        messages.error(request, "Blog not found or you do not have permission to modify it.")
        return redirect(reverse("view_blogs"))


def login_page(request):
    url = reverse("home_page")
    if request.method == "POST":
        data = request.POST
        email = data.get("email")  # Ensure the form uses 'email'
        password = data.get("password")

        customuser = authenticate(request=request, username=email, password=password)
        print(customuser)
        if customuser is None:
            messages.info(request, "Invalid email or password")
            return redirect("/login/")
        else:
            login(request, customuser)
            return redirect(url)  # Redirect to a valid URL

    return render(request, "posts/login.html", {"page_name": "Login Page"})


def register_page(request):
    if request.method == "POST":
        data = request.POST
        name = data.get("name")
        email = data.get("email")
        mobno = data.get("mobno")
        password = data.get("password")

        customuser = CustomUser.objects.filter(email=email)

        if customuser.exists():
            messages.info(request, "Email already in use")
            return redirect("/register/")

        customuser = CustomUser.objects.create(name=name, mobno=mobno, email=email)
        customuser.set_password(password)
        customuser.save()

        messages.info(request, "Account created successfully!")
        return redirect("/login/")

    return render(request, "posts/register.html", {"page_name": "Register Page"})


def logout_page(request):
    logout(request)
    return redirect("/login/")


def contact_page(request):

    return render(request, "posts/contact.html", {"page_name": "Contact US"})
