import time

class PatternMatching:
    @staticmethod
    def kmp(text: str, pattern: str) -> bool:
        n = len(text)
        m = len(pattern)

        if m == 0:
            return True
        if n == 0 and m > 0:
            return False
        if m > n:
            return False

        lps = [0] * m
        
        length = 0
        i = 1
        while i < m:
            if pattern[i] == pattern[length]:
                length += 1
                lps[i] = length
                i += 1
            else:
                if length != 0:
                    length = lps[length - 1]
                else:
                    lps[i] = 0
                    i += 1

        i = 0
        j = 0
        while i < n:
            if pattern[j] == text[i]:
                i += 1
                j += 1

            if j == m:
                return True
            elif i < n and pattern[j] != text[i]:
                if j != 0:
                    j = lps[j - 1]
                else:
                    i += 1
        return False
    
    @staticmethod
    def bm(text: str, pattern: str) -> bool:
        n = len(text)
        m = len(pattern)

        if m == 0:
            return True
        if m > n:
            return False

        skip = {pattern[i]: m - i - 1 for i in range(m - 1)}

        i = 0
        while i <= n - m:
            j = m - 1
            while j >= 0 and pattern[j] == text[i + j]:
                j -= 1
            if j < 0:
                return True

            next_char = text[i + m - 1]
            i += skip.get(next_char, m)

        return False
    
    @staticmethod
    def ld(text: str, pattern: str) -> int:
        n = len(text)
        m = len(pattern)
        prev = [i for i in range(m + 1)]
        curr = [0] * (m + 1)

        for i in range(1, n + 1):
            curr[0] = i
            for j in range(1, m + 1):
                if text[i - 1] == pattern[j - 1]:
                    curr[j] = prev[j - 1]  
                else:
                    curr[j] = min(
                        prev[j] + 1,      # Deletion
                        curr[j - 1] + 1,  # Insertion
                        prev[j - 1] + 1   # Substitution
                    )
            prev, curr = curr, prev  
        return prev[m]
    
    @staticmethod
    def aho_corasick(text: str, patterns: list[str]) -> tuple[int, dict[str, int]]:
        from collections import deque, defaultdict

        class Node:
            def __init__(self):
                self.children = {}
                self.fail = None
                self.output = set()

        root = Node()

        for pattern in patterns:
            node = root
            for char in pattern:
                if char not in node.children:
                    node.children[char] = Node()
                node = node.children[char]
            node.output.add(pattern)

        queue = deque()
        for child in root.children.values():
            child.fail = root
            queue.append(child)

        while queue:
            current = queue.popleft()
            for key, child in current.children.items():
                fail_node = current.fail
                while fail_node and key not in fail_node.children:
                    fail_node = fail_node.fail
                child.fail = fail_node.children[key] if fail_node and key in fail_node.children else root
                child.output |= child.fail.output
                queue.append(child)

        node = root
        match_count = 0
        match_dict: dict[str, int] = defaultdict(int)

        for char in text:
            while node and char not in node.children:
                node = node.fail
            node = node.children[char] if node and char in node.children else root
            for match in node.output:
                match_dict[match] += 1
                match_count += 1

        return match_count, dict(match_dict)

    
# janlup tes dulu, ganti aja methodnya jadi method algoritma lu pada
if __name__ == "__main__":
    test_cases = [
        ("ABABDABACDABABCABAB", "ABABCABAB", True), # Found
        ("ABCDEFG", "EFG", True),                   # Found
        ("ABCDEFG", "XYZ", False),                  # Not found
        ("AAAAAA", "AAA", True),                    # Repeating pattern
        ("AAAAAB", "AAAB", True),                   # Repeating pattern at end
        ("ABCABCABC", "ABC", True),                 # Repeating text
        ("TESTINGTEST", "TEST", True),              # Overlapping pattern
        ("SHORT", "LONGPATTERN", False),            # Pattern longer than text
        ("", "A", False),                           # Empty text
        ("A", "", True),                            # Empty pattern
        ("A", "A", True),                           # Single character match
        ("A", "B", False),                          # Single character mismatch
    ]

    print("--- KMP Function Test with Time Execution ---")

    for i, (text, pattern, expected) in enumerate(test_cases):
        start_time = time.perf_counter()
        result = PatternMatching.kmp(text, pattern)
        end_time = time.perf_counter()
        execution_time = (end_time - start_time) * 1000 # Convert to milliseconds

        print(f"\nTest Case {i+1}:")
        print(f"  Text: '{text}'")
        print(f"  Pattern: '{pattern}'")
        print(f"  Expected: {expected}")
        print(f"  Result: {result}")
        print(f"  Match: {result == expected}")
        print(f"  Execution Time: {execution_time:.4f} ms")



    print("--- Boyer-Moore Function Test ---")

    for i, (text, pattern, expected) in enumerate(test_cases):
        result = PatternMatching.bm(text, pattern)
        print(f"\nTest Case {i+1}:")
        print(f"  Text: '{text}'")
        print(f"  Pattern: '{pattern}'")
        print(f"  Expected: {expected}")
        print(f"  Result: {result}")
        print(f"  Match: {result == expected}")


    print("--- Levenshtein Distance Test ---")

    test_cases_ld = [
        ("kitten", "sitting", 3),  # substitution, substitution, insertion
        ("flaw", "lawn", 2),       # deletion, substitution
        ("saturday", "sunday", 3), # substitution, insertion, deletion
        ("abc", "abc", 0),         # exact match
        ("abc", "abd", 1),         # one substitution
        ("abc", "ab", 1),          # one deletion
        ("ab", "abc", 1),          # one insertion
        ("", "", 0),               # empty strings
        ("a", "", 1),              # text to empty
        ("", "a", 1),              # empty to pattern
        ("apple", "aple", 1),      # one deletion
        ("gfg", "gfg", 0),
        ("horse", "ros", 3),
    ]

    for i, (text, pattern, expected) in enumerate(test_cases_ld):
        result = PatternMatching.ld(text, pattern)
        print(f"\nTest Case {i+1}:")
        print(f"  Text: '{text}'")
        print(f"  Pattern: '{pattern}'")
        print(f"  Expected Levenshtein Distance: {expected}")
        print(f"  Result: {result}")
        print(f"  Match: {result == expected}")

    print("--- Aho-Corasick Function Test ---")

    test_cases_ac = [
        ("ABABDABACDABABCABAB", ["ABABCABAB", "XYZ"], 1),  # One pattern matches
        ("ABCDEFG", ["XYZ", "LMN"], 0),                   # No pattern matches
        ("ABCDEFG", ["EFG", "HIJ"], 1),                   # One pattern matches
        ("AAAAAA", ["AAA", "BBBB"], 4),                   # "AAA" matches 4 times in overlapping substrings
        ("ABCDEFG", [], 0),                               # No patterns, no matches
        ("", ["A", "B"], 0),                              # Empty text, no matches
        ("ABCDEFG", [""], 8),                             # Empty pattern matches at every position (length + 1)
        ("ABCDEFG", ["CDE", "XYZ"], 1),                   # One pattern matches
        ("ABCDEFG", ["xyz", "efg"], 0),                   # Case-sensitive: no matches
    ]

    for i, (text, patterns, expected) in enumerate(test_cases_ac):
        result = PatternMatching.aho_corasick(text, patterns)
        print(f"\nTest Case {i+1}:")
        print(f"  Text: '{text}'")
        print(f"  Patterns: {patterns}")
        print(f"  Expected: {expected}")
        print(f"  Result: {result}")
        print(f"  Match: {result == expected}")

