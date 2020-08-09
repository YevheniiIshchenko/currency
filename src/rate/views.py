from django.http import HttpResponse
from django.urls import reverse_lazy
from django.views.generic import ListView, TemplateView, View, UpdateView, DeleteView
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.contrib.auth.mixins import UserPassesTestMixin

from openpyxl import Workbook

from rate.models import Rate
from rate.selectors import get_latest_rates


def display_atr(rate, atr):
    if hasattr(rate, f'get_{atr}_display'):
        return getattr(rate, f'get_{atr}_display')()
    else:
        return getattr(rate, atr)


class RateListView(ListView):
    model = Rate
    queryset = Rate.objects.all().order_by('created').iterator()
    template_name = 'show-rates.html'


class LatestRates(TemplateView):
    template_name = 'latest-ratest.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['object_list'] = get_latest_rates()
        return context


class RateDownloadCSV(View):
    HEADERS = (
        'id',
        'created',
        'source',
        'currency_type',
        'type',
        'amount',
    )

    queryset = Rate.objects.all().iterator()

    def get(self, request):

        response = HttpResponse(
            content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',
        )
        response['Content-Disposition'] = 'attachment; filename="rates.xlsx"'

        workbook = Workbook()
        worksheet = workbook.active

        worksheet.append(self.HEADERS)

        # counter = 1
        for rate in self.queryset:
            row = []
            for atr in self.HEADERS:
                row.append(display_atr(rate, atr))
            worksheet.append(row)

        workbook.save(response)
        return response


class EditRate(UserPassesTestMixin, UpdateView):
    template_name = 'edit-rate.html'
    queryset = Rate.objects.all()
    fields = ('source', 'currency_type', 'type', 'amount')
    success_url = reverse_lazy('rate:show-rates')

    def test_func(self):
        return self.request.user.is_staff


class DeleteRate(UserPassesTestMixin, DeleteView):
    template_name = 'delete-rate.html'
    model = Rate
    success_url = reverse_lazy('rate:show-rates')

    def test_func(self):
        return self.request.user.is_staff
