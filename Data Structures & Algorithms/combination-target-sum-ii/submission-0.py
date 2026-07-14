#DFS approach to use recursion to check if target at the point could be reduced to 0
# For each item, we create a subset of answers to append to output

class Solution:
    def combinationSum2(self, candidates: List[int], target: int) -> List[List[int]]:
        candidates.sort()
        combinations = []
        subset = []
        
        # need to keep track of both if target's reached and combination? no just None for target <0
        def dfs(index, target):
            subset.append(candidates[index])
            target -= candidates[index]
            if target < 0:
                subset.pop()
                return
            
            if target == 0:
                combinations.append(subset.copy())
                subset.pop()    
                return

            for i in range(index + 1, len(candidates)):
                if i > index + 1 and candidates[i] == candidates[i-1]:
                    continue
                dfs(i, target)
            subset.pop()

        for i in range(len(candidates)):
            if i > 0 and candidates[i] == candidates[i-1]:
                continue
            dfs(i, target)

        return combinations
            
        
