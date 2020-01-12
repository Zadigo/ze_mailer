from ze_mailer.app.core.messages import Info
import re

class UtilitiesMixin:
    """A mixin used to extend classes with various definitions on 
    repetitive tasks on names such as normalizing them etc.
    """
    @staticmethod
    def check_name_structure(name):
        """Check the structure of a name. Sometimes, we might
        get names like 'eugenie bouchard' or 'eugenie' and we
        have to able to distinguish that
        """
        is_normal = re.match(r'^(?:\w+\s?)+$', name)
        is_single = re.match(r'^(?:\w+)$', name)

        if is_normal:
            return {'regex': is_normal, 'match': 'normal'}
        else:
            return {'regex': is_single, 'match': 'single'}

    def split_name(self, name):
        """Create an array with a single name by splitting it.

        Result
        ------
        
        `Eugénie Bouchard` becomes `[Eugénie, Bouchard]`.
        """
        # We have to assert through a regex
        # that we are getting a classic pattern:
        # 'eugenie bouchard' as opposed to 'eugenie'
        check = self.check_name_structure(name)
        if check['match'] == 'single':
            # If we do not have a match,
            # it means that the name is a single
            # element and need to return as is
            return name
        return name.split(' ')

    @classmethod
    def split_multiple_names(cls, names:list):
        """Split multiple names into arrays
        """
        for name in names:
            yield cls.split_name(name)

    @staticmethod
    def normalize_name(name):
        """A helper function that normalizes a name to lowercase
        and strips any whitespaces

        Example
        -------

            "Eugenie Bouchard " becomes "eugenie bouchard"
        """
        return name.lower().strip()

    @classmethod
    def normalize_names(cls, names:list):
        for index, name in enumerate(names):
            # TODO: Cases where the array contains
            # two names - Build something
            # [Eugénie Bouchard, ...]
            names[index][0] = cls.normalize_name(name[0])
        return names

    @classmethod
    def flatten_name(cls, name):
        """Replace all accents from a name and
        normalize it.
        
        Example
        ------

            "Eugénie Bouchard" or "Eugénie Bouchard\\s?"
            becomes `eugenie bouchard`.

            NOTE - This method will also normalize the name
        """
        new_name=''
        accents = {
            'é': 'e',
            'è': 'e',
            'ê': 'e',
            'ë': 'e',
            'ï': 'i',
            'î': 'i',
            'ü': 'u',
            'ù': 'u',
            'à': 'a',
        }
        for letter in name:
            for key, value in accents.items():
                if letter == key:
                    letter = value
            new_name += letter
        return cls.normalize_name(new_name)

    @classmethod
    def reverse(cls, name):
        """Reverse an array with names.

        Example
        -------
        
            [Eugenie, Bouchard] to [Bouchard, Eugenie]
        """
        return list(reversed(cls.split_name(name)))

    def decompose(self, name, change_position=False):
        """Structures composed names into two unique names

        Example
        -------
        
            "Eugenie Pauline Bouchard" becomes "Eugenie" "Pauline Bouchard"

            [Eugenie, Pauline Bouchard] or [Eugenie Pauline, Bouchard]

        Parameters
        ----------

            change_position - changes the direction in which the composed name
                              should appear. The default position is on the left.
        """
        # [Eugenie, Pauline, Bouchard]
        splitted_name = self.split_name(name)
        # Test if list = 3
        if len(splitted_name) != 3:
            print(Info('Cannot perform operation. Your name seems to be a '
                    'non composed name: %s') % name)
            return None
        # Pop middle name
        middle_name = splitted_name.pop(1)
        # Create composed name by joining parts
        if change_position:
            # .. Eugenie and Pauline
            composed_name = ' '.join([splitted_name[0], middle_name])
            splitted_name[0] = composed_name
        else:
            # .. Pauline and Bouchard
            composed_name = ' '.join([middle_name, splitted_name[1]])
            # ..
            splitted_name[1] = composed_name
        # [Eugenie, Pauline Bouchard] or
        # [Eugenie Pauline, Bouchard]
        return splitted_name
