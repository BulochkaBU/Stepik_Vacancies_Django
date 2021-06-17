from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import Http404, HttpResponseNotFound, HttpResponseServerError
from django.shortcuts import render, get_object_or_404, redirect

from django.urls import reverse
from django.utils.datetime_safe import datetime
from django.views import View


from vacancy.forms import SendApplicationsForm, MyCompanyForm, MyVacanciesForm, SearchForm
from vacancy.models import Specialty, Company, Vacancy, Application


