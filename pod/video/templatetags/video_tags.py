from django import template
from django.utils.text import capfirst
from django.urls import reverse
from ..forms import VideoVersionForm

import importlib

register = template.Library()


@register.simple_tag
def get_app_link(video, app):
    mod = importlib.import_module('pod.%s.models' % app)
    if hasattr(mod, capfirst(app)):
        video_app = eval(
            'mod.%s.objects.filter(video__id=%s).all()' % (
                capfirst(app), video.id))
        if (app == "interactive"
                and video_app.first() is not None
                and video_app.first().is_interactive() is False):
            video_app = False
        if video_app:
            url = reverse('%(app)s:video_%(app)s' %
                          {"app": app}, kwargs={'slug': video.slug})
            return ('<a href="%(url)s" title="%(app)s" '
                    'class="dropdown-item" target="_blank">%(link)s</a>') % {
                "app": app,
                "url": url,
                "link": mod.__NAME__}
    return ""


@register.simple_tag
def get_version_form(video):
    form = VideoVersionForm()
    return form
