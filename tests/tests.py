from django.test import TestCase
from udf.models import UDF
from .models import MyModel
from .forms import MyModelForm

# Create your tests here.


class UDFModelTest(TestCase):

    def setUp(self):
        UDF.objects.create(
            name='pro_name', type='CharField',
            content_type=MyModel.get_content_type())

    def test_model_can_be_saved(self):
        instance = MyModel.objects.create()
        pk = instance.pk
        instance.pro_name = 'Dude'
        instance.save()
        instance = MyModel.objects.get(pk=pk)
        self.assertEqual(instance.pro_name, 'Dude')
        self.assertEqual(MyModel.objects.all()[0].pro_name, 'Dude')


class UDFModelFormTest(TestCase):

    def setUp(self):
        UDF.objects.create(
            name='pro_name', type='CharField',
            content_type=MyModel.get_content_type(), required=True)

    def test_model_form_has_custom_fields(self):
        form = MyModelForm()
        self.assertTrue(form.fields['pro_name'] is not None)
