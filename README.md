# VPR Parser
Pydantic-based VOCALOID5 Editor Project (.vpr) file parser &amp; unparser

For parsing and manipulating Yamaha VPR (Vocaloid 5 Project) files, this tool allows you to read, modify, and save VPR files programmatically using Pydantic models for type safety and validation.

## Features

- Parsing: Extract structured data from `.vpr` files into Pydantic models.
- Modifying: Update or manipulate the parsed data and save it back to a `.vpr` file.
- Well-typed: Uses Pydantic for robust data validation and serialization.
- Detailed performance logging: Includes a `Timer` utility for profiling operations.

## Installation

Install the package using `pip`:

```bash
pip install vpr-parser
```

Or install from source:

```bash
git clone https://github.com/0x24a/vpr-parser.git
cd vpr-parser
pip install .
```

## Usage

### Parsing a VPR File

```python
from vpr_parser import VPRParser

parser = VPRParser()
vpr_file = parser.parse("path/to/your/project.vpr")

# Access parsed data
print(vpr_file.title)  # Print the project title
print(vpr_file.tracks)  # List all tracks
```

### Modifying and Saving a VPR File

```python
from vpr_parser import VPRParser, models

parser = VPRParser()
vpr_file = parser.parse("path/to/your/project.vpr")

# Modify the title
vpr_file.title = "New Project Title"

# Save the modified file
parser.dump(vpr_file, "path/to/modified_project.vpr")
```

### Available Models

The following Pydantic models are provided for working with VPR data:

- `VPRFile`: Root model representing the entire VPR file.
- `Track`: Represents a track in the project.
- `Part`: Represents a part (segment) within a track.
- `Note`: Represents a note.
- And many, literally, MANY more (see `models.py` for details).

## Development

### Dependencies

- Python 3.8+ (ONLY tested on Python 3.11+, but should work on other versions?)
- Pydantic

### Running Tests

WIP, bcs it just works...?

### Contributing

PRs are welcome! For major changes, please open an issue first to discuss the proposed changes.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.