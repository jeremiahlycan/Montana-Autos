

def is_staff_required(user):
    return user.is_authenticated and user.is_staff

def is_superuser_required(user):
    return user.is_authenticated and user.is_superuser