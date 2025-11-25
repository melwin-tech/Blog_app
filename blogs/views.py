from django.shortcuts import render,redirect,HttpResponse,get_object_or_404
from .models import *
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
# Create your views here.

@login_required
def home(request):
    blogs = Blog.objects.all().order_by('-created_at')
    return render(request, "blogs/home.html", {'blogs':blogs})

def signup(request):
    if request.method == "POST":
        username = request.POST.get("username")
        email = request.POST.get("email")
        password = request.POST.get("password")
        # Validate empty fields
        if not username or not email or not password:
            messages.error(request, "All fields are necessary")
            return redirect('signup')
        # Check if username already exists
        if User.objects.filter(username=username).exists():
            messages.error(request, "Username already exists")
            return redirect('signup')
        # Create user with hashed password
        user = User.objects.create_user(
            username=username,
            email=email,
            password=password
        )
        user.save()
        messages.success(request, "Account created successfully")
        return redirect('login')
    return render(request, "blogs/signup.html")

def signin(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")
        #validating the user 
        user = authenticate(request, username = username, password = password)
        if user is not None:
            login(request,user)
            return redirect('home')
        else:
            messages.error(request, "Invalid crediantials")
            return redirect('signin')
    return render(request,"blogs/login.html")

def signout(request):
    logout(request)
    return redirect('home')

@login_required
def create_blog(request):
    if request.method == "POST":
        title = request.POST.get("title")
        content = request.POST.get("content")
        Blog.objects.create(
            user=request.user,
            title=title,
            content=content,
        )
        return redirect("home")
    return render(request, "blogs/create.html")

@login_required
def edit_blog(request, blog_id):
    blog = get_object_or_404(Blog, id=blog_id)
    if blog.user != request.user:
        return redirect("home")
    if request.method == "POST":
        blog.title = request.POST.get("title")
        blog.content = request.POST.get("content")
        blog.save()
        return redirect("detail", blog_id=blog.id)
    return render(request, "blogs/edit.html", {"blog": blog})

@login_required
def blog_detail(request, blog_id):
    blog = get_object_or_404(Blog, id=blog_id)
    reviews = Review.objects.filter(blog=blog)
    # Check if user is owner
    can_review = True
    if request.user == blog.user:
        can_review = False   # Disable review for own blog
    context = {
        'blog': blog,
        'reviews': reviews,
        'can_review': can_review,
    }
    return render(request, "blogs/details.html", context)


@login_required
def reply_review(request, review_id):
    review = get_object_or_404(Review, id=review_id)
    # Only blog owner can reply
    if review.blog.user != request.user:
        return redirect("home")
    if request.method == "POST":
        reply_text = request.POST.get("reply")
        ReviewReply.objects.create(
            review=review,
            owner=request.user,
            reply_text=reply_text
        )
        print(review)
        return redirect("detail", blog_id=review.blog.id)
    return render(request, "blogs/reviews.html", {"review": review})




