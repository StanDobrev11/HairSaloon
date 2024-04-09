from django.contrib.auth import get_user_model
from django.contrib.auth import mixins as auth_mixins
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views import generic as views

from HairSaloon.common.forms import CommentForm
from HairSaloon.common.models import Comment
from HairSaloon.hairdressers.models import HairDresser
from HairSaloon.services.mixins import AdminRequiredMixin
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


class AddCommentView(auth_mixins.LoginRequiredMixin, views.CreateView):
    template_name = 'common/add_comment.html'
    form_class = CommentForm
    success_url = reverse_lazy('blog')

    def form_valid(self, form):
        form = form.save(commit=False)
        user = UserModel.objects.get(pk=self.request.user.pk)
        form.user = user
        form.save()
        return redirect(self.success_url)


class DeleteCommentView(AdminRequiredMixin, views.DeleteView):
    model = Comment
    success_url = reverse_lazy('blog')
    template_name = 'common/delete_comment.html'

    def get_object(self, queryset=None):
        return Comment.objects.get(pk=self.kwargs['pk'])


class AboutView(views.ListView):
    template_name = 'common/about.html'
    queryset = HairDresser.objects.select_related('user')
