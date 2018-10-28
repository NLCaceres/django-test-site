from django.shortcuts import render
#from django.contrib.auth.decorators import login_required

# Create your views here.
from catalog.models import Book, Author, BookInstance, Genre

# If you wanted to restrict a particular page/view if not logged in
# You can add from django.contrib.auth.decorators import login_required and
# @login_required
def index(request):
  """ View function for home page of site. """

  # Generate counts of some of the main objects
  num_books = Book.objects.all().count()
  num_instances = BookInstance.objects.all().count()

  # Available books (status = 'a')
  num_instances_available = BookInstance.objects.filter(status__exact='a').count()

  # The 'all()' is implied by default.
  num_authors = Author.objects.count()

  # Similar to rest but for genres
  num_genres = Genre.objects.count()

  # Slightly different since we're looking for a word!
  num_instances_of_word = Book.objects.filter(title__icontains='the').count()

  # Number of visits to this view, as counted in the session variable.
  num_visits = request.session.get('num_visits', 0)
  request.session['num_visits'] = num_visits + 1

  context = {
    'num_books': num_books,
    'num_instances': num_instances,
    'num_instances_available': num_instances_available,
    'num_authors': num_authors,
    'num_genres': num_genres,
    'num_instances_of_word': num_instances_of_word,
    'num_visits': num_visits,
  }

  # Render the HTML template index.html with the data in the context variable
  return render(request, 'index.html', context=context)

from django.views import generic
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin

# Maybe you don't want users to be able to see this class-based view without logging in
# Add from django.contrib.auth.mixins import LoginRequiredMixin
# Then add LoginRequiredMixin as a param to this below (It must be before the view param)
class BookListView(generic.ListView):
  # When you add LoginRequiredMixin param you can set
  # login_url = '/login/'
  # redirect_field_name = 'redirect_to'
  # To designate a path and field

  model = Book
  paginate_by = 10
  # context_object_name = 'my_book_list'   # your own name for the list as a template variable
  # queryset = Book.objects.filter(title__icontains='war')[:5] # Get 5 books containing the title war
  # template_name = 'books/my_arbitrary_template_name_list.html'  # Specify your own template name/location


  # Instead of simply calling the queryset function we can actually OVERRIDE it! Just like JAVA
  """def get_queryset(self):
    return Book.objects.filter(title__icontains='the')[:5] #Case insensitive for 'the'. Array up to fifth index.

  def get_context_data(self, **kwargs):
    # PATTERN: GET super/original context.   ADD in NEW context.   RETURN all context

    # Call base implementation first to get the context
    context = super(BookListView, self).get_context_data(**kwargs)
    # Create any data and add it to context
    context['some_data'] = 'This is just some data'
    return context
      """

class BookDetailView(generic.DetailView):
  model = Book


# Similar to the Book listview and detail view this will set up the Author version
class AuthorListView(generic.ListView):
  model = Author

class AuthorDetailView(generic.DetailView):
  model = Author

class LoanedBooksByUserListView(LoginRequiredMixin, generic.ListView):
  """ Generic class-based view listing books on loan to current user."""
  model = BookInstance
  template_name='catalog/bookinstance_list_borrowed_user.html'
  paginate_by=10

  def get_queryset(self):
      return BookInstance.objects.filter(borrower=self.request.user).filter(status__exact='o').order_by('due_back')

class BorrowedBookListView(PermissionRequiredMixin, generic.ListView):
  permission_required = 'catalog.can_mark_returned'
  model = BookInstance
  template_name = 'catalog/bookinstance_list_borrowed_books.html'
  paginate_by = 10

  def get_queryset(self):
    return BookInstance.objects.filter(status__exact='o').order_by('due_back')

import datetime

from django.contrib.auth.decorators import permission_required
from django.shortcuts import get_object_or_404
from django.http import HttpResponseRedirect
from django.urls import reverse

from catalog.forms import RenewBookForm

@permission_required('catalog.can_mark_returned')
def renew_book_librarian(request, pk):
  """View function for renewing a specific BookInstance by librarian."""
  book_instance = get_object_or_404(BookInstance, pk=pk)

  # If this is a POST request then process the Form data
  if request.method == 'POST':

    # Create a form instance and populate it with data from the request (binding):
    book_renewal_form = RenewBookForm(request.POST)

    # Check if the form is valid:
    if book_renewal_form.is_valid():
      # process the data in form.cleaned_data as required (here we just write it to the model due_back field)
      book_instance.due_back = book_renewal_form.cleaned_data['renewal_date']
      book_instance.save()

      # redirect to a new URL:
      return HttpResponseRedirect(reverse('all-borrowed'))

  # If this is a GET (or any other http method) create the default form.
  else:
    proposed_renewal_date = datetime.date.today() + datetime.timedelta(weeks=3)
    book_renewal_form = RenewBookForm(initial={'renewal_date': proposed_renewal_date})

  context = {
    'form': book_renewal_form,
    'book_instance': book_instance,
  }

  return render(request, 'catalog/book_renew_librarian.html', context)
  
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy

# BOTH CREATE AND UPDATE need fields
# BOTH use a template that is model_name_FORM.html
# E.g. author_form.html
class AuthorCreate(PermissionRequiredMixin, CreateView):
  model = Author
  # One way to get all fields of a class
  fields = '__all__'

  permission_required = 'catalog.add_author'

  # Can set init values, so really this is unnecessary 
  # but could be useful in a real situation
  initial = {'date_of_death':'05/01/2018'}

  # Feel like changing the template suffix from author_form.html?
  # Then use template_name_suffix 
  # So no more _form required! author still is though 

class AuthorUpdate(PermissionRequiredMixin, UpdateView):
  model = Author
  # or you could list all fields of a class in an array
  fields = ['first_name', 'last_name', 'date_of_birth', 'date_of_death']

  permission_required = 'catalog.change_author'

# On the other hand this expects 
# model_name_CONFIRM_DELETE.html
# e.g. auhor_confirm_delete.html
class AuthorDelete(PermissionRequiredMixin, DeleteView):
  model = Author

  permission_required = 'catalog.delete_author'

  # If success_url isn't specified it will display a page with new object and its values
  success_url = reverse_lazy('authors')
  # Reverse lazy used because it links to a class based view
  # AKA Author List View with its url-name specified in urls.py 'authors'

class BookCreate(PermissionRequiredMixin, CreateView):
  model = Book
  fields = '__all__'
  permission_required = 'catalog.add_book'

class BookUpdate(PermissionRequiredMixin, UpdateView):
  model = Book
  fields = '__all__'
  permission_required = 'catalog.change_book'

class BookDelete(PermissionRequiredMixin, DeleteView):
  model = Book
  success_url = reverse_lazy('books')
  permission_required = 'catalog.delete_book'