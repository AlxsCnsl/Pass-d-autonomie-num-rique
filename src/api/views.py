from rest_framework import generics, permissions, filters
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework_simplejwt.views import TokenObtainPairView
from django.core.exceptions import ObjectDoesNotExist
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework.views import APIView
from rest_framework import status
from .permissions import IsAdmin, IsDistributor, IsReceptor
from datetime import datetime
from django.utils.timezone import now
from django.db.models import Q
from math import ceil
from django.http import FileResponse, Http404
from django.shortcuts import get_object_or_404
import csv
import os
from django.conf import settings
from django.http import HttpResponse
from django.http import StreamingHttpResponse
from .models import DownloadFile


from .models import (
    StructureType, Structure, Agent, Role, Need, Situation, Town, Street, Genre, 
    Recipient, Workshop, Cheque, DownloadFile
)

from .serializers import (
    StructureTypeSerializer, StructureSerializer, StructureFilterListeSerializer, RoleSerializer, NeedSerializer, 
    SituationSerializer, TownSerializer, StreetSerializer, GenreSerializer, 
    RecipientSerializer, WorkshopSerializer, RecipientFilterListSerializer,
    ChequeSerializer, ChequeGeneratorSerializer, ChequeFilterListeSerializer, AssignChequesSerializer,
    AgentSerializer, RegisterSerializer, LoginSerializer
)

import logging
logger = logging.getLogger(__name__)

# ROLE
class RoleListCreateView(generics.ListCreateAPIView):
    queryset = Role.objects.all()
    serializer_class = RoleSerializer
    permission_classes = [permissions.IsAuthenticated, IsAdmin]

class RoleDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Role.objects.all()
    serializer_class = RoleSerializer
    permission_classes = [permissions.IsAuthenticated, IsAdmin]

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
    
class StructureFilteredListView(APIView):
    permission_classes = [permissions.AllowAny]
    def get(self, request):
        x = int(request.query_params.get('x', 20))  # éléments par page
        y = int(request.query_params.get('y', 1))   # numéro de page
        start = (y - 1) * x
        end = start + x
        filters = Q()
        if 'structure_name' in request.query_params:
            filters &= Q(name__icontains=request.query_params['structure_name'])
        if 'structure_type_name' in request.query_params:
            filters &= Q(type__name__icontains=request.query_params['structure_type_name'])
        queryset = Structure.objects.filter(filters).order_by('name')
        total_matching = queryset.count()
        page_items = queryset[start:end]
        serializer = StructureFilterListeSerializer(page_items, many=True)
        return Response({
            "total_matching": total_matching,
            "page": y,
            "per_page": x,
            "total_page": ceil(total_matching / x),
            "structures": serializer.data
        }, status=status.HTTP_200_OK)

# STRUCTURE
class StructureListCreateView(generics.ListCreateAPIView):
    queryset = Structure.objects.all()
    serializer_class = StructureSerializer
    permission_classes = [permissions.AllowAny]

class StructureDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Structure.objects.all()
    serializer_class = StructureSerializer
    permission_classes = [permissions.AllowAny]

# RECIPIENT
class RecipientListCreateView(generics.ListCreateAPIView):
    queryset = Recipient.objects.all()
    serializer_class = RecipientSerializer
    permission_classes = [permissions.AllowAny]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    filterset_fields = ['birthyear']
    search_fields = ['first_name', 'last_name']

class RecipientDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Recipient.objects.all()
    serializer_class = RecipientSerializer
    permission_classes = [permissions.AllowAny]

class RecipientFilteredListView(APIView):
    permission_classes = [permissions.AllowAny]
    def get(self, request):
        x = int(request.query_params.get('x', 20))
        y = int(request.query_params.get('y', 1))
        start = (y - 1) * x
        end = start + x
        filters = Q()
        if 'first_name' in request.query_params:
            filters &= Q(first_name__iexact=request.query_params['first_name'])
        if 'last_name' in request.query_params:
            filters &= Q(last_name__iexact=request.query_params['last_name'])
        if 'birthyear' in request.query_params:
            filters &= Q(birthyear=int(request.query_params['birthyear']))
        if 'genre' in request.query_params:
            filters &= Q(genre__name__iexact=request.query_params['genre'])
        if 'town' in request.query_params:
            filters &= Q(street__town__name__iexact=request.query_params['town'])
        if 'street' in request.query_params:
            filters &= Q(street__name__iexact=request.query_params['street'])
        if 'situation' in request.query_params:
            filters &= Q(situation__description__iexact=request.query_params['situation'])
        if 'need' in request.query_params:
            filters &= Q(need__description__iexact=request.query_params['need'])
        queryset = Recipient.objects.filter(filters).order_by('last_name')
        page_items = queryset[start:end]
        serializer = RecipientFilterListSerializer(page_items, many=True)
        total_matching = queryset.count()
        return Response({
            "total_matching": total_matching,
            "page": y,
            "per_page": x,
            "total_page": ceil(total_matching / x),
            "recipients": serializer.data
        }, status=status.HTTP_200_OK)

# WORKSHOP
class WorkshopListCreateView(generics.ListCreateAPIView):
    queryset = Workshop.objects.all()
    serializer_class = WorkshopSerializer
    permission_classes = [permissions.AllowAny]

class WorkshopDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Workshop.objects.all()
    serializer_class = WorkshopSerializer
    permission_classes = [permissions.AllowAny]

# CHEQUE
class ChequeListCreateView(generics.ListCreateAPIView):
    queryset = Cheque.objects.all()
    serializer_class = ChequeSerializer
    permission_classes = [permissions.AllowAny]

class ChequeDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Cheque.objects.all()
    serializer_class = ChequeSerializer
    permission_classes = [permissions.AllowAny]
    
    
class ChequesGenerator(APIView):
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        try:
            count = request.query_params.get("count")
            if count is None:
                return Response({"error": "Le paramètre 'count' est requis."},
                                status=status.HTTP_400_BAD_REQUEST)
            try:
                count = int(count)
                if count < 1:
                    raise ValueError
            except ValueError:
                return Response({"error": "Le paramètre 'count' doit être un nombre entier positif."},
                                status=status.HTTP_400_BAD_REQUEST)
            numbers = self.generate_numbers(count)
            date_obj = datetime.now().date()
            cheques = [Cheque(number=number, created_at=date_obj) for number in numbers]
            Cheque.objects.bulk_create(cheques)
            queryset = Cheque.objects.filter(number__in=numbers)
            serializer = ChequeGeneratorSerializer(cheques, many=True)
            file_path = self.create_csv(numbers)
            download_file = DownloadFile(name=f"cheques_{date_obj}.csv", path=file_path)
            download_file.save()
            return Response({"message": f"{count} chèques générés avec succès!", "cheques": serializer.data},
                            status=status.HTTP_201_CREATED)
        except Exception as e:
            import traceback
            print(traceback.format_exc())
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def generate_numbers(self, count: int):
        numbers = set()
        date = datetime.now()
        year = date.year
        month = date.month
        day = date.day
        sufix = f"{year}{str(month).zfill(2)}{str(day).zfill(2)}"  # Exemple 20250101
        index = 0
        while len(numbers) < count:
            prefix = str(index).zfill(4)  # Exemple 0001
            number = int(f"{sufix}{prefix}")  # Exemple 202501010001
            if not Cheque.objects.filter(number=number).exists():
                numbers.add(number)
            index += 1
        return numbers

    def create_csv(self, numbers):
        base_path = settings.DOWNLOADS_CHEQUES_CSV_ROOT
        if not os.path.exists(base_path):
            os.makedirs(base_path)
        base_name = f"cheques_{datetime.now().date()}"
        extension = ".csv"
        file_path = generate_unique_filename(base_path, base_name, extension)
        with open(file_path, mode='w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(["number"])
            for number in sorted(numbers):
                writer.writerow([number])
        return file_path
    
def generate_unique_filename( base_path, base_name, extension):
    counter = 1
    unique_name = f"{base_name}{extension}"
    unique_path = os.path.join(base_path, unique_name)
    while os.path.exists(unique_path):
        unique_name = f"{base_name}({counter}){extension}"
        unique_path = os.path.join(base_path, unique_name)
        counter += 1
    
    return unique_path

    

    
class ChequeFilteredListView(APIView):
    permission_classes = [permissions.AllowAny]
    def get(self, request):
        x = int(request.query_params.get('x', 20))
        y = int(request.query_params.get('y', 1))
        start = (y - 1) * x
        end = start + x
        filters = Q()
        if 'first_name' in request.query_params:
            filters &= Q(recipient__first_name__iexact=request.query_params['first_name'])
        if 'last_name' in request.query_params:
            filters &= Q(recipient__last_name__iexact=request.query_params['last_name'])
        if 'number_cheque' in request.query_params:
            filters &= Q(number=request.query_params['number_cheque'])
        if 'created_at' in request.query_params:
            filters &= Q(created_at__date=request.query_params['created_at'])
        if 'distribution_at' in request.query_params:
            filters &= Q(distribution_at__date=request.query_params['distribution_at'])
        if 'used_at' in request.query_params:
            filters &= Q(used_at__date=request.query_params['used_at'])
        queryset = Cheque.objects.filter(filters).order_by('number')
        page_items = queryset[start:end]
        serializer = ChequeFilterListeSerializer(page_items, many=True)
        total_matching = queryset.count()
        return Response({
            "total_matching": total_matching,
            "page": y,
            "per_page": x,
            "total_page": ceil(total_matching/x),
            "cheques": serializer.data
        }, status=status.HTTP_200_OK)
        
class AssignChequesView(APIView):
    permission_classes = [permissions.AllowAny]
    def post(self, request):
        logger.info("Received request: %s", request.data)
        serializer = AssignChequesSerializer(data=request.data)
        if not serializer.is_valid():
            logger.error("Validation error: %s", serializer.errors)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        cheque_id = serializer.validated_data['cheque_id']
        recipient_id = serializer.validated_data['recipient_id']
        try:
            cheque = Cheque.objects.get(id=cheque_id)
            logger.info("Cheque found: %s", cheque.number)
        except Cheque.DoesNotExist:
            logger.error("Cheque not found: %d", cheque_id)
            return Response({"error": "Cheque not found"}, status=status.HTTP_404_NOT_FOUND)
        try:
            recipient = Recipient.objects.get(id=recipient_id)
            logger.info("Recipient found: %s %s", recipient.first_name, recipient.last_name)
        except Recipient.DoesNotExist:
            logger.error("Recipient not found: %d", recipient_id)
            return Response({"error": "Recipient not found"}, status=status.HTTP_404_NOT_FOUND)
        if cheque.number % 10 != 0:
            logger.error("Cheque number does not start with 0: %d", cheque.number)
            return Response({"error": "Cheque number must start with 0 in the unit place"}, status=status.HTTP_400_BAD_REQUEST)
        cheque_numbers = [cheque.number + i for i in range(10)]
        cheques = Cheque.objects.filter(number__in=cheque_numbers)
        if cheques.count() < 10:
            logger.error("Not enough consecutive cheques available. Needed: %s, Found: %d", cheque_numbers, cheques.count())
            return Response({"error": "Not enough consecutive cheques available"}, status=status.HTTP_400_BAD_REQUEST)
        if cheques.filter(recipient__isnull=False).exists():
            logger.error("One or more cheques are already assigned")
            return Response({"error": "One or more cheques are already assigned"}, status=status.HTTP_400_BAD_REQUEST)
        cheques.update(recipient=recipient, distribution_at=now())
        logger.info("Successfully assigned cheques: %s", cheque_numbers)
        return Response({
            "message": "Cheques successfully assigned",
            "cheques": list(cheques.values("id", "number", "recipient_id", "distribution_at"))
        }, status=status.HTTP_200_OK)


#USER
class RegisterView(generics.CreateAPIView):
    queryset = Agent.objects.all()
    serializer_class = RegisterSerializer
    permission_classes = [permissions.AllowAny]

class LoginView(TokenObtainPairView):
    serializer_class = LoginSerializer

    def post(self, request, *args, **kwargs):
        # Appel à la méthode post de TokenObtainPairView pour obtenir le token
        response = super().post(request, *args, **kwargs)

        # Vérifier que response.data est un dictionnaire mutable
        response_data = response.data.copy() if isinstance(response.data, dict) else {}

        # Sérialiser les données reçues
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        # L'utilisateur authentifié est directement l'instance d'Agent (si l'authentification a réussi)
        user = serializer.validated_data['user']  # Utilisation de 'user' pour accéder à l'utilisateur

        logger.info(f"Utilisateur authentifié: {user}")

        # Vérifier que l'utilisateur est bien un Agent
        if isinstance(user, Agent):
            logger.info(f"Utilisateur est un Agent: {user.username}")

            # Sérialiser les informations de l'agent
            agent_serializer = AgentSerializer(user)
            response_data["user"] = agent_serializer.data
        else:
            logger.warning(f"L'utilisateur n'est pas un agent ou non authentifié.")
            response_data["user"] = None

        # Retourner la réponse finale avec les données supplémentaires
        return Response(response_data)


class AgentListView(generics.ListAPIView):
    queryset = Agent.objects.all()
    serializer_class = AgentSerializer
    permission_classes = [permissions.AllowAny]
    
class AgentDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Agent.objects.all()
    serializer_class = AgentSerializer
    permission_classes = [permissions.AllowAny]
    
@api_view(['POST'])
def logout_view(request):
    """Déconnexion en blacklistant le token"""
    try:
        refresh_token = request.data["refresh"]
        token = RefreshToken(refresh_token)
        token.blacklist()
        return Response({"message": "Déconnexion réussie"}, status=200)
    except Exception as e:
        return Response({"error": str(e)}, status=400)
    
class DownloadChequesFileView(APIView):
    permission_classes = [permissions.AllowAny]

    def get(self, request, file_name):
        file_path = os.path.join(settings.DOWNLOADS_CHEQUES_CSV_ROOT, file_name)

        if not os.path.exists(file_path):
            raise Http404("Le fichier n'existe pas.")

        response = FileResponse(open(file_path, 'rb'))
        response['Content-Disposition'] = f'attachment; filename="{file_name}"'
        return response
    