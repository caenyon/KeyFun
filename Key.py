import Constants

__author__ = 'Felix'


class SimpleKey(object):
    def __init__(self, key_name):
        self.vKeyName = key_name


class SimpleModifier(object):
    def __init__(self, layer):
        self.newLayer = layer


class ComplexKey(object):
    def __init__(self, key_name, layer):
        self.vKeyName = key_name
        self.newLayer = layer


class VirtualKey(object):
    def __init__(self, i):
        if isinstance(i, int):
            if i in Constants.key_id_to_name:
                self.id = i
            else:
                raise AttributeError('Integer {} ({}) is not a valid virtual key ID.'.format(i, hex(i)))
        elif isinstance(i, str):
            if not i.startswith('VK_'):
                i = 'VK_{0}'.format(i)

            if i in Constants.key_name_to_id:
                self.id = Constants.key_name_to_id[i]
            else:
                raise AttributeError('String {} is not a valid virtual key name.'.format(i))
        else:
            raise AttributeError('Key has to be int or str.')

    def __str__(self):
        return Constants.key_id_to_name.get(self.id)

    def __repr__(self):
        return '<Virtual Key "{}" ({})>'.format(Constants.key_id_to_name.get(self.id), hex(self.id))

    def __int__(self):
        return self.id

    def __hex__(self):
        return hex(self.id)


class SimpleUnicodeKey(object):
    def __init__(self, i):
        if isinstance(i, int):
            if 0 <= i <= 2**16-1:
                self.id = i
            else:
                raise AttributeError('Integer {} ({}) is not a valid unicode key ID.'.format(i, hex(i)))
        elif isinstance(i, str):
            if len(i) != 1:
                raise AttributeError('String {} is too long or too short.'.format(i))

            i = ord(i)
            if 0 <= i <= 2**16-1:
                self.id = i
            else:
                raise AttributeError('Integer {} ({}) is not a valid unicode key ID.'.format(i, hex(i)))
        else:
            raise AttributeError('Key has to be int or str.')

    def __str__(self):
        return unichr(self.id)

    def __repr__(self):
        return '<Unicode Key {}>'.format(hex(self.id))

    def __int__(self):
        return self.id

    def __hex__(self):
        return hex(self.id)
