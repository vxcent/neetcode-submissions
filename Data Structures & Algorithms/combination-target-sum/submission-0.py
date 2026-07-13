class Solution:
    def combinationSum(self, nums: List[int], target: int) -> List[List[int]]:
        output = []
        subset = []

        def dfs(index, total):
            if total == target:
                output.append(subset.copy())
                return
            if total > target:
                return
            for i in range(index, len(nums)):
                n = nums[i]

                subset.append(n)
                dfs(i, total + n)
                subset.pop()
        dfs(0, 0)
        return output