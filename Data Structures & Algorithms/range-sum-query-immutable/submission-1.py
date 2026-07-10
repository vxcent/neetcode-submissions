class NumArray:

    def __init__(self, nums: List[int]):
        self.nums = nums
        self.prefixSums = []
        
        prefix = 0
        for num in nums:
            prefix += num
            self.prefixSums.append(prefix)
        


    def sumRange(self, left: int, right: int) -> int:
        rightSum = self.prefixSums[right]
        leftSum = 0
        if left > 0:
            leftSum = self.prefixSums[left - 1]
        return rightSum - leftSum

# Your NumArray object will be instantiated and called as such:
# obj = NumArray(nums)
# param_1 = obj.sumRange(left,right)