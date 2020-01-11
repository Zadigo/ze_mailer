from ze_mailer.app.patterns.algorithms import NamesAlgorithm


class NamePatterns(NamesAlgorithm):
    """Use this class to represent the list
    of emails that were created by the super class

    Example
    -------
        class MyClass(NamePatterns):
            pattern = 'nom.prenom'

    Description
    -----------

    By subclassing this class you will get a list of values
    such as :
        [
            [ headers ],
            [ name, email ],
            ...
        ]
    """
    def __str__(self):
        return str(self.construct_pattern())
    
    def __unicode__(self):
        return self.__str__()

    def __repr__(self):
        return '%s(%s)' % (self.__class__.__name__, str(self.construct_pattern()))

    def __getitem__(self, index):
        # Add one in order to return
        # a list not being the headers
        if index == 0:
            index = index + 1
        return str(self.construct_pattern()[index])

    def __len__(self):
        return len(self.construct_pattern())

    @property
    def emails(self):
        items = self.construct_pattern()
        # Pop headers
        items.pop(0)
        for item in items:
            yield item[1:]
