from djoser.serializers import (
    UserCreatePasswordRetypeSerializer as BaseUserCreatePasswordRetypeSerializer, 
    UserSerializer as BaseUserSerializer)


# Serializer for create the user
class UserCreatePasswordRetypeSerializer(BaseUserCreatePasswordRetypeSerializer):
    class Meta(BaseUserCreatePasswordRetypeSerializer.Meta):
        fields = ['id', 'username', 'first_name', 'last_name', 'email', 'password']
        

# Serializer for getting info of current user
class UserSerializer(BaseUserSerializer):
    class Meta(BaseUserSerializer.Meta):
        fields = ['id', 'username', 'first_name', 'last_name', 'email']