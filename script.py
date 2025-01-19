import os
import re

def parse_search_terms(search_input):
    terms = search_input.split()
    required = [term[1:] for term in terms if term.startswith('+')]
    optional = [term for term in terms if not term.startswith('+')]
    return required, optional

def create_search_pattern(required, optional):
    pattern_parts = []
    
    # Required terms - all must match using positive lookahead
    if required:
        pattern_parts.extend(f'(?=.*{term})' for term in required)
    
    # Optional terms - may or may not match
    if optional:
        opt_pattern = '|'.join(optional)
        pattern_parts.append(f'(?:.*(?:{opt_pattern}))??')
    
    # If no patterns, match anything
    return ''.join(pattern_parts) if pattern_parts else '.*'

def search_in_files(search_input):
    required, optional = parse_search_terms(search_input)
    pattern = create_search_pattern(required, optional)
    results = []
    
    for root, dirs, files in os.walk('.'):
        for file in files:
            filepath = os.path.join(root, file)
            try:
                with open(filepath, 'r', encoding='utf-8') as f:
                    lines = f.readlines()
                    for line_num, line in enumerate(lines, 1):
                        if re.search(pattern, line, re.IGNORECASE):
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
    search_input = input("Enter search terms (+ for required): ")
    results = search_in_files(search_input)
    display_results(results)