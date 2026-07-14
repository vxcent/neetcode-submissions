class Solution:
    def combinationSum2(self, candidates: List[int], target: int) -> List[List[int]]:
        output = []
        subset = []
        candidates.sort()

        def dfs(index, currSum):
            if currSum == target:
                output.append(subset.copy())
                return
            if currSum > target:
                return
            
            for i in range(index, len(candidates)):
                if i > index and candidates[i] == candidates[i - 1]:
                    continue
                
                subset.append(candidates[i])
                dfs(i + 1, currSum + candidates[i])
                subset.pop()
        
        dfs(0, 0)
        return output
