from rest_framework import serializers
from .models import (
    StructureType, Structure, Role, Need, Situation, Town, Street, Genre, 
    User, Workshop, Cheque
)

class StructureTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = StructureType
        fields = '__all__'

class StructureSerializer(serializers.ModelSerializer):
    type = serializers.PrimaryKeyRelatedField(queryset=StructureType.objects.all())

    class Meta:
        model = Structure
        fields = '__all__'

class RoleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Role
        fields = '__all__'

class NeedSerializer(serializers.ModelSerializer):
    class Meta:
        model = Need
        fields = '__all__'

class SituationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Situation
        fields = '__all__'

class TownSerializer(serializers.ModelSerializer):
    class Meta:
        model = Town
        fields = '__all__'

class StreetSerializer(serializers.ModelSerializer):
    class Meta:
        model = Street
        fields = '__all__'

class GenreSerializer(serializers.ModelSerializer):
    class Meta:
        model = Genre
        fields = '__all__'

class UserSerializer(serializers.ModelSerializer):
    role = serializers.PrimaryKeyRelatedField(queryset=Role.objects.all())
    town = serializers.PrimaryKeyRelatedField(queryset=Town.objects.all())
    street = serializers.PrimaryKeyRelatedField(queryset=Street.objects.all())
    genre = serializers.PrimaryKeyRelatedField(queryset=Genre.objects.all())
    need = serializers.PrimaryKeyRelatedField(queryset=Need.objects.all(), allow_null=True)
    situation = serializers.PrimaryKeyRelatedField(queryset=Situation.objects.all(), allow_null=True)

    class Meta:
        model = User
        fields = '__all__'
        extra_kwargs = {'password': {'write_only': True}}

class WorkshopSerializer(serializers.ModelSerializer):
    structure = serializers.PrimaryKeyRelatedField(queryset=Structure.objects.all())

    class Meta:
        model = Workshop
        fields = '__all__'

class ChequeSerializer(serializers.ModelSerializer):
    user = serializers.PrimaryKeyRelatedField(queryset=User.objects.all(), allow_null=True)
    structure = serializers.PrimaryKeyRelatedField(queryset=Structure.objects.all(), allow_null=True)
    workshop = serializers.PrimaryKeyRelatedField(queryset=Workshop.objects.all(), allow_null=True)

    class Meta:
        model = Cheque
        fields = '__all__'
