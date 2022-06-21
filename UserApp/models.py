from django.contrib.auth.models import User
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
genre_choices = (
        ("Детектив", "Детектив"),
        ("Фантастика", "Фантастика"),
        ("Приключения", "Приключения"),
        ("Роман", "Роман"),
        ("Научная книга", "Научная книга"),
        ("Фольклор", "Фольклор"),
        ("Юмор", "Юмор"),
        ("Справочная книга", "Справочная книга"),
        ("Поэзия", "Поэзия"),
        ("Детская книга", "Детская книга"),
        ("Документальная литература", "Документальная литература"),
        ("Деловая литература", "Деловая литература"),
        ("Религиозная литература", "Религиозная литература"),
        ("Учебная книга", "Учебная книга"),
        ("Книги о психологии", "Книги о психологии"),
        ("Хобби", "Хобби"),
        ("Зарубежная", "Зарубежная"),
        ("Техника", "Техника"),
    )

# Create your models here.
class Account(models.Model):
    # Разобраться с профилем придумать идеи
    sex_choise = (
        ('мужской','мужской'),
        ('женский','женский')
    )
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    avatar = models.ImageField(upload_to='account/avatar', default='../static/img/books_page/logo.png',verbose_name='Фото профиля')
    list_read_book = models.ManyToManyField('Book', verbose_name='Прочитанные книги',related_name='users_read_this_book',blank=True)
    status = models.CharField(max_length=50,verbose_name='Статус',null=True,blank=True)
    age = models.IntegerField(verbose_name='Возраст',validators=[MinValueValidator(16)],null=True,blank=True)
    region = models.CharField(max_length=20,verbose_name='Регион',blank=True,null=True)
    sex = models.CharField(max_length=7,choices=sex_choise,null=True,blank=True)
    about_me = models.CharField(max_length=1000,verbose_name='Обо мне',blank=True,null=True)
    likes_genre = models.ManyToManyField('Genre',verbose_name='Любимые жанры', null=True,blank=True)
    favorite_book = models.OneToOneField('Book',on_delete=models.CASCADE,verbose_name='Любая книга',null=True,blank=True)
    def __str__(self):
        return self.user.username


class Genre(models.Model):

    name = models.CharField(max_length=40, choices=genre_choices, verbose_name='Жанр', unique=True)

    def __str__(self):
        return self.name

class Rate(models.Model):
    account = models.ForeignKey(Account, on_delete=models.CASCADE, verbose_name='Пользователь')
    rate = models.IntegerField(default=0, verbose_name='Оценка',validators=[MinValueValidator(0),MaxValueValidator(5)])
    book = models.ForeignKey('Book', on_delete=models.CASCADE, verbose_name='Книга', related_name='rates')

    class Meta:
        unique_together = ('account', 'book',)

    def __str__(self):
        return f"{self.account.user.username} оценил {self.book.name} на {self.rate}"

class Book(models.Model):
    name = models.CharField(max_length=40, verbose_name='Название книги')
    author = models.CharField(max_length=40, verbose_name='Автор')
    genres = models.ManyToManyField(Genre, related_name='books')
    description = models.TextField(verbose_name='Описание')
    cover = models.ImageField(upload_to='books/cover', verbose_name='Обложка книги')
    file = models.FileField(upload_to='books/text_files/', verbose_name='Файл книги')

    def __str__(self):
        return f"{self.author} - {self.name}"