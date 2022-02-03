from django.db import models


# Create your models here.


class Predicts(models.Model):
    datetime = models.DateTimeField('Дата прогноза', auto_now_add=True)
    one_week_predict = models.FloatField('Прогноз на 1 неделю')
    two_weeks_predict = models.FloatField('Прогноз на 2 недели')
    four_weeks_predict = models.FloatField('Прогноз на 4 недели')

    def __str__(self):
        return str(self.datetime)

    class Meta:
        verbose_name = 'Predicts'
        verbose_name_plural = 'Predicts'
