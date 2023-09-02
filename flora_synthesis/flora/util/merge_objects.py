from django.db import transaction
from django.db.models.fields.related import ManyToManyField
from django.db.models.fields.reverse_related import ManyToOneRel, ManyToManyRel, OneToOneRel


def merge_objects(object_to_delete, object_to_keep):
    fields = object_to_delete._meta.get_fields()

    o2ol = []
    fkl = []
    m2ml = []

    m2m_r = []

    for field in fields:
        if isinstance(field, OneToOneRel):
            o2ol.append(field)
        elif isinstance(field, ManyToOneRel):
            fkl.append(field)
        elif isinstance(field, ManyToManyRel):
            m2ml.append(field)
        elif isinstance(field, ManyToManyField):
            m2m_r.append(field)

    with transaction.atomic():
        for o2o in o2ol:
            model = o2o.related_model
            objs_to_update = model.objects.filter(**{o2o.field.name: object_to_delete})
            objs_to_update.delete()

        for fk in fkl:
            model = fk.related_model
            objs_to_update = model.objects.filter(**{fk.field.name: object_to_delete})

            for obj in objs_to_update:
                q = [i for i in model._meta.unique_together if fk.field.name in i]

                if len(q) > 0:
                    c_target = q[0]
                    d = {}
                    for i in c_target:
                        if i == fk.field.name:
                            d[i] = object_to_keep
                        else:
                            d[i] = getattr(obj, i)
                    to_merge = model.objects.filter(**d)

                    if to_merge.count() > 0:
                        merge_objects(obj, to_merge[0])
                    else:
                        setattr(obj, fk.field.name, object_to_keep)
                        obj.save()
                else:
                    setattr(obj, fk.field.name, object_to_keep)
                    obj.save()

        for m2m in m2ml:
            model = m2m.related_model
            objs_to_update = model.objects.filter(**{m2m.field.name: object_to_delete})

            for obj in objs_to_update:
                getattr(obj, m2m.field.name).remove(object_to_delete)
                getattr(obj, m2m.field.name).add(object_to_keep)

        for m2mr in m2m_r:
            for obj in getattr(object_to_delete, m2mr.name).all():
                getattr(object_to_keep, m2mr.name).add(obj)

        object_to_delete.delete()
