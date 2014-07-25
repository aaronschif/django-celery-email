# -*- coding: utf-8 -*-

import pytest
from django.core.mail import EmailMultiAlternatives, EmailMessage, get_connection
from django.core import mail

from django_stored_email.backends import CeleryEmailBackend
from django_stored_email.models import EMail


@pytest.mark.django_db
def test_html(html_email):
    me = EMail(message=html_email)
    me.send()


@pytest.mark.django_db
def test_unicode(email):
    
    chess = """
      a b c d e f g h
    8 ♜ ♞ ♝ ♛ ♚ ♝ ♞ ♜
    7 ♟ ♟ ♟ ♟ ♟ ♟ ♟ ♟
    6        
    5        
    4        
    3        
    2 ♙ ♙ ♙ ♙ ♙ ♙ ♙ ♙
    1 ♖ ♘ ♗ ♕ ♔ ♗ ♘ ♖
    """

    email.body += chess
    me = EMail(message=email)
    me.send()
