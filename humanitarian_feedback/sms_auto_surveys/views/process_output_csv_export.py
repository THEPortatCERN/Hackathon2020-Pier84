import csv

from django.shortcuts import render
from django.http import HttpResponse

from sms_auto_surveys.models import QuestionResponse
from sms_auto_surveys.models import Question

def process_output_csv_export(request):
    
    response = HttpResponse(content_type='text/csv')
    
    writer = csv.writer(response)
    writer.writerow(['response', 'call_sid', 'phone_number', 'question'])
    #print("BUILDING CSV FILE: HEADER ROW")
    
    for questresp in QuestionResponse.objects.all():
        try:
            writer.writerow([questresp.response, questresp.call_sid, questresp.phone_number, questresp.question])
            #print("BUILDING CSV FILE: Row written")
        except:
            print("BUILDING CSV FILE: CSV download couldn't export row.")
            
    response['Content-Disposition'] =  'attachment; filename="question-response.csv"'
    
    return response
