import frontmatter
import os
import re
import subprocess
import logging
from argparse import ArgumentParser

from .consts import *
from .table import generate_table
from .log import log

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

def parse_arguments():
  parser = ArgumentParser(
    prog='auto-example-table',
    description='pre-commit hook to automatically update example overview table',
    epilog='''NOTE: this program exits with a non-zero exit code if `readme`
    was updated in order to be used with pre-commit directly.''',
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
    '-d', '--debug',
    help="print debug messages",
    action="store_const",
    dest="log_level",
    const=logging.DEBUG,
  )
  parser.add_argument(
    '-m', '--marker',
    type=str,
    help="table marker identifier name",
    default=DEFAULT_MARKER,
  )
  parser.add_argument(
    '-e', '--encoding',
    type=str,
    help="repository file encoding",
    default='utf-8',
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
    with open(readme, encoding=opts.encoding) as file:
      try:
        fm = frontmatter.load(file)
      except Exception as e:
        log.warning(f"failed to read {readme}, skipping...")
        log.debug(e)
        continue
      metadata = fm.metadata
      if not metadata:
        continue
      log.info(f"found frontmatter in {readme}")
      metadata["path"] = readme
      exapmles.append(fm.metadata)
  table = generate_table(exapmles)
  with open(opts.readme, "r+", encoding=opts.encoding) as file:
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

