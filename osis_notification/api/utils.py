# ##############################################################################
#
#    OSIS stands for Open Student Information System. It's an application
#    designed to manage the core business of higher education institutions,
#    such as universities, faculties, institutes and professional schools.
#    The core business involves the administration of students, teachers,
#    courses, programs and so on.
#
#    Copyright (C) 2015-2022 Université catholique de Louvain (http://www.uclouvain.be)
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    A copy of this license - GNU General Public License - is available
#    at the root of the source code of this program.  If not,
#    see http://www.gnu.org/licenses/.
#
# ##############################################################################
import re
from urllib.parse import urlparse

import requests
from django.conf import settings
from django.http import HttpResponse
from django.shortcuts import resolve_url


def proxy_view(view_cls):
    """
    Forward as close to an exact copy of the request as possible along to the
    given url.  Respond with as close to an exact copy of the resulting
    response as possible.
    If there are any additional arguments you wish to send to requests, put
    them in the requests_args dictionary.
    """

    if not getattr(settings, 'OSIS_NOTIFICATION_BASE_URL', False):
        # Do not proxy if OSIS_NOTIFICATION_BASE_URL is not set
        return view_cls.as_view()

    def wrapped(request, *args, **kwargs):
        local_base_url = resolve_url('osis_notification:notification-list')
        url_for_remote_api = request.path
        url = settings.OSIS_NOTIFICATION_BASE_URL + url_for_remote_api.replace(local_base_url, '')
        headers = {
            'accept-language': request.user.person.language or settings.LANGUAGE_CODE,
            'x-user-firstname': request.user.person.first_name or '',
            'x-user-lastname': request.user.person.last_name or '',
            'x-user-email': request.user.email or '',
            'x-user-globalid': request.user.person.global_id,
            'authorization': f"ESB {settings.REST_FRAMEWORK_ESB_AUTHENTICATION_SECRET_KEY}",
        }
        response = requests.request(request.method, url, params=request.GET.copy(), headers=headers)

        proxy_response = HttpResponse(response.content, status=response.status_code)

        excluded_headers = {
            # Hop-by-hop headers
            # ------------------
            # Certain response headers should NOT be just tunneled through.  These
            # are they.  For more info, see:
            # http://www.w3.org/Protocols/rfc2616/rfc2616-sec13.html#sec13.5.1
            'connection',
            'keep-alive',
            'proxy-authenticate',
            'proxy-authorization',
            'te',
            'trailers',
            'transfer-encoding',
            'upgrade',
            # Although content-encoding is not listed among the hop-by-hop headers,
            # it can cause trouble as well.  Just let the server set the value as
            # it should be.
            'content-encoding',
            # Since the remote server may or may not have sent the content in the
            # same encoding as Django will, let Django worry about what the length
            # should be.
            'content-length',
        }
        for key, value in response.headers.items():
            if key.lower() in excluded_headers:
                continue
            elif key.lower() == 'location':
                # If the location is relative at all, we want it to be absolute to
                # the upstream server.
                proxy_response[key] = make_absolute_location(response.url, value)
            else:
                proxy_response[key] = value

        return proxy_response

    return wrapped


def make_absolute_location(base_url, location):
    """
    Convert a location header into an absolute URL.
    """
    absolute_pattern = re.compile(r'^[a-zA-Z]+://.*$')
    if absolute_pattern.match(location):
        return location

    parsed_url = urlparse(base_url)

    if location.startswith('//'):
        # scheme relative
        return f'{parsed_url.scheme}:{location}'

    elif location.startswith('/'):
        # host relative
        return f'{parsed_url.scheme}://{parsed_url.netloc}{location}'

    else:
        # path relative
        return f'{parsed_url.scheme}://{parsed_url.netloc}{parsed_url.path.rsplit("/", 1)[0]}/{location}'


class CorsAllowOriginMixin:
    ACCESS_CONTROL_ALLOW_ORIGIN = "Access-Control-Allow-Origin"
    ACCESS_CONTROL_ALLOW_METHODS = "Access-Control-Allow-Methods"
    ACCESS_CONTROL_ALLOW_HEADERS = "Access-Control-Allow-Headers"

    def finalize_response(self, request, response, *args, **kwargs):
        response = super().finalize_response(request, response, *args, **kwargs)

        response[self.ACCESS_CONTROL_ALLOW_METHODS] = "GET, POST"
        response[self.ACCESS_CONTROL_ALLOW_HEADERS] = "Content-Type"

        origin = request.META.get("HTTP_ORIGIN")
        if not origin:
            return response

        if self.origin_in_allowed_list(urlparse(origin)):
            response[self.ACCESS_CONTROL_ALLOW_ORIGIN] = origin

        return response

    def origin_in_allowed_list(self, url):
        origins = [urlparse(o) for o in settings.OSIS_NOTIFICATION_DOMAIN_LIST]
        return any(origin.scheme == url.scheme and origin.netloc == url.netloc for origin in origins)
