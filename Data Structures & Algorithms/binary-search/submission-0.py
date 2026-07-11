class Solution:
    def search(self, nums: List[int], target: int) -> int:
        return self.binarySearch(nums, 0, len(nums) -1, target)
        
    def binarySearch(self, nums, left, right, target):
        if left > right:
            return -1
        
        middle = (left + right) // 2
        if nums[middle] == target:
            return middle
        elif nums[middle] < target:
            return self.binarySearch(nums, middle + 1, right, target)
        else:
            return self.binarySearch(nums, left, middle -1, target)
            