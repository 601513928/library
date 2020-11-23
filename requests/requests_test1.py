import requests
from PIL import Image
from io import BytesIO
import json
# if __name__ == "__main__":
#     pass

# r = requests.get('https://api.github.com/events')
# print(r.status_code)

# r = requests.post('http://httpbin.org/post', data= {'key': 'value'})
# print(r.status_code)
# print(r.text)

# payload = {'key1': 'value1', 'key2': 'value2'}
# r = requests.get('http://httpbin.org/get', params=payload)
# print(r.url)

# payload = {'key1': 'value1', 'key2': ['value2', 'value3']}
# r = requests.get('http://httpbin.org/get', params=payload)
# print(r.url, '\n', r.text, '\n', r.encoding, '\n', r.content)

# i = Image.open(BytesIO(r.content))

# r = requests.get('https://api.github.com/events')
# print(r.json())
# url = 'https://api.github.com/some/endpoint'
# headers = {'user-agent': 'my-app/0.0.1'}
# r = requests.get(url, headers=headers)

# payload = {'key1': 'value1', 'key2': 'value2'}
# r = requests.post("http://httpbin.org/post", data=payload)
# print(r.text)

# url = "https://api.github.com/some/endpoint"
# payload = {'some': 'data'}
# #也可以使用 json = payload 直接传递参数
# r = requests.post(url, data=json.dumps(payload))
# print(r.text)

#POST一个多部分编码的文件
# url = 'http://httpbin.org/post'
# files = {'file': ('report.xls', open('report.xls', 'rb'), 'application/vnd.ms-excel', {'Expires': '0'})}
# files = {'file': open('report.xls', 'rb')}
# files = {'file': ('report.csv', 'some,data,to,send/nanother,row,to,send\n')}
# r = requests.post(url, files=files)
# print(r.text)
# print(r.status_code == requests.codes.ok)
# print(r.headers)
# print(r.headers['Content-Type'])

#Cookie

# url = 'http://example.com/some/cookie/setting/url'
# r = requests.get(url)
# print(r.cookies['example_cookie_name'])
# url = 'http://httpbin.org/cookies'
# cookies = dict(cookies_are='working')

# r = requests.get(url, cookies=cookies)
# print(r.text)

# jar = requests.cookies.RequestsCookieJar()
# jar.set('tasty_cookie', 'yum', domain="httpbin.org", path='/cookies')
# jar.set('gross_cookie', 'blech', domain='httpbin.org', path='/elsewhere')
# url = 'http://httpbin.org/cookies'
# r = requests.get(url, cookies=jar)
# print(r.text)

#重定向与请求历史

# r = requests.get('http://github.com')
# print(r.url, '\n', r.status_code, '\n', r.history)

#allow_redirects = False 禁用重定向
# r = requests.get('http://github.com', allow_redirects=False)
# print(r.status_code, '\n', r.history)

#使用head可以启用重定向
# r = requests.head('http://github.com', allow_redirects=True)

# print(r.url, '\n', r.history)

# requests.get('http://github.com', timeout=0.001)

#请求与响应对象
# r = requests.get('https://www.baidu.com')
# print(r.headers)
# print(r.request.headers)

#SSL证书验证
# requests.get('https://requestb.in')
print(requests.get('https://github.com', verify=True))