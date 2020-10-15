from rest_framework import serializers
from .models import Post
from users.models import User
class GetSerializer(serializers.ModelSerializer):
    user = serializers.SerializerMethodField("post_owner")
    
    class Meta:
        model=Post
        fields=['id','title','user','Student','Entreprise','promo','tags','introduction','tools','details','creating_date','approved']
    
    def post_owner(self,obj):
            user= obj.user.__str__()
            return user

class PostSerializer(serializers.ModelSerializer):
    class Meta:
        model=Post
        fields=['title','promo','tags','introduction','tools','details']