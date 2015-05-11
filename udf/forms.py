from django import forms
from udf.models import UDF
from django.contrib.contenttypes.models import ContentType


def field_for_udf(field):
    return getattr(forms, field.type)()


class UDFModelForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super(UDFModelForm, self).__init__(*args, **kwargs)
        content_type = ContentType.objects.get_for_model(self._meta.model)
        custom_fields = UDF.objects.filter(content_type=content_type)

        for field in custom_fields:
            self.fields[field.name] = field_for_udf(field)
            self.fields[field.name].required = field.required
