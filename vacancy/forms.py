from crispy_forms.helper import FormHelper
from django import forms
from vacancy.models import Application, Company, Vacancy


class SendApplicationsForm(forms.ModelForm):
    class Meta:
        model = Application
        fields = ('written_username', 'written_phone', 'written_cover_letter')
        labels = {
            'written_username': 'Ваше имя',
            'written_phone': 'Ваш телефон',
            'written_cover_letter': 'Сопроводительное письмо',
        }


class MyCompanyForm(forms.ModelForm):
    class Meta:
        model = Company
        fields = ('name', 'logo', 'location', 'employee_count', 'description')
        labels = {
            'name': 'Название компании',
            'logo': 'Логотип',
            'location': 'География',
            'employee_count': 'Количество человек в компании',
            'description': 'Информация о компании'
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_enctype = 'multipart/form-data'


class MyVacanciesForm(forms.ModelForm):
    class Meta:
        model = Vacancy
        fields = ('title', 'specialty', 'skills', 'salary_min', 'salary_max', 'description')
        labels = {
            'title': 'Название вакансии',
            'specialty':  'Специализация',
            'skills': 'Требуемые навыки',
            'salary_min': 'Зарплата от',
            'salary_max': 'Зарплата до',
            'description': 'Описание вакансии'

        }
