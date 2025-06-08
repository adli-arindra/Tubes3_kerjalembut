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

        # Preprocess: create bad character shift table (Horspool variant)
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
        return 0
    
    @staticmethod
    def aho_corasick(text: str, patterns: list[str]) -> bool:
        return False
    
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

    # Large string test
    print("\n--- Large String Test ---")
    long_text = "A" * 1000000 + "B"
    long_pattern_found = "A" * 500000
    long_pattern_not_found = "C" * 1000

    start_time = time.perf_counter()
    result_long_found = PatternMatching.kmp(long_text, long_pattern_found)
    end_time = time.perf_counter()
    execution_time_long_found = (end_time - start_time) * 1000
    print(f"\nLong Text Search (Found):")
    print(f"  Text Length: {len(long_text)}, Pattern Length: {len(long_pattern_found)}")
    print(f"  Result: {result_long_found} (Expected: True)")
    print(f"  Execution Time: {execution_time_long_found:.4f} ms")

    start_time = time.perf_counter()
    result_long_not_found = PatternMatching.kmp(long_text, long_pattern_not_found)
    end_time = time.perf_counter()
    execution_time_long_not_found = (end_time - start_time) * 1000
    print(f"\nLong Text Search (Not Found):")
    print(f"  Text Length: {len(long_text)}, Pattern Length: {len(long_pattern_not_found)}")
    print(f"  Result: {result_long_not_found} (Expected: False)")
    print(f"  Execution Time: {execution_time_long_not_found:.4f} ms")
