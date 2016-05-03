class Metrics(object):
    """Metrics abstract layer, accept uri-style configuration
    """
    def __init__(self, metrics_uri):
        import urlparse

        # parse the uri
        parsed_metrics_url = urlparse.urlsplit(metrics_uri)

        # validate metrics uri is set with correct scheme, `metrics`
        metrics_url_scheme = parsed_metrics_url.scheme
        if metrics_url_scheme != 'metrics':
            raise ValueError('Metrics URI must start with metrics://, got %s' % metrics_url_scheme)

        # api key has to be in the auth's user name
        api_key = parsed_metrics_url.username
        parsed_options = urlparse.parse_qs(parsed_metrics_url.query)

        # parsed options is a dictionary with querystring
        # value as list (since it's legal to contain duplicate keys),
        # just take the first value
        options = {k:v_list[0] for k, v_list in parsed_options.iteritems()}

        backend_cls = self._load_backend_module(parsed_metrics_url.hostname)

        self.backend = backend_cls(api_key=api_key, **options)

    def _load_backend_module(self, backend_name):

        from . import backends

        try:
            return getattr(backends, backend_name)
        except AttributeError:
            raise NotImplementedError("backend %s is not supported" % backend_name)

    # send a metric
    def send(self, name, value, metrics_type='gauge', tags=None, timestamp=None):
        self.backend.send(
            name=name,
            value=value,
            metrics_type=metrics_type,
            tags=tags,
            timestamp=timestamp
        )
