import datetime 

from django import forms
from django.core.exceptions import ValidationError
# Below is import for I18N and L10N
from django.utils.translation import ugettext_lazy as _

class RenewBookForm(forms.Form):
  # Based on this line it'll take any Date listed as YYYY-MM-DD, MM/DD/YYYY, MM/DD/YY
  # Rendered as a DateInput Widget 
  # It also makes a default label based off var name w/out underscores and by default with a colon at end
  renewal_date = forms.DateField(help_text="Enter a date between now and 4 weeks (default 3).")

  def clean_renewal_date(self):
    """ Common data validation pattern clean_<fieldname>() """

    # SANITIZATION STEP aka prevent shady users from poisoning links etc.
    data = self.cleaned_data['renewal_date']

    # Check if a date if not in the past.
    if data < datetime.date.today():
      # That _() as a parameter is for translating later
      raise ValidationError(_('Invalid date - renewal in past'))

    # Check if a date is in the alloweed range (+4 weeks from today).
    if data > datetime.date.today() + datetime.timedelta(weeks=4):
      raise ValidationError(_('Invalid date - renewal more than 4 weeks ahead'))

    # MUST return cleaned data
    return data

#### IF YOU WANT TO USE THE TOP ONE ITS 
#### RenewBookModelForm(initial={'renewal_date': proposed_renewal_date}
#### vs
#### RenewBookModelForm(initial={'due_back': proposed_renewal_date} 
#### BELOW

"""
If you need to simply map the fields of your model
using a form then this sort of technique will work

from catalog.models import BookInstance
class RenewBookForm(ModelForm):

  def clean_due_back(self):
    data = self.cleaned_data['due_back']

    # Check if date is not in the past
    if data < datetime.date.today():
      raise ValidationError(_('Invalid date - renewal in past'))

    # Check if date is in the allowed range (+4 weeks from today)
    if data > datetime.date.today() + datetime.timedelta(weeks=4):
      raise ValidationError(_('Invalid date - renewal more than 4 weeks ahead'))

    # Remember to always return data
    return data

  # When using this ModelForm class add in Meta for mapping
  class Meta:

    # Link to the model to grab fields
    model = BookInstance

    # Could use fields = '__all__'
    # or instead exclude, just like fields is ued
    fields = ['due_back']

    # We could further customize 
    # (more than just automatically creating it via field name etc.)
    labels = {'due_back': _('New renewal date')}
    help_texts = {'due_back': _('Enter a date between now and 4 weeks (default 3).')}
    # There's also widgets and error_messages
    """