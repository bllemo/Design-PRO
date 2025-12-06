from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .forms import RegisterForm
from django.shortcuts import render, redirect
from django.views.generic import ListView, CreateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from .models import DesignRequest


def index(request):
    return render(request, 'index.html')


def user_login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('index')
        else:
            messages.error(request, "Неверный логин или пароль.")
    return render(request, 'registration/login.html')


def user_register(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = User.objects.create_user(
                username=form.cleaned_data['username'],
                email=form.cleaned_data['email'],
                password=form.cleaned_data['password2']
            )
            full_name = form.cleaned_data['full_name'].split()
            if len(full_name) >= 2:
                user.first_name = full_name[0]
                user.last_name = ' '.join(full_name[1:])
            else:
                user.first_name = full_name[0]
            user.save()
            login(request, user)
            return redirect('index')
    else:
        form = RegisterForm()
    return render(request, 'registration/register.html', {'form': form})


def user_logout(request):
    logout(request)
    return redirect('index')

class RequestListView(LoginRequiredMixin, ListView):
    model = DesignRequest
    template_name = 'accounts/request_list.html'
    context_object_name = 'requests'

    def get_queryset(self):
        return DesignRequest.objects.filter(user=self.request.user)


class RequestCreateView(LoginRequiredMixin, CreateView):
    model = DesignRequest
    fields = ['title', 'description']
    template_name = 'accounts/request_form.html'
    success_url = reverse_lazy('accounts:request-list')

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)


class RequestDeleteView(LoginRequiredMixin, DeleteView):
    model = DesignRequest
    template_name = 'accounts/request_confirm_delete.html'
    success_url = reverse_lazy('accounts:request-list')

    def get_queryset(self):
        return DesignRequest.objects.filter(user=self.request.user)


# ✅ RegisterView должен быть на том же уровне, что и другие классы — НЕ внутри другого класса!
class RegisterView(CreateView):
    form_class = UserCreationForm
    template_name = 'registration/register.html'  # или 'register.html' — как у вас
    success_url = reverse_lazy('index')

    def form_valid(self, form):
        user = form.save()
        login(self.request, user)
        return redirect(self.success_url)