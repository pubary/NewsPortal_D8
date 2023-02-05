from django.urls import path
from .views import *

urlpatterns = [
   path('search/', PostSearch.as_view(), name='post_search'),
   path('cat/<slug:slug>/', PostsList.as_view(), name='category_show'),
   # path('cat/<slug:slug>/subscribe', subscribe_me, name='subscription'),
   path('<int:pk>', PostDetail.as_view(), name='post_detail'),
   path('<slug:p_type>/create/', PostCreate.as_view(), name='post_create'),
   path('<int:pk>/edit/', PostEdit.as_view(), name='post_edit'),
   path('<int:pk>/delete/', PostDelete.as_view(), name='post_delete'),
   path('<slug:p_type>/', PostsList.as_view(), name='post_type'),

]