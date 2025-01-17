from . import views
from django.urls import path
from .views import ItemList, ItemDetail, LocationList, LocationDetail
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    path('hello/',views.say_hello),
    path('item/', ItemList.as_view()),
    path('item/<int:pk>', ItemList.as_view()),
    path('location/', LocationList.as_view()),
    path('location/<int:pk>/', LocationDetail.as_view()),
    path('', views.home, name = "home"),
    path('video_stream/', views.video_stream, name='video_stream'),
    path('video_display/', views.video_display, name='video_display'),# 串流 & 擷取
    path('capture_image/', views.capture_image, name='capture_image'), 
    path('inventory/', views.inventory_list, name='inventory_list'),  # 總覽
    path('inventory/create/', views.inventory_create, name='inventory_create'),  # 新增
    path('inventory/update/<int:id>/', views.inventory_update, name='inventory_update'),  # 編輯
    path('inventory/delete/<int:id>/', views.inventory_delete, name='inventory_delete'),  # 刪除
]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

