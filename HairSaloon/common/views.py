from django.views import generic as views

from HairSaloon.hairdressers.models import HairDresser


# Create your views here.
class IndexView(views.TemplateView):
    template_name = 'common/index.html'


class BlogView(views.TemplateView):
    template_name = 'common/blog.html'


class AboutView(views.ListView):
    template_name = 'common/about.html'
    queryset = HairDresser.objects.all()
