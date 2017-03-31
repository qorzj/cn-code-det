"""检查文件的中文编码服务，
返回结果为'utf-8', 'gbk', 'gb18030', 'big5'其中一个，检查失败默认返回gbk
>>> app.request('/?url=parseccrux.qiniudn.com/4465p3cttj10.txt').data
b'gbk'
>>> app.request('/?url=http://www.douban.com').data
b'utf-8'
"""
import web
import requests
from ifsugar import _if, _try

web.config.load('conf.yml')

def detect(url):
    url @= ('http://' + url) @_if('://' not in url)
    headers = {
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.87 Safari/537.36',
            }
    with _try:
        content = requests.get(url, headers=headers, timeout=5).content
        for coding in ['utf-8', 'gbk', 'gb18030']:
            with _try:
                return [content.decode(coding)] and coding

    return 'gbk'

app = web.application()
app.add_frontend(detect, '/', input={'url': '文件的链接'})

application = app.wsgifunc()

if __name__ == '__main__':
    import doctest
    doctest.testmod()
