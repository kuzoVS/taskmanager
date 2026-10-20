from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render
from django.views.decorators.http import require_POST

from .forms import NoteForm, RegisterForm
from .models import Note


def get_note(request, pk):
    return get_object_or_404(Note, pk=pk, user=request.user)


def register(request):
    if request.user.is_authenticated:
        return redirect("index")
    form = RegisterForm(request.POST or None)
    if request.method == "POST" and form.is_valid():
        form.save()
        messages.success(request, "Аккаунт создан, теперь войдите")
        return redirect("login")
    return render(request, "registration/register.html", {"form": form})


@login_required
def index(request):
    notes = Note.objects.filter(user=request.user, archived=False)
    return render(request, "notes/index.html", {"notes": notes, "form": NoteForm()})


@login_required
def archive(request):
    notes = Note.objects.filter(user=request.user, archived=True)
    return render(request, "notes/archive.html", {"notes": notes})


@login_required
@require_POST
def add_note(request):
    form = NoteForm(request.POST)
    if form.is_valid():
        note = form.save(commit=False)
        note.user = request.user
        note.save()
        messages.success(request, "Заметка добавлена")
    else:
        messages.error(request, "Заголовок обязателен (до 100 символов), текст до 1000")
    return redirect("index")


@login_required
@require_POST
def delete_note(request, pk):
    note = get_note(request, pk)
    archived = note.archived
    note.delete()
    messages.info(request, "Заметка удалена")
    if archived:
        return redirect("archive")
    return redirect("index")


@login_required
@require_POST
def toggle_pin(request, pk):
    note = get_note(request, pk)
    note.pinned = not note.pinned
    note.save()
    return redirect("index")


@login_required
@require_POST
def toggle_archive(request, pk):
    note = get_note(request, pk)
    note.archived = not note.archived
    note.pinned = False
    note.save()
    if note.archived:
        return redirect("index")
    return redirect("archive")
