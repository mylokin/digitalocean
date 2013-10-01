class Iterable(object):
    def __iter__(self):
        for i in self.all():
            yield i
