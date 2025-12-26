from markitdown import MarkItDown
import os
import sys

# Set UTF-8 encoding for console output
if sys.platform == 'win32':
    import io
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

# Initialize MarkItDown
md = MarkItDown()

# Directory containing docx files
docs_dir = "docs"
output_dir = "docs/markdown"

# Create output directory if it doesn't exist
os.makedirs(output_dir, exist_ok=True)

# Get all docx files
docx_files = [f for f in os.listdir(docs_dir) if f.endswith('.docx')]

print(f"Found {len(docx_files)} docx files to convert...")

for docx_file in docx_files:
    input_path = os.path.join(docs_dir, docx_file)
    output_filename = docx_file.replace('.docx', '.md')
    output_path = os.path.join(output_dir, output_filename)

    print(f"\nConverting: {docx_file}")
    try:
        # Convert docx to markdown
        result = md.convert(input_path)

        # Write to markdown file
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(result.text_content)

        print(f"  [OK] Saved to: {output_path}")
        print(f"  Content preview (first 200 chars):")
        preview = result.text_content[:200].replace('\n', ' ')
        print(f"  {preview}...")

    except Exception as e:
        print(f"  [ERROR] Error converting {docx_file}: {str(e)[:100]}")

print(f"\n\nConversion complete! Markdown files saved to: {output_dir}")
