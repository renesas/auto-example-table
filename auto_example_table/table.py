import os
from html import escape

from .consts import *
from .html import table, tr, th, td, a, img, p
from .log import log

def get_github_url(example):
  readme: str = example["path"]
  readme = readme.replace("\\", "/")
  return os.path.dirname(readme)

def shields_escape(text: str) -> str:
  text = text.replace("-", "--")
  text = text.replace("_", "__")
  text = text.replace(" ", "_")
  return text

def format_board(board: str) -> str:
  if board in BOARDS:
    info = BOARDS[board]
    return a(info.url,
      img(
        f"{SHIELDS}{shields_escape(info.soc)}-{info.color}",
        alt=f"{info.soc}",
      ),
    )
  else:
    return img(
      f"{SHIELDS}{shields_escape(board)}-gray",
      alt=f"{board}",
    )

def generate_table(examples: list[dict]) -> str:
  # examples must at least have a name
  examples = [example for example in examples if "name" in example]
  # sort examples
  examples = sorted(examples, key=lambda example: (
    # by name (case insensitive)
    example["name"].lower(),
  ))

  log.info(f"formatting {len(examples)} exapmle{'' if len(examples) == 1 else 's'}")

  return table(
    tr(
      th('Name'),
      th('Boards'),
      th('Description'),
    ),
    *[
      tr(
        td(a(get_github_url(example), escape(example["name"]))),
        td(
          *[
            format_board(board)
            for board in sorted(
              example.get("boards", ["unknown"]),
              key= lambda name: name.lower()
            )
          ],
          valign='top',
        ),
        td(
          p(escape(example.get("description", ""))),
          "" if "keywords" not in example else
          p("Keywords: ", ", ".join(example.get("keywords", []))),
          valign='top',
        ),
      )
      for example in examples
    ],
  )

