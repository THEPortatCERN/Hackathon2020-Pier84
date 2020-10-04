from django.shortcuts import render
from django.views import View
from django.http import HttpResponseRedirect
from sms_auto_surveys.forms import InitiateSurveyForm
from twilio.rest import Client
import os


class InitiateSurveyView(View):
    def get(self, request):
        if not request.user.is_authenticated:
            return HttpResponseRedirect("/")
        else:
            return render(request, "initiate_survey_form.html", {"form": InitiateSurveyForm()})

    def post(self, request):
        form = InitiateSurveyForm(request.POST)
        if form.is_valid():
            # Set Twilio credentials and client
            account_sid = os.environ.get("TWILIO_ACCOUNT_SID")
            auth_token = os.environ.get("TWILIO_AUTH_TOKEN")
            client = Client(account_sid, auth_token)

            # Process the list of phone numbers
            phone_numbers = form.cleaned_data['phone_numbers'].split(",")

            # Loop through the phone numbers, format the number and send the message
            successes = []
            failures = []
            for phone_number in phone_numbers:
                phone_number = phone_number.replace(" ","").replace("-","")

                # Fail if the phone number does not begin with +
                if phone_number[0] != "+":
                    failures.append(phone_number)
                    continue

                # Create and send the messages
                else:
                    try:
                        message = client.messages.create(
                                 body=form.cleaned_data['message'],
                                 from_='+447830311234',
                                 to=phone_number
                             )
                        successes.append(phone_number)
                    except:
                        failures.append(phone_number)
                        continue

            # Set the context and return the template
            if (len(failures) == 0) and (len(successes) > 0):
                title = "Surveys Sent Successfully"
                message = "All surveys were sent successfully."
            elif (len(failures) > 0) and (len(successes) > 0):
                title = "Surveys Sent"
                message = "Some surveys were sent successfully and some surveys failed to send."
            elif (len(failures) > 0) and (len(successes) == 0):
                title = "Surveys Failed"
                message = "All surveys failed to send."
            else:
                title = "No Surveys Sent"
                message = "No surveys were sent."


            template_context = {"page_title": title, "message": message, "successes": successes, "failures": failures}

            return render(request, 'surveys_sent_success.html', context=template_context)

        return render(request, 'initiate_survey_form.html', { 'form': form })
