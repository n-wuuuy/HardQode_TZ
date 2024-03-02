from django.urls import path

from src.views import ProductListView, LessonsListView, AddUserView, ProductStatisticListView, ResetGroupsView

urlpatterns = [
    path('api/products', ProductListView.as_view()),
    path('api/product/<int:product_id>', LessonsListView.as_view()),
    path('api/register/product/<int:product_id>', AddUserView.as_view()),
    path('api/statictic', ProductStatisticListView.as_view()),
    path('api/reset/<int:product_id>', ResetGroupsView.as_view())
]
