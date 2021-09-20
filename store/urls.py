from django.urls import path
from .views import updateItem,processOrder,ProductListView,CartListView,CheckoutListView,homeview


urlpatterns = [
    path('',ProductListView.as_view(),name='store'),
    #path('',StoreListView.as_view(),name='store'),
    path('cart/',CartListView.as_view(),name='cart'),
    path('checkout/',CheckoutListView.as_view(),name='checkout'),
    path('update_item/',updateItem,name='update'),
    path('process_order/',processOrder,name='proccess'),
]
