from glob import glob
from pathlib import Path
import re

DIRECTORY = Path(__file__).parents[1]

PYTHON_EXT = ".py"


pattern_checks = [
    ("Check for non-standard imports", r".*from collections.abc " r"import.*"),
    ("Check for use of exec", r".*exec\(.*"),
    ("Check for pytest warns", r".*pytest\.warns.*"),
    ("Check for pytest raises without context", r"\s*pytest.raises"),
    (
        "Check for python2 new-style classes and for empty parentheses",
        r"class\s\S*\((object)?\):",
    ),
    (
        "Check for incorrect sphinx directives",
        r"\.\. ("
        r".*autosummary|contents|currentmodule|deprecated|function|image|important|"
        r"include|ipython|literalinclude|math|module|note|raw|seealso|toctree|"
        r"versionadded|versionchanged|warning):[^:].*",
        ".rst",
    ),
    (
        "Check that 'unittest.mock' is not used (pytest builtin monkeypatch "
        "fixture should be used instead)",
        r".*(unittest(\.| import )mock|mock\.Mock\(\)|mock\.patch).*",
    ),
    ("Check for extra blank lines after the class definition", r'class.*:\n\n( )+"""'),
    ("Check for use of comment-based annotation syntax", r"#\s+type:\s+ignore"),
    ("Check for use of 'foo.__class__' instead of type(foo)", r".*\.__class__.*"),
    ("Check for use of xrange instead of range", ".*xrange.*"),
    ("Check that no file in the repo contains trailing whitespaces", r"^.*[ \t]+$"),
    ("Check for rogue print statements", r".*print\(.*\).*"),
]

PATH = __file__


def get_files_with_extension(extension: str):
    return [
        file
        for file in glob(str(DIRECTORY / "**" / f"*{extension}"), recursive=True)
        if "_version" not in file and "versioneer" not in file
    ]


def get_file_lines(file_path: str):
    with open(file_path) as file:
        for file_line in file.readlines():
            yield file_line


def check_pattern(message: str, pattern: str, extension: str = PYTHON_EXT):
    print(message + "...")
    violation = False
    files = get_files_with_extension(extension)
    if extension == PYTHON_EXT:
        files.remove(__file__)
    for file in files:
        for line_no, line in enumerate(get_file_lines(file)):
            if re.match(pattern, line):
                print(f"{file}:{line_no + 1}: {line}")
                violation = True
    if violation:
        raise Exception("Pattern violations found!")
    print("Passed")


def main():
    for pattern_check in pattern_checks:
        check_pattern(*pattern_check)


if __name__ == "__main__":
    main()
