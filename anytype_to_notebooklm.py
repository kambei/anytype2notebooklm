import os
import re
import argparse
from pathlib import Path

def merge_markdown_files(input_dir, output_file):
    """
    Merges all Markdown files from input_dir into a single output_file.
    If output_file exists, it incrementally adds only missing files.
    """
    input_path = Path(input_dir)
    output_path = Path(output_file)
    
    if not input_path.exists():
        print(f"Error: Input directory '{input_dir}' does not exist.")
        return

    print(f"Scanning '{input_dir}' for Markdown files...")
    
    md_files = sorted(list(input_path.rglob("*.md")))
    
    if not md_files:
        print("No Markdown files found.")
        return

    existing_files = set()
    mode = "w"
    
    if output_path.exists():
        print(f"Output file '{output_file}' exists. Checking for existing content...")
        try:
            with open(output_path, "r", encoding="utf-8") as f:
                content = f.read()
                # Extract paths from headers like "# Source: path/to/file.md"
                matches = re.findall(r'^# Source: (.+)$', content, re.MULTILINE)
                existing_files = set(matches)
            print(f"Found {len(existing_files)} already processed files.")
            mode = "a"
        except Exception as e:
            print(f"Error reading existing output file: {e}. Overwriting...")
            mode = "w"

    print(f"Found {len(md_files)} Markdown files in source. Merging new files...")

    new_files_count = 0
    with open(output_file, mode, encoding="utf-8") as outfile:
        for md_file in md_files:
            try:
                # Get relative path for a nice header
                rel_path = md_file.relative_to(input_path)
                rel_path_str = str(rel_path)
                
                if rel_path_str in existing_files:
                    continue

                header = f"# Source: {rel_path_str}"
                
                with open(md_file, "r", encoding="utf-8") as infile:
                    content = infile.read()
                    
                # Fix escaping issues (e.g. \_ -> _)
                content = content.replace(r"\_", "_")

                # Remove YAML frontmatter
                content = re.sub(r'^---\n.*?\n---\n', '', content, flags=re.DOTALL)
                
                # Ensure separation if appending
                outfile.write(f"{header}\n\n")
                outfile.write(content)
                outfile.write("\n\n===============\n\n") 

                
                print(f"Processed: {rel_path}")
                new_files_count += 1
            except Exception as e:
                print(f"Error processing {md_file}: {e}")

    if new_files_count > 0:
        print(f"Successfully added {new_files_count} new files to '{output_file}'")
    else:
        print("No new files to add.")

def main():
    parser = argparse.ArgumentParser(description="Merge Anytype Markdown exports into a single file for NotebookLM.")
    parser.add_argument("input_dir", help="Directory containing Anytype exported Markdown files")
    parser.add_argument("output_file", help="Path to the output merged Markdown file")
    
    args = parser.parse_args()
    
    merge_markdown_files(args.input_dir, args.output_file)

if __name__ == "__main__":
    main()
