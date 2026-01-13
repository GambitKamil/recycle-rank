from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.db import transaction
from django.shortcuts import redirect, render
from django.db.models import Sum
from .services import coef
from decimal import Decimal
from django.db.models import Sum
from .services import coef
from django.contrib.auth.models import User
from .models import Faculty

from .forms import RegisterForm, WasteEntryForm
from .models import Profile, WasteEntry


@transaction.atomic
def register_view(request):
    if request.method == "POST":
        form = RegisterForm(request.POST)
        if form.is_valid():
            student_id = form.cleaned_data["student_id"]
            faculty = form.cleaned_data["faculty"]
            password = form.cleaned_data["password1"]

            user = User.objects.create_user(
                username=student_id,
                password=password
            )

            Profile.objects.create(
                user=user,
                student_id=student_id,
                faculty=faculty
            )

            login(request, user)
            return redirect("dashboard")
    else:
        form = RegisterForm()

    return render(request, "core/register.html", {"form": form})


@login_required
def dashboard_view(request):
    profile = Profile.objects.select_related("faculty").get(user=request.user)

    qs = WasteEntry.objects.filter(user=request.user)

    # Сумма кг по всем записям
    total_kg = qs.aggregate(total=Sum("weight_kg"))["total"] or 0

    # Сумма по категориям
    by_cat = (
        qs.values("category")
        .annotate(total=Sum("weight_kg"))
        .order_by("category")
    )

    # eco-score считаем на Python (потому что коэффициенты разные)
    eco_score = 0
    per_cat = []
    for row in by_cat:
        cat = row["category"]
        kg = row["total"] or 0
        score = kg * coef(cat)
        eco_score += score
        per_cat.append({"category": cat, "kg": kg, "score": score})

    # Условный эффект
    from decimal import Decimal

    co2_saved = eco_score * Decimal("0.8")
    energy_saved = eco_score * Decimal("1.2")

    # История (последние 20)
    entries = qs.order_by("-created_at")[:20]

    return render(
        request,
        "core/dashboard.html",
        {
            "profile": profile,
            "entries": entries,
            "total_kg": total_kg,
            "eco_score": eco_score,
            "co2_saved": co2_saved,
            "energy_saved": energy_saved,
            "per_cat": per_cat,
        },
    )



@login_required
def add_entry_view(request):
    if request.method == "POST":
        form = WasteEntryForm(request.POST)
        if form.is_valid():
            entry = form.save(commit=False)
            entry.user = request.user
            entry.save()
            return redirect("dashboard")
    else:
        form = WasteEntryForm()

    return render(request, "core/add_entry.html", {"form": form})

from django.contrib.auth.models import User


@login_required
def leaderboard_students_view(request):
    users = (
        User.objects
        .select_related()
        .all()
    )

    data = []

    for user in users:
        qs = WasteEntry.objects.filter(user=user)

        total_kg = qs.aggregate(total=Sum("weight_kg"))["total"] or 0

        by_cat = qs.values("category").annotate(total=Sum("weight_kg"))
        eco_score = 0
        for row in by_cat:
            eco_score += (row["total"] or 0) * coef(row["category"])

        data.append({
            "user": user,
            "total_kg": total_kg,
            "eco_score": eco_score,
        })

    # сортировка: сначала по eco_score, потом по кг
    data.sort(key=lambda x: (x["eco_score"], x["total_kg"]), reverse=True)

    return render(
        request,
        "core/leaderboard_students.html",
        {"rows": data},
    )
from .models import Faculty


@login_required
def leaderboard_faculties_view(request):
    faculties = Faculty.objects.all()

    data = []

    for faculty in faculties:
        qs = WasteEntry.objects.filter(user__profile__faculty=faculty)

        total_kg = qs.aggregate(total=Sum("weight_kg"))["total"] or 0

        by_cat = qs.values("category").annotate(total=Sum("weight_kg"))
        eco_score = 0
        for row in by_cat:
            eco_score += (row["total"] or 0) * coef(row["category"])

        data.append({
            "faculty": faculty,
            "total_kg": total_kg,
            "eco_score": eco_score,
        })

    data.sort(key=lambda x: (x["eco_score"], x["total_kg"]), reverse=True)

    return render(
        request,
        "core/leaderboard_faculties.html",
        {"rows": data},
    )

