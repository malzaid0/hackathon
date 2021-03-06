# Generated by Django 3.1.1 on 2020-09-09 21:58

from django.conf import settings
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Genre',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
            ],
        ),
        migrations.CreateModel(
            name='Book',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=150)),
                ('author', models.CharField(max_length=100)),
                ('release_year', models.PositiveSmallIntegerField(validators=[django.core.validators.MaxValueValidator(2020), django.core.validators.MinValueValidator(500)])),
                ('isbn', models.PositiveBigIntegerField()),
                ('img', models.ImageField(upload_to='')),
                ('added_by', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to=settings.AUTH_USER_MODEL)),
                ('genre', models.ManyToManyField(to='libraryapp.Genre')),
            ],
        ),
    ]
