from django import forms

class InitiateSurveyForm(forms.Form):
    """
    Send a text to a list of phone numbers.
    """
    message = forms.CharField(label="SMS Message", max_length=1000, help_text="This message will be sent to the provided phone numbers.", initial="Hello, this is a text from Afdal Tawassul, we would like to ask for your feedback about assistance you recently received. If you are happy to provide your feedback, please reply to this message.")
    phone_numbers = forms.CharField(label='Phone numbers', max_length=1000, help_text="Please enter a comma-separated list of phone numbers into the form below. An survey will be sent to each phone number by SMS. The phone numbers should begin with '+' and the area code, e.g. +151234567890.")
