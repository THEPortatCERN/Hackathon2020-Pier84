from django.test import TestCase
from sms_auto_surveys.models import Survey, Question, QuestionResponse
from django.urls import reverse
from django.contrib import auth


class SurveyUnauthenticatedTest(TestCase):

    def setUp(self):
        self.survey = Survey(title='A testing survey')
        self.survey.save()
        self.question = Question(body='A Question',
                                 kind=Question.TEXT, survey=self.survey)
        self.question.save()

    def test_show_survey_redirect(self):
        response = self.client.get(reverse('survey',
                                   kwargs={'survey_id': self.survey.id}))

        self.assertEqual(response.status_code, 200)


class SurveyRedirectionTest(TestCase):

    def setUp(self):
        # Create a new user
        self.credentials = {'email': 'logintest@example.com',
                            'password': 'j@PsnJ8H9cprxmn'}
        self.login_credentials = {'username': 'logintest@example.com',
                                  'password': 'j@PsnJ8H9cprxmn'}
        User = auth.get_user_model()
        user = User.objects.create_user(**self.credentials)
        self.client.login(**self.login_credentials)

        # Setup the survey
        self.survey = Survey(title='A testing survey')
        self.survey.save()
        self.question = Question(body='A Question',
                                 kind=Question.TEXT, survey=self.survey)
        self.question.save()

    def test_default_entry_point_redirection(self):
        response = self.client.post(reverse('first_survey'))
        expected_url = reverse('survey', kwargs={'survey_id': self.survey.id})

        assert expected_url in response.url

    def test_redirects_to_save_response_due_session_variable(self):
        session = self.client.session
        session['answering_question_id'] = self.question.id
        session.save()

        response = self.client.post(reverse('first_survey'))

        expected_url = reverse('save_response',
                               kwargs={'survey_id': self.question.survey.id,
                                       'question_id': self.question.id})
        assert expected_url in response.url

    def test_show_message_verb_on_sms(self):
        response = self.client.get(reverse('survey',
                                   kwargs={'survey_id': self.survey.id}),
                                   {'MessageSid': '123'})

        assert '<Message>' in response.content.decode('utf8')
        assert '<Say>' not in response.content.decode('utf8')

    def test_show_survey(self):
        response = self.client.get(reverse('survey',
                                   kwargs={'survey_id': self.survey.id}))

        assert self.survey.title in response.content.decode('utf8')

    def test_redirect_to_first_question(self):
        response = self.client.get(reverse('survey', kwargs={'survey_id':
                                   self.survey.id}))

        url_parameters = {'survey_id': self.survey.id,
                          'question_id': self.question.id}
        redirect_url = reverse('question', kwargs=url_parameters)

        assert redirect_url in response.content.decode('utf8')


class SurveyResultsTest(TestCase):

    def setUp(self):
        # Create a new user
        self.credentials = {'email': 'logintest@example.com',
                            'password': 'j@PsnJ8H9cprxmn'}
        self.login_credentials = {'username': 'logintest@example.com',
                                  'password': 'j@PsnJ8H9cprxmn'}
        User = auth.get_user_model()
        user = User.objects.create_user(**self.credentials)
        self.client.login(**self.login_credentials)

        # Setup the survey
        self.survey = Survey.objects.create(title='A testing survey')
        self.question = Question(body='Question one',
                                 kind=Question.TEXT, survey=self.survey)
        self.question.save()
        QuestionResponse(response='gopher://audio.mp3',
                         call_sid='sup3runiq3',
                         phone_number='+14155552671',
                         question=self.question).save()

    def test_render_context(self):
        survey_results_url = reverse('survey_results', kwargs={'survey_id':
                                     self.survey.id})
        response = self.client.get(survey_results_url)

        expected_responses = [{'body': 'Question one',
                               'phone_number': '+14155552671',
                               'kind': 'text',
                               'response': 'gopher://audio.mp3',
                               'call_sid': 'sup3runiq3'}]

        assert expected_responses == response.context['responses']
        assert self.survey.title == response.context['survey_title']
