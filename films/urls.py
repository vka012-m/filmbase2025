from django.urls import path
from . import views

app_name = "films"
urlpatterns = [
    path('', views.film_list, name='home'),
    path('countries/', views.country_list, name='country_list'),
    path('countries/<int:id>/', views.country_detail, name='country_detail'),
    path('countries/create/', views.country_create, name='country_create'),
    path('countries/<int:id>/update/',
         views.country_update, name='country_update'),
    path('countries/<int:id>/delete/',
         views.country_delete, name='country_delete'),
    path('countries/autocomplete/',
         views.CountryAutocomplete.as_view(), name='country_autocomplete'),

    path('genres/', views.genre_list, name='genre_list'),
    path('genres/<int:id>/', views.genre_detail, name='genre_detail'),
    path('genres/create/', views.genre_create, name='genre_create'),
    path('genres/<int:id>/update/',
         views.genre_update, name='genre_update'),
    path('genres/<int:id>/delete/',
         views.genre_delete, name='genre_delete'),

    path('films/', views.film_list, name='film_list'),
    path('films/<int:id>/', views.film_detail, name='film_detail'),
    path('films/create/', views.film_create, name='film_create'),
    path('films/<int:id>/update/',
         views.film_update, name='film_update'),
    path('film/<int:id>/delete/',
         views.film_delete, name='film_delete'),

    path('people/', views.person_list, name='person_list'),
    path('people/<int:id>/', views.person_detail, name='person_detail'),
    path('people/create/', views.person_create, name='person_create'),
    path('people/<int:id>/update/',
         views.person_update, name='person_update'),
    path('people/<int:id>/delete/',
         views.person_delete, name='person_delete'),
    path('people/autocomplete/',
         views.PersonAutocomplete.as_view(), name='person_autocomplete'),

    path('awards/', views.award_list, name='award_list'),
    path('awards/<int:id>/', views.award_detail, name='award_detail'),
    path('awards/create/', views.award_create, name='award_create'),
    path('awards/<int:id>/update/', views.award_update, name='award_update'),
    path('awards/<int:id>/delete/', views.award_delete, name='award_delete'),

    path('nominations/', views.nomination_list, name='nomination_list'),
    path('nominations/<int:id>/', views.nomination_detail, name='nomination_detail'),
    path('nominations/create/', views.nomination_create, name='nomination_create'),
    path('nominations/<int:id>/update/', views.nomination_update, name='nomination_update'),
    path('nominations/<int:id>/delete/', views.nomination_delete, name='nomination_delete'),

    path('results/', views.result_list, name='result_list'),
    path('results/<int:id>/', views.result_detail, name='result_detail'),
    path('results/create/', views.result_create, name='result_create'),
    path('results/<int:id>/update/', views.result_update, name='result_update'),
    path('results/<int:id>/delete/', views.result_delete, name='result_delete'),
]
