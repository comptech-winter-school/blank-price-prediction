from django.db import models


# Create your models here.


class Predicts(models.Model):
    datetime = models.DateTimeField('Дата прогноза', auto_now_add=True)
    one_week_predict = models.FloatField('Прогноз на 1 неделю')
    two_weeks_predict = models.FloatField('Прогноз на 2 недели', null=True)
    three_weeks_predict = models.FloatField('Прогноз на 3 недели', null=True)
    four_weeks_predict = models.FloatField('Прогноз на 4 недели', null=True)

    def __str__(self):
        return str(self.datetime)

    class Meta:
        verbose_name = 'Predicts'
        verbose_name_plural = 'Predicts'

    def set_datetime(self, datetime):
        self.datetime = datetime

    def set_one_week_predict(self, one_week_predict):
        self.one_week_predict = one_week_predict

    def set_two_weeks_predict(self, two_weeks_predict):
        self.two_weeks_predict = two_weeks_predict

    def set_three_weeks_predict(self, three_weeks_predict):
        self.three_weeks_predict = three_weeks_predict

    def set_four_weeks_predict(self, four_weeks_predict):
        self.four_weeks_predict = four_weeks_predict
