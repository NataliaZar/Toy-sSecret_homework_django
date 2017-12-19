"""lab5 URL Configuration

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
from django.conf.urls import url, include
from labApp.views import *
from django.conf.urls.static import static
from django.conf import settings
from django.contrib.staticfiles.urls import staticfiles_urlpatterns


urlpatterns = [
    url(r'^order_add/(?P<prodact>[^/]+)', order_add, name='order_add'),
    url(r'^$', home),
    url(r'^prodact/(?P<prodact>[^/]+)', prodact_page, name='prodact_page'),
    url(r'^prodact_list/$', ProdactsView.as_view(), name='prodacts_list'),
    url(r'^order_list/$', OrderView.as_view(), name='order_list'),
    url(r'^prodact_add/$', prodact_add, name='prodact_add'),
    url(r'^registration_form/$', registration_form, name='registration_form'),
    url(r'^registration/$', registration, name='registration'),
    url(r'^authorization_form/$', authorization_form, name='authorization_form'),
    url(r'^authorization/$', authorization, name='authorization'),
    url(r'^logout$', logout_view, name='logout'),
    url(r'^success_authorization_form$', success_authorization_form, name='success_authorization_form'),
    url(r'^success_authorization$', success_authorization, name='success_authorization'),
    url(r'^admin/', include(admin.site.urls))
]
ajax_functions = [
    url(r'^ajax/order/', ajax_order, name='ajax_order'),
    #url(r'^ajax/last_bookings/', ajax_last_bookings, name='ajax_last_bookings'),
]
urlpatterns += ajax_functions
urlpatterns += staticfiles_urlpatterns()
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
