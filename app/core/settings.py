"""Module that regroups all the functionnalities for setting
the base configurations for the application

author: pendenquejohn@gmail.com
"""

import json
import os
from collections import OrderedDict
from configparser import ConfigParser


class Configuration:
    """This is the base class to configure the application. 
    This returns a dictionary object that you can use order to update
    """

    def __init__(self):
        settings = OrderedDict()

        # Root path
        settings['base_dir'] = os.getcwd()

        # Data directory path
        settings['data_dir'] = os.path.join(settings['base_dir'], 'app', 'data')

        # Settings for the SMTP server
        settings['user'] = None
        settings['password'] = None
        
        # These are the base regex patterns
        # used in order parse the pattern
        # sent by the user to construct an email
        settings['base_regex_patterns'] = {
            'with_separator': [
                # nom.prenom <-> prenom.nom
                # nom_prenom <-> prenom_nom
                # nom-prenom <-> prenom-nom
                r'^(?:(?:pre)?nom)(\S)(?:(?:pre)?nom)$',
                # n.prenom <-> p.nom
                # n-prenom <-> p-nom
                # n_prenom <-> p_nom
                r'^(?:n|p)(\S)(?:(?:pre)?nom)$'
            ],
            'without_separator': [
                # pnom <-> nprenom
                r'^(p|n)?((?:pre)?nom)$',
                # nomp
                r'^(nom)(p)$',
                # nom or prenom
                r'^((?:pre)?nom)$',
            ]
        }

        # Extension to use by default
        # when creating a file
        settings['output_extension'] = 'csv'

        settings['server_config'] = {
            'default': {
                'name': 'google',
                'host': 'smtp.gmail.com',
                'port': 587,
                'user': settings['user'],
                'password': settings['password']
            },
            'outlook': {
                'name': 'outlook',
                'host': 'smtp.gmail.com',
                'port': 587,
                'user': settings['user'],
                'password': settings['password']
            }
        }

        # This is a test parameter variable
        # created to test the features of the application
        settings['dummy_file'] = os.path.join(settings['data_dir'], 'dummy.csv')

        self.settings = settings

    def __setitem__(self, key, value):
        return self.settings.update({key: value})

    def __getitem__(self, key):
        try:
            value = self.settings[key]
        except KeyError:
            value = None
        return value
    
    def __str__(self):
        return str(self.settings)

    def __unicode__(self):
        return self.__str__()

    def __repr__(self):
        return '%s(%s)' % (self.__class__.__name__, str(self.settings))

    def __call__(self, json_file, **kwargs):
        """You can pass additional configuration elements to the
        settings dictionnary by providing a JSON file
        """
        if json_file:
            with open(json_file, 'r', encoding='utf-8') as f:
                additional_settings = json.load(f)
                self.settings.update(**additional_settings)

        return self.settings

configuration = Configuration()
