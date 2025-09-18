import html

def tag(tag: str, *content: str) -> str:
  return f"<{tag}>{"".join(content)}</{tag.split(" ")[0]}>"

def table(*content: str) -> str:
  return tag('table', *content)

def tr(*content: str) -> str:
  return tag('tr', *content)

def td(*content: str) -> str:
  return tag('td', *content)

def th(*content: str) -> str:
  return tag('th', *content)

def ul(*content: str) -> str:
  return tag('ul', *content)

def li(*content: str) -> str:
  return tag('li', *content)

def a(href: str, *content: str) -> str:
  return tag(f"a href=\"{html.escape(href)}\"", *content)

