import random

from datacenter.models import (Schoolkid, Mark, Chastisement, Lesson, Commendation)
from django.core.exceptions import MultipleObjectsReturned, ObjectDoesNotExist

childs_name, childs_id = ['Фролов Иван', 'Голубев Феофан'], [6551, 6548]

child = Schoolkid.objects.filter(full_name__contains='Фролов Иван')
bad_marks = Mark.objects.filter(schoolkid=child[0], points__lte=3)

last_lessons = Lesson.objects.filter(year_of_study=child[0].year_of_study,
                                     group_letter=child[0].group_letter,
                                     subject__title='Математика').order_by('-date').first()


def search_schoolkid(name: str):
    """Ищет ученика по фамилии и имени"""
    try:
        return Schoolkid.objects.get(full_name__contains=f'{name}')
    except (MultipleObjectsReturned, ObjectDoesNotExist) as error:
        print(f'"{name}" - неверный запрос\n{error}')


def create_commendation(schoolkid: Schoolkid, subject: str):
    """Функция для создания похвалы по последнему заданному уроку."""
    with open('praises.txt', 'r', encoding='utf8') as file:
        praise_list = file.readlines()
        praise = random.choice([praise.strip().split('. ')[1] for praise in praise_list])
    lesson = Lesson.objects.filter(year_of_study=schoolkid.year_of_study,
                                   group_letter=schoolkid.group_letter,
                                   subject__title=f'{subject}').order_by('-date').first()
    Commendation.objects.create(schoolkid=schoolkid,
                                text=praise,
                                created=lesson.date,
                                subject=lesson.subject,
                                teacher=lesson.teacher)
    print('Похвала создана.')


def remove_chastisements(schoolkid: Schoolkid):
    """Функция удаляет все замечания."""
    notes = Chastisement.objects.filter(schoolkid_id=schoolkid.pk)
    for note in notes:
        note.delete()
    print('Замечания удалены.')


def fix_marks(schoolkid: Schoolkid):
    """Функция исправляет двойки и тройки на пятёрки"""
    bad_points = Mark.objects.filter(schoolkid_id=schoolkid.pk, points__lte=3)
    for point in bad_points:
        point.points = 5
        point.save()
    print('Оценки исправлены.')


child = search_schoolkid('Фролов Иван')

fix_marks(child)
remove_chastisements(child)
create_commendation(child, 'Математика')

bad_marks.count()
