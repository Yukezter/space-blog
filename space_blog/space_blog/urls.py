from django.conf import settings
from django.conf.urls import include, url
from django.contrib import admin
from django.views.generic import TemplateView

from wagtail.admin import urls as wagtailadmin_urls
from wagtail.core import urls as wagtail_urls
from wagtail.documents import urls as wagtaildocs_urls

from django.views.generic import TemplateView, ListView

from pages.views import category, search
from blog.views import lazy_load_posts


urlpatterns = [
    url(r'^django-admin/', admin.site.urls),

    url(r'^admin/', include(wagtailadmin_urls)),
    url(r'^documents/', include(wagtaildocs_urls)),

    url(r'^$', TemplateView.as_view(template_name='pages/home.html'), name='home'),
    url(r'^category/(?P<category>technology|missions|politics|discoveries)$', category, name='category'),
    # url(r'^category/(?P<category>technology|missions|politics|discoveries)$', TemplateView.as_view(template_name='pages/category.html'), name='category'),
    url(r'^search/$', search, name='search'),

    url(r'^lazy_load_posts', lazy_load_posts, name='lazy_load_posts'),

    url(r'^blog/', include(wagtail_urls)),
]


if settings.DEBUG:
    from django.conf.urls.static import static
    from django.contrib.staticfiles.urls import staticfiles_urlpatterns

    # Serve static and media files from development server
    urlpatterns += staticfiles_urlpatterns()
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
