import random
from django.core.paginator import Paginator
from django.shortcuts import render, redirect, HttpResponse
from django.views import View
from .models import Dayname, Recipe, Plan, RecipePlan, Page


class IndexView(View):
    """
    Class displays the main page of the app
    """
    def get(self, request):
        """
        Method fetch all recipes, shuffles the list and first three in context
        """
        recipe = list(Recipe.objects.all())
        random.shuffle(recipe)
        try:
            contact = Page.objects.get(slug='contact')

        except Page.DoesNotExist:
            contact = []

        try:
            about = Page.objects.get(slug='about')
        except Page.DoesNotExist:
            about = []
        return render(request, "index.html", {'recipe': recipe[:3], 'contact': contact, 'about': about})




class ContactView(View):
    def get(self, request):
        try:
            contact = Page.objects.get(slug='contact').description.split('\n')

        except Page.DoesNotExist:
            contact = []

        try:
            about = Page.objects.get(slug='about')
        except Page.DoesNotExist:
            about = []
        return render(request, 'contact.html', {'contact': contact, 'about': about})

class AboutView(View):
    def get(self, request):
        try:
            contact = Page.objects.get(slug='contact')

        except Page.DoesNotExist:
            contact = []

        try:
            about = Page.objects.get(slug='about')
        except Page.DoesNotExist:
            about = []
        return render(request, 'about.html', {'contact': contact, 'about': about})


# class Recipes(View):    #   <- is this view being used for anything? seems to be a duplicate?
#     """
#     Class displays list of recipes
#     """
#     def get(self, request):
#         all_recipes = Recipe.objects.all()
#         return render(request, "app-recipes.html", {'recipes': all_recipes})


class DashboardView(View):
    """
    Class display dashboard view of the app
    """
    def get(self, request):
        last_plan = Plan.objects.order_by("-created")[0]
        result = {}
        for object in Dayname.objects.all():
            meals = object.recipeplan_set.filter(plan_id=last_plan.id)
            if meals.exists():
                result[object.day_name] = meals

        recipes_no = Recipe.objects.count()
        plans_count = Plan.objects.count()
        return render(request, 'dashboard.html', context={
            "recipes_no": recipes_no, 
            "plans_count":plans_count,
            'last_plan': last_plan,
            'result': result
        })


class RecipeDetailsView(View):
    """
    Class display details of recipe view of the app
    """
    def get(self, request, id_):
        """
        Creates an instance of :model: Recipe
        Renders detailed view of a recipe

        **Context**
        ``recipe``
           An instance of :model:`Recipe`.

        ``ingridients``
            A list of ingredients.

        **Template:**
        :template:`app-recipe-details.html`
        """
        try:
            recipe = Recipe.objects.get(id=id_)
            ingredients = recipe.ingredients.replace(',', '').split(' ')    # create a list of all ingredients

            return render(request, "app-recipe-details.html", {'recipe': recipe, 'ingredients': ingredients})

        except Recipe.DoesNotExist as e:    # if does not exist for some reason redirects back to recipe list
            print(f'Błąd id: {e}')
            return redirect('/recipe/list')

    def post(self, request, id_):
        """
        Creates an instance of :model: Recipe
        Redirects to detailed view of a recipe

        **Context**
        ``recipe``
           An instance of :model:`Recipe`.

        ``like_dislike``
            gets value of "vote" buttons from the template.
        """
        if not request.COOKIES.get(str(id_)):   # if cookie key = to recipe id does not exists
            like_dislike = request.POST.get('vote')
            recipe = Recipe.objects.get(id=id_)
            if like_dislike == 'like':
                recipe.votes += 1
                recipe.save()
            elif like_dislike == 'dislike':
                recipe.votes -= 1
                recipe.save()
            response = redirect(f'/recipe/{id_}/')
            # set cookie key to be recipe id - this will allow to lock voting for each recipe
            # also set value to 1 (value is irrelevant) and expiry time to 31 days - you can vote once a month
            response.set_cookie(str(id_), 1, 60 * 60 * 24 * 31)
            return response
        else:
            return redirect(f'/recipe/{id_}/')


class RecipeListView(View):
    """
    Class display list of recipe view of the app
    """
    def get(self, request):
        all_recipes = Recipe.objects.order_by('-votes', '-created') # filter by votes and dates
        paginator = Paginator(all_recipes, 50)
        page = request.GET.get('page')
        all_recipes = paginator.get_page(page)
        return render(request, "app-recipes.html", {'recipes': all_recipes})

    def post(self, request):
        search_recipe = request.POST['find']
        all_recipes = Recipe.objects.order_by('-votes', '-created').filter(name__icontains=search_recipe)  # filter by votes and dates, filtering case insensitive, will match closest matching i.e sa -> will match sandwich
        return render(request, "app-recipes.html", {'recipes': all_recipes})


class RecipeAddView(View):
    """
    Class display add recipe view of the app
    """
    def get(self, request):
        return render(request, "app-add-book.html")

    def post(self, request):
        name = request.POST['name']
        description = request.POST['description']
        preparation_time = request.POST['preparation_time']
        ingredients = request.POST['ingredients']
        instruction = request.POST['instruction']
        if name and description and instruction:
            Recipe.objects.create(name=name, description=description, preparation_time=preparation_time, ingredients=ingredients, instruction=instruction)
            return redirect('/recipe/list/', {'err': 'Dodano przepis'})
        else:
            return render(request, 'app-add-recipe.html', {'err': 'Wypełnij formularz!!!'})


class RecipeModifyView(View):
    """
    Class display recipe modify view of the app
    """
    def get(self, request, id_):
        load_recipe = Recipe.objects.get(id=id_)
        print(load_recipe.ingredients)
        return render(request, "app-edit-recipe.html", {'recipe': load_recipe})

    def post(self, request, id_):
        name = request.POST['name']
        description = request.POST['description']
        instructions = request.POST['instructions']
        ingredients = request.POST['ingredients']
        time = request.POST['preparation_time']
        if name and description and instructions:
            Recipe.objects.create(name=name, description=description, instruction=instructions, ingredients=ingredients, preparation_time=time, votes=0)
        return redirect('recipe-list')



class PlanDetailsView(View):
    def get(self, request, id_):
        """
            Creates an instance of :model: Plan
            and a dictionary with day names from
            Renders detailed view of a recipe

            **Context**

            ``current_plan``
              An instance of :model:`Plan`.

            ``result``
               A dictionary containing day names as keys and meals ad values

            **Template:**
            :template:`app-details-schedules.html`
        """
        current_plan = Plan.objects.get(id=id_)
        result = {}
        for object in Dayname.objects.all():
            meals = object.recipeplan_set.filter(plan_id=current_plan.id)
            if meals.exists():
                result[object.day_name] = meals
        return render(request, "app-details-schedules.html", {'current_plan': current_plan, 'result': result})

    def post(self, request, id_):
        """
        Gets ID of a meal from delete button value,
        deletes it and redirects back to plan detail page

        **Context**

        ``o_delete``
          gets id of meal to delete from "delete" button
        """
        to_delete = request.POST['delete']
        RecipePlan.objects.get(id=to_delete).delete()

        return redirect(f'/plan/{id_}/')
    

class PlanAddRecipeView(View):
    """
    Class display add Recipe to plan view of the app
    """
    def get(self, request):
        plans =  Plan.objects.all()
        recipes = Recipe.objects.all()
        daynames = Dayname.objects.all()
        return render(request, "app-schedules-meal-recipe.html", {
            'plans': plans, 
            'recipes': recipes, 
            'daynames': daynames
        })
        
    def post(self, request):
        plan_id = request.POST['plan_id']
        meal_name = request.POST['meal_name']
        meal_order = request.POST['order']
        recipe_id = request.POST['recipe_id']
        dayname_id = request.POST['day_id']
        if plan_id and meal_name and meal_order and recipe_id and dayname_id:
            recipeplan_new = RecipePlan()
            recipeplan_new.meal_name = meal_name
            recipeplan_new.order = meal_order
            recipeplan_new.day_name_id = Dayname.objects.get(id=dayname_id)
            recipeplan_new.plan_id = Plan.objects.get(id=plan_id)
            recipeplan_new.recipe_id = Recipe.objects.get(id=recipe_id)
            recipeplan_new.save()
            return redirect(f'/plan/{plan_id}/')
        else: 
            plans =  Plan.objects.all()
            recipes = Recipe.objects.all()
            daynames = Dayname.objects.all()
            return render(request, "app-schedules-meal-recipe.html", {
                'plans': plans, 
                'recipes': recipes, 
                'daynames': daynames,
                'err': 'Wypełnij formularz poprawnie!'
            })


class PlanAddView(View):
    """
    Class display add plan view of the app
    """
    def get(self, request):

        return render(request, 'app-add-schedules.html')

    def post(self, request):
        name = request.POST['name']
        description = request.POST['description']
        if name and description:
            plan = Plan.objects.create(name=name, description=description)
            return redirect(f'/plan/{plan.id}/')
        else:
            return render(request, 'app-add-schedules.html')



class PlanListView(View):
    """
    Class display list of plan view of the app
    """
    def get(self, request):
        all_plans = Plan.objects.order_by('name') # filter by name
        paginator = Paginator(all_plans, 50)
        page = request.GET.get('page')
        all_plans = paginator.get_page(page)
        return render(request, "app-schedules.html", {'plans': all_plans})
