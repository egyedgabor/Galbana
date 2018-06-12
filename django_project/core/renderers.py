# coding: utf-8
from io import BytesIO

# Django core and 3rd party imports
import unicodecsv as csv
from rest_framework.renderers import BaseRenderer, BrowsableAPIRenderer


def flatten_json(y):
    out = {}

    def flatten(x, name=''):
        if type(x) is dict:
            for a in x:
                flatten(x[a], name + a + '_')
        else:
            out[name[:-1]] = x
    flatten(y)
    return out


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

        f = BytesIO()
        writer = csv.writer(f, encoding='utf-8')
        for elem in data:
            flat = flatten_json(elem)
            keys = flat.keys()
        writer.writerow(keys)

        for elem in data:
            flat = flatten_json(elem)
            writer.writerow(flat.values())

        return f.getvalue()
