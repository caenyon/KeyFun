import Constants

__author__ = 'Felix'

from Key import SimpleKey, SimpleModifier, ComplexKey, VirtualKey, SimpleUnicodeKey


class Layer(object):
    def __init__(self, name):
        self.name = name
        self.layerDict = {}

    def __getitem__(self, item):
        if item in self.layerDict:
            return self.layerDict[item]
        else:
            return None

    def __contains__(self, item):
        return item in self.layerDict

    def add_simple_key(self, key_physical, key_target):
        self.layerDict[int(key_physical)] = SimpleKey(key_target)

    def add_simple_unicode_key(self, key_physical, unicode_key):
        self.layerDict[int(key_physical)] = SimpleUnicodeKey(unicode_key)

    def add_simple_mod(self, key_physical, layer_target):
        self.layerDict[int(key_physical)] = SimpleModifier(layer_target)

    def add_complex_key(self, key_physical, key_target, layer_target):
        self.layerDict[int(key_physical)] = ComplexKey(key_target, layer_target)

    def add_default_keys(self):
        for vKeyName in Constants.key_name_to_id:
            self.add_simple_key(VirtualKey(vKeyName), VirtualKey(vKeyName))
