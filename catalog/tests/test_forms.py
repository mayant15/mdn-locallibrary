# Create tests for forms here

from django.test import TestCase
from django.utils import timezone
from catalog.models import RenewBookForm
import datetime


class RenewBookFormTest(TestCase):

    def test_renew_form_date_field_label(self):
        form = RenewBookForm()
        field_label = form.fields['renewal_date'].label
        self.assertTrue(field_label is None or field_label == 'renewal date')

    def test_renew_form_date_field_help_text(self):
        form = RenewBookForm()
        field_help_text = form.fields['renewal_date'].help_text
        required_help_text = 'Enter a date between now and 4 weeks (default 3)'
        self.assertEqual(field_help_text, required_help_text)

    def test_renew_form_date_in_past(self):
        date = datetime.date.today() - datetime.timedelta(days=1)
        form_data = {'renewal_date': date}
        form = RenewBookForm(data=form_data)
        self.assertFalse(form.is_valid())

    def test_renew_form_date_too_far_in_future(self):
        date = datetime.date.today() + datetime.timedelta(weeks=4) + datetime.timedelta(days=1)
        form_data = {'renewal_date': date}
        form = RenewBookForm(data=form_data)
        self.assertFalse(form.is_valid())

    def test_renew_form_date_today(self):
        date = datetime.date.today()
        form_data = {'renewal_date': date}
        form = RenewBookForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_renew_form_date_max(self):
        date = timezone.now() + datetime.timedelta(weeks=4)
        form_data = {'renewal_date': date}
        form = RenewBookForm(data=form_data)
        self.assertTrue(form.is_valid())
