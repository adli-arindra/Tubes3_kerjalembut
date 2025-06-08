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
        return False
    
    @staticmethod
    def ld(text: str, pattern: str) -> int:
        # n = len(text)
        # m = len(pattern)

        # # Create a 2D table to store results of subproblems
        # # dp[i][j] will be the Levenshtein distance between text[0..i-1] and pattern[0..j-1]
        # dp = [[0] * (m + 1) for _ in range(n + 1)]

        # # Fill the first row and first column
        # for i in range(n + 1):
        #     dp[i][0] = i  # Distance from text[0..i] to an empty pattern
        # for j in range(m + 1):
        #     dp[0][j] = j  # Distance from an empty text to pattern[0..j]

        # # Fill the rest of the table
        # for i in range(1, n + 1):
        #     for j in range(1, m + 1):
        #         if text[i - 1] == pattern[j - 1]:
        #             dp[i][j] = dp[i - 1][j - 1]  # No operation needed if characters match
        #         else:
        #             dp[i][j] = min(
        #                 dp[i - 1][j] + 1,      # Deletion
        #                 dp[i][j - 1] + 1,      # Insertion
        #                 dp[i - 1][j - 1] + 1   # Substitution
        #             )

        # # The Levenshtein distance is stored in dp[n][m]
        # return dp[n][m]
        # error memory 
        
        n = len(text)
        m = len(pattern)
        # Create two rows to store results of subproblems
        prev = [i for i in range(m + 1)]  #  dp[i-1][.]
        curr = [0] * (m + 1)  #  dp[i][.]

        # Fill the rest of the table row by row
        for i in range(1, n + 1):
            curr[0] = i  # The first element of each row is the distance from text[0..i] to an empty pattern
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

    for i, (text, pattern, expected) in enumerate(test_cases):
        result = PatternMatching.ld(text, pattern)
        print(f"\nTest Case {i+1}:")
        print(f"  Text: '{text}'")
        print(f"  Pattern: '{pattern}'")
        print(f"  Expected: {expected}")
        print(f"  Result: {result}")
        print(f"  Match: {result == expected}")



    # Large string test
    print("\n--- Large String Test ---")
    long_text = "A" * 1000000 + "B"
    long_pattern_found = "A" * 500000
    long_pattern_not_found = "C" * 1000

    start_time = time.perf_counter()
    result_long_found = PatternMatching.ld(long_text, long_pattern_found)
    end_time = time.perf_counter()
    execution_time_long_found = (end_time - start_time) * 1000
    print(f"\nLong Text Search (Found):")
    print(f"  Text Length: {len(long_text)}, Pattern Length: {len(long_pattern_found)}")
    print(f"  Result: {result_long_found} (Expected: True)")
    print(f"  Execution Time: {execution_time_long_found:.4f} ms")

    start_time = time.perf_counter()
    result_long_not_found = PatternMatching.ld(long_text, long_pattern_not_found)
    end_time = time.perf_counter()
    execution_time_long_not_found = (end_time - start_time) * 1000
    print(f"\nLong Text Search (Not Found):")
    print(f"  Text Length: {len(long_text)}, Pattern Length: {len(long_pattern_not_found)}")
    print(f"  Result: {result_long_not_found} (Expected: False)")
    print(f"  Execution Time: {execution_time_long_not_found:.4f} ms")