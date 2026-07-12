class Solution:
    def canPartition(self, nums: List[int]) -> bool:

        target = sum(nums)
        if target % 2 != 0:
            return False
        target = target // 2
        cache = [[-1] * (target + 1) for _ in range(len(nums) + 1)]
        
        def dfs(index, target):
            if target == 0:
                return True
            if target < 0 or index >= len(nums):
                return False
            if cache[index][target] != -1:
                return cache[index][target]

            cache[index][target] = dfs(index + 1, target) or dfs(index + 1, target - nums[index])
            return cache[index][target]
        return dfs(0, target)


