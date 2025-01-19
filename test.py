import unittest
from script import parse_search_terms, create_search_pattern
import re

class TestSearchFunctionality(unittest.TestCase):
    def test_search_matches(self):
        test_cases = [
            {
                'search': '+(foo)',
                'should_match': [
                    '"foo bar does not baz bop at all"',
                    '"baz foo creates perfect harmony"',
                    '"bar foo dances with stars"'
                ],
                'should_not_match': [
                    '"biz bop makes the world go round"',
                    '"baz bar lights up the night"'
                ]
            },
            {
                'search': '+(foo bar)',
                'should_match': [
                    '"foo bar does not baz bop at all"',
                    '"bar foo dances with stars"',
                    '"baz bar lights up the night"'
                ],
                'should_not_match': [
                    '"bop baz circles the sun"',
                    '"biz baz sings in moonlight"'
                ]
            }
        ]

        for test in test_cases:
            required, optional = parse_search_terms(test['search'])
            pattern = create_search_pattern(required, optional)
            
            for text in test['should_match']:
                self.assertTrue(re.search(pattern, text, re.IGNORECASE),
                              f"'{test['search']}' should match '{text}'")
            
            for text in test['should_not_match']:
                self.assertFalse(re.search(pattern, text, re.IGNORECASE),
                               f"'{test['search']}' should not match '{text}'")

if __name__ == '__main__':
    unittest.main()