from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("wiki/<str:title>",views.entry, name="entry"),
    path("encyclopedia/new_page",views.new_page,name="new_page"),
    path("encyclopedia/entry",views.random_page, name="random_page"),
    path("encyclopedia/edit",views.edit_page, name="edit_page"),
    path("encyclopedia/save_changes",views.save_changes, name="save_changes"),
    path("encyclopedia/search", views.search_engine, name="search_engine")
]
