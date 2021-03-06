# Generated by Django 3.1.1 on 2020-09-10 03:00

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('libraryapp', '0004_auto_20200910_0528'),
    ]

    operations = [
        migrations.AlterField(
            model_name='bookborrow',
            name='book',
            field=models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='libraryapp.book'),
        ),
        migrations.AlterField(
            model_name='bookborrow',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to=settings.AUTH_USER_MODEL),
        ),
    ]
