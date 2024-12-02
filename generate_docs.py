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
        content.append(f"- [{title}]({filename})\n")

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


def generate_src_index_markdown(root_dir, dirs):
    index_markdown_path = os.path.join(root_dir, 'index.md')

    with open(index_markdown_path, 'w') as f:
        f.write("# Index\n\n")
        for dir in dirs:
            dir_name = os.path.basename(dir)
            f.write(f"- [{dir_name}]({dir_name}/index.md)\n")



import os
from pathlib import Path
import re
from typing import List, Dict, Optional


class DirectoryIndexer:
    def __init__(self, root_path: str, ignore_patterns: Optional[List[str]] = None):
        self.root_path = Path(root_path)
        self.ignore_patterns = ignore_patterns or ['.git', '__pycache__', '.ipynb_checkpoints', 'venv', 'env']
        self.chapter_counter = 1

    def should_ignore(self, path: Path) -> bool:
        return any(pattern in str(path) for pattern in self.ignore_patterns)

    def clean_name(self, name: str) -> str:
        name = os.path.splitext(name)[0]
        name = name.replace('_', ' ').replace('-', ' ')
        name = re.sub('([a-z])([A-Z])', r'\1 \2', name)
        return ' '.join(word.capitalize() for word in name.split())

    def create_markdown_link(self, name: str, path: Path) -> str:
        """Create a markdown link pointing to index.md in each directory."""
        clean_title = self.clean_name(name)
        # Get relative path from root and prepend 'src'
        rel_path = f"src/{os.path.relpath(path, self.root_path)}"
        # Replace backslashes with forward slashes for consistency
        rel_path = rel_path.replace('\\', '/')
        return f"- [{clean_title}]({rel_path}/index.md)"

    def get_directory_structure(self) -> Dict:
        def recurse(current_path: Path, depth: int = 0) -> Dict:
            if self.should_ignore(current_path):
                return None

            result = {
                'name': current_path.name,
                'path': current_path,
                'depth': depth,
                'children': []
            }

            try:
                for path in sorted(current_path.iterdir()):
                    if path.is_dir() and not self.should_ignore(path):
                        child_result = recurse(path, depth + 1)
                        if child_result:
                            result['children'].append(child_result)
            except PermissionError:
                pass

            return result

        return recurse(self.root_path)

    def generate_markdown(self, structure: Dict = None, level: int = 1) -> str:
        if structure is None:
            structure = self.get_directory_structure()

        markdown_lines = []

        # Add title only for root level
        if level == 1:
            markdown_lines.extend([
                "# Folder Contents\n",
                "---\n"
            ])

        # Add current directory as a link if not root
        if level > 1:
            markdown_link = self.create_markdown_link(structure['name'], structure['path'])
            markdown_lines.append(markdown_link)

        # Process children with indentation
        if structure['children']:
            for child in structure['children']:
                child_content = self.generate_markdown(child, level + 1)
                # Add indentation for children
                indented_content = '\n'.join('  ' * (level - 1) + line
                                           for line in child_content.split('\n') if line)
                markdown_lines.append(indented_content)

        return '\n'.join(markdown_lines)

    def create_index_files(self):
        """Create empty index.md files in each directory."""
        def create_indices(path: Path):
            if self.should_ignore(path):
                return

            # Create index.md in current directory
            index_file = path / 'index.md'
            if not index_file.exists():
                index_file.touch()
                print(f"Created: {index_file}")

            # Recursively create index files in subdirectories
            try:
                for subpath in path.iterdir():
                    if subpath.is_dir() and not self.should_ignore(subpath):
                        create_indices(subpath)
            except PermissionError:
                pass

        create_indices(self.root_path)

    def create_index(self, output_file: Optional[str] = None) -> str:
        """Generate main index and create index.md files in all directories."""
        # First create index.md files in all directories
        self.create_index_files()

        # Then generate the main index content
        markdown_content = self.generate_markdown()

        if output_file:
            output_path = Path(output_file)
            output_path.write_text(markdown_content)
            print(f"Main index saved to: {output_path.absolute()}")

        return markdown_content

def generate_outer_index():
    indexer = DirectoryIndexer("src",
                               ignore_patterns=[".idea", ".git", "venv"])
    markdown_content = indexer.create_index("index.md")
    print("Index generated successfully!")



if __name__ == "__main__":
    root_dir = os.path.abspath(__file__).replace("generate_docs.py", "src")
    dirs = get_all_dirs(root_dir)
    generate_markdowns(dirs)
    generate_src_index_markdown(root_dir, dirs)
    generate_outer_index()
    print("generation is done")
