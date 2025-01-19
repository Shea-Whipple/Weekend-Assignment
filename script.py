import os
import re

def search_in_files(search_term):
    results = []
    for root, dirs, files in os.walk('.'):
        for file in files:
            filepath = os.path.join(root, file)
            try:
                with open(filepath, 'r', encoding='utf-8') as f:
                    lines = f.readlines()
                    for line_num, line in enumerate(lines, 1):
                        if re.search(search_term, line, re.IGNORECASE):
                            results.append({
                                'directory': root,
                                'file': file,
                                'line_num': line_num,
                                'content': line.strip()
                            })
            except UnicodeDecodeError:
                continue

    return results

def display_results(results):
    for result in results:
        print(f"Directory: {result['directory']}")
        print(f"File: {result['file']}")
        print(f"Line {result['line_num']}: {result['content']}")
        print("-" * 50)

if __name__ == "__main__":
    search_term = input("Enter search term: ")
    results = search_in_files(search_term)
    display_results(results)