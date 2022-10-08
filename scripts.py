import random

from datacenter.models import (Schoolkid, Mark, Chastisement, Lesson, Commendation)
from django.core.exceptions import MultipleObjectsReturned, ObjectDoesNotExist

praises = ['Молодец!', 'Отлично!', 'Хорошо!', 'Гораздо лучше, чем я ожидал!', 'Ты меня приятно удивил!', 'Великолепно!',
           'Прекрасно!', 'Ты меня очень обрадовал!', 'Именно этого я давно ждал от тебя!',
           'Сказано здорово – просто и ясно!', 'Ты, как всегда, точен!', 'Очень хороший ответ!', 'Талантливо!',
           'Ты сегодня прыгнул выше головы!', 'Я поражен!', 'Уже существенно лучше!', 'Потрясающе!', 'Замечательно!',
           'Прекрасное начало!', 'Так держать!', 'Ты на верном пути!', 'Здорово!', 'Это как раз то, что нужно!',
           'Я тобой горжусь!', 'С каждым разом у тебя получается всё лучше!', 'Мы с тобой не зря поработали!',
           'Я вижу, как ты стараешься!', 'Ты растешь над собой!', 'Ты многое сделал, я это вижу!',
           'Теперь у тебя точно все получится!', ]


def search_schoolkid(name: str):
    """Ищет ученика по фамилии и имени"""
    try:
        return Schoolkid.objects.get(full_name__contains=f'{name}')
    except (MultipleObjectsReturned, ObjectDoesNotExist) as error:
        print(f'"{name}" - неверный запрос\n{error}')


def create_commendation(schoolkid: Schoolkid, subject: str):
    """Функция для создания похвалы по последнему заданному уроку."""
    praise = random.choice(praises)
    lesson = Lesson.objects.filter(year_of_study=schoolkid.year_of_study,
                                   group_letter=schoolkid.group_letter,
                                   subject__title=f'{subject}').order_by('-date').first()
    try:
        Commendation.objects.create(schoolkid=schoolkid,
                                    text=praise,
                                    created=lesson.date,
                                    subject=lesson.subject,
                                    teacher=lesson.teacher)
        print('Похвала создана.')
    except AttributeError:
        print('Урок указан не правильно')


def remove_chastisements(schoolkid: Schoolkid):
    """Функция удаляет все замечания."""
    notes = Chastisement.objects.filter(schoolkid_id=schoolkid.pk)
    notes.delete()
    print('Замечания удалены.')


def fix_marks(schoolkid: Schoolkid):
    """Функция исправляет двойки и тройки на пятёрки"""
    bad_points = Mark.objects.filter(schoolkid_id=schoolkid.pk, points__lte=3)
    bad_points.update(points=5)
    print('Оценки исправлены.')


# поиск ученика
child = search_schoolkid('Фролов Иван')

# исправление оценок
fix_marks(child)

# удаление замечаний
remove_chastisements(child)

# создание похвалы
create_commendation(child, 'Математика')
