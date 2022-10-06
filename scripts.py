from datacenter.models import (Schoolkid, Mark)


child = Schoolkid.objects.get(pk=6551)
bad_marks = Mark.objects.filter(schoolkid=child, points__lte=3)


def fix_marks(schoolkid: Schoolkid):
    bad_points = Mark.objects.filter(schoolkid_id=schoolkid.pk, points__lte=3)
    for point in bad_points:
        point.points = 5
        point.save()


fix_marks(child)
bad_marks.count()
