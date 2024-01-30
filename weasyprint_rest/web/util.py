#!/usr/bin/python
# -*- coding: utf-8 -*-

"""Alternative version of the ToDo RESTful server implemented using the
Flask-RESTful extension."""

import re
import logging
import secrets

from flask import abort, request
from functools import wraps

from ..env import (
    get_api_key, get_allowed_url_pattern, get_blocked_url_pattern
)


def authenticate(func):
    @wraps(func)
    def verify_token(*args, **kwargs):
        try:
            print(f'Correct API Key: {get_api_key()} Provided API Key: {request.headers['X-API-KEY']}', flush=True)
            valid = secrets.compare_digest(get_api_key(), request.headers.get('X-API-KEY'))
            print(f'Compare Digest: {valid}', flush=True)
            authenticated = (
                get_api_key() is None
                or ('X-API-KEY' in request.headers and get_api_key() == request.headers['X-API-KEY'])
            )
            print(f'Authenticated: {authenticated}', flush=True)
        except Exception as error:  # pragma: no cover
            print(f'Request Headers: {request.headers}', flush=True)
            print(f'Error occured during auth: {error}', flush=True)
            return abort(401)

        if authenticated is True:
            return func(*args, **kwargs)
        else:
            abort(401)

    return verify_token


def check_url_access(url):
    allowed_url_pattern = get_allowed_url_pattern()
    blocked_url_pattern = get_blocked_url_pattern()

    try:
        if re.match(allowed_url_pattern, url):
            return True
        if re.match(blocked_url_pattern, url):
            return False
        return True  # pragma: no cover
    except Exception:  # pragma: no cover
        logging.error(
            "Could not parse one of the URL Patterns correctly. Therefor the URL %r was " +
            "blocked. Please check your configuration." % url
        )
        return False
