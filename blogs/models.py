from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Blog(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="blogs")
    title = models.CharField(max_length=255)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

class Review(models.Model):
    blog = models.ForeignKey(Blog, on_delete=models.CASCADE, related_name="reviews")
    reviewer = models.ForeignKey(User, on_delete=models.CASCADE, related_name="reviews")
    rating = models.IntegerField()  # 1–5 stars
    comment = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

class ReviewReply(models.Model):
    review = models.OneToOneField(Review, on_delete=models.CASCADE, related_name="reply")
    owner = models.ForeignKey(User, on_delete=models.CASCADE)  # Blog owner
    reply_text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)





