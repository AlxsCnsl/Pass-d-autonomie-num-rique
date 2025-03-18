from rest_framework import generics, permissions

from .models import (
    StructureType, Structure, Role, Need, Situation, Town, Street, Genre, 
    User, Workshop, Cheque
)

from .serializers import (
    StructureTypeSerializer, StructureSerializer, RoleSerializer, NeedSerializer, 
    SituationSerializer, TownSerializer, StreetSerializer, GenreSerializer, 
    UserSerializer, WorkshopSerializer, ChequeSerializer
)

# ROLE
class RoleListCreateView(generics.ListCreateAPIView):
    queryset = Role.objects.all()
    serializer_class = RoleSerializer
    permission_classes = [permissions.AllowAny]

class RoleDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Role.objects.all()
    serializer_class = RoleSerializer
    permission_classes = [permissions.AllowAny]

# NEED
class NeedListCreateView(generics.ListCreateAPIView):
    queryset = Need.objects.all()
    serializer_class = NeedSerializer
    permission_classes = [permissions.AllowAny]

class NeedDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Need.objects.all()
    serializer_class = NeedSerializer
    permission_classes = [permissions.AllowAny]

# SITUATION
class SituationListCreateView(generics.ListCreateAPIView):
    queryset = Situation.objects.all()
    serializer_class = SituationSerializer
    permission_classes = [permissions.AllowAny]

class SituationDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Situation.objects.all()
    serializer_class = SituationSerializer
    permission_classes = [permissions.AllowAny]

# TOWN
class TownListCreateView(generics.ListCreateAPIView):
    queryset = Town.objects.all()
    serializer_class = TownSerializer
    permission_classes = [permissions.AllowAny]

class TownDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Town.objects.all()
    serializer_class = TownSerializer
    permission_classes = [permissions.AllowAny]

# STREET
class StreetListCreateView(generics.ListCreateAPIView):
    queryset = Street.objects.all()
    serializer_class = StreetSerializer
    permission_classes = [permissions.AllowAny]

class StreetDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Street.objects.all()
    serializer_class = StreetSerializer
    permission_classes = [permissions.AllowAny]

# GENRE
class GenreListCreateView(generics.ListCreateAPIView):
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer
    permission_classes = [permissions.AllowAny]

class GenreDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer
    permission_classes = [permissions.AllowAny]

# STRUCTURE TYPE
class StructureTypeListCreateView(generics.ListCreateAPIView):
    queryset = StructureType.objects.all()
    serializer_class = StructureTypeSerializer
    permission_classes = [permissions.AllowAny]

class StructureTypeDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = StructureType.objects.all()
    serializer_class = StructureTypeSerializer
    permission_classes = [permissions.AllowAny]

# STRUCTURE
class StructureListCreateView(generics.ListCreateAPIView):
    queryset = Structure.objects.all()
    serializer_class = StructureSerializer
    permission_classes = [permissions.AllowAny]

class StructureDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Structure.objects.all()
    serializer_class = StructureSerializer
    permission_classes = [permissions.AllowAny]

# USER (Sécurisé, seul un admin peut créer un utilisateur)
class UserListCreateView(generics.ListCreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [permissions.AllowAny]

class UserDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [permissions.AllowAny]

# WORKSHOP
class WorkshopListCreateView(generics.ListCreateAPIView):
    queryset = Workshop.objects.all()
    serializer_class = WorkshopSerializer
    permission_classes = [permissions.AllowAny]

class WorkshopDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Workshop.objects.all()
    serializer_class = WorkshopSerializer
    permission_classes = [permissions.AllowAny]

# CHEQUE (Sécurisé, seul un admin peut créer un chèque)
class ChequeListCreateView(generics.ListCreateAPIView):
    queryset = Cheque.objects.all()
    serializer_class = ChequeSerializer
    permission_classes = [permissions.AllowAny]

class ChequeDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Cheque.objects.all()
    serializer_class = ChequeSerializer
    permission_classes = [permissions.AllowAny]
