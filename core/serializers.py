from rest_framework import serializers
from core.models import *
from authAPI.serializers import UserDetail

class SubServiceSerializer(serializers.ModelSerializer):
    class Meta:
        model=SubService
        fields = ['id', 'title', 'description', 'coverPhoto', 'icon']


class ServiceSerializer(serializers.ModelSerializer):
    subServices = SubServiceSerializer(many=True)
    class Meta:
        model=Service
        fields = ['id', 'title', 'description', 'coverPhoto', 'icon', 'averagePrice' ,'subServices']

class ServiceDetailSerializer(serializers.ModelSerializer):
    subServices = SubServiceSerializer(many=True)
    class Meta:
        model=Service
        fields = ['id', 'title', 'description', 'coverPhoto', 'icon', 'averagePrice' ,'subServices']

class OptionSerializer(serializers.ModelSerializer):
    class Meta:
        model=ChoiceOption
        fields = ['id', 'title', 'taskerFiltering']


class ServiceChoiceSerializer(serializers.ModelSerializer):
    options = OptionSerializer(many=True)
    class Meta:
        model=ServiceChoice
        fields = ['id', 'title', 'type', 'options']


class TaskerSerializer(serializers.ModelSerializer):
    user = UserDetail()
    class Meta:
        model=Tasker
        fields = ['id', 'user', 'address', 'bio', 'rating', 'completedTaskCount', 'topTasker', 'supervisor', 'createdAt', 'coverPhoto']


class SubServiceDetailSerializer(serializers.ModelSerializer):
    serviceChoices = ServiceChoiceSerializer(many=True)
    class Meta:
        model=SubService
        fields = ['id', 'title', 'description', 'coverPhoto', 'icon','serviceChoices']



class SkillSerializer(serializers.ModelSerializer):
    subService = SubServiceSerializer()
    option = OptionSerializer()
    class Meta:
        model=TaskerSkill
        fields = ['id', 'tasker', 'subService', 'option', 'priceType', 'price']

class CitySerializer(serializers.ModelSerializer):
    class Meta:
        model=City
        fields = ['id', 'name']

class TaskerListSerializer(serializers.ModelSerializer):
    user = UserDetail()
    skills = SkillSerializer (many=True)
    workCities = CitySerializer(many=True)
    class Meta:
        model=Tasker
        fields = ['id', 'user', 'bio', 'rating', 'completedTaskCount', 'topTasker', 'supervisor', 'createdAt', 'coverPhoto', 'skills', 'workCities']


class CommentSerializer(serializers.ModelSerializer):
    author = UserDetail()
    subService = SubServiceSerializer()
    class Meta:
        model=Comment
        fields = ['id', 'author' , 'subService', 'text', 'rating', 'createdAt']





class OrderListSerializer(serializers.ModelSerializer):
    subService = SubServiceSerializer()
    tasker = TaskerSerializer()
    class Meta:
        model=Order
        fields = ['id', 'tasker', 'subService', 'startDate', 'address', 'status', 'createdAt', 'totalAmount']


class PhotoSerializer(serializers.ModelSerializer):
    class Meta:
        model=OrderPhoto
        fields = ['id', 'photo']


class OrderDetailSerializer(serializers.ModelSerializer):
    subService = SubServiceSerializer()
    tasker = TaskerSerializer()
    photos = PhotoSerializer(many=True)
    options = OptionSerializer(many=True)
    class Meta:
        model=Order
        fields = ['id', 'customer', 'tasker', 'subService', 'options', 'startDate', 'address', 'status', 'createdAt', 'detail', 'photos', 'totalAmount', 'discount']


class OrderCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model=Order
        fields = ['id', 'customer', 'tasker', 'options', 'reference', 'subService', 'startDate', 'address', 'status', 'createdAt', 'detail', 'photos', 'totalAmount', 'discount']

class SubBlogSerializer(serializers.ModelSerializer):
    class Meta:
        model=SubBlog
        fields = ['id', 'title', 'text']

class BlogListSerializer(serializers.ModelSerializer): 
    author = UserDetail()
    class Meta:
        model=Blog
        fields = ['id', 'author', 'title', 'description', 'coverPhoto', 'createdAt']


class BlogDetailSerializer(serializers.ModelSerializer): 
    subBlogs = SubBlogSerializer(many=True)
    author = UserDetail()
    class Meta:
        model=Blog
        fields = ['id', 'author', 'title', 'description', 'coverPhoto', 'createdAt' ,'subBlogs']
