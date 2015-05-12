from django.db import models
from django.contrib.contenttypes.models import ContentType
from jsonfield import JSONField
from django.db.models.query import ModelIterator

class UDF(models.Model):

    def __str__(self):
        return "%s's %s" % (self.content_type, self.name)

    content_type = models.ForeignKey(ContentType)
    name = models.CharField(max_length=50)
    type = models.CharField(max_length=100)
    required = models.BooleanField(default=False)


class UDFIterator(ModelIterator):

    def __iter__(self):
        for obj in super(UDFIterator, self).__iter__():
            setattr(obj, 'this', 'that')
            yield obj


class UDFQuerySet(models.QuerySet):

    def __init__(self, *args, **kwargs):
        super(UDFQuerySet, self).__init__(*args, **kwargs)

    def iterator(self):
        return UDFIterator(self)


class UDFModelManager(models.Manager):

    def get_queryset(self):
        return UDFQuerySet(self.model, using=self._db, hints=self._hints)

    def create(self, *args, **kwargs):
        custom_fields = UDF.objects.filter(
            content_type=ContentType.objects.get_for_model(self.model))

        udfs = {}
        for field in custom_fields:
            udfs[field.name] = kwargs[field.name]

        kwargs['udfs'] = udfs
        return super(UDFModelManager, self).create(*args, **kwargs)


class UDFModel(models.Model):

    udfs = JSONField()
    objects = UDFModelManager()

    class Meta:
        abstract = True

    def __init__(self, *args, **kwargs):
        custom_fields = UDF.objects.filter(
            content_type=ContentType.objects.get_for_model(self.__class__))

        for field in custom_fields:
            setattr(self, field.name, kwargs.pop(field.name, None))

        instance = super(UDFModel, self).__init__(*args, **kwargs)
        for key, val in self.udfs.items():
            setattr(self, key, val)

        return instance

    def save(self, *args, **kwargs):
        custom_fields = UDF.objects.filter(
            content_type=ContentType.objects.get_for_model(self.__class__))

        for field in custom_fields:
            self.udfs[field.name] = getattr(self, field.name, None)
        super(UDFModel, self).save(*args, **kwargs)
