from django.contrib.auth import get_user_model
from django.views import generic as views

from HairSaloon.common.models import Comment
from HairSaloon.hairdressers.models import HairDresser
from HairSaloon.services.models import Service

UserModel = get_user_model()


class IndexView(views.ListView):
    template_name = 'common/index.html'

    def get_queryset(self):
        return Service.objects.all()[:5]


class ListBlogView(views.ListView):
    template_name = 'common/blog.html'

    def get_queryset(self, queryset=None):

        try:
            user = UserModel.objects.get(pk=self.request.user.pk)
        except UserModel.DoesNotExist:
            return Comment.objects.filter(is_approved=True).order_by('-created_at')

        if user.is_superuser:
            return Comment.objects.all().order_by('-created_at')
        else:
            return Comment.objects.filter(is_approved=True).order_by('-created_at')


class AddCommentView(views.CreateView):
    template_name = 'common/add_comment.html'


class AboutView(views.ListView):
    template_name = 'common/about.html'
    queryset = HairDresser.objects.select_related('user')
