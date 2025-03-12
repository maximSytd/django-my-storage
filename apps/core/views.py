import os

from django.conf import settings
from django.http import Http404
from django.views.generic import TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.static import serve
from django.contrib.auth.decorators import login_required
from django.utils.translation import gettext_lazy as _

class IndexView(LoginRequiredMixin, TemplateView):
    """Class-based view for index page."""

    template_name = "index.html"


@login_required
def protected_serve(request, path):
    if not os.path.exists(os.path.join(settings.MEDIA_ROOT, path)):
        raise Http404(_("File does not exist"))

    return serve(request, path, document_root=settings.MEDIA_ROOT)