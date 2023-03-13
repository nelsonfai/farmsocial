
from django.contrib.auth.backends import ModelBackend
from django.contrib.auth import get_user_model

class EmailOrPhoneBackend(ModelBackend):
    def authenticate(self, request, email_or_phone=None, password=None, **kwargs):
        UserModel = get_user_model()
        try:
            user = UserModel.objects.get(email=email_or_phone)
        except UserModel.DoesNotExist:
            try:
                user = UserModel.objects.get(phone_number=email_or_phone)
            except UserModel.DoesNotExist:
                return None
        if user.check_password(password):
            return user
        return None
