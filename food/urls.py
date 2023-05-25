from django.urls import path
from . import views
urlpatterns = [
    path('', views.Home.as_view(), name="home"),
    path('cart', views.Carts.as_view(), name="cart"),
    path('cart/remove/', views.Cart_Remove, name="cart_remove"),    
    path('order/cart/<int:id>/', views.Orders.as_view(), name="cart_order"),
    path('order/quick/<int:id>/<int:quantity>/', views.Orders.as_view(), name="quick_order"),
    path('order/items/<str:id>/<str:quantity>/', views.Multi_Orders.as_view(), name="multi_order"),    
    # path('order/cancel/', views.Cancel_Order, name="cancel_order"),
    path('orders/', views.All_Orders.as_view(), name="orders"),
    path('order/summary/', views.count, name='summary'),
]

