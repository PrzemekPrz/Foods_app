from django.db import models



# Create your models here.

class Recipe(models.Model):
    name = models.CharField(max_length=255)
    ingredients = models.TextField(null=True, blank=True)
    description = models.TextField(null=True, blank=True)
    instruction = models.TextField(null=True, blank=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True, null=True)    # Allow to leave field empty
    preparation_time = models.IntegerField(null=True)
    votes = models.IntegerField(default=0)

class Plan(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField(null=True, blank=True)
    created = models.DateTimeField(auto_now_add=True)

class Dayname(models.Model):
    day_name = models.CharField(max_length=16)
    order = models.IntegerField(default=0)

class Page(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField(null=True, blank=True)
    slug = models.SlugField(max_length=255, unique=True)

class RecipePlan(models.Model):
    meal_name = models.CharField(max_length=255)
    order = models.IntegerField(default=0)
    day_name_id = models.ForeignKey('Dayname', on_delete=models.CASCADE)
    plan_id = models.ForeignKey('Plan', on_delete=models.CASCADE)
    recipe_id = models.ForeignKey('Recipe', on_delete=models.CASCADE)
