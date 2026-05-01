from rest_framework import serializers
from .models import Userdata
from .models import ImagePost,Like


class userserializer(serializers.ModelSerializer):

    class Meta:
        model=Userdata
        fields=['username','email','password']






class userSerializer(serializers.ModelSerializer):
     profiles=serializers.SerializerMethodField()
     class Meta:
        model=Userdata
        fields=['username','profiles']
     def get_profiles(self, obj):
        request = self.context.get('request')
        if obj.profiles and request:
            return request.build_absolute_uri(obj.profiles.url)
        return None
    
    


class searchSerializer(serializers.ModelSerializer):
    image=serializers.SerializerMethodField()
    liked=serializers.SerializerMethodField()
    user=userSerializer()
    def get_image(self, obj):
        request = self.context.get('request')  # Get request object
        if obj.image:  # Ensure there's an image
            return request.build_absolute_uri(obj.image.url)  # Full URL with IP
        return None
    def get_liked(self,obj):
        request=self.context.get('request')
        if request and request.user.is_authenticated:
            print(request.user)
            return Like.objects.filter(user=request.user,post=obj.id).exists()
        return False
    class Meta:
        model = ImagePost
        fields = ['id','image','title','description','liked','totallikes','user']




class ImagePostSerializer(serializers.ModelSerializer):
    class Meta:
        model = ImagePost
        fields = ['user','image','title','description']
    def create(self,validated_data):
        user=self.context['request'].user
        return ImagePost.objects.create(user=user,**validated_data)


class loginserializer(serializers.Serializer):
    email=serializers.EmailField()
    password=serializers.CharField()

class profileserializer(serializers.ModelSerializer):
     profiles=serializers.SerializerMethodField()
     class Meta:
        model=Userdata
        fields=['profiles','username']
     def get_profiles(self, obj):
        request = self.context.get('request')
        if obj.profiles and request:
            return request.build_absolute_uri(obj.profiles.url)
        return None

class postdataS(serializers.ModelSerializer):
    image=serializers.SerializerMethodField()

    def get_image(self, obj):
        request = self.context.get('request')  # Get request object
        if obj.image:  # Ensure there's an image
            return request.build_absolute_uri(obj.image.url)  # Full URL with IP
        return None
    class Meta:
        model = ImagePost
        fields = ['id','image','title']
