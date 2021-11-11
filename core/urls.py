from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi

from django.contrib import admin
from django.urls import path, include

from django.conf import settings
from django.conf.urls.static import static


schema_view = get_schema_view(
    openapi.Info(
        title="Meegu API",
        default_version="v1",
        description="The Don't care version.",
        terms_of_service="https://www.google.com/policies/terms/",
        contact=openapi.Contact(email="contact@snippets.local"),
        license=openapi.License(name="BSD License"),
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
)

urlpatterns = [
    path("admin/", admin.site.urls),
    path("classroom/", include("classrooms.urls")),
    path("workspace/", include("workspaces.urls")),
    path("note/", include("notes.urls")),
    path("chat/", include("chats.urls")),
    path("article/", include("articles.urls")),
    path("library/", include("libraries.urls")),
    path("institution/", include("institutions.urls")),
    path("subcription/", include("subscriptions.urls")),
    path("api/user/", include("users.urls", namespace="users")),
    # YASG
    path("docs/", schema_view.with_ui("swagger", cache_timeout=0), name="schema-swagger-ui"),
    path("api/api.json/", schema_view.without_ui(cache_timeout=0), name="schema-swagger-ui"),
    path("redoc/", schema_view.with_ui("redoc", cache_timeout=0), name="schema-redoc"),
    # OAuth
    path("auth/", include("drf_social_oauth2.urls", namespace="drf")),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
