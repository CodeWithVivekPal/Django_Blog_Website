from .models import Category


def create_cat(str):
    category = Category.objects.create(cat_name=str)
