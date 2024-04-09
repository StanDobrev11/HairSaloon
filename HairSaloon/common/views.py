from django.views import generic as views

from HairSaloon.hairdressers.models import HairDresser
from HairSaloon.services.models import Service


class IndexView(views.ListView):
    template_name = 'common/index.html'

    def get_queryset(self):
        return Service.objects.all()[:5]


class BlogView(views.ListView):
    template_name = 'common/blog.html'

    def get_object(self, queryset=None):
        pass


class AboutView(views.ListView):
    template_name = 'common/about.html'
    queryset = HairDresser.objects.select_related('user')
