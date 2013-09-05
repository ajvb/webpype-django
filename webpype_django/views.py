import json

from django.http import HttpResponse

class WebPypeMixin(object):
    '''
    A Django Mixin for making a view a WebPipe

    '''
    http_method_names = ['post', 'options']
    block_definition = None

    def post(self, *args, **kwargs):
        pass

    def options(self, *args, **kwargs):
        data = json.dumps(self.block_definition)
        kwargs['content_type'] = 'application/json'
        return HttpResponse(data, **kwargs)
