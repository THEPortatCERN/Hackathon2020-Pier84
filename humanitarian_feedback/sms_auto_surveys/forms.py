from django import forms


class SetQuestionsFormm(forms.Form):
    """
    A form to allow the user to set and change the survey questions.
    """
    survey_title = forms.CharField(label="Survey title", max_length=100, required=True)

    question1 = forms.CharField(label="Question 1", max_length=1000, required=True)
    questiontype1 = forms.ChoiceField(label="", choices=(('yes-no', 'Yes/ No'), ('numeric', 'Numeric'), ('text', 'Text')), initial='text')
    question2 = forms.CharField(label="Question 2", max_length=1000, required=False)
    questiontype2 = forms.ChoiceField(label="", choices=(('yes-no', 'Yes/ No'), ('numeric', 'Numeric'), ('text', 'Text')), initial='text')
    question3 = forms.CharField(label="Question 3", max_length=1000, required=False)
    questiontype3 = forms.ChoiceField(label="", choices=(('yes-no', 'Yes/ No'), ('numeric', 'Numeric'), ('text', 'Text')), initial='text')
    question4 = forms.CharField(label="Question 4", max_length=1000, required=False)
    questiontype4 = forms.ChoiceField(label="", choices=(('yes-no', 'Yes/ No'), ('numeric', 'Numeric'), ('text', 'Text')), initial='text')
    question5 = forms.CharField(label="Question 5", max_length=1000, required=False)
    questiontype5 = forms.ChoiceField(label="", choices=(('yes-no', 'Yes/ No'), ('numeric', 'Numeric'), ('text', 'Text')), initial='text')
    question6 = forms.CharField(label="Question 6", max_length=1000, required=False)
    questiontype6 = forms.ChoiceField(label="", choices=(('yes-no', 'Yes/ No'), ('numeric', 'Numeric'), ('text', 'Text')), initial='text')
    question7 = forms.CharField(label="Question 7", max_length=1000, required=False)
    questiontype7 = forms.ChoiceField(label="", choices=(('yes-no', 'Yes/ No'), ('numeric', 'Numeric'), ('text', 'Text')), initial='text')
    question8 = forms.CharField(label="Question 8", max_length=1000, required=False)
    questiontype8 = forms.ChoiceField(label="", choices=(('yes-no', 'Yes/ No'), ('numeric', 'Numeric'), ('text', 'Text')), initial='text')
    question9 = forms.CharField(label="Question 9", max_length=1000, required=False)
    questiontype9 = forms.ChoiceField(label="", choices=(('yes-no', 'Yes/ No'), ('numeric', 'Numeric'), ('text', 'Text')), initial='text')
    question10 = forms.CharField(label="Question 10", max_length=1000, required=False)
    questiontype10 = forms.ChoiceField(label="", choices=(('yes-no', 'Yes/ No'), ('numeric', 'Numeric'), ('text', 'Text')), initial='text')


class InitiateSurveyForm(forms.Form):
    """
    Send a text to a list of phone numbers.
    """
    message = forms.CharField(label="SMS Message", max_length=1000, help_text="This message will be sent to the provided phone numbers.", initial="Hello, this is a text from Afdal Tawassul, we would like to ask for your feedback about assistance you recently received. If you are happy to provide your feedback, please reply to this message.")
    phone_numbers = forms.CharField(label='Phone numbers', max_length=1000, help_text="Please enter a comma-separated list of phone numbers into the form below. A survey will be sent to each phone number by SMS. The phone numbers should begin with '+' and the area code, e.g. +151234567890.")
