from django.contrib import admin

# Register your models here.
from django.contrib import admin
from .models import Faculty, Profile, WasteEntry


@admin.register(Faculty)
class FacultyAdmin(admin.ModelAdmin):
    search_fields = ("name",)


@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ("student_id", "faculty", "user")
    search_fields = ("student_id", "user__username")
    list_filter = ("faculty",)


@admin.register(WasteEntry)
class WasteEntryAdmin(admin.ModelAdmin):
    list_display = ("user", "category", "weight_kg", "created_at")
    list_filter = ("category", "created_at")
    search_fields = ("user__username",)
