__author__ = 'andrew'

from django import forms

from django import forms
from cars.models import CarMarks, CarSeries, CarModifications, CarModels


class CarSeriesForm(forms.ModelForm):

    class Meta:
        model = CarSeries
        fields = ("car_mark", )

    def __init__(self, *args, **kwargs):
        super(CarSeriesForm, self).__init__(*args, **kwargs)


class SearchForm(forms.ModelForm):
    series = forms.ChoiceField()
    engineFrom = forms.FloatField(10,0, initial = 0.1)
    engineTo = forms.FloatField(10,0, initial = 2.0)
    car_mark = forms.IntegerField()
    car_mark.widget = car_mark.hidden_widget()

    class Meta:
        model = CarMarks
        fields = ('name', )


    def __init__(self, *args, **kwargs):
        super(SearchForm, self).__init__(*args, **kwargs)
        obj = CarMarks.objects.get(pk = int(kwargs['instance'].id))

        self.fields["series"].choices = [(x.id, x.name) for x in obj.carseries_set.all()]
        self.fields["car_mark"].initial = obj.id












