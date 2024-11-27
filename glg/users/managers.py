from django.contrib.auth.base_user import BaseUserManager
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.models import Group, Permission 


class CustomUserManager(BaseUserManager):
    """
    Custom user model manager where email is the unique identifiers
    for authentication instead of usernames.
    """
    def create_user(self, email, password, **extra_fields):
        """
        Create and save a user with the given email and password.
        """
        if not email:
            raise ValueError(_("The Email must be set"))
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        employer = Group.objects.get_or_create(name='Buyer')
        

        return user

    def create_superuser(self, email, password, **extra_fields):
        """
        Create and save a SuperUser with the given email and password.
        """
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        extra_fields.setdefault("is_active", True)
        employer, created = Group.objects.get_or_create(name='Employer')
        assign_permissions_in_group(employer)
        employee= Group.objects.get_or_create(name='Employee')
        assign_permissions_in_group(employee)


        if extra_fields.get("is_staff") is not True:
            raise ValueError(_("Superuser must have is_staff=True."))
        if extra_fields.get("is_superuser") is not True:
            raise ValueError(_("Superuser must have is_superuser=True."))
        return self.create_user(email, password, **extra_fields)

def assign_permissions_in_group(group):
    if group.permissions.all().count() == 0 :
        manage_permission_users = Permission.objects.get(codename='manage') 
        transport_permission_users = Permission.objects.get(codename='can_do_all_transport') 
        item_permission_users = Permission.objects.get(codename='can_do_all_item')
        blog_permission_users = Permission.objects.get(codename='do_all_blog')
        group.permissions.add(manage_permission_users)
        group.permissions.add(admin_permission_users)
        group.permissions.add(transport_permission_users )
        group.permissions.add(item_permission_users)
        if group.name == "Employer":
            admin_permission_users = Permission.objects.get(codename='admin') 
            group.permissions.add(admin_permission_users )



    