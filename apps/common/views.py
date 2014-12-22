from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import render


class LoginRequiredMixin(object):
    @classmethod
    def as_view(cls, **initkwargs):
        view = super(LoginRequiredMixin, cls).as_view(**initkwargs)
        return login_required(view)


class CSRFExemptMixin(object):
    @classmethod
    def as_view(cls, **initkwargs):
        view = super(CSRFExemptMixin, cls).as_view(**initkwargs)
        return csrf_exempt(view)


def error404(request):
    return render(request, '404.html', status=404)
