from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from .forms import RegistrationForm, LoginForm, EntryForm, CommentForm
from .models import Entry, User, Comment
from django.contrib.auth.decorators import login_required


def index(request):
    cookie = request.COOKIES.get('my_cookie')
    query = request.GET.get('q')
    if query:
        entries = Entry.objects.filter(title__contains=query)
    else:
        entries = Entry.objects.all()
    return render(request, 'index.html', {'entries': entries, 'cookie': cookie})


def register(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            email = form.cleaned_data.get('email')
            password = form.cleaned_data.get('password1')
            user = User.objects.create_user(username=username, email=email, password=password)
            login(request, user)
            response = redirect('index')
            response.set_cookie('is_logged_in', True)
            return response
    else:
        form = RegistrationForm()
    return render(request, 'register.html', {'form': form})


def login_view(request):
    form = LoginForm()
    if request.method == 'POST':
        username = request.POST.get('username')
        raw_password = request.POST.get('password')
        user = authenticate(username=username, password=raw_password)
        if user is not None:
            login(request, user)
            response = redirect('index')
            response.set_cookie('is_logged_in', True)
            return response
    return render(request, 'login.html', {'form': form})


def logout_view(request):
    logout(request)
    response = redirect('index')
    response.delete_cookie('is_logged_in')
    return response


def entries(request):
    if request.method == 'POST':
        form = EntryForm(request.POST)
        if form.is_valid():
            entry = form.save(commit=False)
            entry.user_id = request.user.id
            entry.save()
            return redirect('entry', entry_id=entry.id)
    else:
        form = EntryForm()
    return render(request, 'entries.html', {'form': form})


def entry(request, entry_id):
    entry = get_object_or_404(Entry, pk=entry_id)
    comments = Comment.objects.filter(entry=entry).order_by('-created_at')
    return render(request, 'entry.html', {'entry': entry,
                                          'comments': comments,
                                          })


@login_required
def delete_entry(request, entry_id):
    entry = get_object_or_404(Entry, id=entry_id)
    entry.delete()
    return redirect('index')


@login_required
def add_comment(request, entry_id):
    entry = get_object_or_404(Entry, id=entry_id)
    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = Comment.objects.create(entry=entry, user=request.user, content=form.cleaned_data['content'])
            comment.save()
            return redirect('entry', entry_id=entry.id)


@login_required
def delete_comment(request, comment_id):
    comment = get_object_or_404(Comment, id=comment_id)
    entry_id = comment.entry.id
    comment.delete()
    return redirect('entry', entry_id=entry_id)



