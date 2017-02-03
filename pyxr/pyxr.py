from fnmatch import fnmatch
from itertools import filterfalse

from Xlib.display import Display
from Xlib.Xatom import RESOURCE_MANAGER, STRING

class Namespace:
    def __init__(self, name='*', display=None):
        self.__namespace__ = str(name)
        self.__display__ = Display(display)
        self.__root__ = self.__display__.screen().root

    def __delattr__(self, key):
        if type(key) != str:
            raise TypeError("Expected 'str', got '{}'".format(type(key).__name__ or repr(type(key))))
        elif key not in self:
            raise KeyError(key)

        resources_property = self.__root__.get_full_property(RESOURCE_MANAGER, STRING)
        if not resources_property:
            return None
        else:
            resources = resources_property.value.decode().split('\n')

        resources = list(filterfalse(lambda s: (len(s.split(':', 1)) != 2), resources))
        for line in resources:
            t = [x.strip() for x in line.split(':', 1)]
            if '{}.{}'.format(self.__namespace__, key) == t[0]:
                resources.remove(line)
                break
        resources.sort()
        resources = '\n'.join(resources) + '\n'
        self.__root__.change_property(RESOURCE_MANAGER, STRING, resources_property.format, resources.encode())
        self.__root__.get_full_property(RESOURCE_MANAGER, STRING)

    def __setattr__(self, key, value):
        if type(key) != str:
            raise TypeError("Expected 'str', got '{}'".format(type(key).__name__ or repr(type(key))))
        if key.startswith('__') and key.endswith('__'):
            object.__setattr__(self, key, value)
            return
 
        resources_property = self.__root__.get_full_property(RESOURCE_MANAGER, STRING)
        if not resources_property:
            return None
        else:
            resources = resources_property.value.decode().split('\n')

        resources = list(filterfalse(lambda s: (len(s.split(':', 1)) != 2), resources))
        for line in resources:
            t = [x.strip() for x in line.split(':', 1)]
            if '{}.{}'.format(self.__namespace__, key) == t[0]:
                resources.remove(line)
                break
        resources.append('{}.{}:\t{}'.format(self.__namespace__, key, value.replace('\n', '\\n')))
        resources.sort()
        resources = '\n'.join(resources) + '\n'
        self.__root__.change_property(RESOURCE_MANAGER, STRING, resources_property.format, resources.encode())
        self.__root__.get_full_property(RESOURCE_MANAGER, STRING)

    def __getattr__(self, key):
        if type(key) != str:
            raise TypeError("Expected 'str', got '{}'".format(type(key).__name__ or repr(type(key))))
            
        resources = self.__root__.get_full_property(RESOURCE_MANAGER, STRING)
        if not resources:
            return None
        else:
            resources = resources.value.decode().split('\n')

        resources = filterfalse(lambda s: (len(s.split(':', 1)) != 2), resources)
        value = None

        for line in resources:
            t = [x.strip() for x in line.split(':', 1)]
            if fnmatch('{}.{}'.format(self.__namespace__, key), t[0]):
                value = t[1]

        if value == None:
            raise KeyError(key)
        return value.replace('\\n', '\n')

    def __contains__(self, key):
        return self[key] != None

    def __dir__(self):
        resources = self.__root__.get_full_property(RESOURCE_MANAGER, STRING)
        if not resources:
            return None
        else:
            resources = resources.value.decode().split('\n')

        resources = filterfalse(lambda s: (len(s.split(':', 1)) != 2), resources)
        contents = []

        for line in resources:
            t = [x.strip() for x in line.split(':', 1)]
            t = t[0].split('.', 1)
            if fnmatch(self.__namespace__, t[0]):
                contents.append(t[1])

        return contents

    def __iter__(self):
        return self.__dir__().__iter__()

    def __len__(self):
        return len(self.__dir__())

    __setitem__ = __setattr__
    __getitem__ = __getattr__
