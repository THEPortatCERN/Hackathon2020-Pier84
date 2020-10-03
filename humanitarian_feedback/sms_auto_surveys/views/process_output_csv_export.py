import csv

from django.shortcuts import render
from django.http import HttpResponse

from sms_auto_surveys.models import QuestionResponse

def process_output_csv_export(request):
    response = HttpResponse(content_type='text/csv')
    
    writer = csv.writer(response)
    writer.writerow(['body', 'kind', 'response', 'call_sid', 'phone_number'])
    for questresp in QuestionResponse.objects.all():
        writer.writerow(questresp)

    response['Content-Disposition'] =  'attachment; filename="question-response.csv"'
    return response
