from django.contrib import admin

# Register your models here.
from .models import Articles,Comments,Like,Announcements,Images
# Register your models here.
admin.site.register(Articles)
admin.site.register(Comments)
admin.site.register(Like)
admin.site.register(Images)
admin.site.register(Announcements)