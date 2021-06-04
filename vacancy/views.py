from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.views import LoginView
from django.http import HttpResponseNotFound, HttpResponseServerError
from django.shortcuts import render, get_object_or_404, redirect
from django.views import View
from django.views.generic import CreateView

from vacancy.forms import SendApplicationsForm
from vacancy.models import Specialty, Company, Vacancy


def main_view(request):
    count_vacancy_speciality = {}
    for code in Specialty.objects.all():
        count_vacancy_speciality[code.code] = Vacancy.objects.filter(specialty__code=code.code).count()
    count_vacancy_company = {}
    for company_id in Company.objects.all():
        count_vacancy_company[company_id.id] = Vacancy.objects.filter(company__id=company_id.id).count()
    return render(request, 'index.html', context={
        'specialties': Specialty.objects.all(),
        'companies': Company.objects.all(),
        'count_vacancy_speciality': count_vacancy_speciality,
        'count_vacancy_company': count_vacancy_company,
    })


def vacancies_view(request):
    count_vacancy = Vacancy.objects.count()
    title = "Вакансии"
    return render(request, 'vacancies.html', context={
        'title': title,
        'vacancies': Vacancy.objects.all(),
        'count_vacancy': count_vacancy,
    })


def vacancies_categories_view(request, categories):
    category = get_object_or_404(Specialty, code=categories)
    title = category.title
    vacancies = Vacancy.objects.filter(specialty__code=categories)
    count_vacancy = Vacancy.objects.filter(specialty__code=categories).count()
    return render(request, 'vacancies.html', context={
        'title': title,
        'category': category,
        'vacancies': vacancies,
        'count_vacancy': count_vacancy
    })


def companies_view(request, company_pk):
    company = get_object_or_404(Company, pk=company_pk)
    count_vacancy_company = {}
    for vacancies_in_company in Company.objects.filter(pk=company_pk):
        count_vacancy_company[vacancies_in_company.id] = Vacancy.objects.filter(
            company__id=vacancies_in_company.id).count()
    vacancies_company = Vacancy.objects.filter(company__id=vacancies_in_company.id)
    return render(request, 'company.html', context={
        'company': company,
        'count_vacancy_company': count_vacancy_company,
        'vacancies_company': vacancies_company,

    })


def vacancy_view(request, vacancy_pk):
    vacancy = get_object_or_404(Vacancy, pk=vacancy_pk)
    if request.method == 'POST':
        form = SendApplicationsForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('send_applications')
    else:
        form = SendApplicationsForm()
    return render(request, 'vacancy.html', context={
        'vacancy': vacancy,
        'form': form
    })


class MySignupView(CreateView):
    form_class = UserCreationForm
    success_url = '/'
    template_name = 'register.html'


class MyLoginView(LoginView):
    redirect_authenticated_user = True
    template_name = 'login.html'


def send_applications_view(request, vacancy_pk):
    vacancy = get_object_or_404(Vacancy, pk=vacancy_pk)
    return render(request, 'sent.html', context={'vacancy': vacancy})

def company_lets_start_view(request):
    pass


def my_company_empty_view(request):
    pass


def my_company_view(request):
    return render(request, 'my_company.html')


def my_vacancies_view(request):
    return render(request, 'my_vacancies_list.html')


def my_vacancies_empty_view(request):
    pass


def my_vacancy_view(request, vacancy_pk):
    return render(request, 'my_vacancy.html')


def custom_handler404(request, exception):
    return HttpResponseNotFound('Страницы не существует!')


def custom_handler500(request):
    return HttpResponseServerError('Ошибка сервера!')
