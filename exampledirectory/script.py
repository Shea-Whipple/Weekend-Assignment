import os
import re

def parse_search_terms(search_input):
    terms = []
    i = 0
    while i < len(search_input):
        if search_input[i] == '+':
            if search_input[i+1] == '(':
                # Find closing parenthesis
                end = search_input.find(')', i)
                if end != -1:
                    # Get terms within parentheses
                    group_terms = search_input[i+2:end].split()
                    terms.append(('+', group_terms))
                    i = end + 1
                else:
                    i += 1
            else:
                # Regular required term
                word_end = search_input.find(' ', i)
                if word_end == -1:
                    word_end = len(search_input)
                terms.append(('+', [search_input[i+1:word_end]]))
                i = word_end
        else:
            # Optional term
            word_end = search_input.find(' ', i)
            if word_end == -1:
                word_end = len(search_input)
            if i < word_end:
                terms.append(('?', [search_input[i:word_end]]))
            i = word_end
        i += 1
        
    required = []
    optional = []
    for type, words in terms:
        if type == '+':
            required.append(words)
        else:
            optional.extend(words)
    return required, optional

def create_search_pattern(required, optional):
    pattern_parts = []
    
    # Required terms - each group must match
    for req_group in required:
        if len(req_group) > 1:
            # Multiple terms in group - any must match
            pattern_parts.append(f'(?=.*(?:{"|".join(req_group)}))')
        else:
            # Single required term
            pattern_parts.append(f'(?=.*{req_group[0]})')
    
    # Optional terms - may or may not match
    if optional:
        opt_pattern = '|'.join(optional)
        pattern_parts.append(f'(?:.*(?:{opt_pattern}))??')
    
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
    search_input = input("Enter search terms (use + for required, +(term1 term2) for either/or): ")
    results = search_in_files(search_input)
    display_results(results)