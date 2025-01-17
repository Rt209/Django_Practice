from django.db import models

class Location(models.Model):
    locationName = models.CharField(max_length=100,
                                    unique=True) #不得重複
    def __str__(self):
        return self.locationName
    
class Item(models.Model):
    itemName = models.CharField(max_length=100)
    date_added = models.DateField(auto_now_add=True) #當前時間
    itemLocation = models.ForeignKey(to=Location,
                                     on_delete=models.CASCADE)
    
    def __str__(self):
        return self.itemName

#install Pillow
class Post(models.Model):
    picture = models.ImageField(upload_to='captured_images/',
                                null=True,
                                blank=True) #media\captured_imaged
    upload_time = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Picture{self.id}"

from django.db import models

class Inventory(models.Model):
    name = models.CharField(max_length=200)  # ItemName
    location = models.CharField(max_length=100)  # ItemLocation

    def __str__(self):
        return self.name

    