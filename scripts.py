from datacenter.models import (Schoolkid, Mark, Chastisement)

childs_name, childs_id = ['Фролов Иван', 'Голубев Феофан'], [6551, 6548]

child = Schoolkid.objects.filter(full_name__contains=childs_name[0])
bad_marks = Mark.objects.filter(schoolkid=child[0], points__lte=3)


def remove_chastisements(schoolkid: Schoolkid):
    notes = Chastisement.objects.filter(schoolkid_id=schoolkid.pk)
    for note in notes:
        note.delete()
        print('Замечания удалены.')


def fix_marks(schoolkid: Schoolkid):
    bad_points = Mark.objects.filter(schoolkid_id=schoolkid.pk, points__lte=3)
    for point in bad_points:
        point.points = 5
        point.save()
    print('Оценки исправлены.')


fix_marks(child[0])
remove_chastisements(child[0])
bad_marks.count()
