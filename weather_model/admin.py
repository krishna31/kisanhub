# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin
from import_export import resources
from import_export.admin import ImportExportModelAdmin

from weather_model.models import WeatherData

# Register your models here.


class WeatherDataResource(resources.ModelResource):

    class Meta:
        model = WeatherData
        fields = ('id', 'region', 'year', 'month_season', 'value', 'value_type')


class WeatherDataAdmin(ImportExportModelAdmin):
    list_display = ['region', 'year', 'month_season', 'value', 'value_type']
    search_fields = ['region', 'year']
    resource_class = WeatherDataResource


admin.site.register(WeatherData, WeatherDataAdmin)
