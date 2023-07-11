from rest_framework.throttling import SimpleRateThrottle


class IPRateThrottle(SimpleRateThrottle):
    scope = "ip"

    def get_cache_key(self, request, view):
        return self.get_ident(request)
