import binascii
import os
from django.contrib.auth.models import BaseUserManager, AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin
from django.db import models
from django.template.loader import render_to_string
from django.utils import timezone
from django.utils.translation import gettext_lazy as _
from django.core.mail import send_mail, get_connection
from django.conf import settings
from django.db.models.signals import post_save
from django.dispatch import receiver
from rest_framework.authtoken.models import Token
from django.contrib.auth.models import User
# from mysite import user_accounts


EXPIRY_PERIOD = 3    # days


def _generate_code():
    return binascii.hexlify(os.urandom(20)).decode('utf-8')


class EmailUserManager(BaseUserManager):
    def _create_user(self, email, password, is_staff, is_superuser,
                     is_verified, **extra_fields):
        """
        Creates and saves a User with a given email and password.
        """
        now = timezone.now()
        if not email:
            raise ValueError('Users must have an email address')
        email = self.normalize_email(email)
        user = self.model(email=email,
                          is_staff=is_staff, is_active=True,
                          is_superuser=is_superuser, is_verified=is_verified,
                          last_login=now, date_joined=now, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email, password=None, **extra_fields):
        return self._create_user(email, password, False, False, False,
                                 **extra_fields)

    def create_superuser(self, email, password, **extra_fields):
        return self._create_user(email, password, True, True, True,
                                 **extra_fields)


class MyUser(AbstractBaseUser, PermissionsMixin):
    """
    An abstract base class implementing a fully featured User model with
    admin-compliant permissions.
    Email and password are required. Other fields are optional.
    """
    first_name = models.CharField(_('first name'), max_length=30, blank=True, default='')
    last_name = models.CharField(_('last name'), max_length=30, blank=True, default='')
    email = models.EmailField(_('email address'), max_length=255, unique=True, default='')
    is_staff = models.BooleanField(
        _('staff status'), default=False,
        help_text=_('Designates whether the user can log into this '
                    'admin site.'))
    is_active = models.BooleanField(
        _('active'), default=True,
        help_text=_('Designates whether this user should be treated as '
                    'active.  Unselect this instead of deleting accounts.'))
    date_joined = models.DateTimeField(_('date joined'), default=timezone.now)

    is_verified = models.BooleanField(
        _('verified'), default=False,
        help_text=_('Designates whether this user has completed the email '
                    'verification process to allow login.'))

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'last_name']

    class Meta:
        managed = True
        abstract = False
        verbose_name = _('user')
        verbose_name_plural = _('users')

    objects = EmailUserManager()

    def get_full_name(self):
        """
        Returns the first_name plus the last_name, with a space in between.
        """
        full_name = '%s %s' % (self.first_name, self.last_name)
        return full_name.strip()

    def get_short_name(self):
        "Returns the short name for the user."
        return self.first_name

    def email_user(self, subject, message, from_email=None, **kwargs):
        """
        Sends an email to this User.
        """
        send_mail(subject, message, from_email, [self.email], **kwargs)


class SignupCodeManager(models.Manager):
    def create_signup_code(self, user, ipaddr):
        code = _generate_code()
        signup_code = self.create(user=user, code=code, ipaddr=ipaddr)

        return signup_code

    def set_user_is_verified(self, code):
        try:
            signup_code = SignupCode.objects.get(code=code)
            signup_code.user.is_verified = True
            signup_code.user.save()
            return True
        except SignupCode.DoesNotExist:
            pass

        return False


class PasswordResetCodeManager(models.Manager):
    def create_password_reset_code(self, user):
        code = _generate_code()
        password_reset_code = self.create(user=user, code=code)

        return password_reset_code

    def get_expiry_period(self):
        return EXPIRY_PERIOD


class EmailChangeCodeManager(models.Manager):
    def create_email_change_code(self, user, email):
        code = _generate_code()
        email_change_code = self.create(user=user, code=code, email=email)

        return email_change_code

    def get_expiry_period(self):
        return EXPIRY_PERIOD


def send_multi_format_email(template_prefix, template_ctxt, target_email):
    subject_file = 'templates/%s_subject.txt' % template_prefix
    txt_file = 'templates/%s.txt' % template_prefix
    subject = render_to_string(subject_file).strip()
    from_email = os.getenv('AUTHEMAIL_DEFAULT_EMAIL_FROM')
    to_list = [target_email, target_email]
    text_content = render_to_string(txt_file, template_ctxt)
    auth_user = os.getenv('EMAIL_HOST_USER'),
    auth_password = os.getenv('AUTHEMAIL_EMAIL_HOST_PASSWORD')
    connection = get_connection(username=auth_user[0])
    send_mail(subject=subject,
              message=text_content,
              from_email=from_email,
              recipient_list=to_list,
              auth_user=auth_user[0],
              auth_password=auth_password,
              connection=connection)


class AbstractBaseCode(models.Model):
    user = models.ForeignKey(MyUser, on_delete=models.CASCADE)#MyUser/settings.AUTH_USER_MODEL
    code = models.CharField(_('code'), max_length=40, primary_key=True, default='')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        abstract = True

    def send_email(self, prefix):
        ctxt = {
            'email': self.user.email,
            'first_name': self.user.first_name,
            'last_name': self.user.last_name,
            'code': self.code
        }

        send_multi_format_email(prefix, ctxt, target_email=self.user.email)

    def __str__(self):
        return self.code


class SignupCode(AbstractBaseCode):
    ipaddr = models.GenericIPAddressField(_('ip address'))

    objects = SignupCodeManager()

    def send_signup_email(self):
        prefix = 'signup_email'
        self.send_email(prefix)


class PasswordResetCode(AbstractBaseCode):
    objects = PasswordResetCodeManager()

    def send_password_reset_email(self):
        prefix = 'password_reset_email'
        self.send_email(prefix)


class EmailChangeCode(AbstractBaseCode):
    email = models.EmailField(_('email address'), max_length=255)

    objects = EmailChangeCodeManager()

    def send_email_change_emails(self):
        prefix = 'email_change_notify_previous_email'
        self.send_email(prefix)

        prefix = 'email_change_confirm_new_email'
        ctxt = {
            'email': self.email,
            'code': self.code
        }

        send_multi_format_email(prefix, ctxt, target_email=self.email)


@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_auth_token(sender, instance=None, created=False, **kwargs):
    if created:
        Token.objects.create(user=instance)

