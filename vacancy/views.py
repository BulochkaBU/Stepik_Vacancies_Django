from django.http import HttpResponseNotFound, HttpResponseServerError
from django.shortcuts import render

# Create your views here.
from vacancy.models import Specialty, Company, Vacancy


def main_view(request):
    return render(request, 'index.html', context={
        'specialties': Specialty.objects.all(),
        'companies': Company.objects.all(),

    })


def vacancies_view(request):
    count_vacancy = Vacancy.objects.count()
    return render(request, 'vacancies.html', context={
        'vacancies': Vacancy.objects.all(),
        'count_vacancy': count_vacancy,
    })


def vacancies_categories_view(request, categories):
    category = Specialty.objects.get(code=categories)
    vacancies = Vacancy.objects.filter(specialty__code="backend")
    return render(request, 'vacancies_categories.html', context={
        'category': category,
        'vacancies': vacancies,

    })


def companies_view(request, company_pk):
    company = Company.objects.get(pk=company_pk)

    return render(request, 'company.html', context={
        'company': company,
    })


def vacancy_view(request, vacancy_pk):
    return render(request, 'vacancy.html')


def custom_handler404(request, exception):
    return HttpResponseNotFound('Страница не найдена!')


def custom_handler500(request):
    return HttpResponseServerError('Ошибка сервера!')
