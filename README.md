webpype-django
==============

WebPype functionality for Django

Currently in alpha stage, not ready for production use.

##### Example

##### Taken from: https://github.com/jpf/block-echo

    import json

    from django.views.generic import View

    from webpype_django.view import WebPypeMixin

    class BlockEchoExample(WebPypeMixin, View):
        is_block = True
        block_definition = {"name": "Echo",
                           "description": "An example WebPipe block echo service.",
                           "inputs": [
                               {"name": "in",
                                "type": "string",
                                "description": "String to echo"}],
                           "outputs": [
                               {"name": "out",
                                "type": "string",
                                "description": "Echoed string"}]}

        def block(self, inputs):
            return json.dumps({"outputs":
                                [{"out": json.loads(inputs)['inputs'][0]['in']}]
            })
