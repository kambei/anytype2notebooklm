import sys
import argparse
import markdown
from xhtml2pdf import pisa

def convert_md_to_pdf(input_path, output_path):
    """
    Converts a Markdown file to a PDF file.

    Args:
        input_path (str): Path to the input Markdown file.
        output_path (str): Path to the output PDF file.
    """
    try:
        # 1. Read Markdown content
        with open(input_path, 'r', encoding='utf-8') as f:
            md_content = f.read()

        # 2. Convert Markdown to HTML
        # Using 'extra' extension for tables, footnotes, etc.
        html_content = markdown.markdown(md_content, extensions=['extra'])

        # 3. Convert HTML to PDF
        with open(output_path, "wb") as pdf_file:
            pisa_status = pisa.CreatePDF(
                html_content,                # the HTML to convert
                dest=pdf_file                # file handle to recieve result
            )

        # 4. Check for errors
        if pisa_status.err:
            print(f"Error converting {input_path} to PDF: {pisa_status.err}")
            return False
        
        print(f"Successfully converted '{input_path}' to '{output_path}'.")
        return True

    except FileNotFoundError:
        print(f"Error: The file '{input_path}' was not found.")
        return False
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        return False

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Convert Markdown files to PDF.")
    parser.add_argument("input_file", help="Path to the input Markdown file.")
    parser.add_argument("output_file", help="Path to the output PDF file.")

    args = parser.parse_args()

    convert_md_to_pdf(args.input_file, args.output_file)
