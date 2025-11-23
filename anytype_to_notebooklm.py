import os
import argparse
from pathlib import Path

def merge_markdown_files(input_dir, output_file):
    """
    Merges all Markdown files from input_dir into a single output_file.
    """
    input_path = Path(input_dir)
    
    if not input_path.exists():
        print(f"Error: Input directory '{input_dir}' does not exist.")
        return

    print(f"Scanning '{input_dir}' for Markdown files...")
    
    md_files = sorted(list(input_path.rglob("*.md")))
    
    if not md_files:
        print("No Markdown files found.")
        return

    print(f"Found {len(md_files)} Markdown files. Merging...")

    with open(output_file, "w", encoding="utf-8") as outfile:
        for md_file in md_files:
            try:
                # Get relative path for a nice header
                rel_path = md_file.relative_to(input_path)
                header = f"# Source: {rel_path}"
                
                with open(md_file, "r", encoding="utf-8") as infile:
                    content = infile.read()
                
                outfile.write(f"{header}\n\n")
                outfile.write(content)
                outfile.write("\n\n---\n\n") # Separator
                
                print(f"Processed: {rel_path}")
            except Exception as e:
                print(f"Error processing {md_file}: {e}")

    print(f"Successfully created '{output_file}'")

def main():
    parser = argparse.ArgumentParser(description="Merge Anytype Markdown exports into a single file for NotebookLM.")
    parser.add_argument("input_dir", help="Directory containing Anytype exported Markdown files")
    parser.add_argument("output_file", help="Path to the output merged Markdown file")
    
    args = parser.parse_args()
    
    merge_markdown_files(args.input_dir, args.output_file)

if __name__ == "__main__":
    main()
