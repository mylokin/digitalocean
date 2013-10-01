import functools


def event_id(data):
    data['id'] = data.pop('event_id')
    return data


def getitem(data, key, converter):
    return converter(data[key]) if data.get(key) else None


def require(*attrs):
    def decorator(func):
        @functools.wraps(func)
        def validator(self, *args, **kwargs):
            missed = [a for a in attrs if not (hasattr(self, a) and getattr(self, a))]
            if missed:
                name = '{}.{}'.format(self.__class__.__name__, func.__name__)
                missed = ' '.join('\'{}\''.format(a) for a in missed)
                message = '\'{}\' method has no required attributes: {}'
                raise AttributeError(message.format(name, missed))
            return func(self, *args, **kwargs)
        return validator
    return decorator



def docstring(source, method_name):
    def decorator(method):
        @functools.wraps(method)
        def wrapper(*args, **kwargs):
            return method(*args, **kwargs)
        wrapper.__doc__ = getattr(source, method_name).__doc__
        return wrapper
    return decorator


class Iterator(object):
    def __iter__(self):
        for i in self.all():
            yield i


class Fetch(object):
    def __call__(self):
        return self.fetch()
