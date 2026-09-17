import os
import sys
import markdown


SOURCE_DIRECTORY = "recipes"
OUTPUT_DIRECTORY = "site"
TEMPLATES_DIRECTORY = "templates"

CONTENT_PLACEHOLDER = "{{content}}"
NAME_PLACEHOLDER = "{{name}}"


def md_to_html(name: str):
    source = f"{SOURCE_DIRECTORY}/{name}.md"
    template_path = f"{TEMPLATES_DIRECTORY}/generic.html"
    output_path = f"{OUTPUT_DIRECTORY}/{name}.html"

    print(f"source is {source}")
    print(f"template is {template_path}")
    print(f"output is {output_path}")

    with open(template_path, "r") as f:
        template = f.read()

    print("teamplate is read")

    with open(source, "r") as f:
        source_md= f.readlines()

    name = source_md[0].removeprefix("# ").removesuffix("\n")

    print("source is read")

    source_md = "".join(source_md)
    html_content = markdown.markdown(source_md)

    print("MD is converted to HTML")

    with open(output_path, "w") as f:
        result = template.replace(CONTENT_PLACEHOLDER, html_content)
        result = result.replace(NAME_PLACEHOLDER, name)
        f.write(result)

    print("output is saved")
    print()

    return name


if not os.path.exists(OUTPUT_DIRECTORY):
    os.makedirs(OUTPUT_DIRECTORY)


files = [f.removesuffix(".md") for f in os.listdir(SOURCE_DIRECTORY) if f.endswith(".md")]
files = sorted(files)

print("MD converting is started")
print()

index_name = sys.argv[1]
names = {}

for file_name in files:
    name = md_to_html(file_name)
    names[file_name] = name

with open(os.path.join(SOURCE_DIRECTORY, "index.md"), "w") as f:
    f.write(f"# {index_name}")
    f.write(os.linesep)
    f.write(os.linesep)
    for id, (key, value) in enumerate(iterable=names.items(), start=1):
        f.write(f"{id}. [{value}]({key}.html)")
        f.write(os.linesep)

md_to_html("index")

os.remove(os.path.join(SOURCE_DIRECTORY, "index.md"))

print("MD converting is ended")