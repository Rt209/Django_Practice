from rest_framework import generics
from .models import Item, Location, Post,Inventory
from .serializers import ItemSerializer, LocationSerializer, InventorySerializer
from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
import cv2
import os
from django.http import StreamingHttpResponse
from django.http import JsonResponse
from datetime import datetime
from django.conf import settings
from django.views.decorators.csrf import csrf_exempt
from urllib.parse import urljoin

class ItemList(generics.ListCreateAPIView):
    serializer_class = ItemSerializer

    def get_queryset(self):
        queryset = Item.objects.all()
        location = self.request.query_params.get('location') #索引值
        if location is not None:
            queryset = queryset.filter(itemLocation = location)
        return queryset
    
class ItemDetail(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = ItemSerializer
    queryset = Item.objects.all()

class LocationList(generics.ListCreateAPIView):
    serializer_class = LocationSerializer
    queryset = Location.objects.all()

class LocationDetail(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = LocationSerializer
    queryset = Location.objects.all()

def say_hello(request):
    return HttpResponse("OMGDS")

def home(request):
    return render(request, 'home.html', {})


RTSP = 'RTSP_URL'
DEFAULT_RTSP_URL = 'rtsp://192.168.178.214/'
RTSP_URL = os.getenv(RTSP,DEFAULT_RTSP_URL)
# container -> environment variables -> "RTSP_URL"
#  e.g. -> value = os.getenv('RTSP_url', 'rtsp://192.168.178.214/') 

camera = cv2.VideoCapture(RTSP_URL)

def gen_display():
    """
    攝影機視頻流生成器
    """
    while True:
        ret, frame = camera.read()
        if ret:
            # 將畫面轉換為 JPEG 格式
            ret, buffer = cv2.imencode('.jpeg', frame)
            if ret:
                yield (b'--frame\r\n'
                       b'Content-Type: image/jpeg\r\n\r\n' + buffer.tobytes() + b'\r\n')

def video_stream(request):
    """
    視頻流路由
    """
    return StreamingHttpResponse(gen_display(), content_type='multipart/x-mixed-replace; boundary=frame')

@csrf_exempt
def capture_image(request):
    """
    擷取當前畫面並轉灰階處理，回傳灰階圖片的 URL
    """
    if request.method == 'POST':
        # 獲取當前攝影機畫面
        ret, frame = camera.read()  # 假設 camera 已經正確初始化
        if ret:
            # 保存原始圖片與灰階圖片
            save_path = os.path.join(settings.BASE_DIR, 'static', 'captured_images')  # 修改為 static 資料夾
            os.makedirs(save_path, exist_ok=True)  # 確保目錄存在

            # 生成唯一文件名
            timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
            original_filename = f'original_{timestamp}.jpg'
            processed_filename = f'processed_{timestamp}.jpg'

            # 原始圖片
            original_filepath = os.path.join(save_path, original_filename)
            cv2.imwrite(original_filepath, frame)

            # 轉灰階
            gray_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            processed_filepath = os.path.join(save_path, processed_filename)
            cv2.imwrite(processed_filepath, gray_frame)

            # ======= 信息 =======
            print(f"STATIC_ROOT: {settings.BASE_DIR}")
            print(f"Original image path: {original_filepath}")
            print(f"Processed file path: {processed_filepath}")
            print(f"File exists (original): {os.path.exists(original_filepath)}")
            print(f"File exists (processed): {os.path.exists(processed_filepath)}")
            # ========================

            # 返回處理後圖片的 URL
            processed_image_url = urljoin(settings.STATIC_URL, f'captured_images/{processed_filename}')
            print(f"Processed image URL: {processed_image_url}")  # 調試 URL
            return JsonResponse({'processed_image_url': processed_image_url})

        return JsonResponse({'error': 'Failed to capture image.'}, status=500)

    return JsonResponse({'error': 'Invalid request method.'}, status=400)

def video_display(request):

    """
    返回顯示視頻流和捕捉功能的 HTML
    """
    return render(request, "video_display.html")

def inventory_list(request):
    inventories = Inventory.objects.all()
    return render(request, 'inventory_list.html', {'inventories': inventories})

def inventory_create(request):
    """
    顯示新增頁面，提交後儲存資料，並跳轉回清單頁面。
    """
    if request.method == 'POST':
        name = request.POST.get('name')
        location = request.POST.get('location')
        Inventory.objects.create(name=name, location=location)
        return redirect('inventory_list')
    return render(request, 'inventory_form.html')

def inventory_update(request, id):
    """
    顯示更新頁面，提交後更新資料，並跳轉回清單頁面。
    """
    inventory = get_object_or_404(Inventory, id=id)
    if request.method == 'POST':
        inventory.name = request.POST.get('name')
        inventory.location = request.POST.get('location')
        inventory.save()
        return redirect('inventory_list')
    return render(request, 'inventory_form.html', {'inventory': inventory})

def inventory_delete(request, id):
    """
    刪除指定的項目，並跳轉回清單頁面。
    """
    inventory = get_object_or_404(Inventory, id=id)
    inventory.delete()
    return redirect('inventory_list')