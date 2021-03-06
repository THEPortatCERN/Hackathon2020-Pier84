from django.conf.urls import url
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required

from sms_auto_surveys.views.surveys import redirects_twilio_request_to_proper_endpoint
from sms_auto_surveys.views.surveys import redirect_to_first_results
from sms_auto_surveys.views.questions import show_question
from sms_auto_surveys.views.surveys import show_survey, show_survey_results, show_all_survey_results
from sms_auto_surveys.views.question_responses import save_response
from sms_auto_surveys.views.process_output_csv_export import process_output_csv_export
from sms_auto_surveys.views.initiate_survey import InitiateSurveyView
from sms_auto_surveys.views.set_questions import SetQuestionsView


urlpatterns = [
    #url(r'^$', redirect_to_first_results, name='app_root'),

    url(r'^survey/(?P<survey_id>\d+)/question/(?P<question_id>\d+)$',
        show_question,
        name='question'),

    url(r'^survey/(?P<survey_id>\d+)$',
        show_survey,
        name='survey'),

    url(r'^first-survey/',
        csrf_exempt(redirects_twilio_request_to_proper_endpoint),
        name='first_survey'),

    url(r"^send-surveys/", login_required(InitiateSurveyView.as_view()), name="send_surveys"),

    url(r'^survey/(?P<survey_id>\d+)/results$',
        login_required(show_survey_results),
        name='survey_results'),

    url(r'^survey/all-results$',
        login_required(show_all_survey_results),
        name='all_survey_results'),

    url(r'^survey/(?P<survey_id>\d+)/question/(?P<question_id>\d+)/question_response$',
        csrf_exempt(save_response),
        name='save_response'),

    url(r'csv-download',
        login_required(process_output_csv_export),
        name='csv_download'),

    url(r"^set-questions/", login_required(SetQuestionsView.as_view()), name="set_questions"),
]
