# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.http.response import JsonResponse
from django.contrib import messages

from weather_model.form import WeatherDataImportForm, WeatherDataChartForm


def index(request):
    template = 'weather_model/index.html'
    return render(request, template, {})


def import_data(request):
    if request.method == 'POST':
        post_data = request.POST.copy()
        form = WeatherDataImportForm(post_data)
        if form.is_valid():
            form.save()
            messages.success(request, 'Imported Successfully!')
            return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
        else:
            pass
    else:
        form = WeatherDataImportForm()
    context = {
        'form': form,
    }
    template = 'weather_model/manage_data.html'
    return render(request, template, context)


def chart(request):
    if request.method == 'POST':
        post_data = request.POST.copy()
        form = WeatherDataChartForm(post_data)
        if form.is_valid():
            data = form.save()
            return JsonResponse({'success': True, 'data': data})
        else:
            pass
    else:
        form = WeatherDataChartForm()
    context = {
        'form': form,
    }
    template = 'weather_model/chart.html'
    return render(request, template, context)