from collections import Counter

class Solution:
    def hasDuplicate(self, nums: List[int]) -> bool:
        occurance_counter = Counter(nums)
        for k, v in occurance_counter.items():
            if v > 1:
                return True
        return False