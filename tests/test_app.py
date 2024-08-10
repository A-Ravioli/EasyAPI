import unittest
from EasyAPI.app import EasyAPI
from EasyAPI.request import Request
from EasyAPI.response import Response

class TestEasyAPI(unittest.TestCase):

    def setUp(self):
        self.app = EasyAPI()

    def test_home_route(self):
        def get_home(request):
            return Response("Welcome Home!")

        self.app.add_route('/', get_home)

        environ = {
            'PATH_INFO': '/',
            'REQUEST_METHOD': 'GET',
            'QUERY_STRING': '',
            'wsgi.input': None,
        }
        start_response = lambda status, headers: None
        response = self.app(environ, start_response)

        self.assertEqual(response[0], b"Welcome Home!")

    def test_not_found(self):
        environ = {
            'PATH_INFO': '/notfound',
            'REQUEST_METHOD': 'GET',
            'QUERY_STRING': '',
            'wsgi.input': None,
        }
        start_response = lambda status, headers: None
        response = self.app(environ, start_response)

        self.assertEqual(response[0], b"404 Not Found")

if __name__ == '__main__':
    unittest.main()
