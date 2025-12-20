from djoser.serializers import UserCreatePasswordRetypeSerializer


class UserCreatePasswordRetypeSerializer(UserCreatePasswordRetypeSerializer):
    class Meta(UserCreatePasswordRetypeSerializer.Meta):
        fields = ['id', 'username', 'first_name', 'last_name', 'email', 'password']