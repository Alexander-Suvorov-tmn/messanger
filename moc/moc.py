import json
DEBUG = True

def mock(func):
    @wraps
    def wrapper(self, *args, **kwargs):
        if DEBUG == True:
            func_name = func.__name__ + 'moc'
        else:
            func_name = func.__name__
        result = getattr(self, func_name)(*args, **kwargs)
        return result
    wrapper.__name__ = func
    return wrapper

class Photogr(object):
    @mock
    def get_banners(self):
        url = conf.photogr.get_banners_url + "?server_name=%" % conf.photogr.server_name
        try:
            result = self.request(url)
            result = json.loads(result)
        except ValueError:
            result = []
        return [Banner(b) for in result]

    def get_banners_mock(self):
        banners = [{
            #что предаем заготовленное
        }]
        return [Banner(b) for b in banners]
    
