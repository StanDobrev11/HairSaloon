from django.views import generic as views

from HairSaloon.services.models import Service


# Create your views here.
class DetailServiceView(views.DetailView):
    queryset = Service.objects.all()
    template_name = 'partials/../../templates/services/services_card.html'

    def get_object(self, queryset=queryset):
        return queryset.get(pk=self.kwargs['pk'])

