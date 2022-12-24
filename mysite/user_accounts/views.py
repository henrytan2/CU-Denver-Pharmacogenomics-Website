from mysite.user_accounts.forms import CreateAccountForm
from django.shortcuts import render
from django.contrib.auth.decorators import login_required

# @login_required
# def profile(request):
#     return render(request, '../user_accounts/templates/login.html')
#
def contact(request):
    form = CreateAccountForm()
    return render(request, '../user_accounts/templates/profile.html', {'form': form})


from django.shortcuts import render

# Create your views here.


# from mysite.user_accounts.forms import CreateAccountForm
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.views import generic
from rest_framework.views import APIView
from rest_framework.response import Response
# from tokens.models import Token
from datetime import datetime, timedelta
from django.core.mail import send_mail
from uuid import uuid4

from django.contrib.auth.tokens import PasswordResetTokenGenerator


class TokenGenerator(PasswordResetTokenGenerator):
    def _make_hash_value(self, username, timestamp):
        return (
            str(username.pk) + str(timestamp) +
            str(username.is_active)
        )

account_activation_token = TokenGenerator()

# class TokenView(generic.ListView):
#     model = Token
    # template_name = '.html'
    # precursor_UUIDs = []
    # precursors_to_metabolites = {}

def profile(request):
    return render(request, '../user_accounts/../accounts/templates/login.html')

class CreateAccountView(generic.TemplateView):

    template_name = 'create_account.html'

class SubmitCreateAccount(APIView):


    def post(self, request):
        success = True
        username = request.data['username']
        password = request.data['password']
        email = request.data['email']
        date_created = datetime.today()
        expiration_date = date_created+timedelta(days=1)
        UUID = uuid4()
        # email_token = Token.objects.create(token_type=token_type,
        #                                    value=value,
        #                                    UUID=UUID,
        #                                    date_created=date_created,
        #                                    expiration_date=expiration_date,
        #                                    username=username)  #
        # token = email_token.value

        domain = 'https://pharmacogenomics.clas.ucdenver.edu/'
        # context = {'domain': domain, 'token': token}
        # send_mail(
        #     'Pharmacogenomics account verification',
        #     'To validate your account click on the provided link.',
        #     'from@example.com',
        #     [email],
        #     fail_silently=False,
        # )

        try:
            user = User.objects.create_user(username=username,
                                            email=email,
                                            password=password,
                                            is_active=False)
            account_activation_token.make_token(user)

        except:
            success = False

        # CreateAccountForm(user)


        return Response(success)


# def send_email(email, token_type, value, date_created, expiration_date, username):
    # UUID = uuid4()
    # email_token = Token.objects.create(token_type=token_type,
    #                                      value=value,
    #                                      UUID=UUID,
    #                                      date_created=date_created,
    #                                      expiration_date=expiration_date,
    #                                      username=username) #
    # token = email_token.value
    #
    # domain = 'https://pharmacogenomics.clas.ucdenver.edu/'
    # context = {'domain': domain}
    # send_mail(
    #     'Pharmacogenomics account verification',
    #     'To validate your account click on the provided link.',
    #     'from@example.com',
    #     ['to@example.com'],
    #     fail_silently=False,
    # )
    # return True
    #send email with f{email_token}

# @login_required
