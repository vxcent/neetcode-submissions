class Solution:
    def permute(self, nums: List[int]) -> List[List[int]]:
        output = []
        subset = []
        booleanList = [False for _ in range(len(nums))]

        def dfs(index):
            if len(subset) == len(nums):
                output.append(subset.copy())
                return
            if not False in booleanList:
                return
            
            for i in range(len(nums)):
                if booleanList[i]:
                    continue
                booleanList[i] = True
                subset.append(nums[i])

                dfs(index + 1)

                subset.pop()
                booleanList[i] = False
            
        dfs(0)
        return output


