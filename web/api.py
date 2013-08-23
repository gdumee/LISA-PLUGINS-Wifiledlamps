from tastypie import authorization
from django.conf.urls.defaults import *
from tastypie import resources
from tastypie.utils import trailing_slash
import json
try:
    from web.lisa.settings import LISA_PATH
except ImportError:
    from lisa.settings import LISA_PATH

class Wifileds(object):
    def __init__(self):
        return None

class WifiledsResource(resources.Resource):
    class Meta:
        resource_name = 'wifileds'
        allowed_methods = ()
        authorization = authorization.Authorization()
        object_class = Wifileds
        extra_actions = [
            {
                'name': 'switch',
                'summary': 'Turn on/off all lights of a controller',
                'http_method': 'POST',
                'fields': {}
            },
        ]

    def base_urls(self):
        return [
            url(r"^plugin/(?P<resource_name>%s)%s$" % (self._meta.resource_name, trailing_slash()),
                self.wrap_view('dispatch_list'), name="api_dispatch_list"),
            url(r"^plugin/(?P<resource_name>%s)/schema%s$" % (self._meta.resource_name, trailing_slash()),
                self.wrap_view('get_schema'), name="api_get_schema"),
            # Will be accessible by http://127.0.0.1:8000/api/v1/plugin/chatterbot/gettime/
            url(r"^plugin/(?P<resource_name>%s)/switch%s$" % (self._meta.resource_name, trailing_slash()),
                self.wrap_view('switch'), name="api_plugin_wifileds_switch"),
        ]

    def switch(self, request, **kwargs):
        from tastypie.http import HttpAccepted
        from Wifileds.modules.wifileds import Wifileds

        self.method_check(request, allowed=['get'])
        self.is_authenticated(request)
        self.throttle_check(request)
        self.log_throttled_access(request)
        return self.create_response(request, { 'status': 'success', 'content': json.loads(Wifileds().switch())}, HttpAccepted)
