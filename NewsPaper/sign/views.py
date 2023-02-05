from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User, Group
from django.shortcuts import redirect
from django.views.generic.edit import CreateView

from news.models import Author
from .models import UserRegisterForm


# class UserRegisterView(CreateView):
#     model = User
#     form_class = UserRegisterForm
#     success_url = '/'


@login_required
def upgrade_me(request):
    user = request.user
    author_group = Group.objects.get(name='authors')
    if not request.user.groups.filter(name='authors').exists():
        Author.objects.create(author_acc=user)
        author_group.user_set.add(user)
    return redirect('/')

