def getitem(data, key, converter):
    return converter(data[key]) if key in data else None
