from rest_framework import serializers
from django.contrib.auth import get_user_model, password_validation
from django.contrib.auth.password_validation import validate_password
from rest_framework import status

User = get_user_model()


class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ['id', 'first_name', 'last_name', 'email', 'password']

        extra_kwargs={
            "first_name":{'required':True},
            "last_name":{'required':True},
            "email":{'required':True},
            "password":{'required':True},
        }

    def validate_password(self, value):
        password_validation.validate_password(value, self.instance)
        return value

    def create(self, validate_data):
        user = super(UserSerializer, self).create(validate_data)
        user.set_password(validate_data.get('password'))
        user.save()

        return user


class ChangePasswordSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=True, validators=[validate_password])
    password2 = serializers.CharField(write_only=True, required=True)
    old_password = serializers.CharField(write_only=True, required=True)

    class Meta:
        model = User
        fields = ('old_password', 'password', 'password2')

    def validate(self, attrs):
        if attrs['password'] != attrs['password2']:
            raise serializers.ValidationError({"password": "Password fields didn't match."})

        return attrs

    def validate_old_password(self, value):
        user = self.context['request'].user
        if not user.check_password(value):
            raise serializers.ValidationError({"old_password": "Old password is not correct"})
        return value

    def update(self, instance, validated_data):

        instance.set_password(validated_data['password'])
        instance.save()
        response = {
                'status': 'success',
                'code': status.HTTP_200_OK,
                'message': 'Password updated successfully',
            }
        print(instance)    
        return instance


class UserDetail(serializers.ModelSerializer):
    class Meta:
        model=User
        fields = ['id', 'first_name', 'last_name', 'email', 'profilePhoto']


class UpdateUserSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(required=True)
    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'email','profilePhoto')
        extra_kwargs = {
            'first_name': {'required': True},
            'last_name': {'required': True},
            'email':{'required':True},
            'profilePhoto':{'required':False}
        }

    def validate_email(self, value):
        user = self.context['request'].user
        if User.objects.exclude(pk=user.pk).filter(email=value).exists():
            raise serializers.ValidationError({"email": "This email is already in use."})
        return value
    

    def update(self, instance, validated_data):
        print('data : ', validated_data)
        user = self.context['request'].user

        if user.pk != instance.pk:
            raise serializers.ValidationError({"authorize": "You dont have permission for this user."})

        instance.first_name = validated_data['first_name']
        instance.last_name = validated_data['last_name']
        instance.email = validated_data['email']
        instance.profilePhoto = validated_data['profilePhoto']

        instance.save()

        return instance