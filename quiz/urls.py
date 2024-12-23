"""
URL configuration for quiz project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from rest_framework_simplejwt import views as jwt_views
from core.views import RegisterView, ranking_by_match_api,create_match_user,quiz_player,get_quiz_with_match_user,get_user_by_id

urlpatterns = [
    path("admin/", admin.site.urls),
    path('api/token/', jwt_views.TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', jwt_views.TokenRefreshView.as_view(), name='token_refresh'),
    path('api/token/api-auth/', include('rest_framework.urls')),
    path('api/token/register/', RegisterView.as_view(), name='register'),
    path('api/', include('core.urls')),
    path('api/ranking/<int:match_id>/', ranking_by_match_api, name='ranking_by_match_api'),
    path('api/quiz/<int:match_id>/', quiz_player, name='quiz_player'),
    path('api/match-users', create_match_user, name='create_match_user'),
    path('api/quiz/<int:quiz_id>/match-user/<int:match_user_id>/', get_quiz_with_match_user, name='get_quiz_with_match_user'),
    path('api/userid/<int:user_id>/', get_user_by_id, name='get_user_by_id'),
]
