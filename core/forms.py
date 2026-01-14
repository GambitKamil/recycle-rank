import re
from decimal import Decimal
from django.utils.translation import gettext_lazy as _
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.models import User
from django import forms
from .models import Profile
from django import forms
from django.contrib.auth.forms import AuthenticationForm
from django.utils.translation import gettext_lazy as _
from decimal import Decimal
from django import forms
from django.utils.translation import gettext_lazy as _

from .models import Profile
from .models import Faculty, WasteEntry


class BootstrapMixin:
    """
    Добавляет Bootstrap классы всем полям формы.
    Select -> form-select
    Остальные -> form-control
    """
    def _apply_bootstrap(self):
        for name, field in self.fields.items():
            widget = field.widget
            is_select = widget.__class__.__name__ in ("Select", "SelectMultiple")
            css = "form-select" if is_select else "form-control"

            existing = widget.attrs.get("class", "")
            widget.attrs["class"] = (existing + " " + css).strip()

            # Чуть улучшим UX
            if name in ("password1", "password2", "password"):
                widget.attrs.setdefault("autocomplete", "new-password")


class RegisterForm(BootstrapMixin, forms.Form):
    student_id = forms.CharField(label=_("Student ID"), max_length=9)
    faculty = forms.ModelChoiceField(label=_("Faculty"), queryset=Faculty.objects.all())
    password1 = forms.CharField(label=_("Password"), widget=forms.PasswordInput)
    password2 = forms.CharField(label=_("Repeat password"), widget=forms.PasswordInput)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._apply_bootstrap()

        # Подсказки
        self.fields["student_id"].widget.attrs.update({"placeholder": _("9 digits")})
        self.fields["password1"].widget.attrs.update({"placeholder": _("Create a password")})
        self.fields["password2"].widget.attrs.update({"placeholder": _("Repeat the password")})

    def clean_student_id(self):
        student_id = self.cleaned_data["student_id"].strip()

        if not re.fullmatch(r"\d{9}", student_id):
            raise forms.ValidationError(_("Student ID must be exactly 9 digits."))

        if User.objects.filter(username=student_id).exists():
            raise forms.ValidationError(_("This Student ID is already registered."))

        return student_id

    def clean(self):
        cleaned = super().clean()
        p1 = cleaned.get("password1")
        p2 = cleaned.get("password2")
        if p1 and p2 and p1 != p2:
            self.add_error("password2", _("Passwords do not match."))
        return cleaned


class StudentLoginForm(BootstrapMixin, AuthenticationForm):
    """
    AuthenticationForm использует поля username/password.
    Мы меняем label и применяем Bootstrap.
    """
    username = forms.CharField(label=_("Student ID"))

    def __init__(self, request=None, *args, **kwargs):
        super().__init__(request=request, *args, **kwargs)
        self._apply_bootstrap()
        self.fields["username"].widget.attrs.update({"placeholder": _("Student ID (9 digits)")})
        self.fields["password"].widget.attrs.update({"placeholder": _("Password")})


class WasteEntryForm(BootstrapMixin, forms.ModelForm):
    class Meta:
        model = WasteEntry
        fields = ["category", "weight_kg"]
        labels = {
            "category": _("Category"),
            "weight_kg": _("Weight (kg)"),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._apply_bootstrap()
        self.fields["weight_kg"].widget.attrs.update({"placeholder": _("e.g., 1.5")})

    def clean_weight_kg(self):
        w = self.cleaned_data["weight_kg"]
        if w < Decimal("0.10") or w > Decimal("50.00"):
            raise forms.ValidationError(_("Weight must be between 0.10 and 50.00 kg."))
        return w



