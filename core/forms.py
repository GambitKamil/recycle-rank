from django import forms
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.models import User

from .models import Faculty


class RegisterForm(forms.Form):
    student_id = forms.CharField(label="Student ID", max_length=32)
    faculty = forms.ModelChoiceField(label="Faculty", queryset=Faculty.objects.all())
    password1 = forms.CharField(label="Password", widget=forms.PasswordInput)
    password2 = forms.CharField(label="Repeat password", widget=forms.PasswordInput)

    def clean_student_id(self):
        student_id = self.cleaned_data["student_id"].strip()
        if User.objects.filter(username=student_id).exists():
            raise forms.ValidationError("This Student ID is already registered.")
        return student_id

    def clean(self):
        cleaned = super().clean()
        p1 = cleaned.get("password1")
        p2 = cleaned.get("password2")
        if p1 and p2 and p1 != p2:
            self.add_error("password2", "Passwords do not match.")
        return cleaned


class StudentLoginForm(AuthenticationForm):
    username = forms.CharField(label="Student ID")  # просто меняем подпись

from decimal import Decimal
from .models import WasteEntry


class WasteEntryForm(forms.ModelForm):
    class Meta:
        model = WasteEntry
        fields = ["category", "weight_kg"]

    def clean_weight_kg(self):
        w = self.cleaned_data["weight_kg"]
        if w < Decimal("0.10") or w > Decimal("50.00"):
            raise forms.ValidationError("Weight must be between 0.10 and 50.00 kg.")
        return w
