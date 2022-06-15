import json

from django import views
from django.contrib.auth import login, authenticate
from django.contrib.auth.models import User
from django.http import HttpResponseRedirect, JsonResponse
from django.shortcuts import render
from django.templatetags.static import static
from django.urls import reverse
from django.views.generic import ListView, DetailView

from .forms import RegistrationForm, LoginForm

# Create your views here.
from .mixins import BooksJsonContextMixin
from .models import Book, Rate, Account


def is_ajax(request):
    return request.headers.get('x-requested-with') == 'XMLHttpRequest'


def check_authenticated(func):
    def check(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return HttpResponseRedirect(reverse('books'))
        return func(self, request, *args, **kwargs)

    return check





class RegistrationView(views.View):
    @check_authenticated
    def get(self, request):
        form = RegistrationForm()
        return render(request, 'auth/registration.html', {'form': form})

    @check_authenticated
    def post(self, request):
        form = RegistrationForm(request.POST)

        if form.is_valid():
            # Добавить апкаст юзера
            user = User.objects.create_user(username=form.cleaned_data['username'],
                                            password=form.cleaned_data['password'],
                                            email=form.cleaned_data['email'])

            login(request, user)
            Account.objects.create(user=user)
        return HttpResponseRedirect(reverse('registration'))  # Edit


class LoginView(views.View):
    @check_authenticated
    def get(self, request):
        form = LoginForm()
        return render(request, 'auth/login.html', {'form': form})

    @check_authenticated
    def post(self, request):
        form = LoginForm(request.POST)

        if form.is_valid():
            # Добавить апкаст юзера
            user = authenticate(username=form.cleaned_data['username'], password=form.cleaned_data['password'])
            login(request, user)
            return HttpResponseRedirect(reverse('books'))
        return render(request, 'auth/login.html', {'form': form})


class BookInfoView(BooksJsonContextMixin, DetailView):
    model = Book
    context_object_name = 'book'
    template_name = "books/book_info.html"

    def get_context_data(self, **kwargs):
        context = super(BookInfoView, self).get_context_data(**kwargs)
        context['rate'] = self.object.rates.filter(account__user=self.request.user).first()
        return context


class BooksView(BooksJsonContextMixin, ListView):
    model = Book
    template_name = 'books/books.html'
    context_object_name = 'books'


def rate_system_view(request):
    if request.method == "POST" and is_ajax(request):

        book = Book.objects.get(pk=int(request.POST['book_pk']))
        account = Account.objects.get(user=request.user)
        current_rate = book.rates.filter(account=account).first()
        rate = int(request.POST["rate"])
        if current_rate:
            current_rate.rate = rate
            current_rate.save()
        else:
            rate_book = Rate.objects.create(account=account,
                                            rate=rate,
                                            book=book)
            rate_book.save()
    return JsonResponse({}, status=200)

def add_to_reads_books(request):
    if request.method == "POST" and is_ajax(request):
        book = Book.objects.get(pk=request.POST['book_id'])
        account = Account.objects.get(user=request.user)
        if book in account.list_read_book.all():
            account.list_read_book.remove(book)
            icon_added_img_url = static('img/books_page/bookmark.png')
        else:
            account.list_read_book.add(book)
            icon_added_img_url = static('img/books_page/notebook.png')
        return JsonResponse({'icon_url' : icon_added_img_url},status=200)
        #TODO доделать добавление в прочитанное


class ProfileView(views.View):
    def get(self,request):
        return render(request,'profile/profile.html',{})