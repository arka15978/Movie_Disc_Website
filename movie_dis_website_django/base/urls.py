from django.urls import path
from . import views

urlpatterns = [
    path('signup/', views.signUpScreen, name="signup"),
    path('signin/', views.signinScreen, name="signin"),
    path('signout/', views.signout, name="signout"),
    path('', views.homePage, name="home-page"),
    path('room-page/<str:pk>/', views.roomPage, name="room-page"),
    path('profile/<str:pk>/', views.userProfileView, name="user-profile"),

    path('create-room/', views.createRoom, name="create-room"),
    path('update-room/<str:pk>/', views.updateRoom, name="update-room"),
    path('delete-room/<str:pk>/', views.deleteRoom, name="delete-room"),
    path('delete-message/<str:pk>/', views.deleteMessage, name="delete-message"),

    path('edit-user/', views.editUser, name="edit-user"),

    path('search-movies/', views.moviesCard, name="search-movies"),
    path('activity/', views.activityPage, name="activity"),
]
