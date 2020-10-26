from django.urls import path, include

from kaucu import views
from django.contrib.auth import views as auth_views


user_patterns = ([
    path('', views.UserList.as_view() , name='list'),
    path('<str:slug>/', views.UserDetail.as_view() , name='detail'),
    path('<str:slug>/update', views.UserUpdate.as_view() , name='update'),
    path('<str:slug>/delete', views.UserDelete.as_view() , name='delete'),
    path('create_user', views.UserCreate.as_view() , name='create'),
], 'user')

contact_patterns = ([
    path('', views.ContactList.as_view() , name='list'),
    path('<str:slug>/', views.ContactDetail.as_view() , name='detail'),
    path('<str:slug>/update', views.ContactUpdate.as_view() , name='update'),
    path('<str:slug>/delete', views.ContactDelete.as_view() , name='delete'),
    path('create_contact', views.ContactCreate.as_view() , name='create'),
    path('search/<str:query>', views.ContactSearch.search , name='search'),
], 'contact')

package_patterns = ([
  path('create_package', views.PackageCreate.as_view() , name='create'),
  path('', views.PackageList.as_view() , name='list'),
  path('<int:pk>/', views.PackageDetail.as_view() , name='detail'),
  path('<int:pk>/update', views.PackageUpdate.as_view() , name='update'),
  path('<int:pk>/delete', views.PackageDelete.as_view() , name='delete'),
], 'package')

sale_patterns = ([
  path('', views.SaleList.as_view() , name='list'),
  path('<str:slug>/', views.SaleDetail.as_view() , name='detail'),
  path('<str:slug>/payment', views.SaleDetail.as_view() , name='payment'),
  path('<str:slug>/passenger', views.SaleDetail.as_view() , name='passenger'),
  path('<str:slug>/activity', views.SaleDetail.as_view() , name='activity'),

  path('<str:slug>/update', views.SaleUpdate.as_view() , name='update'),
  path('<str:slug>/delete', views.SaleDelete.as_view() , name='delete'),
  path('<str:slug>/create', views.SaleCreate.as_view() , name='create'),
  path('create', views.SaleCreate.as_view() , name='create'),

], 'sale')

hotel_patterns = ([
  path('<str:slug>/create', views.HotelCreate.as_view() , name='create'),
  path('<int:pk>/update', views.HotelUpdate.as_view() , name='update'),
  path('<int:pk>/delete', views.HotelDelete.as_view() , name='delete'),
], 'hotel')

flight_patterns = ([
  path('<str:slug>/create', views.FlightCreate.as_view() , name='create'),
  path('<int:pk>/update', views.FlightUpdate.as_view() , name='update'),
  path('<int:pk>/delete', views.FlightDelete.as_view() , name='delete'),
], 'flight')

transfer_patterns = ([
  path('<str:slug>/create', views.TransferCreate.as_view() , name='create'),
  path('<int:pk>/update', views.TransferUpdate.as_view() , name='update'),
  path('<int:pk>/delete', views.TransferDelete.as_view() , name='delete'),
], 'transfer')


passenger_patterns = ([
  path('<int:pk>/', views.PassengerDelete.as_view() , name='detail'),
  path('<str:slug>/create', views.PassengerCreate.as_view() , name='create'),
  path('<int:pk>/update', views.PassengerUpdate.as_view() , name='update'),
  path('<int:pk>/delete', views.PassengerDelete.as_view() , name='delete'),
], 'passenger')


payment_patterns = ([
    path('', views.PaymentList.as_view() , name='list'),
    path('<str:slug>/delete', views.PaymentDelete.as_view() , name='delete'),
    path('create_payment', views.PaymentCreate.as_view() , name='create'),
], 'payment')

sale_payment = ([
    path('<str:slug>/<int:pk>/delete', views.Sale_PaymentDelete.as_view() , name='delete'),
    path('<str:slug>/create', views.Sale_PaymentCreate.as_view() , name='create'),
], 'sale_payment')

supplier_payment = ([
    path('<int:pk>/delete', views.Supplier_PaymentDelete.as_view() , name='delete'),
    path('<int:pk>/create', views.Supplier_PaymentCreate.as_view() , name='create'),
], 'supplier_payment')

supplier_patterns = ([
    path('', views.SupplierList.as_view() , name='list'),
    path('<int:pk>/', views.SupplierDetail.as_view() , name='detail'),
    path('<int:pk>/update', views.SupplierUpdate.as_view() , name='update'),
    path('<int:pk>/delete', views.SupplierDelete.as_view() , name='delete'),
    path('create_supplier', views.SupplierCreate.as_view() , name='create'),
], 'supplier')

responder_patterns = ([
    path('<int:pk>/respond', views.Responder.as_view(), name='respond'),
    path('<str:slug>/respond', views.Responder.as_view(), name='respond'),
    path('<str:path>/redirect', views.ResponderRedirect.as_view(), name='redirect'),
    path('<str:slug>/<str:path>/redirect_slug', views.ResponderRedirectArgs.as_view(), name='redirect_slug'),
    path('<int:pk>/<str:path>/redirect_pk', views.ResponderRedirectArgs.as_view(), name='redirect_pk'),

], 'responder')

urlpatterns = [
    path('', views.Dashboard.as_view(), name='dashboard'),
    path('login/', auth_views.LoginView.as_view(redirect_authenticated_user=True), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('password_reset/', auth_views.PasswordResetView.as_view(), name='password_reset'),

    path('responder/', include(responder_patterns)),
    path('contact/', include(contact_patterns)),
    path('user/', include(user_patterns)),

    path('package/', include(package_patterns)),
    path('sale/', include(sale_patterns)),
    path('hotel/', include(hotel_patterns)),
    path('flight/', include(flight_patterns)),
    path('transfer/', include(transfer_patterns)),
    path('payment/', include(payment_patterns)),
    path('sale_payment/', include(sale_payment)),
    path('supplier_payment/', include(supplier_payment)),
    path('supplier/', include(supplier_patterns)),

    path('passenger/', include(passenger_patterns)),
]
