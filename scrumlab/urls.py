"""scrumlab URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
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
from django.urls import path
from jedzonko.views import (
    IndexView,
    DashboardView,
    RecipeDetailsView,
    RecipeListView,
    RecipeAddView,
    RecipeModifyView,
    PlanAddRecipeView,
    PlanDetailsView,
    PlanAddView,
    PlanListView,
    ContactView,
    AboutView,
)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('index/', IndexView.as_view()),
    path('', IndexView.as_view()), # App main page
    path('main/', DashboardView.as_view()), # App dashboard page
    path('recipe/<int:id_>/', RecipeDetailsView.as_view(), name='recipe_detail'),
    path('recipe/list/', RecipeListView.as_view(), name='recipe-list'),
    path('recipe/add/', RecipeAddView.as_view()),
    path('recipe/modify/<int:id_>/', RecipeModifyView.as_view()),
    path('plan/<int:id_>/', PlanDetailsView.as_view(), name='plan_detail'),
    path('plan/add/', PlanAddView.as_view()),
    path('plan/add-recipe/', PlanAddRecipeView.as_view()),
    path('plan/list/', PlanListView.as_view()),
    path('recipe/modify/<int:id_>/', RecipeModifyView.as_view(), name='modify-recipe'),
    path('contact/', ContactView.as_view(), name='contact'),
    path('about/', AboutView.as_view(), name="about"),
]
