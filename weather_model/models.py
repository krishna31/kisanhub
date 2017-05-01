# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models

# Create your models here.


class WeatherData(models.Model):
    MONTH_SEASON_CHOICES = (
        ('JAN', 'January'),
        ('FEB', 'February'),
        ('MAR', 'March'),
        ('APR', 'April'),
        ('MAY', 'May'),
        ('JUN', 'June'),
        ('JUL', 'July'),
        ('AUG', 'August'),
        ('SEP', 'September'),
        ('OCT', 'October'),
        ('NOV', 'November'),
        ('DEC', 'December'),
        ('SUM', 'Summer'),
        ('WIN', 'Winter'),
        ('SPR', 'Spring'),
        ('AUT', 'Autumn'),
        ('ANN', 'Annual'),
    )

    VALUE_TYPE_CHOICES = (
        ("MIN", "Minimum Temperature((Degrees C)"),
        ("MAX", "Maximum Temperature((Degrees C)"),
        ("MEAN", "Mean Temperature((Degrees C)"),
        ("SUNSHINE", "Sunshine (Total hours)"),
        ("RAINFALL", "Rainfall (mm)"),
    )

    REGION_CHOICE = (
        ('UK', 'UK'),
        ('England', 'England'),
        ('Wales', 'Wales'),
        ('Scotland', 'Scotland')
    )

    region = models.CharField(max_length=100, choices=REGION_CHOICE)
    month_season = models.CharField(max_length=3, choices=MONTH_SEASON_CHOICES)
    year = models.IntegerField()
    value_type = models.CharField(max_length=100, choices=VALUE_TYPE_CHOICES)
    value = models.FloatField(null=True, blank=True, default=None)

    class Meta:
        verbose_name = "WeatherData"
        verbose_name_plural = "WeatherDatas"

    def __unicode__(self):
        return "%s|%s|%s|%s" % (
            self.region,
            str(self.year),
            self.month_season,
            str(self.value),
        )
