from django.contrib import admin
from blog.models import Post,Comment
# Register your models here.

class PostAdmin(admin.ModelAdmin):
    fields = ['author','title','text','hotel_Main_Img','create_date','published_date']
    search_fields = ['title']
    list_filter = ['create_date','published_date']
    list_display = ['author','title','text','published_date']
    list_editable = ['title','text']


admin.site.register(Post,PostAdmin)
admin.site.register(Comment)