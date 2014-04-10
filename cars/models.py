from django.db import models


# Create your models here.


class CarMarks (models.Model):
    """
    class defines Car Marks
    name - name of the mark (for example "Skoda")
    id_auto_ria - id of the mark in auto.ria.com database
    """
    name = models.CharField("Car Name", max_length=50)
    auto_ria_id = models.SmallIntegerField(default=0)


    def __str__(self):
        return self.name



class CarSeries(models.Model):
    """
    class defines Car Models
    name - name of Model (for example "Octavia")
    car - ForeignKey refers to CarMark
    car_mark_auto_ria_id - reference to car_mark_id in auto.ria.com database
    series_auto_ria_id - reference to car_series in auto.ria.com database
    """
    name = models.CharField(max_length=50)
    car_mark = models.ForeignKey(CarMarks, verbose_name="Car Name")
    series_auto_ria_id = models.IntegerField(default=0)

    def __str__(self):
        return self.name


class CarModels(models.Model):
    """
    class defines CarSeries
    name - name of CarSeries (for example III means 3-rd generation)
    """
    name = models.CharField(max_length=50)
    car_mark = models.ForeignKey(CarMarks)
    car_series = models.ForeignKey(CarSeries)

    def __str__(self):
        return self.name


class CarModifications(models.Model):
    """
    class defines modification of auto
    """
    name = models.CharField(max_length=50)
    car_model = models.ForeignKey(CarModels)

    def __str__(self):
        return self.name























