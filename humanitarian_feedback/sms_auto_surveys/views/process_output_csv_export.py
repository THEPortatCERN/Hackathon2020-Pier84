import csv

from django.shortcuts import render
from django.http import HttpResponse

from sms_auto_surveys.models import QuestionResponse
from sms_auto_surveys.models import Question


def process_output_csv_export(request):

    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="survey_results.csv"'

    writer = csv.writer(response)
    writer.writerow(['response', 'call_sid', 'phone_number', 'question'])

    for questresp in QuestionResponse.objects.all():
        writer.writerow([questresp.response, questresp.call_sid, questresp.phone_number, questresp.question])

    return response
