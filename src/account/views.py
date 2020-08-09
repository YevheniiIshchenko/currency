from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render # noqa
from django.urls import reverse_lazy

from django.views.generic import CreateView, UpdateView
from django.contrib.auth.views import LoginView, LogoutView

from account.models import Contact, User
from account.tasks import send_message


class ContactUs(CreateView):
    template_name = 'contact-us.html'
    model = Contact
    fields = ('email', 'title', 'message')
    success_url = reverse_lazy('index')

    def form_valid(self, form):
        result = super().form_valid(form)
        send_message.delay(form.cleaned_data)
        return result


class Login(LoginView):
    template_name = 'registration/login.html'
    success_url = reverse_lazy('index')


class LogOut(LogoutView):
    template_name = 'registration/logout.html'
    success_url = reverse_lazy('index')


class MyProfile(LoginRequiredMixin, UpdateView):
    template_name = 'my-profile.html'
    queryset = User.objects.all()
    fields = ('username', 'first_name', 'last_name', 'email')
    success_url = reverse_lazy('index')

    def get_object(self, queryset=None):
        obj = self.get_queryset().get(id=self.request.user.id)
        return obj
