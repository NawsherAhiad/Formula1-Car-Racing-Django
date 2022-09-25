import imp
from django.contrib import admin
from django.urls import path
from formula1 import views
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('index/', views.index),
    path('signup/', views.signup),
    path('input_driver/', views.input_driver),
    path('insert_driver/', views.insert_driver),
    path('input_team/', views.input_team),
    path('input_circuit/', views.input_circuit),
    path('input_schedule/',views.input_schedule),
    path('insert_schedule/',views.insert_schedule),
    path('input_merch/', views.input_merch),
    path('insert_merch/', views.insert_merch),
    path('input_standings/', views.input_standings),
    path('insert_standings/', views.insert_standings),
    path('input_participation/', views.input_participation),
    path('insert_participation/', views.insert_participation),
    path('report_driver/',views.report_driver),
    path('report_circuit/',views.report_circuit),
    path('report_team/',views.report_team),
    path('report_merch/',views.report_merch),
    path('report_schedule/<str:years>',views.report_schedule),
    path('report_standing/<str:schedule_ids>',views.report_standing),
    path('report_participation/<str:schedule_id>',views.report_participation),
    path('report_users/',views.report_users),
    path('signin/',views.signin),
    path('signout/',views.signout),
    path('admin_page/',views.admin),
    path('edit_driver/<str:driver_id>',views.edit_driver),
    path('update_driver/<str:driver_id>',views.update_driver),
    path('delete_driver/<str:driver_id>',views.delete_driver),
    path('edit_standings/<str:standing_id>',views.edit_standings),
    path('update_standings/<str:standing_id>',views.update_standings),
    path('delete_standings/<str:standing_id>',views.delete_standings),
    path('edit_schedule/<str:schedule_id>',views.edit_schedule),
    path('update_schedule/<str:schedule_id>',views.update_schedule),
    path('delete_schedule/<str:schedule_id>',views.delete_schedule),
    path('edit_team/<str:team_id>',views.edit_team),
    path('update_team/<str:team_id>',views.update_team),
    path('delete_team/<str:team_id>',views.delete_team),
    path('edit_circuit/<str:circuit_serial>',views.edit_circuit),
    path('update_circuit/<str:circuit_serial>',views.update_circuit),
    path('delete_circuit/<str:circuit_serial>',views.delete_circuit),
    path('edit_merch/<str:product_id>',views.edit_merch),
    path('update_merch/<str:product_id>',views.update_merch),
    path('delete_merch/<str:product_id>',views.delete_merch),

    
]


urlpatterns += staticfiles_urlpatterns()
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)