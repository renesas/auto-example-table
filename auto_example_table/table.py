import os
from html import escape

from .consts import *
from .html import table, tr, th, td, a, ul, li
from .log import log

def get_github_url(example):
  readme: str = example["path"]
  readme = readme.replace("\\", "/")
  return os.path.dirname(readme)

def generate_table(examples: list[dict]) -> str:
  # examples must at least have a name
  examples = [example for example in examples if "name" in example]
  # sort examples
  examples = sorted(examples, key=lambda example: (
    # by module (case insensitive)
    example.get("module", "").lower(),
    # then by name (case insensitive)
    example["name"].lower(),
  ))

  log.info(f"formatting {len(examples)} exapmle{'' if len(examples) == 1 else 's'}")

  return table(
    tr(
      th('Module'),
      th('Name'),
      th('Boards'),
      th('Description'),
    ),
    *[
      tr(
        td(escape(example.get("module", ""))),
        td(a(get_github_url(example), escape(example["name"]))),
        td(
          ul(
            *[
              li(BOARDS.get(board, board))
              for board in example.get("boards", ["unknown"])
            ],
          ),
          valign='top',
        ),
        td(
          escape(example.get("description", "")),
          "" if "keywords" not in example else "<br><br>Keywords: ",
          ", ".join(example.get("keywords", [])),
          valign='top',
        ),
      )
      for example in examples
    ],
  )

