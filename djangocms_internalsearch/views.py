from django.views.generic import ListView, TemplateView
from cms.models import CMSPlugin, Page
from .forms import SearchForm
from django.http import HttpResponse

class SearchView(ListView):
    template_name = "djangocms_internalsearch/search.html"
    model = CMSPlugin
    form_class = SearchForm

    def get_queryset(self):
        return CMSPlugin.objects.values('plugin_type').distinct()

class ResultsView(ListView):
    template_name = 'djangocms_internalsearch/searchdetail.html'
    model = Page
    
    def dispatch(self, request, *args, **kwargs):
        #query = self.request.GET.get('q')
        return super(ResultsView, self).dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        return super(ResultsView, self).get_context_data(**kwargs)
    
    def get_queryset(self):
        query = self.request.GET.get('q')
        print(self.request.META['HTTP_REFERER'])
        return Page.objects.filter(publisher_public_id=CMSPlugin.objects.values_list('placeholder_id').filter(plugin_type__startswith=query))

