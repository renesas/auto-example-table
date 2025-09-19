import html

def tag(name: str, *content: str, **attrs: str) -> str:
  str_attrs = " ".join(f"{key}=\"{html.escape(value)}\"" for key, value in attrs.items())
  return f"<{name} {str_attrs}>{"".join(content)}</{name}>"

def table(*content: str, **attrs: str) -> str:
  return tag('table', *content, **attrs)

def tr(*content: str, **attrs: str) -> str:
  return tag('tr', *content, **attrs)

def td(*content: str, **attrs: str) -> str:
  return tag('td', *content, **attrs)

def th(*content: str, **attrs: str) -> str:
  return tag('th', *content, **attrs)

def ul(*content: str, **attrs: str) -> str:
  return tag('ul', *content, **attrs)

def li(*content: str, **attrs: str) -> str:
  return tag('li', *content, **attrs)

def a(href: str, *content: str, **attrs: str) -> str:
  return tag('a', *content, **attrs, href=href)

