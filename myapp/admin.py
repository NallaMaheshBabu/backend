from django.contrib import admin
from .models import ImagePost,Like,CustomToken
from myapp.models import Userdata





admin.site.register(Userdata)
admin.site.register(ImagePost)
admin.site.register(CustomToken)
admin.site.register(Like)
