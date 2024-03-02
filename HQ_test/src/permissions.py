from rest_framework import permissions

from src.models import Group


class HasAccessToProduct(permissions.BasePermission):
    def has_permission(self, request, view):
        return Group.objects.filter(
            products_id=view.kwargs.get("product_id"), students=request.user
        ).exists()
