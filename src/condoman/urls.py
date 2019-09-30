from django.conf import settings
from django.conf.urls.i18n import i18n_patterns
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path
from django.utils.translation import gettext_lazy as _
from django.views.i18n import JavaScriptCatalog

import accounts.urls
import profiles.urls

from . import views


# Personalized admin site settings like title and header
admin.site.site_title = "Condoman Site Admin"
admin.site.site_header = "Condoman Administration"

urlpatterns = [
    path("jsi18n/", JavaScriptCatalog.as_view(), name="javascript-catalog"),
    path("i18n/", include("django.conf.urls.i18n")),
]


urlpatterns += i18n_patterns(
    path("", views.HomePage.as_view(), name="home"),
    path(_("about/"), views.AboutPage.as_view(), name="about"),
    path(_("users/"), include(profiles.urls)),
    path("admin/", admin.site.urls),
    path("", include(accounts.urls)),
)

# User-uploaded files like profile pics need to be served in development
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

# Include django debug toolbar if DEBUG is on
if settings.DEBUG:
    import debug_toolbar

    urlpatterns += [path("__debug__/", include(debug_toolbar.urls))]
