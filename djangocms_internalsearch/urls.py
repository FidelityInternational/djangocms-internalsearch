from django.conf.urls import include, url


urlpatterns = [
        url(r'^search/', include('haystack.urls')),
    ]
