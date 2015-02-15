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

    def add_SimpleKey(self, vKey_physical, vKey_target):
        self.layerDict[int(vKey_physical)] = SimpleKey(vKey_target)

    def add_SimpleUnicodeKey(self, vKey_physical, unicode_key):
        self.layerDict[int(vKey_physical)] = SimpleUnicodeKey(unicode_key)

    def add_SimpleMod(self, vKey_physical, layer_target):
        self.layerDict[int(vKey_physical)] = SimpleModifier(layer_target)

    def add_ComplexKey(self, vKey_physical, vKey_target, layer_target):
        self.layerDict[int(vKey_physical)] = ComplexKey(vKey_target, layer_target)

    def add_default_keys(self):
        for vKeyName in Constants.vk_to_id:
            self.add_SimpleKey(VirtualKey(vKeyName), VirtualKey(vKeyName))
