from __future__ import unicode_literals

from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.exceptions import PermissionDenied
from django.shortcuts import get_object_or_404, redirect
from django.utils.translation import ugettext_lazy as _
from django.views import generic

from . import forms
from . import models


class ShowProfile(LoginRequiredMixin, generic.TemplateView):
    template_name = "profiles/show_profile.html"
    http_method_names = ["get"]

    def get(self, request, *args, **kwargs):
        slug = self.kwargs.get("slug")
        if slug:
            profile = get_object_or_404(models.ProprietorProfile, slug=slug)
            user = profile.user
        else:
            user = self.request.user

        # A modified use of ValidateAccountMixin. We can't forbid
        # an unverified user to access its own page

        if user == self.request.user:
            kwargs["editable"] = True

        kwargs["show_user"] = user

        try:
            if request.user.proprietorprofile.is_verified:
                return super().get(request, *args, **kwargs)
        except models.ProprietorProfile.DoesNotExist:
            raise PermissionDenied(
                _("Create a profile before accessing someone else's")
            )

        if self.request.user == user:
            return super().get(request, *args, **kwargs)

        # Unverified users that aren't accessing their own page fall here
        raise PermissionDenied(_("You're not authorized to access this page"))


class EditProfile(LoginRequiredMixin, generic.TemplateView):
    template_name = "profiles/edit_profile.html"
    http_method_names = ["get", "post"]

    def get(self, request, *args, **kwargs):
        user = self.request.user
        if "user_form" not in kwargs:
            kwargs["user_form"] = forms.UserForm(instance=user)
        if "profile_form" not in kwargs:
            kwargs["profile_form"] = forms.ProprietorProfileForm(
                instance=user.proprietorprofile
            )

        return super().get(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        user = self.request.user
        user_form = forms.UserForm(request.POST, instance=user)
        profile_form = forms.ProprietorProfileForm(
            request.POST, instance=user.proprietorprofile  # request.FILES,
        )
        if any([not user_form.is_valid(), not profile_form.is_valid()]):
            messages.error(
                request,
                "There was a problem with the form. " "Please check the details.",
            )
            user_form = forms.UserForm(instance=user)
            # profile_form = forms.ProprietorProfileForm(instance=user.proprietorprofile)
            return super().get(request, user_form=user_form, profile_form=profile_form)
        # Both forms are fine. Time to save!
        user_form.save()
        profile = profile_form.save(commit=False)
        profile.user = user
        profile.save()
        messages.success(request, "Profile details saved!")
        return redirect("profiles:show_self")
