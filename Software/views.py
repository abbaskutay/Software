from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect
from django.views.generic import TemplateView


class TestPage(TemplateView):
    template_name = 'test.html'


class HomePage(TemplateView):
    template_name = "index.html"

    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated():
            return HttpResponseRedirect(reverse("test"))
        return super(HomePage,self).get(request, *args, **kwargs)





class AboutPage(TemplateView):
    template_name = 'about.html'
