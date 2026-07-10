# use prefix to solve and use the index as the liminer to go through the list via a for loop
class Solution:
    def pivotIndex(self, nums: List[int]) -> int:
        self.prefixSums = []
        prefix = 0
        for num in nums:
            prefix += num
            self.prefixSums.append(prefix)
        leftSum = 0
        rightSum = 0
        for i, _ in enumerate(nums):
            leftSum = 0 if i == 0 else self.prefixSums[i - 1]
            rightSum = 0 if i == len(nums) - 1 else self.prefixSums[-1] - self.prefixSums[i]
            if leftSum == rightSum:
                return i
        return -1
