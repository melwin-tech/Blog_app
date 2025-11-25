from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('signup/', views.signup, name='signup'),
    path('login/', views.signin, name='login'),
    path('logout/', views.signout, name='logout'),
    path('create/', views.create_blog, name='create'),
    path('blog/<int:blog_id>', views.blog_detail, name='detail'),
    path('edit/<int:blog_id>', views.edit_blog, name='edit'),
    path('review/<int:review_id>', views.reply_review, name='review'),
]
