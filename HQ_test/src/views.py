from django.contrib.auth.models import User
from django.db.models import Count
from django.http import JsonResponse
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView

from src.group_service import add_student, sorting_group
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
    permission_classes = [IsAuthenticated, ]

    def post(self, request, **kwargs):
        product = Product.objects.filter(pk=kwargs.get('product_id')).annotate(group_count=Count('group'))[0]
        if Group.objects.filter(products_id=kwargs.get('product_id'), students__id=request.user.id).exists():
            return JsonResponse({"message": "This user is already included in the group."})
        groups = Group.objects.filter(products_id=kwargs.get('product_id')).annotate(
            student_count=Count('students')).order_by('id')
        massage = add_student(product, groups, request.user.id)
        return JsonResponse(massage)


class ResetGroupsView(APIView):
    def post(self, request, **kwargs):
        product = Product.objects.filter(pk=kwargs.get('product_id')).annotate(group_count=Count('group'))[0]
        if product.started:
            return JsonResponse({"message": "The course has already started. Can't rebuild group."})
        groups = Group.objects.filter(products=product)
        try:
            sorting_group(product, groups)
        except Exception as e:
            exception_massage = e.__str__()
            return JsonResponse({"message": exception_massage})
        return JsonResponse({"message": "Groups successfully reassembled."})


class ProductStatisticListView(generics.ListAPIView):
    queryset = Product.objects.all().prefetch_related('group').annotate(student_quantity=Count('group__students'),
                                                                        acquisition_percentage=100 * Count(
                                                                            'group__students') / User.objects.count())
    serializer_class = ProductsStaticticSerializer
