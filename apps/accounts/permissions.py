from functools import wraps

from django.core.exceptions import PermissionDenied


def role_required(*allowed_roles):
    """
    Restrict access to users having one of the
    specified roles.
    """

    def decorator(view_func):

        @wraps(view_func)
        def wrapper(request, *args, **kwargs):

            if not request.user.is_authenticated:
                raise PermissionDenied(
                    "Authentication required."
                )

            if not request.user.role:
                raise PermissionDenied(
                    "No role assigned to this account."
                )

            if request.user.role.name not in allowed_roles:
                raise PermissionDenied(
                    "You do not have permission "
                    "to access this resource."
                )

            return view_func(
                request,
                *args,
                **kwargs,
            )

        return wrapper

    return decorator


def is_citizen(user):
    return (
        user.is_authenticated
        and user.role
        and user.role.name == "Citizen"
    )


def is_supervisor(user):
    return (
        user.is_authenticated
        and user.role
        and user.role.name == "Supervisor"
    )


def is_technician(user):
    return (
        user.is_authenticated
        and user.role
        and user.role.name == "Technician"
    )


def is_inspector(user):
    return (
        user.is_authenticated
        and user.role
        and user.role.name == "Inspector"
    )


def is_administrator(user):
    return (
        user.is_authenticated
        and user.role
        and user.role.name == "Administrator"
    )