from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User
from django.contrib.auth.views import LoginView
from django.db.models import Count
from django.http import HttpResponseNotFound, HttpResponseServerError, Http404, HttpResponseRedirect
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse
from django.views import View
from django.views.generic import CreateView

from vacancy.forms import SendApplicationsForm, MyCompanyForm
from vacancy.models import Specialty, Company, Vacancy, Application


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
            form.save(commit=False)

            return redirect('send_applications', vacancy.id)
    else:
        form = SendApplicationsForm()
    return render(request, 'vacancy.html', context={
        'vacancy': vacancy,
        'form': form
    })


class MySignupView(CreateView):
    form_class = UserCreationForm
    success_url = '/'
    template_name = 'accounts/register.html'


class MyLoginView(LoginView):
    redirect_authenticated_user = True
    template_name = 'accounts/login.html'


def send_applications_view(request, vacancy_pk):
    vacancy = get_object_or_404(Vacancy, pk=vacancy_pk)
    return render(request, 'sent.html', context={'vacancy': vacancy})


class MyCompanyLetsStart(LoginRequiredMixin, View):
    def get(self, request):
        return render(request, 'my_company_create.html')


class MyCompanyView(LoginRequiredMixin, View):
    def get(self, request):
        try:
            company = get_object_or_404(Company, owner=request.user.id)
        except Http404:
            return redirect(reverse('company_lets_start'))
        return render(request, 'my_company.html', context={'form': MyCompanyForm(instance=company)})

    def post(self, request):
        company = get_object_or_404(Company, owner=request.user.id)
        form = MyCompanyForm(request.POST, instance=company)
        print(form.is_valid())
        if form.is_valid():
            form.save()
            return redirect('my_company')
        return render(request, 'my_company.html', context={'form': form})


class MyCompanyNew(LoginRequiredMixin, View):
    def get(self, request):
        return render(request, 'my_company.html', context={'form': MyCompanyForm})

    def post(self, request):
        form = MyCompanyForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('my_company')
        return render(request, 'my_company.html', context={'form': form})


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
