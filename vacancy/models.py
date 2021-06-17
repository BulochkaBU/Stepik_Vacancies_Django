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


class Application(models.Model):
    written_username = models.CharField(max_length=120)
    written_phone = models.IntegerField()
    written_cover_letter = models.TextField()
    vacancy = models.ForeignKey(Vacancy, on_delete=models.CASCADE, related_name='applications')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='applications')


class Resume(models.Model):
    class Grades(models.TextChoices):
        JUN = 'Junior'
        INT = 'Intern'
        MID = 'Middle'
        SEN = 'Senior'
        TIM = 'Team Lead'

    class Status(models.TextChoices):
        not_looking_for_a_job = 'Не ищу работу'
        considering_offers = 'Рассматриваю предложения'
        looking_for_a_job = 'Ищу работу'

    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='resume')
    name = models.CharField(max_length=120)
    surname = models.CharField(max_length=120)
    salary = models.PositiveIntegerField()
    grade = models.CharField(choices=Grades.choices, max_length=120)
    status = models.CharField(choices=Status.choices, max_length=120)
    specialty = models.ForeignKey(Specialty, on_delete=models.CASCADE, related_name='resume')
    education = models.TextField()
    experience = models.TextField()
    portfolio = models.CharField(max_length=120)


