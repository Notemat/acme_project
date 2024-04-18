from django.views.generic import (
    CreateView, DeleteView, DetailView, ListView, UpdateView
)
from django.urls import reverse, reverse_lazy
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import UserPassesTestMixin, LoginRequiredMixin
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, redirect

from .forms import BirthdayForm, CongratulationForm
from .models import Birthday, Congratulation
from .utils import calculate_birthday_countdown


class OnlyAuthorMixin(UserPassesTestMixin):
    """Миксин для проверки на авторство поста."""

    def test_func(self):
        object = self.get_object()
        return object.author == self.request.user


@login_required
def simple_view(request):
    return HttpResponse('Страница для залогиненных пользователей!')


class CongratulationCreateView(LoginRequiredMixin, CreateView):
    """Создание поздравления(комментарии)."""

    birthday = None
    model = Congratulation
    form_class = CongratulationForm

    def dispatch(self, request, *args, **kwargs):
        self.birthday = get_object_or_404(Birthday, pk=kwargs['pk'])
        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        form.instance.author = self.request.user
        form.instance.birthday = self.birthday
        return super().form_valid(form)

    def get_success_url(self):
        return reverse('birthday:detail', kwargs={'pk': self.birthday.pk})
    
    


class BirthdayCreateView(LoginRequiredMixin, CreateView):
    """Создание объекта формы."""

    model = Birthday
    form_class = BirthdayForm
 
    def form_valid(self, form):
        """Присваиваем полю автора значение из запроса пользователя."""
        form.instance.author = self.request.user
        return super().form_valid(form)


class BirthdayUpdateView(OnlyAuthorMixin, UpdateView):
    """Редактирование объектов."""

    model = Birthday
    form_class = BirthdayForm


class BirthdayDeleteView(OnlyAuthorMixin, DeleteView):
    """Удаление объектов."""

    model = Birthday


class BirthdayListView(ListView):
    """Создание списка объектов, сортировка и пагинация."""

    model = Birthday
    queryset = Birthday.objects.prefetch_related(
        'tags'
    ).select_related('author')
    ordering = 'id'
    paginate_by = 10


class BirthdayDetailView(DetailView):
    """Создание отдельного объекта."""

    model = Birthday

    def get_context_data(self, **kwargs):
        """Утилита по подсчету дней рождения."""
        context = super().get_context_data(**kwargs)
        context["birthday_countdown"] = calculate_birthday_countdown(
            self.object.birthday
        )
        context['form'] = CongratulationForm()
        context['congratulations'] = (
            self.object.congratulations.select_related('author')
        )
        return context
