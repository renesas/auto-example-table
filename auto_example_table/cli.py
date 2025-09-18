import frontmatter
import logging
import os
import re
import subprocess
from argparse import ArgumentParser

from .html import table, tr, th, td, a, ul, li
from .consts import *

from html import escape

log = logging.getLogger()

def get_repository_root() -> str:
  sp = subprocess.run(
    ('git', 'rev-parse', '--show-toplevel'),
    stdout=subprocess.PIPE,
  )
  return sp.stdout.decode().strip()

def find_readmes() -> list[str]:
  readmes = []
  for root, _, filenames in os.walk("."):
    for filename in filenames:
      if not filename in README_FILES:
        continue
      full_path = os.path.join(root, filename)
      readmes.append(full_path)
  return readmes

def get_github_url(example):
  readme: str = example["path"]
  readme = readme.replace("\\", "/")
  return os.path.dirname(readme)

def generate_table(examples: list[dict]) -> str:
  # examples must at least have a name
  examples = [example for example in examples if "name" in example]
  # sort examples by name (case insensitive)
  examples = sorted(examples, key=lambda example: example["name"].lower())

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
        ),
        td(
          escape(example.get("description", "")),
          "" if "keywords" not in example else "<br><br>Keywords: ",
          ", ".join(example.get("keywords", [])),
        ),
      )
      for example in examples
    ],
  )

def parse_arguments():
  parser = ArgumentParser(
    prog='auto-example-table',
    description='pre-commit hook to automatically update example overview table'
  )
  parser.add_argument(
    '-q', '--quiet',
    help="only print critical errors",
    action="store_const",
    dest="log_level",
    default=logging.WARNING,
    const=logging.CRITICAL,
  )
  parser.add_argument(
    '-v', '--verbose',
    help="print info messages",
    action="store_const",
    dest="log_level",
    const=logging.INFO,
  )
  parser.add_argument(
    '-m', '--marker',
    type=str,
    help="table marker identifier name",
    default=DEFAULT_MARKER,
  )
  parser.add_argument(
    'readme',
    help="readme file to update",
  )

  return parser.parse_args()

def main() -> int:
  ec = 0
  opts = parse_arguments()
  logging.basicConfig(
    level=opts.log_level,
    format="[%(levelname)7s] %(message)s",
  )

  repository_root = get_repository_root()
  os.chdir(repository_root)
  log.info(f"changed into {repository_root}")

  log.info(f"readme is {opts.readme}")

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
  with open(opts.readme, "r+") as file:
    content = file.read()
    table = f"@{opts.marker}_BEGIN@\n--->\n{table}\n<!---\n@{opts.marker}_END@"
    updated_content = re.sub(
      f"^@{re.escape(opts.marker)}_BEGIN@$.*^@{re.escape(opts.marker)}_END@$",
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

