from django.utils.translation import gettext_lazy as _

from django.contrib.auth.models import User
from django.db import models

from vacancies.settings import MEDIA_COMPANY_IMAGE_DIR, MEDIA_SPECIALITY_IMAGE_DIR


class Company(models.Model):
    name = models.CharField(max_length=120)
    location = models.CharField(max_length=120)
    logo = models.ImageField(upload_to=MEDIA_COMPANY_IMAGE_DIR)
    description = models.TextField()
    employee_count = models.IntegerField()
    owner = models.OneToOneField(User, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.name}'


class Specialty(models.Model):
    code = models.CharField(max_length=20)
    title = models.CharField(max_length=120)
    picture = models.ImageField(upload_to=MEDIA_SPECIALITY_IMAGE_DIR)

    def __str__(self):
        return f'{self.title}'


class Vacancy(models.Model):
    title = models.CharField(max_length=120)
    specialty = models.ForeignKey(Specialty, on_delete=models.CASCADE, related_name='vacancies')
    company = models.ForeignKey(Company, on_delete=models.CASCADE, related_name='vacancies')
    skills = models.CharField(max_length=120)
    description = models.TextField()
    salary_min = models.IntegerField()
    salary_max = models.IntegerField()
    published_at = models.DateField()

    def __str__(self):
        return f'{self.title}'


class Application(models.Model):
    written_username = models.CharField(max_length=120)
    written_phone = models.IntegerField()
    written_cover_letter = models.TextField()
    vacancy = models.ForeignKey(Vacancy, on_delete=models.CASCADE, related_name='applications')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='applications')

    def __str__(self):
        return f'{self.written_username}, {self.written_cover_letter}'


class Resume(models.Model):
    class Grades(models.TextChoices):
        INTERN = 'INT', _('Стажер')
        JUNIOR = 'JUN', _('Джуниор')
        MIDDLE = 'MID', _('Миддл')
        SENIOR = 'SNR', _('Синьор')
        LEAD = 'LD', _('Лид')

    class Status(models.TextChoices):
        not_looking_for_a_job = 'not_looking_for_a_job', _('Не ищу работу')
        considering_offers = 'considering_offers', _('Рассматриваю предложения')
        looking_for_a_job = 'looking_for_a_job', _('Ищу работу')

    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='resume')
    name = models.CharField(max_length=120)
    surname = models.CharField(max_length=120)
    salary = models.PositiveIntegerField()
    grade = models.CharField(choices=Grades.choices, max_length=4)
    status = models.CharField(choices=Status.choices, max_length=26)
    specialty = models.ForeignKey(Specialty, on_delete=models.CASCADE, related_name='resume')
    education = models.TextField()
    experience = models.TextField()
    portfolio = models.CharField(max_length=120)

    def __str__(self):
        return f'{self.name}, {self.surname} {self.experience}'
