from dataclasses import dataclass

DEFAULT_MARKER = "EXAMPLE_TABLE"

SHIELDS = "https://img.shields.io/badge/"

README_FILES = (
  'README.md',
  'Readme.md',
  'readme.md',
)

@dataclass
class Board:
  soc: str
  color: str
  url: str

BOARDS: dict[str, Board] = {
  "da14531": Board(
    soc="DA14531",
    url="https://www.renesas.com/en/products/da14531",
    color="darkblue",
  ),
  "da14585": Board(
    soc="DA14585",
    url="https://www.renesas.com/en/products/da14585",
    color="blue",
  ),
  "da14592": Board(
    soc="DA14592",
    url="https://www.renesas.com/en/products/da14592",
    color="slategray",
  ),
  "da14594": Board(
    soc="DA14594",
    url="https://www.renesas.com/en/products/da14594",
    color="darkslategray",
  ),
}

