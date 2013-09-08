import json
from exceptions import NotImplementedError

from django.http import HttpResponse, HttpResponseBadRequest
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import View

from webpype.client import WebPypeClient

webpipe = WebPypeClient()

class WebPypeMixin(View):
    '''
    A Django Mixin for making a view a WebPipe

    '''
    http_method_names = ['post', 'options']
    block_definition = None
    is_block = False
    is_trigger = False
    is_action = False

    def __init__(self, **kwargs):
        if not (self.is_block or self.is_trigger or self.is_action):
            msg = 'Boolean is_block, is_trigger or is_action must be specified'
            raise NotImplementedError(msg)

        if not self.block_definition:
            raise NotImplementedError('block_definition not defined')

        return super(WebPypeMixin, self).__init__(**kwargs)

    def _parse_inputs(self, inputs):
        resp = webpipe._validate_input(inputs)
        return json.dumps(resp)

    def block(self, inputs):
        raise NotImplementedError('block() not defined')

    def trigger(self):
        raise NotImplementedError('trigger() not defined')

    def action(self, inputs):
        raise NotImplementedError('action() not defined')

    def post(self, request, *args, **kwargs):
        if not self.is_trigger:
            #TODO this sucks
            inputs = request.POST.items()[0][0]
            if inputs:
                inputs = self._parse_inputs(inputs)
            else:
                return HttpResponseBadRequest(*args, **kwargs)

        if self.is_block:
            output = self.block(inputs)
        elif self.is_action:
            self.action(inputs)
        elif self.is_trigger:
            output = self.trigger()
        else:
            msg = 'Boolean is_block, is_trigger or is_action must be specified'
            raise NotImplementedError(msg)

        kwargs['content_type'] = 'application/json'
        if self.is_action:
            return HttpResponse('OK', *args, **kwargs)
        else:
            return HttpResponse(output, *args, **kwargs)

    def options(self, request, *args, **kwargs):
        output = json.dumps(self.block_definition)
        kwargs['content_type'] = 'application/json'
        return HttpResponse(output, *args, **kwargs)

    @method_decorator(csrf_exempt)
    def dispatch(self, *args, **kwargs):
        return super(WebPypeMixin, self).dispatch(*args, **kwargs)
