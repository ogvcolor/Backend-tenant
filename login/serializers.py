
from .models import CustomUser
from rest_framework import serializers
from django.contrib.auth import authenticate
from django.contrib.auth.hashers import make_password
from django.contrib.auth.hashers import check_password

class UserSerializer(serializers.ModelSerializer):
    '''serializer for the user object'''
    class Meta:
        model = CustomUser
        fields = ('id', 'email', 'password' )
    
    """ def create(self, validated_data):
        return User.objects.create_user(**validated_data) """


class CreateUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = '__all__'
        extra_kwargs = {
            'password': {'required': True}
        }


    def validate(self, attrs):
        email = attrs.get('email', '').strip().lower()
        if CustomUser.objects.filter(email=email).exists():
            raise serializers.ValidationError('User with this email id already exists.')
        return attrs

    def create(self, validated_data):
        # Hash the password before saving
        validated_data['password'] = make_password(validated_data['password'])
        user = CustomUser.objects.create(**validated_data)
        return user

    
class UpdateUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ('username', 'first_nam', 'last_name', 'email', 'password', 'is_active')
    
    def update(self, instance, validated_data):
        password = validated_data.pop('password')
        if password:
            instance.set_password(password)
        instance = super().update(instance, validated_data)
        return instance
    

class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(style={'input_type': 'password'}, trim_whitespace=False)

    def validate(self, attrs):
        email = attrs.get('email').lower()
        password = attrs.get('password')

        if not email or not password:
            raise serializers.ValidationError('Please give both email and password.')

        if not CustomUser.objects.filter(email=email).exists():
            raise serializers.ValidationError('Email does not exist.')

        user = authenticate(request=self.context.get('request'), email=email, password=password)

        if not user or not check_password(password, user.password):
            raise serializers.ValidationError('Wrong credentials.')

        attrs['user'] = user
        return attrs


""" class AuthSerializer(serializers.Serializer):
    '''serializer for the user authentication object'''
    username = serializers.CharField()
    password = serializers.CharField(
        style={'input_type': 'password'},
        trim_whitespace=False
    )    
    def validate(self, attrs):
        username = attrs.get('username')
        password = attrs.get('password')
        
        user = authenticate(
            request=self.context.get('request'),
            username=username,
            password=password
        )
        
        if not user:
            msg = ('Unable to authenticate with provided credentials')
            raise serializers.ValidationError(msg, code='authentication')

        attrs['user'] = user
        return  """


# Custom UserSerializer (Not used anymore)
""" UserModel = get_user_model()

class UserRegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserModel
        fields = '__all__'
    
    def create(self, clean_data):
        user_obj = UserModel.objects.create_user(email=clean_data['email'],
                                                 password=clean_data['password'])
        user_obj.username = clean_data['username']
        user_obj.save()

        return user_obj

class UserLoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField()
    ##
    def check_user(self, clean_data):
        user = authenticate(username=clean_data['email'], password=clean_data['password'])

        if not user:
            raise ValueError('user not found')
        return user

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model: UserModel
        fields = ('email', 'username') """