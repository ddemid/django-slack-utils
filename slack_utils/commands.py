class CommandsRegistryError(Exception):
    pass


class CommandsRegistry(object):
    def __init__(self):
        self._handlers = dict()

    def register(self, command, handler):
        if command in self._handlers:
            raise CommandsRegistryError("`{}` already registered".format(command))
        self._handlers[command] = handler

    def __getitem__(self, item):
        return self._handlers[item]

    def clear(self):
        self._handlers = dict()


registry = CommandsRegistry()
