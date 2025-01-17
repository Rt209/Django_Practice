from django.contrib import admin
from .models import Item, Location, Post

class pictureAdmin(admin.ModelAdmin):
    readonly_fields = ('id',)

admin.site.register(Item)
admin.site.register(Location)
admin.site.register(Post, pictureAdmin)