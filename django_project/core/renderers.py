# coding: utf-8
from io import BytesIO
import json

# Django core and 3rd party imports
import unicodecsv as csv
from rest_framework.renderers import BaseRenderer, BrowsableAPIRenderer


class BrowsableAPIRendererWithoutForm(BrowsableAPIRenderer):
    template = 'rest_framework/improved_base.html'

    def show_form_for_method(self, view, method, request, obj):
        return False


class CSVRenderer(BaseRenderer):
    media_type = 'text/csv'
    format = 'csv'
    charset = 'utf-8'
    csv_filename = 'data.csv'

    def get_csv_filename(self, view):
        if hasattr(view, 'csv_filename'):
            return view.csv_filename
        return self.csv_filename

    def render(self, data, media_type=None, renderer_context=None):
        view = renderer_context['view']
        response = renderer_context['response']
        filename = self.get_csv_filename(view)
        response['Content-Disposition'] = 'attachment; filename=%s' % filename

        for key, value in data.iteritems():
            print(key, value)

        f = BytesIO()
        f.write(b'\xef\xbb\xbf')  # utf-8 BOM
        w = csv.writer(f, encoding='utf-8')

        start = data['hits']['hits']
        second = start[0]['_source']
        header = list(second.keys())
        w.writerow(header)
        # print(second)
        # for row in start:
        #     for key in row['_source']:
        #         print(key.values_list)


        return f.getvalue()
