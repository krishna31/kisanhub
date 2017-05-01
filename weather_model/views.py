# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render
import requests
import re
import csv

from weather_model.models import WeatherData

# Create your views here.

VALUE_TYPE_CHOICES = {
    "MIN": "Tmin",
    "MAX": "Tmax",
    "MEAN": "Tmean",
    "SUNSHINE": "Sunshine",
    "RAINFALL": "Rainfall"
}


def _convert_txt_to_csv(file_name):
    output_file_name = file_name.replace(".txt", ".csv")
    with open(file_name, "rb") as infile, open(output_file_name, "wb") as outfile:
        reader = csv.reader(infile)
        for i in range(0, 7):
            next(reader, None)  # skip first 7 lines
        writer = csv.writer(outfile)
        for row in reader:
            row = re.sub(r"\s+", '|', row[0])
            writer.writerow([row])

    return output_file_name


def _download_file(url):
    local_filename = '/tmp/' + url.split('/')[-1]
    resp = requests.get(url)
    if resp.status_code == 200:
        with open(local_filename, 'wb') as f:
            f.write(resp.content)
    else:
        raise Exception(resp.reason)

    return local_filename


def _insert_data(csv_file, region, value_type):
    with open(csv_file, 'rb') as file_obj:
        reader = csv.DictReader(file_obj, delimiter=str(u'|'), quoting=csv.QUOTE_NONE)
        month_season_list = dict(WeatherData.MONTH_SEASON_CHOICES).keys()
        for row in reader:
            for m in month_season_list:
                obj, created = WeatherData.objects.get_or_create(
                    region=region,
                    value_type=value_type,
                    month_season=m,
                    year=row['Year'],
                    value=None if row[m] == '---' else row[m]
                )


def import_data(request):
    if request.method == 'POST':
        region = request.POST.get('region', None)
        value_type = request.POST.get('value_type', None)

        url = 'http://www.metoffice.gov.uk/pub/data/weather/%s/climate/datasets/%s/date/%s.txt' % (
            region,
            VALUE_TYPE_CHOICES[value_type]
        )


    else:
        pass
