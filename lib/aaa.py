#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
The MIT License (MIT)

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the e, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in
all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.

Created by: Rui Carmo <https://github.com/rcarmo>
Description: Authentication and Authorization for the Codebits digital signage
             system, modeled on the Cork sample app.
"""

import bottle, logging
from cork import Cork
from config import settings

log = logging.getLogger()

base_url = settings.http.base_url

# Use users.json and roles.json in the local 'etc' directory
aaa = Cork('etc', email_sender='noreply@codebits.eu', smtp_server='127.0.0.1')

authorize = aaa.make_auth_decorator(fail_redirect=base_url+'/auth/unauthorized')

def auth(fail_redirect=base_url+'/auth/login'):
    """Decorator for wrapping a route into a simple authentication test"""
    def _auth(f):
        def _inner(*args, **kwargs):
            aaa.require(fail_redirect=fail_redirect)

            return f(*args, **kwargs)
        return _inner
    return _auth


"""
Authentication handlers
"""

@bottle.get('/auth/unauthorized')
def unauthorized():
    bottle.response.status = '401 Unauthorized'

@bottle.post('/auth/login')
def login():
    """Authenticate users"""

    username = bottle.request.POST.get('username','').strip()
    password = bottle.request.POST.get('password','').strip()
    aaa.login(username, password, success_redirect=base_url, fail_redirect=base_url+'/auth/login?denied=1')


@bottle.route('/auth/login')
@bottle.view('auth/login')
def login_form():
    """Display the login form"""
    if bottle.request.GET.get('denied', None):
        return {'denied_msg': 'Invalid credentials'}
    else:
        return {'denied_msg': ''}


@bottle.route('/auth/logout')
def logout():
    """End the session"""
    aaa.logout(success_redirect=base_url+'/auth/login', fail_redirect=base_url+'/auth/login')


@bottle.route('/auth/denied')
@bottle.view('auth/denied')
def auth_denied():
    """Display an access denied message"""
    return {}


"""
User Registration
"""

def post_get(name):
    return bottle.request.POST.get(name)

@bottle.post('/auth/register')
@bottle.view('auth/register')
def register():
    """Send out a registration email"""
    aaa.register(post_get('username'), post_get('password'), post_get('email'))
    return {}


@bottle.route('/auth/validate/:registration_code')
@bottle.view('auth/validated')
def validate_registration(registration_code):
    """Validate registration, create user account"""
    aaa.validate_registration(registration_code)
    return {}


"""
Password Reset and Change
"""


@bottle.post('/auth/reset')
@bottle.view('auth/reset')
def send_password_reset_email():
    """Send out password reset email"""
    aaa.send_password_reset_email(username=post_get('username'), email_addr=post_get('email'))
    return {}


@bottle.route('/auth/change/:reset_code')
@bottle.view('auth/change')
def reset_password(reset_code):
    """Show password change form"""
    return dict(reset_code=reset_code)


@bottle.post('/auth/update')
@bottle.view('auth/validated')
def change_password():
    """Change password"""
    aaa.reset_password(post_get('reset_code'), post_get('password'))
    return {}
