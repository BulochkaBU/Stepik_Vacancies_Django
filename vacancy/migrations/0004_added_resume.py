# Generated by Django 3.2.4 on 2021-06-15 16:58

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('vacancy', '0003_changed_models_logo_and_picture'),
    ]

    operations = [
        migrations.AlterField(
            model_name='company',
            name='owner',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='auth.user'),
        ),
        migrations.CreateModel(
            name='Resume',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=120)),
                ('surname', models.CharField(max_length=120)),
                ('salary', models.PositiveIntegerField()),
                ('grade', models.CharField(choices=[('Junior', 'Jun'), ('Intern', 'Int'), ('Middle', 'Mid'), ('Senior', 'Sen'), ('Team Lead', 'Tim')], max_length=120)),
                ('status', models.CharField(choices=[('Не ищу работу', 'Not Looking For A Job'), ('Рассматриваю предложения', 'Considering Offers'), ('Ищу работу', 'Looking For A Job')], max_length=120)),
                ('education', models.TextField()),
                ('experience', models.TextField()),
                ('portfolio', models.CharField(max_length=120)),
                ('specialty', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='resume', to='vacancy.specialty')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='resume', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
