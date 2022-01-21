from django.urls import URLPattern, path
from .views import blogDetail, index, searchCategory, searchWriter

urlpatterns = [
    path('',index,name='index'),
    path('blog/<int:id>',blogDetail,name='blogDetail'),
    path('blog/category/<int:category_id>',searchCategory,name='searchCategory'),
    path('blog/writer/<str:writer>',searchWriter,name='searchWriter'),
    ]