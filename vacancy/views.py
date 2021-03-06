from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from django.db.models import Q
from django.http import Http404, HttpResponseNotFound, HttpResponseServerError
from django.shortcuts import render, get_object_or_404, redirect
from django.utils.datetime_safe import datetime
from django.utils.decorators import method_decorator
from django.views import View

from vacancy.forms import SendApplicationsForm, MyCompanyForm, MyVacanciesForm
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


class SearchVacanciesView(View):

    def get(self, request, *args, **kwargs):
        vacancies_query = self.request.GET.get('s')
        vacancies_found = Vacancy.objects.filter(
            Q(title__icontains=vacancies_query) | Q(description__icontains=vacancies_query),
        )
        return render(request, 'search.html', context={
            'vacancies_found': vacancies_found,
            'vacancies_query': vacancies_query,
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
        'count_vacancy': count_vacancy,
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


class VacancyView(View):

    def get(self, request, vacancy_pk):
        vacancy = get_object_or_404(Vacancy, pk=vacancy_pk)
        form = SendApplicationsForm()
        return render(request, 'vacancy.html', context={
            'vacancy': vacancy,
            'form': form,
        })

    @method_decorator(login_required)
    def post(self, request, vacancy_pk):
        vacancy = get_object_or_404(Vacancy, pk=vacancy_pk)
        form = SendApplicationsForm(request.POST)
        if form.is_valid():
            application = form.save(commit=False)
            form.instance.user = request.user
            form.instance.vacancy = vacancy
            application.save()
            return redirect('send_applications', vacancy.id)


def send_applications_view(request, vacancy_pk):
    return render(request, 'sent.html', context={'vacancy_pk': vacancy_pk})


class MyCompanyLetsStart(LoginRequiredMixin, View):
    def get(self, request):
        company = Company.objects.filter(owner=request.user.id).first()
        if company:
            return redirect('my_company')
        return render(request, 'my_company_create.html')


class MyCompanyView(LoginRequiredMixin, View):

    def get(self, request):
        try:
            company = get_object_or_404(Company, owner=request.user.id)
        except Http404:
            return redirect('company_lets_start')
        return render(request, 'my_company.html', context={'form': MyCompanyForm(instance=company)})

    def post(self, request):
        company = get_object_or_404(Company, owner=request.user.id)
        form = MyCompanyForm(request.POST, request.FILES, instance=company)
        if form.is_valid():
            form.save()
            messages.add_message(request, messages.SUCCESS, 'Компания успешно обновлена!')
            return redirect('my_company')
        return render(request, 'my_company.html', context={'form': form})


class MyCompanyNew(LoginRequiredMixin, View):
    def get(self, request):
        company = Company.objects.filter(owner=request.user.id).first()
        if company:
            return redirect('my_company')
        return render(request, 'my_company.html', context={'form': MyCompanyForm})

    def post(self, request):
        form = MyCompanyForm(request.POST, request.FILES)
        if form.is_valid():
            form.instance.owner = self.request.user
            form.save()
            return redirect('my_company')
        return render(request, 'my_company.html', context={'form': form})


class MyVacanciesView(LoginRequiredMixin, View):
    def get(self, request):
        company = Company.objects.filter(owner=request.user.id).first()
        if company:
            vacancy = Vacancy.objects.filter(company__owner=request.user.id)
            count_applications = {}
            for vac in vacancy:
                count_applications[vac.id] = Application.objects.filter(vacancy=vac.id).count()
            return render(request, 'my_vacancies.html',
                          context={'vacancy': vacancy, 'count_applications': count_applications})
        return redirect('company_lets_start')


class MyVacancyView(LoginRequiredMixin, View):
    def get(self, request, vacancy_pk):
        company = Company.objects.filter(owner=request.user.id).first()
        if company:
            vacancy = get_object_or_404(Vacancy, company__owner=request.user.id, id=vacancy_pk)
            count_application = Application.objects.filter(vacancy=vacancy_pk).count()
            applications = Application.objects.filter(vacancy=vacancy_pk)

            return render(request, 'my_vacancy.html', context={
                'form': MyVacanciesForm(instance=vacancy),
                'vacancy_pk': vacancy_pk,
                'count_application': count_application,
                'applications': applications,
                'vacancy': vacancy,
            })
        return redirect('company_lets_start')

    def post(self, request, vacancy_pk):
        vacancy = get_object_or_404(Vacancy, company__owner=request.user.id, id=vacancy_pk)
        form = MyVacanciesForm(request.POST, instance=vacancy)
        if form.is_valid():
            form.save()
            messages.add_message(request, messages.SUCCESS, 'Вакансия успешно обновлена!')
            return redirect('my_vacancy', vacancy_pk)
        return render(request, 'my_vacancies.html', context={'form': form})


class MyVacancyNewView(LoginRequiredMixin, View):
    def get(self, request):
        company = Company.objects.filter(owner=request.user.id).first()
        if company:
            return render(request, 'my_vacancy.html', context={'form': MyVacanciesForm})
        return redirect('company_lets_start')

    def post(self, request):
        form = MyVacanciesForm(request.POST)
        if form.is_valid():
            vacancy = form.save(commit=False)
            form.instance.published_at = datetime.now()
            company = Company.objects.filter(owner=request.user)
            for company in company:
                company_pk = company.id
            form.instance.company_id = company_pk
            vacancy.save()
            return redirect('my_vacancies')
        return render(request, 'my_vacancy.html', context={'form': form})


def custom_handler404(request, exception):
    return HttpResponseNotFound('Страницы не существует!')


def custom_handler500(request):
    return HttpResponseServerError('Ошибка сервера!')
