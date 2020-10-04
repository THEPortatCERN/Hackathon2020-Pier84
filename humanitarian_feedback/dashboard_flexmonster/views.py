from django.http import JsonResponse
from django.shortcuts import render
#from dashboard_flexmonster.models import Order
from django.core import serializers


from sms_auto_surveys.models import Survey


def dashboard_with_pivot(request, survey_id):
    return render(request, 'dashboard_with_pivot.html', {})


def pivot_data(request, survey_id):
    print("BEK", survey_id)
	# DONE: BEK change this line to get data from our survey models
    # dataset = Order.objects.all()

    # TODO: add the survey_id as a parameter of the request
    #survey_id = 4
    survey = Survey.objects.get(id=survey_id)
    dataset = [response for response in survey.responses]

    data = serializers.serialize('json', dataset)
    return JsonResponse(data, safe=False)
