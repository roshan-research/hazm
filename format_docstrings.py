import re, textwrap, glob


def format_all_docstrings(py_file):
    text = open(py_file, encoding="utf-8").read()
    text = text.replace("\t", "    ")

    # Regex pattern that matches all docstrings
    docString_pattern = r"^[ \t]*\"{3}[\s\S]+?\"{3}"

    for match in re.finditer(docString_pattern, text, flags=re.MULTILINE):
        old_doc = match.group(0)
        new_doc = format_docstring(old_doc)
        text = text.replace(old_doc, new_doc)

    open(py_file, "w", encoding="utf-8").write(text)


def format_section(section, new):
    pattern = rf" +{section}:\n[\s\S]+?(?=Examples:\n|Args:\n|Returns:\n|Yields:\n|Raises:\n|Attributes:\n|\"\"\")"
    result = re.search(pattern, new, flags=re.MULTILINE)
    if result is None:
        return ""
    result = result.group(0)
    result = result.replace(f"{section}:", "")
    result = remove_empty_lines(result)
    spaces = len(result) - len(result.lstrip())
    result = re.sub(" " * spaces, "    ", result, flags=re.MULTILINE)
    result = section + ":\n" + result
    return result


def remove_empty_lines(text):
    return "\n".join([line.rstrip() for line in text.splitlines() if line.strip()])


def wrap_text(text, width):
    result = ""
    lines = text.split("\n")
    for line in lines:
        wrapped_line = textwrap.fill(line, width)
        result += wrapped_line + "\n"

    return result


def format_docstring(doc):
    # Number of spaces at the beginning of the docstring
    spaces = len(doc) - len(doc.lstrip())

    section_names = ["Examples", "Args", "Returns", "Yields", "Raises", "Attributes"]
    formatted_section = ""

    # Reformat each section and concatenate to the string variable
    for name in section_names:
        formatted_section += format_section(name, doc) + "\n\n"

    # Find the description of the docstring
    desc = re.search(
        r"\"{3}[\s\S]*?(?=Examples:\n|Args:\n|Returns:\n|Yields:\n|Raises:\n|Attributes:\n|\"\"\")",
        doc,
    ).group(0)

    # Remove leading spaces from each line in the description
    desc = re.sub(r"^ *", "", desc, flags=re.MULTILINE)

    # Wraps the description
    desc = wrap_text(desc, 90)

    doc = desc + "\n\n" + formatted_section + "\n" + '"""'

    # Replaces all occurrences of 3 or more consecutive newline characters with 2 newline characters.
    doc = re.sub(r"\n{3,}", "\n\n", doc, flags=re.MULTILINE)

    # Put some spaces at the beginning of each lines. The number of spaces is determined by the variable "spaces"
    doc = re.sub(r"^", " " * spaces, doc, flags=re.MULTILINE)

    return doc


for pyFile in glob.glob("./hazm/*.py"):
    format_all_docstrings(pyFile)
