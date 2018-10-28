from django.test import TestCase

# Create your tests here
# Run ALL the tests by python manage.py test
# Run specific ones by making it test catalog.tests.file_name
# Or Even specific classes test catalog.tests.file_name.className
# Or EVEN SPECIFIC METHODS! test catalog.tests.file_name.className.test_one_plus_one
# E.g. python manage.py test catalog.tests.test_models.YourTestClass.test_false_is_false
# Need more detail add --verbosity tag with 0, 1 or 2 for increased verbage.

# If you receive a static files error
# running python manage.py collectstatic should fix it

from catalog.models import Author

# Example of properly testing 
class AuthorModelTest(TestCase):
  @classmethod
  def setUpTestData(cls):
    # Print to show reason for this particular built-in method
    # DO NOT normally use print in your tests
    print("setUpTestData: Run once to set up non-modified data for all class methods.")
    Author.objects.create(first_name='Big', last_name='Bob')
    
  def setUp(self):
    # Print to show reason for this particular built-in method
    print("setUp: Run once for every test method to setup clean data.")
    #### There's also a tearDown() method but django handles DB destruction anyway so not needed

  def test_first_name_label(self):
    author = Author.objects.get(id=1)
    field_label = author._meta.get_field('first_name').verbose_name
    # Using assert equals here gives you what label was
    # Could have used assertTrue(field_label == 'first name') but not as verbose
    self.assertEqual(field_label, 'first name')

  def test_date_of_death_label(self):
    author=Author.objects.get(id=1)
    field_label = author._meta.get_field('date_of_death').verbose_name
    # This next line will fail (ON PURPOSE) Django typically makes fields start lowercase
    self.assertEqual(field_label, 'died')

  def test_first_name_max_length(self):
    author = Author.objects.get(id=1)
    max_length = author._meta.get_field('first_name').max_length
    self.assertEqual(max_length, 100)

  def test_object_name_is_last_name_comma_first_name(self):
    author = Author.objects.get(id=1)
    expected_object_name = f'{author.last_name}, {author.first_name}'
    self.assertEqual(expected_object_name, str(author))

  def test_get_absolute_url(self):
    author = Author.objects.get(id=1)
    # This will also fail if the urlconf is not defined.
    self.assertEqual(author.get_absolute_url(), '/catalog/author/1')

  # In addition to these asserts shown, can also check 
  # assertRedirects and assertTemplateUsed