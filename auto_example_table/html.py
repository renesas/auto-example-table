import html

def tag(name: str, *content: str, **attrs: str) -> str:
  open = " ".join((name, *(f"{key}=\"{html.escape(value)}\"" for key, value in attrs.items()),))
  if len(content) > 0:
    return f"<{open}>{"".join(content)}</{name}>"
  else:
    return f"<{open}/>"

def table(*content: str, **attrs: str) -> str:
  return tag('table', "", *content, **attrs)

def tr(*content: str, **attrs: str) -> str:
  return tag('tr', "", *content, **attrs)

def td(*content: str, **attrs: str) -> str:
  return tag('td', "", *content, **attrs)

def th(*content: str, **attrs: str) -> str:
  return tag('th', "", *content, **attrs)

def ul(*content: str, **attrs: str) -> str:
  return tag('ul', "", *content, **attrs)

def li(*content: str, **attrs: str) -> str:
  return tag('li', "", *content, **attrs)

def a(href: str, *content: str, **attrs: str) -> str:
  return tag('a', "", *content, **attrs, href=href)

def img(src: str, **attrs: str) -> str:
  return tag('img', **attrs, src=src)

def p(*content: str, **attrs: str) -> str:
  return tag('p', "", *content, **attrs)

