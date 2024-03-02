from math import floor

from django.contrib.auth.models import User
from django.db.models import QuerySet

from src.models import Product


def _distribution_users_into_groups(groups: QuerySet, users: list,
                                    additional_users: int,
                                    avg_users_in_groups: int) -> None:
    """Filling students"""
    for group in groups:
        group.students.clear()
        split_students = 0
        if additional_users:
            split_students = 1
            additional_users -= 1
        group.students.add(*users[:avg_users_in_groups+split_students])
        users = users[avg_users_in_groups+split_students:]


def _create_data_to_separate_group(product: Product, users: list) -> tuple:
    """Finding data for user distribution.
       Calculates the number of groups required for the minimum filling and
       the number of users in these groups."""
    try:
        group_count = product.group_count
        students_count = len(users)
        while (students_count / group_count) < product.min_students:
            group_count -= 1
        avg_users_in_groups = floor(students_count / group_count)
        additional_users = students_count % group_count
    except ZeroDivisionError:
        avg_users_in_groups = 0
        additional_users = 0
    finally:
        return avg_users_in_groups, additional_users


def add_student(product: Product, groups: QuerySet, user_id: int) -> dict[str, str]:
    """Adds a student to a group."""
    for group in groups:
        if group.student_count < product.max_students:
            group.students.add(user_id)
            return {"message": "Users distributed to groups successfully."}
    return {"message": "All groups are full."}


def sorting_group(product: Product, groups: QuerySet) -> None:
    """Group distribution algorithm"""
    users = [person_id.id for person_id in User.objects.filter(students__in=groups)]
    print(users)
    avg_users_in_groups, additional_users = _create_data_to_separate_group(product, users)
    if avg_users_in_groups == 0:
        raise Exception("This product has no groups.")
    _distribution_users_into_groups(groups, users, additional_users, avg_users_in_groups)
