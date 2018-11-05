from google.appengine.api import urlfetch
from urllib import urlencode

from poster.encode import multipart_encode, MultipartParam
from pylovepdf.response import Response


class Request(object):

    @staticmethod
    def send(method, url, payload, headers={}, files=None, stream=None,
             verify_ssl=True, proxies=None, endpoint=None):

        if endpoint == 'auth':
            response = urlfetch.fetch(
                url,
                payload=urlencode(payload),
                method=urlfetch.POST,
                validate_certificate=verify_ssl
            )
            return Response(response)

        if endpoint.startswith('start'):

            response = urlfetch.fetch(
                url,
                method=urlfetch.GET,
                headers=headers,
                validate_certificate=verify_ssl
            )
            return Response(response)

        if endpoint == 'upload':
            payload.update(files)
            datagen, headers_gen = multipart_encode(payload)
            headers.update(headers_gen)
            response = urlfetch.fetch(
                url,
                payload=''.join(datagen),
                method=urlfetch.POST,
                headers=headers,
                validate_certificate=verify_ssl
            )
            return Response(response)

        if endpoint == 'process':
            del headers['Content-Type']
            payload['webhook'] = ''
            response = urlfetch.fetch(
                url,
                payload=urlencode(payload),
                method=urlfetch.POST,
                headers=headers,
                validate_certificate=verify_ssl
            )
            return Response(response)

        if endpoint.startswith('download'):
            response = urlfetch.fetch(
                url,
                method=urlfetch.GET,
                headers=headers,
                validate_certificate=verify_ssl
            )
            return Response(response)

        if endpoint.startswith('task'):
            response = urlfetch.fetch(
                url,
                method=urlfetch.POST,
                headers=headers,
                validate_certificate=verify_ssl
            )
            return Response(response)
