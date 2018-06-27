from django.conf.urls import url


from . import views

urlpatterns = [
        url(r'^$', views.SearchView.as_view(), name='search'),
        url(r'^searchdetail$', views.ResultsView.as_view(), name='searchdetail'),
        ]
