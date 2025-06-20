from django.urls import path
from . import views

app_name = "pressupostos"

urlpatterns = [
    path('', views.list_pressuposts),  # 👈 Esto permite acceder directamente a /pressupostos/
    path('list/', views.list_pressuposts, name='list'),
    path('form/', views.form_pressupost, name='create'),
    path('form/<int:id>/', views.form_pressupost, name='edit'),
    path('delete/<int:id>/', views.delete_pressupost, name='delete'),

    # AJAX endpoints
    path('get_increment_hores/', views.get_increment_hores, name='get_increment_hores'),
    path('get_projectes/<int:id_client>/', views.get_projectes_by_client, name='get_projectes_by_client'),
    path('get_tasques/<int:id_treball>/', views.get_tasques_by_treball, name='get_tasques_by_treball'),
    path('get_recurso/<int:id_recurso>/', views.get_recurso_by_id, name='get_recurso'),
    path('pdf/<int:id>/', views.ver_pdf_pressupost, name='pdf'),
    path('<int:pressupost_id>/generar_pdf/', views.generar_pdf_y_guardar, name='generar_pdf'),
    #path('detail/<int:pk>/', views.detail_view, name='detail')


]
