"""infoauto URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
# from django.conf.urls import url
# from django.contrib import admin

from django.conf.urls import url, include
from django.contrib import admin

from rest_framework import routers
from rest_framework_jwt.views import obtain_jwt_token, verify_jwt_token
from rest_framework.documentation import include_docs_urls

# from rest_framework.documentation import include_docs_urls

from general import views
# from general.views import selectraw

router = routers.DefaultRouter()

# router.register(r'users', views.UserViewSet)
# router.register(r'groups', views.GroupViewSet)

# router.register(r'pais', views.PaisViewSet)
# router.register(r'estado', views.EstadoViewSet)
# router.register(r'ciudad', views.CiudadViewSet)
#
# router.register(r'cia', views.CiaViewSet)
# router.register(r'usercia', views.UserCiaViewSet)
# router.register(r'ciaconsecutivo', views.CiaConsecutivoViewSet)
# router.register(r'userlog', views.UserLogViewSet)
# router.register(r'persona', views.PersonaViewSet)
# router.register(r'personajuridica', views.PersonaJuridicaViewSet)
# router.register(r'personanatural', views.PersonaNaturalViewSet)
# router.register(r'producto', views.ProductoViewSet)
# router.register(r'direccion', views.DireccionViewSet)
# router.register(r'sesiontrabajo', views.SesionTrabajoViewSet)
# router.register(r'docrep', views.DocRepViewSet)
# router.register(r'docrepdet', views.DocRepDetViewSet)


# urlpatterns = [
#     url(r'^admin/', admin.site.urls),
# ]

urlpatterns = [
    url(r'^api-token-auth/', obtain_jwt_token),
    url(r'^admin/', admin.site.urls),
    url(r'^docs/', include_docs_urls(title='API Taller')),
    url(r'^', include(router.urls)),
    # url(r'^selectraw/', selectraw),
    # url(r'^report/$', views.reporte),
    # url(r'^estadopdf/$', views.estado_to_pdf_view),
]