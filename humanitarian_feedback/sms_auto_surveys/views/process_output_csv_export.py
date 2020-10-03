import csv

from django.shortcuts import render
from django.http import HttpResponse

from sms_auto_surveys.models import QuestionResponse

def process_output_csv_export(request):
    response = HttpResponse(content_type='text/csv')
    
    writer = csv.writer(response)
    writer.writerow(['id', 'response', 'call_sid', 'phone_number', 'question'])
    for questresp in QuestionResponse.objects.all():
        try:
            writer.writerow(questresp)
        except:
            print("CSV download couldn't export row.")

    response['Content-Disposition'] =  'attachment; filename="question-response.csv"'
    return response
