from django import forms
from weather_model.models import WeatherData

import requests
import csv
import re


class WeatherDataImportForm(forms.ModelForm):
    VALUE_TYPE_CHOICES = {
        "MIN": "Tmin",
        "MAX": "Tmax",
        "MEAN": "Tmean",
        "SUNSHINE": "Sunshine",
        "RAINFALL": "Rainfall"
    }

    class Meta:
        model = WeatherData
        fields = ['region', 'value_type']
        widgets = {
            'region': forms.Select(attrs={'class': 'form-control'}),
            'value_type': forms.Select(attrs={'class': 'form-control'}),
        }

    def _download_file(self, url):
        local_filename = '/tmp/' + url.split('/')[-1]
        resp = requests.get(url)
        if resp.status_code == 200:
            with open(local_filename, 'wb') as f:
                f.write(resp.content)
        else:
            raise Exception(resp.reason)

        return local_filename

    def _convert_txt_to_csv(self, file_name):
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

    def _insert_data(self, csv_file, region, value_type):
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

    def _construct_url(self, region, value_type):
        return "http://www.metoffice.gov.uk/pub/data/weather/uk/climate/datasets/%s/date/%s" % (
            self.VALUE_TYPE_CHOICES[value_type],
            str(region) + '.txt'
        )

    def save(self):
        cd = self.cleaned_data
        region = cd['region']
        value_type = cd['value_type']
        url = self._construct_url(region, value_type)
        file_name = self._download_file(url)
        csv_file = self._convert_txt_to_csv(file_name)
        self._insert_data(csv_file, region, value_type)


class WeatherDataChartForm(forms.Form):
    BACKGROUND_COLOR_CHOICES = {
        'UK': "rgba(153,255,51,0.6)",
        'England': "rgba(255,153,0,0.6)",
        'Wales': "rgb(220,220,220)",
        'Scotland': "#9b59b6",
    }

    year = forms.ChoiceField(
        widget=forms.Select(attrs={'class': 'form-control'}),
        required=True
    )
    value_type = forms.ChoiceField(
        widget=forms.Select(attrs={'class': 'form-control'}),
        required=True
    )

    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop('request', None)
        super(WeatherDataChartForm, self).__init__(*args, **kwargs)
        years = WeatherData.objects.all().distinct('year')
        self.fields['value_type'].choices = WeatherData.VALUE_TYPE_CHOICES
        self.fields['year'].choices = [(a.year, a.year) for a in years]

    def save(self):
        cd = self.cleaned_data
        data = {}
        weather_data = WeatherData.objects.filter(
            year=cd['year'],
            value_type=cd['value_type']
        ).distinct('month_season').order_by('month_season')

        data['labels'] = list(weather_data.values_list('month_season', flat=True))
        data['datasets'] = []

        for region in WeatherData.REGION_CHOICE:
            data_sets = {}
            data_sets['data'] = list(weather_data.filter(region=region[0]).values_list('value', flat=True))
            data_sets['label'] = region[0]
            data_sets['backgroundColor'] = self.BACKGROUND_COLOR_CHOICES[region[0]]
            data['datasets'].append(data_sets)

        return data