class Solution:
        
    def canPartition(self, nums: List[int]) -> bool:
        # calculate target and send it down dfs
        target = sum(nums)
        if target % 2 != 0:
            return False
        target //= 2
        matrix = [[-1] * (target + 1) for _ in range(len(nums) + 1)]

        def dfs(index, target):
            if index >= len(nums):
                return False
            if target < 0:
                return False
            if target == 0:
                return True
            curr = nums[index]
            if matrix[index][target] != -1:
                return matrix[index][target]
            matrix[index][target] = dfs(index + 1, target) or dfs(index + 1, target - curr)
            return matrix[index][target]
        return dfs(0, target)
    
    
        
        
        
        