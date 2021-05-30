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
from django.urls import path

from vacancy.views import main_view, vacancies_view, vacancies_categories_view, companies_view, vacancy_view
from vacancy.views import custom_handler404, custom_handler500

urlpatterns = [
    path('', main_view, name='main'),
    path('vacancies', vacancies_view, name='vacancies'),
    path('vacancies/cat/<str:categories>', vacancies_categories_view, name='vacancies_cat'),
    path('companies/<int:company_pk>', companies_view, name='companies'),
    path('vacancies/<int:vacancy_pk>', vacancy_view, name='vacancy'),

]

handler500 = custom_handler500
handler404 = custom_handler404
