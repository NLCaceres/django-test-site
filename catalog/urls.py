from django.urls import path, re_path
from catalog import views

urlpatterns = [
	# Open single quote is home page
	path('', views.index, name='index'),

	path('books/', views.BookListView.as_view(), name='books'),
	# This line below specifies a variable to grab and put in the URL
	# More specifically the first half defines that its an int
	# The second half specifies the name of the variable 'pk'
	# It is also possible to just say <pk> (short for primary key) without specifiying the type
	path('book/<int:pk>', views.BookDetailView.as_view(), name='book-detail'),
	# In cases where RegEx is required use re_path (re being short for RegEx)
	# All these reg expressions will begin with  r'^
	# So we could have wrote re_path(r'^book/(?P<pk>\d+)$', foo, bar)
	# IT DOES REQUIRE AN IMPORT THOUGH! 

	# Small note: $ matches the end of a text so re^'(bar)$' might match fooBAR 
	# (would have to check case insensitive)
	# In fact (NOW MEGA-NEW-TO-ME) the ^ actually is used to match beginning of text

	# [] is used to match one of the patterns within it
	# so [-\w] will match either a '-' or a word

	# One I haven't seen before is ?P<var-name>
	# It simply captures the pattern that follows 
	# and sends a var to the view named var-name or in this 'pk'
	# It's worth noting that it sends the var as a string so convert as needed

	# EXTRA OPTIONS FOR THESE PATHS
	# You can also pass in a third parameter into the argument
	# A Dictionary that contains a name of a template as the key and a path as the value
	# This is used to reuse views and configure the behavior 
	# E.g. path('books/', views.reusedTemplateView, '{some_template : urlPath}, name='aURL')) vs
	# path('books/', views.reusedTemplateView, '{some_template: otherURLPath}, name='otherURL')
	# BUT BE CAREFUL if you re-use names because these will be sent as variables that step on each other


	path('authors/',views.AuthorListView.as_view(),name='authors'), 
	re_path(r'^author/(?P<pk>\d+)$', views.AuthorDetailView.as_view(),name='author-detail'),

	# Users
	path('mybooks/', views.LoanedBooksByUserListView.as_view(), name='my-borrowed'),

	# Librarian only views
	path('borrowed/', views.BorrowedBookListView.as_view(), name='all-borrowed'),
	path('book/<uuid:pk>/renew/', views.renew_book_librarian, name='renew-book-librarian'),


	# FORMS
	path('author/create/', views.AuthorCreate.as_view(), name='author_create'),
	path('author/<int:pk>/update/', views.AuthorUpdate.as_view(), name='author_update'),
	path('author/<int:pk>/delete/', views.AuthorDelete.as_view(), name='author_delete'),

	path('books/create/', views.BookCreate.as_view(), name='book_create'),
	path('book/<int:pk>/update/', views.BookUpdate.as_view(), name='book_update'),
	path('book/<int:pk>/delete/', views.BookDelete.as_view(),name='book_delete'),
]