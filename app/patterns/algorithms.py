import csv
import os
import re

from ze_mailer.app.core.mixins.utilities import UtilitiesMixin
from ze_mailer.app.core.errors import SeparatorError
from ze_mailer.app.core.fileopener import FileOpener, FileWriter
from ze_mailer.app.core.messages import Info
from ze_mailer.app.core.settings import configuration

# e = 'r'
# u = 'paramount'
# s = re.sub(r'^(n)(\W?)(prenom)', rf'\0{e}\2{u}', 'nprenom@gmail.com')
# print(s)

REGEX_PATTERNS = [
    # nprenom
    r'^(?P<nom>n)(?P<prenom>prenom)$',
    # pnom
    r'^(?P<prenom>p)(?P<nom>nom)$',
    # p.nom
    r'^(?P<prenom>p)(?P<separator>\S)+(?P<nom>nom)$',
    # n.prenom

    # prenom.nom
    r'^(?P<prenom>prenom)(?P<separator>\S)+(?P<nom>nom)$',
    # nom.prenom
    r'^(?P<nom>nom)(?P<separator>\S)+(?P<prenom>prenom)$'
]


class NamesAlgorithm(FileOpener, FileWriter):
    """Subclass this class and build basic email patterns such 
    as `name.surname`

    Send a `pattern` as a string, ex. `name.surname`, that
    will be used to construct the email. You can explicitly
    set the separator to be used or rely on the engine 
    presets for that

    These presets are '.' or '-' or '_'

    If provided, the `domain` will be appended, otherwise
    the structure will be returned as set by your pattern.
    The `particle` variable can be used to construct emails
    such as `nom.prenom-bba`. It must be a tuple or a list
    containing the string to append and the separator:
        (bba, -)
    """
    # ex. name.surname
    pattern = ''
    domain = None
    # . - _
    # separator = None
    particle = None

    def construct_pattern(self):
        # A switch that tells if the regex
        # detected a separator or not -;
        # By default, we'll assume that there
        # is a separator
        with_separator = True

        base_regex_patterns = {
            'with_separator': [
                # nom.prenom // prenom.nom
                # nom_prenom // prenom_nom
                # nom-prenom // prenom-nom
                r'^(?:(?:pre)?nom)(\S)(?:(?:pre)?nom)$',
                # n.prenom // p.nom
                # n-prenom // p-nom
                # n_prenom // p_nom
                r'^(?:n|p)(\S)(?:(?:pre)?nom)$'
            ],
            'without_separator': [
                # pnom
                # nprenom
                r'^(p|n)?((?:pre)?nom)$'
            ]
        }

        if self.pattern:
            new_rows = []

            # Unify the patterns in a single array in order to facilitate iteration
            patterns = base_regex_patterns['with_separator'] + base_regex_patterns['without_separator']
            for index, pattern in enumerate(patterns):
                is_match = re.search(pattern, self.pattern)
                if is_match:
                    # If the last pattern is matched,
                    # then we matched a pattern without
                    # a separator
                    if index == 2:
                        with_separator = False
                    break
            
            # Differenciate techniques for groups
            # [nom, ., prenom] and [n, prenom]
            if not with_separator:
                # Since we do not have a separator,
                # just used the match groups
                template_items = list(is_match.groups())
                # We have to create a reusable
                # canvas to prevent changing
                # the names[...] data on each
                # iteration
                copy_of_template_items = template_items.copy()

            else:
                # We can split the names once the separator has
                # been correctly identified ex. ['nom', 'prenom']
                separator_object = is_match.group(1)
                template_items = self.pattern.split(separator_object, 1)
                copy_of_template_items = template_items.copy()
            
            try:
                # We can now get the index of items in the array
                # in order to replace them with the real names
                index_of_surname = copy_of_template_items.index('nom')
                index_of_name = copy_of_template_items.index('prenom')
            except ValueError:
                try:
                    index_of_surname = copy_of_template_items.index('n')
                    index_of_name = copy_of_template_items.index('prenom')
                except ValueError:
                    index_of_surname = copy_of_template_items.index('nom')
                    index_of_name = copy_of_template_items.index('p')
                else:
                    # If we cannot match anything,
                    # just fail the program safely
                    print(Info('We could not find any match with the pattern (%s) that was provided' % self.pattern))
                    raise SystemExit()

            # Replace [name, surname] by the
            # respective names in the file
            # according to the index of name
            # and surname in the array
            # ex. [name, surname] => [pauline, lopez]
            for items in self.csv_content:
                # Values from the csv file can come in two
                # different ways:
                # e.g. [eugenie bouchard], [eugénie, bouchard]
                # If the array comes like in the first example,
                # we need to separate the items
                if with_separator:
                    first, second = items[0].split(' ')
                    # We also need to flatten the elements
                    # in the array
                
                    # Join both using the separator
                    # e.g. pauline.lopez
                    copy_of_template_items[index_of_surname] = second
                    copy_of_template_items[index_of_name] = first

                    final_pattern = separator_object.join(copy_of_template_items)
                else:
                    # Case for pnom
                    if template_items[0] == 'p':
                        copy_of_template_items[index_of_surname] = items[0][:1]
                        copy_of_template_items[index_of_name] = items[1]

                    # Case for nprenom
                    if template_items[0] == 'n':
                        copy_of_template_items[index_of_surname] = items[0]
                        copy_of_template_items[index_of_name] = items[1][:1]

                    final_pattern = ''.join(copy_of_template_items)

                # If a domain was provided,
                # append it to the names
                if self.domain:
                    # e.g. pauline.lopez@gmail.com
                    items.append(self.append_domain(final_pattern))
                    new_rows.append(items)
                else:
                    items.append(final_pattern)
                    new_rows.append(items)
                # Reset the template with the original
                # template elements above
                copy_of_template_items = template_items

            # Update & reinsert headers
            self.headers.append('email')
            new_rows.insert(0, self.headers)

            return new_rows

    @classmethod
    def append_domain(cls, name):
        """Appends a domain to a pattern
        """
        return name + '@' + cls.domain

    def create_file(self, file_name='ZEMAILER_EMAILS.csv'):
        full_path = os.path.join(configuration['output_dir'], file_name)
        super().create_file(full_path, ['name', 'emails'], self.construct_pattern())

class SimpleNamesAlgorithm(UtilitiesMixin):
    """Use this class to construct a list of of multiple emails 
    from scratch providing a person's `name` or a `filepath` names.

    Contrarily to the other classes, this class in particular does
    not need to be subclassed to be used.
    
    Description
    -----------
    This will take a name and create patterns with all provided domains.
    
    Ex. with `Aurélie Konaté`

        [
            'aurelie.konate@gmail.com', 'aurelie.konate@outlook.com', 
            'aurelie-konate@gmail.com', 'aurelie-konate@outlook.com', 
            'aurelie_konate@gmail.com', 'aurelie_konate@outlook.com'
        ]

    You can use this class directly as an iterable to output the values to a given file:
        with open(file_path, 'w') as f:
            f.writelines(BasicPatterns('Aurélie Konaté'))

    Parameters
    ----------
    `name_or_filepath` is a single string name or a file path containing a list of names
    
    `separators` contains a list of separators to use in order to create the email patterns
    `domains` is the list of all the domains that you wish to use to construct the emails
    """

    def __init__(self, name_or_filepath, separators=['.', '-', '_'], 
                    domains=['gmail', 'outlook']):
        patterns = []

        # We have to check whether name_or_filepath
        # is a path, a comma separated list or
        # a list containing names
        if isinstance(name_or_filepath, list):
            self.patterns = self.create_multiple_emails(name_or_filepath, separators, domains)

        elif ',' in name_or_filepath:
            # Do something here when we receive
            # comma separated names:
            # "eugenie  bouchard, kendall jenner"
            has_match = re.match(r'(\w+\s?\w+\,?)+', name_or_filepath)
            if has_match:
                names = name_or_filepath.split(',')
                self.patterns = self.create_multiple_emails(names, separators, domains)

        elif os.path.exists(name_or_filepath):
            if not name_or_filepath.endswith('.csv'):
                pass
            with open(name_or_filepath, 'r', encoding='utf-8') as f:
                csv_file = csv.reader(f)
                # Pop the headers
                csv_file.pop(0)
                names = self.split_multiple_names(csv_file)
        else:
            name = self.split_name(self.flatten_name(name_or_filepath))

            # In the case the name is just a
            # single as opposed to a list,
            # we just have to return the name
            # the remaining domain
            if not isinstance(name, list):
                for domain in domains:
                    pattern = f'{name}@{domain}.com'
                    patterns.append(pattern)
                self.patterns = patterns
            else:
                # Create occurences
                for separator in separators:
                    for domain in domains:
                        pattern = f'{name[0]}{separator}{name[1]}@{domain}.com'
                        patterns.append(pattern)
                self.patterns = patterns

    def __str__(self):
        return str(self.patterns)

    def __repr__(self):
        return '%s(%s)' % (self.__class__.__name__, str(self.patterns))

    def __getitem__(self, index):
        return str(self.patterns[index])

    def append(self, value):
        self.patterns.append(value)
        return self.patterns

    def create_multiple_emails(self, names:list, separators:list, domains:list):
        """A definition for creating and generating multiple email addresses with
        multiple different names in a list
        """
        patterns = []
        for name in names:
            name = self.normalize_name(name)
            splitted_name = self.split_name(name)
            for separator in separators:
                for domain in domains:
                    pattern = f'{splitted_name[0]}{separator}{splitted_name[1]}@{domain}.com'
                    patterns.append(pattern)
        return patterns
