# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.contrib import messages

from weather_model.form import WeatherDataImportForm


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
