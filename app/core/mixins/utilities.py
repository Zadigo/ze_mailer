from ze_mailer.app.core.messages import Info


class UtilitiesMixin:
    """A mixin used to extend classes with various definitions on 
    repetitive tasks on names such as normalizing them etc.
    """

    @staticmethod
    def split_name(name):
        """Create an array with a single name by splitting it.

        Result
        ------
        
        `Eugénie Bouchard` becomes `[Eugénie, Bouchard]`.
        """
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
        for index, name in names:
            names[index] = cls.normalize_name(name)
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
