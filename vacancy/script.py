import os

import django

os.environ["DJANGO_SETTINGS_MODULE"] = 'vacancies.settings'
django.setup()

if __name__ == '__main__':

    from vacancy import data
    from vacancy.models import Company, Specialty, Vacancy
    from vacancy.data import specialties, companies

    for companies_data in data.companies:
        companies = Company.objects.create(
            name=companies_data['title'],
            location=companies_data['location'],
            logo=companies_data['logo'],
            description=companies_data['description'],
            employee_count=companies_data['employee_count'],
        )

    for specialties_data in data.specialties:
        specialties = Specialty.objects.create(
            code=specialties_data['code'],
            title=specialties_data['title'],
        )

# for vacancy_data in data.jobs:
#     vacancies = Vacancy.objects.create(
#         title=vacancy_data['title'],
#         specialty=specialties,
#         company=companies,
#         skills=vacancy_data['skills'],
#         description=vacancy_data['description'],
#         salary_min=vacancy_data['salary_from'],
#         salary_max=vacancy_data['salary_to'],
#         published_at=vacancy_data['posted'],
#     )

    update_logo = Company.objects.all().update(logo="https://place-hold.it/100x60")
    delete_vacancy = Vacancy.objects.all().delete()

 for vacancy_data in data.jobs:
     vacancies = Vacancy.objects.create(
         title=vacancy_data['title'],
         specialty=Specialty.objects.get(code=vacancy_data['specialty']),
         company=Company.objects.get(id=vacancy_data['company']),
         skills=vacancy_data['skills'],
         description=vacancy_data['description'],
         salary_min=vacancy_data['salary_from'],
         salary_max=vacancy_data['salary_to'],
         published_at=vacancy_data['posted'],
     )
