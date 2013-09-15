import inspect


class Exception(Exception):
    status_code = None


class AccessDenied(Exception):
    status_code = 401


class NotFound(Exception):
    status_code = 404


status_codes = {e.status_code: e for e in locals().values() if inspect.isclass(e) and issubclass(e, Exception) and e.status_code}
