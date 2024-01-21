from django.shortcuts import render
from django.http import HttpResponse
from .models import Book, BookInstance, Language, Genre, Author
from django.views.generic import CreateView, DetailView, ListView
from django.urls import reverse, reverse_lazy
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.forms import UserCreationForm


# Create your views here.
def index(request):
    num_books = Book.objects.all().count()
    num_book_instance = BookInstance.objects.all().count()
    num_books_available = BookInstance.objects.filter(status__exact='a').count()

    context = {'num_books': num_books, 'num_book_instance': num_book_instance,
               'num_books_available': num_books_available}

    return render(request, 'catalogue/index.html', context=context)


class BookCreate(LoginRequiredMixin, CreateView):#book_form.html
    model = Book
    fields = '__all__'


class BookDetail(DetailView):
    model = Book

#@login_required(login_url="/accounts/login/")
@login_required
def my_view(request):
    return render(request, 'catalogue/my_view.html')


class SignUpView(CreateView):
    form_class = UserCreationForm
    success_url = reverse_lazy('login')
    template_name = 'registration/signup.html'

class CheckedOutBooksByUserView(LoginRequiredMixin, ListView):
    model = BookInstance
    template_name = 'catalogue/profile.html'
    paginate_by = 5

    def get_queryset(self):
        return BookInstance.objects.filter(borrower=self.request.user)
