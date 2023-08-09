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

    assets_url_pattern = r'(href|src)="(assets/[^"]+)"'
    content = re.sub(assets_url_pattern, r'\1="{{ url_for(\'static\', filename=\'\2\') }}"', content)
    content = content.replace("\\", "")

    with open(file_path, 'w') as file:
        file.write(content)

    print(f"Replacement completed successfully.")

def generate_route(file_name,sub_folder):
    route_name = file_name.replace(".html", "")
    return f"@app.route('/{route_name}', methods=['GET'])\ndef {route_name}():\n    return render_template('{sub_folder}/{file_name}')"

file_directory = 'templates/vertical copy'
routes_file = 'routes.txt'

try:
    with open(routes_file, 'w') as routes:
        for file_name in os.listdir(file_directory):
            if file_name.endswith(".html"):
                file_path = os.path.join(file_directory, file_name)

                replace_assets_urls(file_path)

                route = generate_route(file_name,"vertical copy")
                routes.write(route + '\n\n')

except Exception as e:
    print(f"Error occurred: {e}")
