"""检查文件的中文编码服务，
返回结果为'utf-8', 'gbk', 'gb18030', 'big5'其中一个，检查失败默认返回gbk
>>> app.request('/?url=http://parseccrux.qiniudn.com/4465p3cttj10.txt').data
b'gbk'
>>> app.request('/?url=www.zhihu.com').data
b'utf-8'
"""
import web
import requests

web.config.load('conf.yml')

class _:
    def __init__(self, x):
        if x is False:
            self.value = None
        self.value = x

    def __matmul__(self, x):
        if self.value is not None:
            self.value = x
        return self

    def __rmatmul__(self, x):
        if self.value is None:
            return x
        return self.value

    def __call__(self, x):
        if self.value is None:
            return None
        try:
            self.value = self.value(x)
        except:
            self.value = None
        return self

    def __and__(self, x):
        if self.value is None:
            return None
        return x


def detect(url):
    url @= _('://' not in url) @ ('http://' + url)
    assert '://' in url
    try:
        content = requests.get(url).content
        for coding in ['utf-8', 'gbk', 'gb18030']:
            try: content.decode(coding)
            except: continue
            return coding
    except: pass
    return 'gbk'

app = web.application()
app.add_frontend(detect, '/', input={'url': '文件的链接'})

application = app.wsgifunc()

if __name__ == '__main__':
    import doctest
    doctest.testmod()
