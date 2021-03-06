"""vacancies URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.contrib.auth.views import LogoutView
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static

from account.views import MySignupView, MyLoginView
from vacancy.resume import ResumeLetsStart, ResumeNew, ResumeView
from vacancy.views import main_view, vacancies_view, vacancies_categories_view, companies_view, \
    MyCompanyLetsStart, send_applications_view, MyCompanyView, MyCompanyNew, MyVacanciesView, MyVacancyView, \
    MyVacancyNewView, SearchVacanciesView, VacancyView
from vacancy.views import custom_handler404, custom_handler500

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', main_view, name='main'),
    path('vacancies', vacancies_view, name='vacancies'),
    path('vacancies/cat/<str:categories>', vacancies_categories_view, name='vacancies_cat'),
    path('companies/<int:company_pk>', companies_view, name='companies'),
    path('vacancies/<int:vacancy_pk>', VacancyView.as_view(), name='vacancy'),
    path('vacancies/<int:vacancy_pk>/send', send_applications_view, name='send_applications'),

    path('mycompany/letsstart', MyCompanyLetsStart.as_view(), name='company_lets_start'),
    path('mycompany/create', MyCompanyNew.as_view(), name='my_company_new'),
    path('mycompany', MyCompanyView.as_view(), name='my_company'),

    path('mycompany/vacancies/create', MyVacancyNewView.as_view(), name='my_vacancy_new'),
    path('mycompany/vacancies', MyVacanciesView.as_view(), name='my_vacancies'),
    path('mycompany/vacancies/<int:vacancy_pk>', MyVacancyView.as_view(), name='my_vacancy'),

    path('search', SearchVacanciesView.as_view(), name='search'),

    path('myresume/letsstart', ResumeLetsStart.as_view(), name='resume-create'),
    path('myresume/create', ResumeNew.as_view(), name='resume-new'),
    path('myresume', ResumeView.as_view(), name='resume-edit'),

]

urlpatterns += [
    path('register', MySignupView.as_view(), name='register'),
    path('login', MyLoginView.as_view(), name='login'),
    path('logout', LogoutView.as_view(), name='logout'),

]


if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL,
                          document_root=settings.MEDIA_ROOT)

handler500 = custom_handler500
handler404 = custom_handler404
