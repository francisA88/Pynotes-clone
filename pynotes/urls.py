from django.contrib import admin
from django.urls import path
from django.conf.urls.static import static 
from django.conf import settings

import main.views as views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('notes/save/', views.save_note, name='save'),
    path('notes/<int:note_num>/view', views.view_note_check, name='view_check'),
    path('notes/<str:temp_key>/<int:note_num>', views.view_note, name='view'),
    path('', views.home),
    path('notes/<int:note_num>/delete', views.delete_note, name='delete'),
    path('search/<str:search_key>', views.get_search_results, name='search'),
    path('notes/api/fetch/<int:note_num>', views.api_fetch),
    path('notes/create', views.create_note, name='create'),
    path('notes/<int:note_num>/password', views.password_entry),
    path('notes/<int:note_num>/validate', views.validate_password)
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

#print(static(settings.STATIC_URL, document_root=settings.STATIC_ROOT))