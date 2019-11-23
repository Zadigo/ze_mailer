"""Regroups all the modules created in order to deal with sending
email requests using Gmail, Outlook or other email server

author: pendenquejohn@gmail.com
"""
import os
import smtplib
from smtplib import SMTP

from errors import CredentialsError
from ze_mailer.app.core.settings import configuration


class BaseServer:
    """This is the base class used to create a
    an SMTP connection to a server.

    Description
    -----------

    This class should not be used directly but subclassed
    in order to create a connection to a given SMTP server.
    """
    def __init__(self, host=None, port=None, user=None, password=None):
        try:
            # Create an SMTP object from host and port
            # :: <smtplib.SMTP> object
            smtp_connection = SMTP(host=host, port=port)
        except smtplib.SMTPConnectError:
            raise
        else:
            
            # Optional : Identify ourselves to
            # the server - normaly this is called
            # when .sendemail() is called
            smtp_connection.ehlo()
            # Put connection in TLS mode
            # (Transport Layer Security)
            smtp_connection.starttls()
            # It is advised by the documentation to
            # call EHLO after TLS [once again]
            smtp_connection.ehlo()

            try:
                # Check that the creadentials are set and that
                # we can use them for later
                credentials = self.init_credentials(user, password)

                # Login user with password
                smtp_connection.login(credentials['user'], credentials['password'])
            except smtplib.SMTPAuthenticationError:
                # Provided credentials are not good?
                # Get credentials from configuration
                # Raise an error since there's no purpose
                # using such an app without credentials
                # configuration = Configuration()
                # If user and password are none,
                # raises an ImproperlyConfiguredError()
                # user = configuration['USER']
                # password = configuration['PASSWORD']
                raise
            else:
                print(f'Logged in as {user} to {smtp_connection._host}.')
                # return smtp_connection
                self.smtp_connection = smtp_connection

    @staticmethod
    def init_credentials(user, password):
        if not user and not password:
            # Search for the credentials in the environment
            user = os.environ.get('ZEMAILER_USER')
            password = os.environ.get('ZEMAILER_PASSWORD')

            if not user and not password:
                # Sarch for the credentials in configuration
                # for the application
                user = configuration['user']
                password = configuration['password']

        # Raise an error. We cannot find the
        # user and password anywhere
        if not user and not password:
            raise CredentialsError('Could not find any valid credentials e.g. '
                'user, password. Did you forget to set them?')

        return {'user': user, 'password': password}

class Gmail(BaseServer):
    """The server to use for sending emails with Gmail
    """
    def __init__(self, user=None, password=None):
        super().__init__('smtp.gmail.com', 587, user=user, password=password)

class Outlook(BaseServer):
    """The server to use for sending emails with Outlook
    """
    def __init__(self, user=None, password=None):
        super().__init__('smtp.gmail.com', 587, user=user, password=password)
