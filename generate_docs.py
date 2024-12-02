import os
import glob
from datetime import datetime

from jedi.inference.finder import filter_name


def get_foldernames(root_dir):
    folder_names = [name for name in os.listdir(root_dir) if os.path.isdir(os.path.join(root_dir, name))]
    return folder_names

def get_non_foldernames(root_dir):
    folder_names = [name for name in os.listdir(root_dir) if not os.path.isdir(os.path.join(root_dir, name))]
    return folder_names


def get_dirs(root_dir,paths):
    folder_names = get_foldernames(root_dir)
    if not folder_names:
        return []
    dirs = [os.path.join(root_dir, dir_name) for dir_name in os.listdir(root_dir) if os.path.isdir(os.path.join(root_dir, dir_name)) and not dir_name.startswith('.')]
    for dir in dirs:
        get_dirs(dir,paths)
    paths.extend(dirs)

def get_all_dirs(root_dir):
    paths = []
    get_dirs(root_dir, paths)
    return paths

def generate_index(directory):
    """Generate index.md content for a given directory"""
    # Get all markdown files in the directory
    md_files = glob.glob(os.path.join(directory, "*.md"))
    md_files = [f for f in md_files if os.path.basename(f) != "index.md"]

    # Generate content
    content = [f"# {os.path.basename(directory).replace('_', ' ').title()}\n\n"]
    content.append(f"Last updated: {datetime.now().strftime('%Y-%m-%d')}\n\n")

    # Add links to each markdown file
    for md_file in md_files:
        filename = os.path.basename(md_file)
        title = filename.replace('.md', '').replace('_', ' ').title()
        relative_path = md_file[md_file.index("src"):]
        content.append(f"- [{title}]({relative_path})\n")

    return ''.join(content)


def update_main_index(root_dir):
    """Update the main index.md with links to all sections"""
    sections = []
    for item in os.listdir(root_dir):
        if os.path.isdir(os.path.join(root_dir, item)) and not item.startswith('.'):
            sections.append(item)

    content = ["# Notebook Documentation\n\n"]
    content.append("## Sections\n\n")

    for section in sorted(sections):
        section_title = section.replace('_', ' ').title()
        content.append(f"- [{section_title}]({section}/index.md)\n")

    return ''.join(content)


def main():
    # Get the root directory (where the script is run)
    root_dir = os.path.dirname(os.path.abspath(__file__))

    # Generate index.md for each subdirectory
    for root, dirs, files in os.walk(root_dir):
        # Skip hidden directories
        dirs[:] = [d for d in dirs if not d.startswith('.')]

        # Generate index.md for current directory
        if root != root_dir:  # Skip root directory
            index_content = generate_index(root)
            with open(os.path.join(root, "index.md"), "w") as f:
                f.write(index_content)

    # Generate main index.md
    main_index = update_main_index(root_dir)
    with open(os.path.join(root_dir, "index.md"), "w") as f:
        f.write(main_index)


def generate_each_markdown(dir):
    files = get_non_foldernames(dir)
    filterd_markdown_files =[os.path.join(dir,_) for _ in files if _!="index.md" and _.endswith(".md")]
    index_md_path = os.path.join(dir,'index.md')
    if filterd_markdown_files:
        index_content = generate_index(dir)
        with open(index_md_path, "w") as f:
            f.write(index_content)


def generate_markdowns(dirs):
    for dir in dirs:
        generate_each_markdown(dir)


def generate_root_index_markdown(root_dir, dirs):
    index_markdown_path = os.path.join(root_dir, 'index.md')

    with open(index_markdown_path, 'w') as f:
        f.write("# Index\n\n")
        for dir in dirs:
            dir_name = os.path.basename(dir)
            f.write(f"- [{dir_name}]({dir_name}/README.md)\n")


if __name__ == "__main__":
    root_dir = os.path.abspath(__file__).replace("generate_docs.py", "src")
    dirs = get_all_dirs(root_dir)
    generate_markdowns(dirs)
    generate_root_index_markdown(root_dir, dirs)
    print("generation is done")
