import urllib2, json

class LazyLoad(object):
    def __init__(self, loader):
        self._loader = loader

    def __get__(self, obj, _=None):
        if obj is None:
            return self
        value = self._loader(obj)
        setattr(obj, self._loader.func_name, value)
        return value

class Currency(object):
    @LazyLoad
    def exchange(self):
        app_id = "74d37b616df44690baa2bdcbc6706c7b"
        url = "http://openexchangerates.org/api/latest.json?app_id=%s"%app_id
        response = json.loads(urllib2.urlopen(url).read())
        return response

    def convert(self, amount, code):
        code = code.encode("utf-8").upper()
        if not code in self.exchange:
            return False
        return amount * self.exchange["rates"][code]
