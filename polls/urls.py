from django.urls import path
from .views import (
    RegistroView, InicioSesionView, SalirView, ListaRecetasView, ListaMisRecetasView, 
    IngresarRecetaView, EditarRecetaView, AsociarRecetaAUsuarioView, AgregarComentarioView,UsuarioListaView, SeleccionarRecetasView, ListaComprasView,ListaFavoritasView, MarcarFavoritoView, RegistrarCocinadoView,HistorialCocinadoView, ReporteEstadisticasView, ExportarEstadisticasCSVView, AgregarComentarioView, MarcarNotificacionLeidaView, NotificacionesView
)

urlpatterns = [
    path('', ListaRecetasView.as_view(), name='lista_recetas'),
    path('lista_recetas/', ListaRecetasView.as_view(), name='lista_recetas'),
    path('inicio_sesion/', InicioSesionView.as_view(), name='inicio_sesion'),
    path('ingresar_receta/', IngresarRecetaView.as_view(), name='ingresar_receta'),
    path('recetas_usuario/', ListaMisRecetasView.as_view(), name='lista_recetas_usuario'), 
    path('asociar_receta/<int:receta_id>/', AsociarRecetaAUsuarioView.as_view(), name='asociar_receta'),
    path('logout/', SalirView.as_view(), name='salir'),
    path('registro/', RegistroView.as_view(), name='registro'),
    path('receta/editar/<int:pk>/', EditarRecetaView.as_view(), name='editar_receta'),
    path('comentarios_calificaciones/<int:receta_id>/', AgregarComentarioView.as_view(), name='comentarios_calificaciones'),
    path('usuario_lista/', UsuarioListaView.as_view(), name='usuario_lista'),  
    # Seleccionar recetas para generar la lista de compras
    path('seleccionar_recetas/', SeleccionarRecetasView.as_view(), name='seleccionar_recetas'),
    # Ver lista de compras generada
    path('lista_compras/', ListaComprasView.as_view(), name='ver_lista_compras'),
    #funciones de favorito
    path('recetas_favoritas/', ListaFavoritasView.as_view(), name='recetas_favoritas'),
    path('marcar_favorito/<int:pk>/', MarcarFavoritoView.as_view(), name='marcar_favorito'),
    path('receta/<int:receta_id>/cocinado/', RegistrarCocinadoView.as_view(), name='registrar_cocinado'),
    path('historial/', HistorialCocinadoView.as_view(), name='historial_cocinados'),
    path('reporte_estadisticas/', ReporteEstadisticasView.as_view(), name='reporte_estadisticas'),
    path('exportar_estadisticas_csv/', ExportarEstadisticasCSVView.as_view(), name='exportar_estadisticas_csv'),
    path('notificaciones/', NotificacionesView.as_view(), name='notificaciones'),
    path('agregar_comentario/<int:receta_id>/', AgregarComentarioView.as_view(), name='agregar_comentario'),
    path('notificaciones/marcar_leida/<int:notificacion_id>/', MarcarNotificacionLeidaView.as_view(), name='marcar_notificacion_leida'),
    ]



