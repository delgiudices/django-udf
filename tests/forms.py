from udf.forms import UDFModelForm
from .models import MyModel


class MyModelForm(UDFModelForm):

    class Meta:
        model = MyModel
        fields = []
