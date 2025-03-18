from django.urls import path
from .views import (
    StructureTypeListCreateView, StructureTypeDetailView, StructureListCreateView, StructureDetailView,
    RoleListCreateView, RoleDetailView, NeedListCreateView, NeedDetailView, SituationListCreateView, SituationDetailView,
    TownListCreateView, TownDetailView, StreetListCreateView, StreetDetailView, GenreListCreateView, GenreDetailView,
    UserListCreateView, UserDetailView, WorkshopListCreateView, WorkshopDetailView,
    ChequeListCreateView, ChequeDetailView
)


from django.urls import path
from .views import (
    StructureTypeListCreateView, StructureTypeDetailView, StructureListCreateView, StructureDetailView,
    RoleListCreateView, RoleDetailView, NeedListCreateView, NeedDetailView, SituationListCreateView, SituationDetailView,
    TownListCreateView, TownDetailView, StreetListCreateView, StreetDetailView, GenreListCreateView, GenreDetailView,
    UserListCreateView, UserDetailView, WorkshopListCreateView, WorkshopDetailView,
    ChequeListCreateView, ChequeDetailView
)

urlpatterns = [
    # ROLE
    path('roles/', RoleListCreateView.as_view(), name='role-list'),
    path('roles/<int:pk>/', RoleDetailView.as_view(), name='role-detail'),

    # NEED
    path('needs/', NeedListCreateView.as_view(), name='need-list'),
    path('needs/<int:pk>/', NeedDetailView.as_view(), name='need-detail'),

    # SITUATION
    path('situations/', SituationListCreateView.as_view(), name='situation-list'),
    path('situations/<int:pk>/', SituationDetailView.as_view(), name='situation-detail'),

    # TOWN
    path('towns/', TownListCreateView.as_view(), name='town-list'),
    path('towns/<int:pk>/', TownDetailView.as_view(), name='town-detail'),

    # STREET
    path('streets/', StreetListCreateView.as_view(), name='street-list'),
    path('streets/<int:pk>/', StreetDetailView.as_view(), name='street-detail'),

    # GENRE
    path('genres/', GenreListCreateView.as_view(), name='genre-list'),
    path('genres/<int:pk>/', GenreDetailView.as_view(), name='genre-detail'),

    # STRUCTURE TYPE
    path('structure-types/', StructureTypeListCreateView.as_view(), name='structure-type-list'),
    path('structure-types/<int:pk>/', StructureTypeDetailView.as_view(), name='structure-type-detail'),

    # STRUCTURE
    path('structures/', StructureListCreateView.as_view(), name='structure-list'),
    path('structures/<int:pk>/', StructureDetailView.as_view(), name='structure-detail'),

    # USER
    path('users/', UserListCreateView.as_view(), name='user-list'),
    path('users/<int:pk>/', UserDetailView.as_view(), name='user-detail'),

    # WORKSHOP
    path('workshops/', WorkshopListCreateView.as_view(), name='workshop-list'),
    path('workshops/<int:pk>/', WorkshopDetailView.as_view(), name='workshop-detail'),

    # CHEQUE
    path('cheques/', ChequeListCreateView.as_view(), name='cheque-list'),
    path('cheques/<int:pk>/', ChequeDetailView.as_view(), name='cheque-detail'),
]
