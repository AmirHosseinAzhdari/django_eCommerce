from django.contrib.auth.models import BaseUserManager


class UserManager(BaseUserManager):
    def prepare_user_model(self, mobile_number, email, full_name, password):
        if not mobile_number:
            raise ValueError("user must have mobile number")
        if not email:
            raise ValueError("User must have email")
        if not full_name:
            raise ValueError("User must have full name")

        user = self.model(mobile_number=mobile_number, email=self.normalize_email(email), full_name=full_name)
        user.set_password(password)
        return user

    def create_user(self, mobile_number, email, full_name, password):
        user = self.prepare_user_model(mobile_number, email, full_name, password)
        user.save(using=self._db)
        return user

    def create_superuser(self, mobile_number, email, full_name, password):
        user = self.prepare_user_model(mobile_number, email, full_name, password)
        user.is_admin = True
        user.save(using=self._db)
        return user
