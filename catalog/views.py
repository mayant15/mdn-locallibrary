from django.shortcuts import render
from django.views import generic
from .models import Book, Author, BookInstance
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.mixins import PermissionRequiredMixin


def index(request):
    """
    View function for home page of site.
    """
    # Generate counts of some of the main objects
    num_books = Book.objects.all().count()
    # Available books (status = 'a')
    num_books_available = 0
    for book in Book.objects.all():
        num_books_available += book.bookinstance_set.filter(status='a').count()
    num_authors = Author.objects.count()  # The 'all()' is implied by default.

    # Number of visits to this view, as counted in the session variable
    num_visits = request.session.get('num_visits', 0)
    request.session['num_visits'] = num_visits + 1

    # Render the HTML template index.html with the data in the context variable
    return render(
        request,
        'index.html',
        context={
            'num_books': num_books,
            'num_books_available': num_books_available,
            'num_authors': num_authors,
            'num_visits': num_visits
        },
    )


# to show the book list, using a predefined view
class BookListView(generic.ListView):
    model = Book


# To show the book  details, using a predefined view
class BookDetailView(generic.DetailView):
    model = Book


# To show the author list, using a predefined view
class AuthorListView(generic.ListView):
    model = Author


# To show the author detail, using a predefined view
class AuthorDetailView(generic.DetailView):
    model = Author


# To show the borrowed books, using a predefined view
class LoanedBooksByUserListView(LoginRequiredMixin, generic.ListView):
    model = BookInstance
    template_name = 'catalog/bookinstance_list_borrowed_user.html'
    paginate_by = 10

    def get_queryset(self):
        return BookInstance.objects.filter(borrower=self.request.user).filter(status='o').order_by('due_back')


class AllLoanedBooksListView(PermissionRequiredMixin, generic.ListView):
    permission_required = 'catalog.can_mark_returned'
    model = BookInstance
    template_name = 'catalog/bookinstance_list_borrowed_all.html'
    paginate_by = 10

    def get_queryset(self):
        return BookInstance.objects.filter(status__exact='o').order_by('due_back')
