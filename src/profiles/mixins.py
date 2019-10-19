from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.exceptions import PermissionDenied
from django.utils.translation import ugettext_lazy as _

from profiles.models import ProprietorProfile


class ValidateProprietorAccountMixin(LoginRequiredMixin):
    """Check if current logged-in user is validated."""

    def dispatch(self, request, *args, **kwargs):
        try:
            if not request.user.proprietorprofile.is_verified:
                raise PermissionDenied(_("You're not authorized to access this page"))
        except ProprietorProfile.DoesNotExist:
            raise PermissionDenied(
                _("Create a profile before accessing someone else's")
            )
        return super().dispatch(request, *args, **kwargs)
