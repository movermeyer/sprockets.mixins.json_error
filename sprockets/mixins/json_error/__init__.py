"""
mixins.json_error

Handler mixin for writing JSON errors

"""
version_info = (1, 0, 0)
__version__ = '.'.join(str(v) for v in version_info)


class JsonErrorMixin(object):

    def write_error(self, status_code, **kwargs):
        """Suppress the automatic rendering of HTML code upon an error.

           :param int status_code:
                The HTTP status code the :class:`HTTPError` raised.

           :param dict kwargs:
                Automatically filled with exception information including
                the error that was raised, the class of error raised, and an
                object.

        """
        if kwargs.get('error'):
            raised_error = kwargs.get('error')
        else:
            _, raised_error, _ = kwargs['exc_info']

        error_message = getattr(
            raised_error, 'log_message', 'Unexpected Error')
        error_type = getattr(raised_error, 'error_type', self._reason)

        self.error = {
            'message': error_message,
            'type': error_type,
        }
        if hasattr(raised_error, 'documentation_url'):
            self.error['documentation_url'] = raised_error.documentation_url

        error_status_code = getattr(raised_error, 'status_code', status_code)
        self.set_status(error_status_code)

        self.set_header('Content-Type', 'application/json; charset=UTF-8')
        self.finish(self.error)
