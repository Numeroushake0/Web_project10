from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    path('', views.index, name='index'),  # Головна зі списком цитат + пагінація
    path('author/<int:pk>/', views.author_detail, name='author_detail'),
    path('quote/<int:pk>/', views.quote_detail, name='quote_detail'),

    path('add-author/', views.add_author, name='add_author'),
    path('add-quote/', views.add_quote, name='add_quote'),

    path('register/', views.register, name='register'),

    path('login/', auth_views.LoginView.as_view(template_name='quotes_app/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(next_page='index'), name='logout'),

    path('tag/<str:tag_name>/', views.quotes_by_tag, name='quotes_by_tag'),

    path('scrape/', views.scrape_view, name='scrape'),
]
