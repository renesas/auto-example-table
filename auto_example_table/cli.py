#!/bin/python3

import frontmatter
import html
import logging
import os
import re
import subprocess

log = logging.getLogger()

def get_repository_root() -> str:
  sp = subprocess.run(
    ('git', 'rev-parse', '--show-toplevel'),
    stdout=subprocess.PIPE,
  )
  return sp.stdout.decode().strip()

MARKER = "EXAMPLE_TABLE"
ROOT_README = "Readme.md"
README_FILES = (
  'README.md',
  'Readme.md',
  'readme.md',
)
BOARDS = {
  "da14531_pro": "DA14531 Pro Dev Kit",
  "da14585_pro": "DA14585 Pro Dev Kit",
  "da14585_basic": "DA14585 Basic Kit",
  "da14531_usb": "DA14531 USB Kit",
  "unknown": "Unknown",
}

def find_readmes() -> list[str]:
  readmes = []
  for root, _, filenames in os.walk("."):
    for filename in filenames:
      if not filename in README_FILES:
        continue
      full_path = os.path.join(root, filename)
      if full_path == ROOT_README:
        continue
      readmes.append(full_path)
  return readmes

def tag(tag: str, *content: str) -> str:
  return f"<{tag}>{"".join(content)}</{tag.split(" ")[0]}>"

# HTML tag shorthands
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

def get_github_url(example):
  readme: str = example["path"]
  readme = readme.replace("\\", "/")
  for name in README_FILES:
    if not readme.endswith(name):
      continue
    readme = readme.replace(name, "")
    break
  return readme

def generate_table(examples: list[dict]) -> str:
  # examples must at least have a name
  examples = [example for example in examples if "name" in example]
  # sort examples by name (case insensitive)
  examples = sorted(examples, key=lambda example: example["name"].lower())

  log.info(f"formatting {len(examples)} exapmle{'' if len(examples) == 1 else 's'}")

  output = f"@{MARKER}_BEGIN@\n--->\n"
  output += table(
    tr(
      th('Module'),
      th('Name'),
      th('Boards'),
      th('Description'),
    ),
    *[
      tr(
        td(html.escape(example.get("module", ""))),
        td(a(get_github_url(example), html.escape(example["name"]))),
        td(
          ul(
            *[
              li(BOARDS[board])
              for board in example.get("boards", ["unknown"])
            ],
          ),
        ),
        td(
          html.escape(example.get("description", "")),
          "" if "keywords" not in example else "<br><br>Keywords: ",
          ", ".join(example.get("keywords", [])),
        ),
      )
      for example in examples
    ],
  )
  output += f"\n<!---\n@{MARKER}_END@"
  return output

def main() -> int:
  ec = 0
  logging.basicConfig(
    # level=logging.INFO,
    format="[%(levelname)7s] %(message)s",
  )

  repository_root = get_repository_root()
  os.chdir(repository_root)
  log.info(f"changed into {repository_root}")

  log.info(f"main readme is {ROOT_README}")

  readmes = find_readmes()
  exapmles = []
  for readme in readmes:
    with open(readme) as file:
      fm = frontmatter.load(file)
      metadata = fm.metadata
      if not metadata:
        continue
      log.info(f"found frontmatter in {readme}")
      metadata["path"] = readme
      exapmles.append(fm.metadata)
  table = generate_table(exapmles)
  with open(ROOT_README, "r+") as file:
    content = file.read()
    updated_content = re.sub(
      f"^@{re.escape(MARKER)}_BEGIN@$.*^@{re.escape(MARKER)}_END@$",
      table, content, flags=re.DOTALL | re.MULTILINE
    )
    if content == updated_content:
      log.info("table already up-to-date, exiting")
      return ec
    else:
      log.info("updating table in main readme")
      # return non-zero exit code for use in pre-commit hook
      ec = 1
    file.truncate(0)
    file.seek(0, os.SEEK_SET)
    file.write(updated_content)
  return ec

if __name__ == "__main__":
  exit(main())

