from django.contrib.auth.models import User
from django.db.models import Count, F, Case, When
from django.http import JsonResponse
from rest_framework import generics
from rest_framework.generics import get_object_or_404
from rest_framework.views import APIView

from src.group_service import distribution_users_into_groups, create_list_groups_to_fill
from src.models import Product, Lesson, Group
from src.permissions import HasAccessToProduct
from src.serializers import ProductsSerializer, LessonSerializer, ProductsStaticticSerializer


# Create your views here.

class ProductListView(generics.ListAPIView):
    queryset = Product.objects.filter(started=True).annotate(lessons_quantity=Count('lesson'))
    serializer_class = ProductsSerializer


class LessonsListView(generics.ListAPIView):
    serializer_class = LessonSerializer
    permission_classes = [HasAccessToProduct, ]

    def get_queryset(self):
        return Lesson.objects.filter(product_id=self.kwargs['product_id'])


class AddUserView(APIView):
    def post(self, request, *args, **kwargs):
        product = get_object_or_404(Product, id=kwargs.get('product_id'))
        groups = Group.objects.filter(products_id=kwargs.get('product_id')).annotate(
            student_count=Count('students'))
        for group in groups:
            if group.student_count < product.max_students:
                group.students.add(request.user.id)
                return JsonResponse({"message": "Users distributed to groups successfully."})
        return JsonResponse({"message": "All groups are full."})


class ResetGroupsView(APIView):
    def post(self, request, *args, **kwargs):
        products = Product.objects.filter(pk=kwargs.get('product_id')).annotate(group_count=Count('group'),
                                                                               sum_students=Count('group__students'))
        if products[0].started:
            return JsonResponse({"message": "The course has already started. Can't rebuild group."})
        list_groups = create_list_groups_to_fill(products)
        distribution_users_into_groups(list_groups)
        return JsonResponse({"message": "Groups successfully reassembled."})


class ProductStatisticListView(generics.ListAPIView):
    queryset = Product.objects.all().prefetch_related('group').annotate(student_quantity=Count('group__students'),
                                                                        acquisition_percentage=100 * Count(
                                                                            'group__students') / User.objects.count())
    serializer_class = ProductsStaticticSerializer
