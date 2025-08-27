from django.db import models

class Recipe(models.Model):
    DIFFICULTY_CHOICES = [
        ('easy', 'Easy'),
        ('medium', 'Medium'),
        ('hard', 'Hard'),
    ]
     
    title = models.CharField(max_length=200)

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

    ingredients = models.JSONField(default=list) 
    steps = models.JSONField(default=list)

    def __str__(self):
        return self.title
