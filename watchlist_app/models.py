from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator

# Create your models here.

class StreamPlatform(models.Model):
    name = models.CharField(max_length=30)
    about = models.CharField(max_length=150)
    website = models.URLField(max_length=100)
    
    def __str__(self):
        return self.name


class WatchList(models.Model):
    title = models.CharField(max_length=50)
    storyline = models.CharField(max_length=200)
    active = models.BooleanField(default=True)
    created = models.DateTimeField(auto_now_add=True)
    platform = models.ForeignKey(StreamPlatform, on_delete=models.CASCADE, related_name="watchlist")   # establishing a one-to-many relationship
    
    def __str__(self):
        return self.title


class Reviews(models.Model):
    rating = models.PositiveIntegerField(validators=[MinValueValidator(1), MaxValueValidator(5)])
    description = models.CharField(max_length=200, null=True)
    active = models.BooleanField(default=True)
    created = models.DateTimeField(auto_now_add=True)   # date time will set only once int its lifetime
    update = models.DateTimeField(auto_now=True)   # date time will set each time the object is updated
    watchlist = models.ForeignKey(WatchList, on_delete=models.CASCADE, related_name="reviews")
    
    def __str__(self):
        return f"{self.watchlist.title} - ({self.rating})"

