from dal import autocomplete
from django.shortcuts import get_object_or_404, redirect, render
from django.contrib.auth.decorators import user_passes_test
from .models import Country, Film, Genre, Person
from .forms import CountryForm, GenreForm, FilmForm, PersonForm
from .models import Award, Nomination, Result
from .forms import AwardForm, NominationForm, ResultForm
from .helpers import paginate
from django.contrib import messages


def check_admin(user):
    return user.is_superuser


def country_list(request):
    countries = Country.objects.all()
    return render(request, 'films/country/list.html', {'countries': countries})


def country_detail(request, id):
    country = get_object_or_404(Country, id=id)
    films = Film.objects.filter(country=country)

    films = paginate(request, films)
    return render(request, 'films/country/detail.html',
                  {'country': country, 'films': films})


@user_passes_test(check_admin)
def country_create(request):
    if request.method == 'POST':
        form = CountryForm(request.POST)
        if form.is_valid():
            country = form.save()
            messages.success(request, 'Страна добавлена')
            return redirect('films:country_detail', id=country.id)
    else:
        form = CountryForm()
    return render(request, 'films/country/create.html', {'form': form})


@user_passes_test(check_admin)
def country_update(request, id):
    country = get_object_or_404(Country, id=id)
    if request.method == 'POST':
        form = CountryForm(request.POST, instance=country)
        if form.is_valid():
            form.save()
            messages.success(request, 'Страна изменена')
            return redirect('films:country_detail', id=country.id)
    else:
        form = CountryForm(instance=country)
    return render(request, 'films/country/update.html',
                  {'form': form})


@user_passes_test(check_admin)
def country_delete(request, id):
    country = get_object_or_404(Country, id=id)
    if request.method == 'POST':
        country.delete()
        messages.success(request, 'Страна удалена')
        return redirect('films:country_list')
    return render(request, 'films/country/delete.html',
                  {'country': country})


def genre_list(request):
    genres = Genre.objects.all()
    return render(request, 'films/genre/list.html', {'genres': genres})


def genre_detail(request, id):
    genre = get_object_or_404(Genre, id=id)
    films = Film.objects.filter(genres=genre)

    films = paginate(request, films)
    return render(request, 'films/genre/detail.html',
                  {'genre': genre, 'films': films})


@user_passes_test(check_admin)
def genre_create(request):
    if request.method == 'POST':
        form = GenreForm(request.POST)
        if form.is_valid():
            genre = form.save()
            messages.success(request, 'Жанр добавлен')
            return redirect('films:genre_detail', id=genre.id)
    else:
        form = GenreForm()
    return render(request, 'films/genre/create.html', {'form': form})


@user_passes_test(check_admin)
def genre_update(request, id):
    genre = get_object_or_404(Genre, id=id)
    if request.method == 'POST':
        form = GenreForm(request.POST, instance=genre)
        if form.is_valid():
            form.save()
            messages.success(request, 'Жанр изменён')
            return redirect('films:genre_detail', id=genre.id)
    else:
        form = GenreForm(instance=genre)
    return render(request, 'films/genre/update.html',
                  {'form': form})


@user_passes_test(check_admin)
def genre_delete(request, id):
    genre = get_object_or_404(Genre, id=id)
    if request.method == 'POST':
        genre.delete()
        messages.success(request, 'Жанр удалён')
        return redirect('films:genre_list')
    return render(request, 'films/genre/delete.html',
                  {'genre': genre})


def film_list(request):
    films = Film.objects.all()
    query = request.GET.get('query', '')
    if query:
        films = films.filter(name__icontains=query)
    films = paginate(request, films)
    return render(request, 'films/film/list.html', {'films': films,
                                                    'query': query})


def film_detail(request, id):
    queryset = Film.objects.prefetch_related(
        "country", "genres", "director", "people",
        "results__nomination__award"
    )
    film = get_object_or_404(queryset, id=id)
    awards_results = film.results.all()
    return render(request, 'films/film/detail.html',
                  {'film': film, 'awards_results': awards_results})


@user_passes_test(check_admin)
def film_create(request):
    if request.method == 'POST':
        form = FilmForm(request.POST, request.FILES)
        if form.is_valid():
            film = form.save()
            messages.success(request, 'Фильм добавлен')
            return redirect('films:film_detail', id=film.id)
    else:
        form = FilmForm()
    return render(request, 'films/film/create.html', {'form': form})


@user_passes_test(check_admin)
def film_update(request, id):
    film = get_object_or_404(Film, id=id)
    if request.method == 'POST':
        form = FilmForm(request.POST, request.FILES, instance=film)
        if form.is_valid():
            form.save()
            messages.success(request, 'Фильм изменён')
            return redirect('films:film_detail', id=film.id)
    else:
        form = FilmForm(instance=film)
    return render(request, 'films/film/update.html',
                  {'form': form})


@user_passes_test(check_admin)
def film_delete(request, id):
    film = get_object_or_404(Film, id=id)
    if request.method == 'POST':
        film.delete()
        messages.success(request, 'Фильм удалён')
        return redirect('films:film_list')
    return render(request, 'films/film/delete.html',
                  {'film': film})


def person_list(request):
    people = Person.objects.all()
    query = request.GET.get('query', '')
    if query:
        people = people.filter(name__icontains=query)
    people = paginate(request, people)
    return render(request, 'films/person/list.html', {'people': people,
                                                      'query': query})


def person_detail(request, id):
    queryset = Person.objects.prefetch_related(
        "film_set", "directed_films",
        "results__nomination__award"
    )
    person = get_object_or_404(queryset, id=id)
    awards_results = person.results.all()
    return render(request, 'films/person/detail.html',
                  {'person': person, 'awards_results': awards_results})


@user_passes_test(check_admin)
def person_create(request):
    if request.method == 'POST':
        form = PersonForm(request.POST, request.FILES)
        if form.is_valid():
            person = form.save()
            messages.success(request, 'Персона добавлена')
            return redirect('films:person_detail', id=person.id)
    else:
        form = PersonForm()
    return render(request, 'films/person/create.html', {'form': form})


@user_passes_test(check_admin)
def person_update(request, id):
    person = get_object_or_404(Person, id=id)
    if request.method == 'POST':
        form = PersonForm(request.POST, request.FILES, instance=person)
        if form.is_valid():
            form.save()
            messages.success(request, 'Персона изменена')
            return redirect('films:person_detail', id=person.id)
    else:
        form = PersonForm(instance=person)
    return render(request, 'films/person/update.html',
                  {'form': form})


@user_passes_test(check_admin)
def person_delete(request, id):
    person = get_object_or_404(Person, id=id)
    if request.method == 'POST':
        person.delete()
        messages.success(request, 'Персона удалена')
        return redirect('films:person_list')
    return render(request, 'films/person/delete.html',
                  {'person': person})


class PersonAutocomplete(autocomplete.Select2QuerySetView):
    def get_queryset(self):
        people = Person.objects.all()
        if self.q:
            people = people.filter(name__istartswith=self.q)
        return people


class CountryAutocomplete(autocomplete.Select2QuerySetView):
    def get_queryset(self):
        countries = Country.objects.all()
        if self.q:
            countries = countries.filter(name__istartswith=self.q)
        return countries

def award_list(request):
    query = request.GET.get('query', '').strip()
    year_query = request.GET.get('year', '').strip()

    awards = Award.objects.all().order_by('-year', 'name')

    if query:
        awards = awards.filter(name__icontains=query)

    if year_query.isdigit():
        awards = awards.filter(year=int(year_query))

    context = {
        'awards': awards,
        'query': query,
        'year_query': year_query,
    }
    return render(request, 'films/award_list.html', context)

def award_detail(request, id):
    award = get_object_or_404(Award, id=id)
    nominations = Nomination.objects.filter(award=award).prefetch_related('results') # Оптимизация запроса
    return render(request, 'films/award/detail.html', {'award': award, 'nominations': nominations})

@user_passes_test(check_admin)
def award_create(request):
    if request.method == 'POST':
        form = AwardForm(request.POST)
        if form.is_valid():
            award = form.save()
            messages.success(request, 'Премия добавлена')
            return redirect('films:award_detail', id=award.id)
    else:
        form = AwardForm()
    return render(request, 'films/award/create.html', {'form': form})

@user_passes_test(check_admin)
def award_update(request, id):
    award = get_object_or_404(Award, id=id)
    if request.method == 'POST':
        form = AwardForm(request.POST, instance=award)
        if form.is_valid():
            form.save()
            messages.success(request, 'Премия изменена')
            return redirect('films:award_detail', id=award.id)
    else:
        form = AwardForm(instance=award)
    return render(request, 'films/award/update.html', {'form': form})

@user_passes_test(check_admin)
def award_delete(request, id):
    award = get_object_or_404(Award, id=id)
    if request.method == 'POST':
        award.delete()
        messages.success(request, 'Премия удалена')
        return redirect('films:award_list')
    return render(request, 'films/award/delete.html', {'award': award})

def nomination_list(request):
    nominations = Nomination.objects.select_related('award').all()
    return render(request, 'films/nomination/list.html', {'nominations': nominations})

def nomination_detail(request, id):
    nomination = get_object_or_404(Nomination, id=id)
    results = Result.objects.filter(nomination=nomination).select_related('person', 'film')
    return render(request, 'films/nomination/detail.html', {'nomination': nomination, 'results': results})

@user_passes_test(check_admin)
def nomination_create(request):
    if request.method == 'POST':
        form = NominationForm(request.POST)
        if form.is_valid():
            nomination = form.save()
            messages.success(request, 'Номинация добавлена')
            return redirect('films:nomination_detail', id=nomination.id)
    else:
        form = NominationForm()
    return render(request, 'films/nomination/create.html', {'form': form})

@user_passes_test(check_admin)
def nomination_update(request, id):
    nomination = get_object_or_404(Nomination, id=id)
    if request.method == 'POST':
        form = NominationForm(request.POST, instance=nomination)
        if form.is_valid():
            form.save()
            messages.success(request, 'Номинация изменена')
            return redirect('films:nomination_detail', id=nomination.id)
    else:
        form = NominationForm(instance=nomination)
    return render(request, 'films/nomination/update.html', {'form': form})

@user_passes_test(check_admin)
def nomination_delete(request, id):
    nomination = get_object_or_404(Nomination, id=id)
    if request.method == 'POST':
        nomination.delete()
        messages.success(request, 'Номинация удалена')
        return redirect('films:nomination_list')
    return render(request, 'films/nomination/delete.html', {'nomination': nomination})

def result_list(request):
    results = Result.objects.select_related('nomination', 'person', 'film').all()
    return render(request, 'films/result/list.html', {'results': results})

def result_detail(request, id):
    result = get_object_or_404(Result, id=id)
    return render(request, 'films/result/detail.html', {'result': result})

@user_passes_test(check_admin)
def result_create(request):
    if request.method == 'POST':
        form = ResultForm(request.POST)
        if form.is_valid():
            result = form.save()
            messages.success(request, 'Результат добавлен')
            return redirect('films:result_detail', id=result.id)
    else:
        form = ResultForm()
    return render(request, 'films/result/create.html', {'form': form})

@user_passes_test(check_admin)
def result_update(request, id):
    result = get_object_or_404(Result, id=id)
    if request.method == 'POST':
        form = ResultForm(request.POST, instance=result)
        if form.is_valid():
            form.save()
            messages.success(request, 'Результат изменён')
            return redirect('films:result_detail', id=result.id)
    else:
        form = ResultForm(instance=result)
    return render(request, 'films/result/update.html', {'form': form})

@user_passes_test(check_admin)
def result_delete(request, id):
    result = get_object_or_404(Result, id=id)
    if request.method == 'POST':
        result.delete()
        messages.success(request, 'Результат удален')
        return redirect('films:result_list')
    return render(request, 'films/result/delete.html', {'result': result})