from django.urls import path,re_path
from . import views
app_name = 'goods'
urlpatterns = [
    path('login/', views.login_site, name='login'),
    path('logout/', views.logout_site, name='logout'),
    path('', views.show_list,name='product_list'),
    re_path('(?P<page>\d+)/$', views.show_list),
    path('search/', views.search, name='search'),
    path('download/',views.export_excel,name = 'export_excel'),
] 


