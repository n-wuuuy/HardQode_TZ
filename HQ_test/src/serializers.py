from django.contrib.auth.models import User
from django.db.models import Count
from rest_framework import serializers

from src.models import Product, Lesson, Group


class ProductsSerializer(serializers.ModelSerializer):
    lessons_quantity = serializers.IntegerField(read_only=True)

    class Meta:
        model = Product
        fields = '__all__'


class LessonSerializer(serializers.ModelSerializer):
    class Meta:
        model = Lesson
        fields = '__all__'


class ProductsStaticticSerializer(serializers.ModelSerializer):
    student_quantity = serializers.IntegerField(read_only=True)
    product_fullness = serializers.SerializerMethodField()
    acquisition_percentage = serializers.DecimalField(read_only=True, max_digits=5, decimal_places=2)

    class Meta:
        model = Product
        fields = ('name', 'student_quantity', 'product_fullness', 'acquisition_percentage')

    def get_product_fullness(self, obj):
        group_count = Group.objects.filter(products_id=obj.id).count()
        num_users = obj.student_quantity
        if group_count and num_users:
            acquisition_percentage = (100 * num_users / group_count) / obj.max_students
        else:
            acquisition_percentage = 0
        return acquisition_percentage
