from django.contrib import admin
from .models import Country, Film, Person, Genre, Award, Nomination, Result
from .forms import AwardForm

admin.site.register(Film)
admin.site.register(Person)
admin.site.register(Country)
admin.site.register(Genre)

@admin.register(Award)
class AwardAdmin(admin.ModelAdmin):
    form = AwardForm
    list_display = ('name', 'year')
    search_fields = ('name',)
