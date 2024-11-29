import os
import glob
from datetime import datetime


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
        relative_path = os.path.relpath(md_file, directory)
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


if __name__ == "__main__":
    main()