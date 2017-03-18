"""检查文件的中文编码服务，
返回结果为'utf-8', 'gbk', 'gb18030', 'big5'其中一个，检查失败默认返回gbk
>>> app.request('/?url=parseccrux.qiniudn.com/4465p3cttj10.txt').data
b'gbk'
>>> app.request('/?url=http://www.douban.com').data
b'utf-8'
"""
import web
import requests

web.config.load('conf.yml')

class go:
    def __init__(self, x=True):
        self.value = x

    def is_nil(self):
        return self.value is None or self.value is False

    def __call__(self, *a, **b):
        if self.is_nil():
            return self
        try:
            self.value = self.value(*a, **b)
        except:
            self.value = None
        return self

    def __getattr__(self, attr):
        if self.is_nil():
            return self
        try:
            self.value = getattr(self.value, attr)
        except:
            self.value = None
        return self

    def __and__(self, x):
        if self.is_nil():
            return self
        self.value = x
        return self

    def __or__(self, x):
        if self.is_nil():
            return x
        return self.value

    def __rmatmul__(self, x):
        if self.is_nil():
            return x
        return self.value


def detect(url):
    url @= go('://' not in url) & ('http://' + url)
    headers = {
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.87 Safari/537.36',
            }
    content = go(requests).get(url, headers=headers, timeout=5).content | None
    #content = go(requests).get(url).content | None
    if content is None: return 'gbk'
    for coding in ['utf-8', 'gbk', 'gb18030']:
        is_ok = go(content).decode(coding) | None
        if is_ok is not None: return coding

    return 'gbk'

app = web.application()
app.add_frontend(detect, '/', input={'url': '文件的链接'})

application = app.wsgifunc()

if __name__ == '__main__':
    import doctest
    doctest.testmod()
