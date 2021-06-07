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


from vacancy.views import main_view, vacancies_view, vacancies_categories_view, companies_view, vacancy_view, \
    MySignupView, MyLoginView, MyCompanyLetsStart, my_vacancies_view, my_vacancies_empty_view, my_vacancy_view, \
    send_applications_view, MyCompanyView, MyCompanyNew
from vacancy.views import custom_handler404, custom_handler500





urlpatterns = [
    path('admin/', admin.site.urls),
    path('', main_view, name='main'),
    path('vacancies', vacancies_view, name='vacancies'),
    path('vacancies/cat/<str:categories>', vacancies_categories_view, name='vacancies_cat'),
    path('companies/<int:company_pk>', companies_view, name='companies'),
    path('vacancies/<int:vacancy_pk>', vacancy_view, name='vacancy'),
    path('vacancies/<int:vacancy_pk>/send', send_applications_view, name='send_applications'),
    path('mycompany/letsstart', MyCompanyLetsStart.as_view(), name='company_lets_start'),
    path('mycompany/create', MyCompanyNew.as_view(), name='my_company_new'),
    path('mycompany', MyCompanyView.as_view(), name='my_company'),
    path('mycompany/vacancies/create', my_vacancies_empty_view, name='my_vacancies_empty'),
    path('mycompany/vacancies', my_vacancies_view, name='my_vacancies'),
    path('mycompany/vacancies/<int:vacancy_pk>', my_vacancy_view, name='my_vacancy'),




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
