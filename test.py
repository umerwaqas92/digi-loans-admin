import os
import re

def is_file_writable(file_path):
    return os.path.exists(file_path) and os.access(file_path, os.W_OK)

def replace_assets_urls(file_path):
    if not os.path.exists(file_path):
        print(f"Error: File '{file_path}' does not exist.")
        return

    if not is_file_writable(file_path):
        print(f"Error: File '{file_path}' is not writable.")
        return

    print(f"Replacing URLs in file: {file_path}")
    with open(file_path, 'r') as file:
        content = file.read()

    # Define a regular expression to match URLs starting with "assets/"
    assets_url_pattern = r'(href|src)="(assets/[^"]+)"'
    # Replace the matched URLs with Flask's url_for
    content = re.sub(assets_url_pattern, r'\1="{{ url_for(\'static\', filename=\'\2\') }}"', content)
    content=content.replace("\\","")

    with open(file_path, 'w') as file:
        file.write(content)

    print(f"Replacement completed successfully.")

# Specify the file path of the icons-line-icons.html file
file_path = 'templates/vertical/index.html'

# Call the function to perform the replacement
try:
    dir_path="templates/vertical"
    for file in os.listdir(dir_path):
        if file.endswith(".html"):
            file_path=os.path.join(dir_path, file)
            
            replace_assets_urls(file_path)
except Exception as e:
    print(f"Error occurred: {e}")
