import codecs
from markdown2 import markdown
from xml.etree.ElementTree import fromstring, tostring


input_file = codecs.open("README.md", mode="r", encoding="utf-8")
text = input_file.read()
html = markdown(text).encode('utf-8')
html = '<html><head></head><body>' + html + '</body></html>'
HTML = fromstring(html)
l = tostring(HTML, method='html', encoding='us-ascii')
