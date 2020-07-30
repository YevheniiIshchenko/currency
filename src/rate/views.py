from django.views.generic import ListView

from rate.models import Rate


# def show_rates(request):
#    items = Rate.objects.all()
#    content = {'items': items}
#    return render(request, 'show-rates.html', context=content)


class RateListView(ListView):
    model = Rate
    queryset = Rate.objects.all()
    template_name = 'show-rates.html'
