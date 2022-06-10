# Generated by Django 4.0.4 on 2022-06-07 13:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('UserApp', '0004_remove_genre_book_book_genres'),
    ]

    operations = [
        migrations.AddField(
            model_name='book',
            name='count_rate_vote',
            field=models.IntegerField(default=0, verbose_name='Колл-во оценок'),
        ),
        migrations.AddField(
            model_name='book',
            name='rate',
            field=models.FloatField(default=0, verbose_name='Оценка'),
        ),
    ]