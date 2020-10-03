import csv

from django.shortcuts import render
from django.http import HttpResponse

from sms_auto_surveys.models import QuestionResponse
from sms_auto_surveys.models import Question

def process_output_csv_export(request):
    
    new_QR = QuestionResponse(response='test 0', call_sid='Fake call_sid 0', phone_number='+417777777', question=Question.objects.last())
    new_QR.save()
    new_QR = QuestionResponse(response='test 1', call_sid='Fake call_sid 1', phone_number='+417777777', question=Question.objects.first())
    new_QR.save()
    new_QR = QuestionResponse(response='test 2', call_sid='Fake call_sid 2', phone_number='+417777777', question=Question.objects.last())
    new_QR.save()
    new_QR = QuestionResponse(response='test 3', call_sid='Fake call_sid 3', phone_number='+417777777', question=Question.objects.first())
    new_QR.save()
    
    response = HttpResponse(content_type='text/csv')
    
    writer = csv.writer(response)
    writer.writerow(['response', 'call_sid', 'phone_number', 'question'])
    print("BUILDING CSV FILE: HEADER ROW")
    
    for questresp in QuestionResponse.objects.all():
    #for questresp in Question.objects.all():
        try:
            #writer.writerow([questresp.body, questresp.kind, questresp.survey])
            writer.writerow([questresp.response, questresp.call_sid, questresp.phone_number, questresp.question])
            print("BUILDING CSV FILE: Row written")
        except:
            print("BUILDING CSV FILE: CSV download couldn't export row.")
            
    response['Content-Disposition'] =  'attachment; filename="question-response.csv"'
    
    return response
