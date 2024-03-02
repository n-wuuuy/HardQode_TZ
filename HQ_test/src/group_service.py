from django.db.models import QuerySet, Count

from src.models import Group


def distribution_users_into_groups(groups: QuerySet) -> None:
    while groups.last().student_count - groups.first().student_count >= 1:
        max_group = groups.last()
        min_group = groups.first()
        user = max_group.students.last().id
        max_group.students.remove(user)
        min_group.students.add(user)


def create_list_groups_to_fill(product: QuerySet) -> QuerySet:
    group_len = product[0].group_count
    print(group_len)
    students = product[0].sum_students
    while (students / group_len) < product[0].min_students:
        group_len -= 1
    # исправить
    sliced_queryset = Group.objects.filter(products_id=product[0].id).annotate(
            student_count=Count('students')).order_by('-student_count')[:group_len]
    groups = Group.objects.filter(id__in=sliced_queryset).annotate(
            student_count=Count('students')).order_by('student_count')
    return groups


def add_student_standard(groups: QuerySet, max_students: int, user_id: int) -> None:
    for group in groups:
        if group.student_count < max_students:
            group.students.add(user_id)


def add_student_with_sorting(product: QuerySet, max_students: int, min_students: int, user_id: int):
    add_student_standard(product, max_students, user_id)
    list_groups = create_list_groups_to_fill(product)
    distribution_users_into_groups(list_groups)
