from django.db import models
from django.utils.text import slugify

# Utility to generate unique slugs
def generate_unique_slug(instance, new_slug=None):
    slug = new_slug or slugify(instance.title)
    Klass = instance.__class__
    qs = Klass.objects.filter(slug=slug).exclude(pk=instance.pk)
    if qs.exists():
        # append a number if slug already exists
        new_slug = f"{slug}-{qs.count() + 1}"
        return generate_unique_slug(instance, new_slug=new_slug)
    return slug

# Category model for ingredients
class Category(models.Model):
    name = models.CharField(max_length=50, unique=True)  # Veg, Non-Veg, Dairy, Dry Fruits
    slug = models.SlugField(unique=True, blank=True, null=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name

# Ingredients model
class Ingredient(models.Model):
    name = models.CharField(max_length=100)
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, blank=True)
    image = models.ImageField(upload_to='ingredients/', blank=True, null=True)

    def __str__(self):
        return self.name

# Recipe model
class Recipe(models.Model):
    DIFFICULTY_CHOICES = [
        ('easy', 'Easy'),
        ('medium', 'Medium'),
        ('hard', 'Hard'),
    ]
     
    title = models.CharField(max_length=200)
    slug = models.SlugField(unique=True, blank=True, null=True)
    
    photo1 = models.ImageField(upload_to='recipes/', blank=True, null=True)
    photo2 = models.ImageField(upload_to='recipes/', blank=True, null=True)
    photo3 = models.ImageField(upload_to='recipes/', blank=True, null=True)
    photo4 = models.ImageField(upload_to='recipes/', blank=True, null=True)
    photo5 = models.ImageField(upload_to='recipes/', blank=True, null=True)

    time = models.CharField(max_length=10)
    difficulty = models.CharField(
        max_length=10,
        choices=DIFFICULTY_CHOICES,
        default='easy'
    )

    ingredients = models.ManyToManyField(Ingredient, blank=True)
    steps = models.JSONField(default=list)

    def save(self, *args, **kwargs):
        if not self.slug:  # only create slug if empty
            self.slug = generate_unique_slug(self)
        super().save(*args, **kwargs) 


    def photos(self):
        return [p for p in [self.photo1, self.photo2, self.photo3, self.photo4, self.photo5] if p]

    def __str__(self):
        return self.title
