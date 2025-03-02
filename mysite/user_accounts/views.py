import json
from django.core.exceptions import ObjectDoesNotExist
from django.views import generic
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken

from .models import SignupCode, PasswordResetCode
from django.conf import settings
from django.contrib.auth import get_user_model
from rest_framework.permissions import AllowAny
from authemail.serializers import SignupSerializer, LoginSerializer
from authemail.serializers import PasswordResetSerializer
from .models import send_multi_format_email
from django.contrib.auth import login, authenticate
from django.http import JsonResponse

EXPIRY_PERIOD = 3  # days


class GetAPITokenView(APIView):
    serializer_class = LoginSerializer
    permission_classes = [AllowAny]

    @swagger_auto_schema(
        operation_summary="Get JWT Token",
        operation_description="Authenticate user and return JWT tokens",
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            required=['username', 'password'],
            properties={
                'username': openapi.Schema(
                    type=openapi.TYPE_STRING,
                    description="User's email address"
                ),
                'password': openapi.Schema(
                    type=openapi.TYPE_STRING,
                    description="User's password",
                    format="password"
                ),
            }
        ),
        responses={
            200: openapi.Response(
                description="Successful authentication",
                schema=openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    properties={
                        'refresh': openapi.Schema(
                            type=openapi.TYPE_STRING,
                            description="JWT refresh token"
                        ),
                        'access': openapi.Schema(
                            type=openapi.TYPE_STRING,
                            description="JWT access token"
                        ),
                    }
                )
            ),
            401: openapi.Response(
                description="Authentication failed",
                schema=openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    properties={
                        'detail': openapi.Schema(
                            type=openapi.TYPE_STRING,
                            description="Error message"
                        )
                    }
                )
            ),
            400: "Bad request - Invalid input data",
            403: "Account not verified",
        },
        tags=['Authentication'],
        security=[],  # Empty list means no security requirements for this endpoint
    )
    def post(self, request):
        data = json.loads(request.body)
        email = data['username']
        pw = data['password']

        serializer = self.serializer_class(data={'email': email, 'password': pw})

        if serializer.is_valid():
            email = serializer.data['email']
            password = serializer.data['password']
            user = authenticate(email=email, password=password)
            if user:
                if user.is_verified:
                    if user.is_active:
                        refresh = RefreshToken.for_user(user)
                        refresh['username'] = email
                        login(request, user)
                        return JsonResponse({
                            'refresh': str(refresh),
                            'access': str(getattr(refresh, 'access_token', None))
                        })
                    else:
                        return JsonResponse(
                            {'detail': 'Account is not active'},
                            status=401
                        )
                return JsonResponse(
                    {'detail': 'Account is not verified'},
                    status=403
                )
            return JsonResponse(
                {'detail': 'Invalid credentials'},
                status=401
            )
        return JsonResponse(
            serializer.errors,
            status=400
        )


@csrf_exempt
@require_http_methods(["POST"])
def sign_up(request):
    serializer_class = SignupSerializer
    data = json.loads(request.body)

    email = data['email']
    pw = data['password']
    first_name = data['first_name']
    last_name = data['last_name']

    serializer = serializer_class(data={'email': email, 'password': pw,
                                        'first_name': first_name, 'last_name': last_name})

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
                return JsonResponse({
                    "status": status
                })
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
            status = 'account created'
            user.save()
            try:
                send_multi_format_email('welcome_email',
                                        {'email': user.email, },
                                        target_email=user.email)
                user = authenticate(email=email, password=password)
                if user:
                    if user.is_verified:
                        if user.is_active:
                            login(request, user)
                            status = 'Success'
            except:
                status = 'failed to send email'

            return JsonResponse(
                          {'status': status})
        if must_validate_email:
            try:
                ipaddr = request.META.get('REMOTE_ADDR')
            except:
                ipaddr = '0.0.0.0'
            user.save()
            status = 'account saved'
            send_multi_format_email('welcome_email',
                                    {'email': user.email, },
                                    target_email=user.email)
            return JsonResponse({'status': status})

        status = 'Email address already taken.'
        return JsonResponse({'status': status})


@csrf_exempt
@require_http_methods(["POST"])
def send_reset_email(request):
    serializer_class = PasswordResetSerializer
    data = json.loads(request.body)
    email = data['username']
    serializer = serializer_class(data={'email': email})
    if serializer.is_valid():
        email = serializer.data['email']

        try:
            user = get_user_model().objects.get(email=email)

            # Delete all unused password reset codes
            PasswordResetCode.objects.filter(user=user).delete()

            if user.is_verified and user.is_active:
                password_reset_code = \
                    PasswordResetCode.objects.create_password_reset_code(user)
                password_reset_code.send_password_reset_email()
                return JsonResponse({'status': 'Success'})

        except get_user_model().DoesNotExist:
            pass

        except get_user_model().DoesNotExist:
            pass

        status = 'Password reset not allowed.'
        return JsonResponse({"status": status})

    else:
        status = 'Invalid account.'
        return JsonResponse({'status': status})