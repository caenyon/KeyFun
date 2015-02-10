import Constants

__author__ = 'Felix'


class SimpleKey(object):
    def __init__(self, vKeyName):
        self.vKeyName = vKeyName


class SimpleModifier(object):
    def __init__(self, layer):
        self.newLayer = layer


class ComplexKey(object):
    def __init__(self, vKeyName, layer):
        self.vKeyName = vKeyName
        self.newLayer = layer


class VirtualKey(object):
    def __init__(self, i):
        if isinstance(i, int):
            if i in Constants.id_to_vk:
                self.id = i
            else:
                raise AttributeError('Integer {} ({}) is not a valid virtual key ID.'.format(i, hex(i)))
        elif isinstance(i, str):
            if not i.startswith('VK_'):
                i = 'VK_' + i

            if i in Constants.vk_to_id:
                self.id = Constants.vk_to_id[i]
            else:
                raise AttributeError('String {} is not a valid virtual key name.'.format(i))
        else:
            raise AttributeError('Key has to be int or str.')

    def __str__(self):
        return Constants.id_to_vkey(self.id)

    def __repr__(self):
        return '<Virtual Key "{}" ({})>'.format(Constants.id_to_vkey(self.id), hex(self.id))

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
