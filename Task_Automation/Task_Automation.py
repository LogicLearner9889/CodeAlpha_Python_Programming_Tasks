import os
import re
import shutil
import sys
import urllib.request
import urllib.error

def move_jpg_files() -> None:
    """Moves all .jpg/.jpeg files from a source directory to a destination directory."""
    try:
        source_dir = input("Enter source folder path:- ").strip().strip('"')
        dest_dir = input("Enter destination folder path:- ").strip().strip('"')

        if not os.path.exists(source_dir) or not os.path.isdir(source_dir):
            print(f"Error:- Source directory '{source_dir}' does not exist.")
            return

        if os.path.abspath(source_dir) == os.path.abspath(dest_dir):
            print("Source and destination directories cannot be the same.")
            return

        os.makedirs(dest_dir, exist_ok=True)

        moved_count = 0
        for filename in os.listdir(source_dir):
            if filename.lower().endswith((".jpg", ".jpeg")):
                src_path = os.path.join(source_dir, filename)
                dst_path = os.path.join(dest_dir, filename)

                if os.path.isfile(src_path):
                    # Avoid overwriting existing files with the same name
                    if os.path.exists(dst_path):
                        base, ext = os.path.splitext(filename)
                        counter = 1
                        while os.path.exists(dst_path):
                            dst_path = os.path.join(dest_dir, f"{base}_{counter}{ext}")
                            counter += 1

                    shutil.move(src_path, dst_path)
                    moved_count += 1
                    print(f"  Moved: {filename}")

        print(f"Task complete! Moved {moved_count} image(s) to '{dest_dir}'.")

    except PermissionError:
        print("Permission denied: Make sure files aren't open and you have folder write access.")
    except shutil.Error as e:
        print(f"File move error:- {e}")
    except Exception as e:
        print(f"Unexpected error:- {e}")


def extract_emails_from_txt() -> None:
    """Extracts unique email addresses from a .txt file and saves them to an output file."""
    try:
        input_file = input("Enter path to input .txt file:- ").strip().strip('"')
        output_file = input("Enter path for output .txt file (e.g., emails.txt):- ").strip().strip('"')

        if not os.path.isfile(input_file):
            print(f"Error:- File '{input_file}' not found.")
            return

        with open(input_file, "r", encoding="utf-8", errors="replace") as f:
            content = f.read()

        email_pattern = r"[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}"
        found_emails = sorted(set(re.findall(email_pattern, content)))

        if not found_emails:
            print("No email addresses found in the provided file.")
            return

        with open(output_file, "w", encoding="utf-8") as f:
            for email in found_emails:
                f.write(email + "\n")

        print(f"Extracted {len(found_emails)} unique email(s) to '{output_file}'.")

    except PermissionError:
        print("Permission denied while reading/writing files.")
    except OSError as e:
        print(f"File I/O error:- {e}")
    except Exception as e:
        print(f"Unexpected error:- {e}")


def scrape_webpage_title() -> None:
    """Fetches a webpage URL, extracts its <title> tag, and saves it to a file."""
    try:
        url = input("Enter webpage URL (e.g., https://www.abc.tech):- ").strip()
        if not url.startswith(("http://", "https://")):
            url = "https://" + url

        output_file = input("Enter output file name (default: page_title.txt):- ").strip() or "page_title.txt"

        req = urllib.request.Request(
            url,
            headers={"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"}
        )

        with urllib.request.urlopen(req, timeout=10) as response:
            html = response.read().decode("utf-8", errors="replace")

        match = re.search(r"<title[^>]*>(.*?)</title>", html, re.IGNORECASE | re.DOTALL)
        title = match.group(1).strip() if match else "No <title> tag found"
        # Clean extra whitespace/newlines inside title
        title = re.sub(r"\s+", " ", title)

        with open(output_file, "w", encoding="utf-8") as f:
            f.write(f"URL:- {url}\nTitle: {title}\n")

        print(f"Title scraped:- '{title}'")
        print(f"Saved result to '{output_file}'.")

    except urllib.error.HTTPError as e:
        print(f"HTTP Error {e.code}:- {e.reason}")
    except urllib.error.URLError as e:
        print(f"Network/URL Error:- {e.reason}")
    except TimeoutError:
        print("Request timed out while trying to reach the website.")
    except Exception as e:
        print(f"Unexpected error:- {e}")


def main() -> None:
    """CLI menu for Task Automation scripts."""
    while True:
        print("\n" + "=" * 45)
        print("PYTHON TASK AUTOMATION SUITE")
        print("=" * 45)
        print("1. Move all .jpg files from one folder to another")
        print("2. Extract all email addresses from a .txt file")
        print("3. Scrape the title of a webpage and save it")
        print("4. Exit")

        try:
            choice = input("\nSelect an option (1-4):- ").strip()
            if choice == "1":
                move_jpg_files()
            elif choice == "2":
                extract_emails_from_txt()
            elif choice == "3":
                scrape_webpage_title()
            elif choice == "4":
                print("Exiting automation suite. Goodbye!")
                break
            else:
                print("Invalid option. Please enter 1, 2, 3, or 4.")
        except (KeyboardInterrupt, EOFError):
            print("\nExiting safely...")
            sys.exit(0)


if __name__ == "__main__":
    main()