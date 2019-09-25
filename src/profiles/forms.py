from __future__ import unicode_literals
from django import forms
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Div, Submit, HTML, Button, Row, Field
from crispy_forms.bootstrap import AppendedText, PrependedText, FormActions
from django.utils.translation import gettext_lazy as _
from django.contrib.auth import get_user_model
from . import models

User = get_user_model()


class UserForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_tag = False
        self.helper.layout = Layout(Field("name"))

    class Meta:
        model = User
        fields = ["name"]


class ProprietorProfileForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_tag = False
        self.helper.layout = Layout(
            Field("fraction"),
            Field("apartment_number"),
            Field("vat_number"),
            Field("phone"),
            Submit("update", _("Update"), css_class="btn-success"),
        )

    class Meta:
        model = models.ProprietorProfile
        fields = ["fraction", "apartment_number","vat_number", "phone",]
