from django.shortcuts import render
from django.views import View
from django.http import HttpResponseRedirect
from sms_auto_surveys.forms import SetQuestionsFormm
from twilio.rest import Client
from sms_auto_surveys.models import Survey, Question


class SetQuestionsView(View):
    def get(self, request):
        if not request.user.is_authenticated:
            return HttpResponseRedirect("/")
        else:
            # Get the current survey details
            first_survey = Survey.objects.last()
            initial_data = {'survey_title': first_survey}

            # Loop through the current survey questions and add them to the initial data for the form
            i = 1
            for question in Question.objects.filter(survey__id=first_survey.id).order_by('id'):
                initial_data['question'+str(i)] = question.body
                initial_data['questiontype'+str(i)] = question.kind
                i += 1

            return render(request, "set_questions_form.html", {"form": SetQuestionsFormm(initial=initial_data)})

    def post(self, request):
        form = SetQuestionsFormm(request.POST)
        if form.is_valid():

            # Get the questions for the form
            valid_form_questions = []
            for question_number in range(1, 11):
                if form.cleaned_data['question'+str(question_number)]:
                    valid_form_questions.append({'body': form.cleaned_data['question'+str(question_number)],
                                                 'kind': form.cleaned_data['questiontype'+str(question_number)]})

            # Create a new survey and save it in the database
            new_survey = Survey(title=form.cleaned_data["survey_title"])
            questions = [Question(body=question['body'],
                                  kind=question['kind'])
                         for question in valid_form_questions]
            new_survey.save()
            for question in questions:
                question.survey = new_survey
                question.save()
            new_survey.question_set.add(*questions)

            return render(request, 'set_questions_success.html')

        return render(request, 'set_questions_form.html', { 'form': form })
