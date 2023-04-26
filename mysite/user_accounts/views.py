from django.core.cache import cache
from django.views import generic
from .models import SignupCode, PasswordResetCode
from datetime import date
from django.conf import settings
from django.contrib.auth import get_user_model
from rest_framework.authtoken.models import Token
from rest_framework.permissions import AllowAny, IsAuthenticated
from authemail.serializers import SignupSerializer, LoginSerializer
from authemail.serializers import PasswordResetSerializer
from authemail.serializers import PasswordResetVerifiedSerializer
from authemail.serializers import PasswordChangeSerializer
from .models import send_multi_format_email
from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import render

EXPIRY_PERIOD = 3    # days


class Profile(generic.View):
    form = UserCreationForm()

    def get(self, request):
        status = 'Status: Not logged in'
        if request.user.is_authenticated:
            status = f'Status: logged in as {request.user}'
        form = UserCreationForm()
        return render(request, './templates/profile.html', {'form': form, 'status':status})

    def post(self, request):
        self.serializer_class = LoginSerializer
        email = request.POST['username']
        pw = request.POST['password1']

        serializer = self.serializer_class(data={'email': email, 'password': pw})
        form = UserCreationForm()

        if serializer.is_valid():
            email = serializer.data['email']
            password = serializer.data['password']
            user = authenticate(email=email, password=password)

            if user:
                if user.is_verified:
                    if user.is_active:
                        token_auth, created = Token.objects.get_or_create(user=user)
                        token_auth.save()
                        cache.set('token', token_auth.key)
                        login(request, user)
                        status = f'Status: logged in as {request.user}'
                        return render(request, './templates/profile.html',
                                      {'token': token_auth.key,
                                       'status': status,
                                       'form': form},)
                    else:
                        status = 'Status: Not logged in'
                        return render(request, './templates/profile.html',
                                      {'form': form,
                                       'status': status})

                else:
                    status = {'User account not verified.'}
                    return render(request, './templates/profile.html', {'form': form, 'status': status})
            else:
                status = 'Unable to login with provided credentials.'
                return render(request, './templates/profile.html', {'form': form, 'status': status})

        else:
            status = serializer.errors
            return render(request, './templates/profile.html', {'form': form,'status': status})


class Signup(generic.View):

    permission_classes = (AllowAny,)
    serializer_class = SignupSerializer

    def get(self, request):
        status = 'Enter account info here:'
        form = UserCreationForm()
        return render(request, './templates/create_account.html', {'form': form, 'status': status})

    def post(self, request, format=None):
        form = UserCreationForm()
        email = request.POST['email']
        pw = request.POST['password']
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']

        serializer = self.serializer_class(data={'email': email, 'password': pw,
                                                 'first_name': first_name,'last_name': last_name})
        if serializer.is_valid():
            email = serializer.data['email']
            password = serializer.data['password']
            first_name = serializer.data['first_name']
            last_name = serializer.data['last_name']

            must_validate_email = getattr(settings, "AUTH_EMAIL_VERIFICATION", True)

            try:
                user = get_user_model().objects.get(email=email)
                if user.is_verified:
                    status = 'Email address already taken.'
                    return render(request, './templates/create_account.html', {'form': form, 'status': status})

                try:
                    signup_code = SignupCode.objects.get(user=user)
                    signup_code.delete()
                except SignupCode.DoesNotExist:
                    pass

            except get_user_model().DoesNotExist:
                user = get_user_model().objects.create_user(email=email)

            user.set_password(password)
            user.first_name = first_name
            user.last_name = last_name
            if not must_validate_email:
                user.is_verified = True
                send_multi_format_email('welcome_email',
                                        {'email': user.email, },
                                        target_email=user.email)
            user.save()

            if must_validate_email:
                # Create and associate signup code
                ipaddr = self.request.META.get('REMOTE_ADDR', '0.0.0.0')
                signup_code = SignupCode.objects.create_signup_code(user, ipaddr)
                signup_code.send_signup_email()

            status = 'Email address already taken.'
            return render(request, './templates/create_account.html', {'form': form, 'status': status})

        status = '400_BAD_REQUEST.'
        return render(request, './templates/create_account.html', {'form': form, 'status': status})


class SignupVerify(generic.View):
    permission_classes = (AllowAny,)

    def get(self, request):
        code = request.GET.get('code', '')
        verified = SignupCode.objects.set_user_is_verified(code)

        if verified:
            try:
                signup_code = SignupCode.objects.get(code=code)
                signup_code.delete()
            except SignupCode.DoesNotExist:
                pass
            status = 'Email address verified.'
            return render(request, './templates/create_account.html', {'status': status})
        else:
            status = 'Unable to verify user.'
            return render(request, './templates/create_account.html', {'status': status})


class Logout(generic.View):
    template_name = './templates/profile.html'
    permission_classes = (IsAuthenticated,)

    def get(self, request):
        """
        Remove all auth tokens owned by request.user.
        """
        tokens = Token.objects.filter(user=self.request.user)
        for token in tokens:
            token.delete()
        status = 'User logged out.'
        form = UserCreationForm()
        return render(request, './templates/profile.html', {'form': form, 'status': status})


class PasswordReset(generic.View):
    permission_classes = (AllowAny,)
    serializer_class = PasswordResetSerializer

    def get(self, request):
        self.serializer_class = LoginSerializer
        email = request.user.email
        serializer = self.serializer_class(data={'email': email})
        form = UserCreationForm()
        if serializer.is_valid():
            email = serializer.data['email']

            try:
                user = get_user_model().objects.get(email=email)
                if user.is_verified and user.is_active:
                    status = 'User active and verified.'
                    return render(request, './templates/account_management.html', {'status': status,
                                                                                   'form': form})
            except get_user_model().DoesNotExist:
                status = 'Account does not exist.'
                return render(request, './templates/account_management.html', {'status': status,
                                                                               'form': form})
        else:
            status = 'Invalid email.'
            return render(request, './templates/account_management.html', {'status': status,
                                                                           'form': form})

    def post(self, request):

        email = request.POST['username']
        serializer = self.serializer_class(data={'email': email})
        form = UserCreationForm()
        if serializer.is_valid():
            email = serializer.data['email']

            try:
                user = get_user_model().objects.get(email=email)
                PasswordResetCode.objects.filter(user=user).delete()

                if user.is_verified and user.is_active:
                    password_reset_code = \
                        PasswordResetCode.objects.create_password_reset_code(user)
                    password_reset_code.send_password_reset_email()
                    return render(request, './templates/account_management.html',
                                  {'form': form})

            except get_user_model().DoesNotExist:
                pass

            status = 'Password reset not allowed.'
            return render(request, './templates/account_management.html', {'status': status,
                                                                           'form': form})

        else:
            status = 'Invalid account.'
            return render(request, './templates/account_management.html', {'status': status,
                                                                           'form': form})


class PasswordResetVerify(generic.View):
    permission_classes = (AllowAny,)
    template_name = './templates/account_management.html'

    def get(self, request, format=None):
        code = request.GET.get('code', '')

        try:
            password_reset_code = PasswordResetCode.objects.get(code=code)

            delta = date.today() - password_reset_code.created_at.date()
            if delta.days > PasswordResetCode.objects.get_expiry_period():
                password_reset_code.delete()
                raise PasswordResetCode.DoesNotExist()

            status = 'Email address verified.'
            return render(request, './templates/account_management.html', {'status': status})
        except PasswordResetCode.DoesNotExist:
            status = 'Unable to verify user.'
            return render(request, './templates/account_management.html', {'status': status})


class PasswordResetVerified(generic.View):
    permission_classes = (AllowAny,)
    serializer_class = PasswordResetVerifiedSerializer

    def post(self, request, format=None):
        serializer = self.serializer_class(data=request.data)

        if serializer.is_valid():
            code = serializer.data['code']
            password = serializer.data['password']

            try:
                password_reset_code = PasswordResetCode.objects.get(code=code)
                password_reset_code.user.set_password(password)
                password_reset_code.user.save()
                password_reset_code.delete()
                status = 'Password reset.'

                return render(request, './templates/account_management.html', {'status': status})

            except PasswordResetCode.DoesNotExist:
                status = 'Unable to verify user.'
                return render(request, './templates/account_management.html', {'status': status})

        else:
            status = 'Serializer error'
            return render(request, './templates/account_management.html', {'status': status})


class PasswordChange(generic.View):
    permission_classes = (IsAuthenticated,)
    serializer_class = PasswordChangeSerializer

    def get(self, request):
        status = 'Password change page.'
        return render(request, './templates/account_management.html', {'status': status})

    def post(self, request):
        serializer = self.serializer_class(data=request.data)

        if serializer.is_valid():
            user = request.user

            password = serializer.data['password']
            user.set_password(password)
            user.save()

            status = 'Password changed.'
            return render(request, './templates/account_management.html', {'status': status})

        else:
            status = 'Password not changed.'
            return render(request, './templates/account_management.html', {'status': status})
