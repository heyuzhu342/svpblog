"""django_blog URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.10/topics/http/urls/
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

from django.urls import path, include, re_path
from django.contrib import admin
from blog import views
from django.conf.urls.static import static
from django_blog import settings

from blog.views import PhotoGroupView, PhotoView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('blog/', include(('blog.urls', 'blog'), namespace='blog')),
    path('', views.index, name='index'),
    path('ckeditor/', include('ckeditor_uploader.urls')),
    path('photogroup/', PhotoGroupView.as_view(), name="photogroup"),
    re_path(r'photogroup/(?P<group>\w+)/', PhotoView.as_view(), name="photo"),


]

handler404 = views.page_not_found_error
handler500 = views.page_error

if settings.DEBUG:
    # 仅在开发环境下添加媒体文件服务
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)