from rest_framework.renderers import JSONRenderer
import uuid

class CustomJSONRenderer(JSONRenderer):
    def render(self, data, accepted_media_type=None, renderer_context=None):
        if renderer_context:
            response = renderer_context['response']
            if 200 <= response.status_code < 300:
                # Format success response
                if isinstance(data, dict) and 'meta' in data:
                    formatted_data = {
                        'data': data.get('data'),
                        'meta': data.get('meta')
                    }
                else:
                    formatted_data = {
                        'data': data,
                        'meta': {
                            'correlationId': str(uuid.uuid4())
                        }
                    }
                return super().render(formatted_data, accepted_media_type, renderer_context)
            else:
                # Error responses are handled by custom_exception_handler
                return super().render(data, accepted_media_type, renderer_context)
        return super().render(data, accepted_media_type, renderer_context)