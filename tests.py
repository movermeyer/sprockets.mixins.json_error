"""
Tests for the sprockets.mixins.json_error package

"""
import json

from sprockets.mixins import json_error
from tornado import testing, web


class HTTPErrorRequestHandler(
        json_error.JsonErrorMixin, web.RequestHandler):

    def get(self):
        raise web.HTTPError(400, 'Error Reason')


class CustomExceptionRequestHandler(
        json_error.JsonErrorMixin, web.RequestHandler):

    class FailureError(Exception):

        status_code = 400
        error_type = 'FailureError'
        documentation_url = 'http://www.example.com'

        def get_message(self):
            return 'Too much Foo'

    def get(self):
        raise self.FailureError()


class UnexpectedErrorRequestHandler(
        json_error.JsonErrorMixin, web.RequestHandler):

    def get(self):
        raise Exception()


class TestHTTPError(testing.AsyncHTTPTestCase):

    def get_app(self):
        return web.Application([('/', HTTPErrorRequestHandler)])

    def test_tornado_thrown_exception(self):
        response = self.fetch('/')
        expected = {'message': 'Unexpected Error', 'type': 'Bad Request'}
        self.assertEqual(json.loads(response.body.decode('utf-8')), expected)


class TestCustomExceptions(testing.AsyncHTTPTestCase):

    def get_app(self):
        return web.Application([('/', CustomExceptionRequestHandler)])

    def test_tornado_custom_exception(self):
        response = self.fetch('/')
        expected = {
            'message': 'Too much Foo',
            'type': 'FailureError',
            'documentation_url': 'http://www.example.com',
        }
        self.assertEqual(json.loads(response.body.decode('utf-8')), expected)


class TestUnexpectedError(testing.AsyncHTTPTestCase):

    def get_app(self):
        return web.Application([('/', UnexpectedErrorRequestHandler)])

    def test_unexpected_exception(self):
        response = self.fetch('/')
        expected = {
            'message': 'Unexpected Error',
            'type': 'Internal Server Error'
        }
        self.assertEqual(json.loads(response.body.decode('utf-8')), expected)
