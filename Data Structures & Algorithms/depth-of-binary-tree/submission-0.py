# Definition for a binary tree node.
# class TreeNode:
#     def __init__(self, val=0, left=None, right=None):
#         self.val = val
#         self.left = left
#         self.right = right

class Solution:
    def maxDepth(self, root: Optional[TreeNode]) -> int:
        if not root:
            return 0
        else:
            return self.dfs(root, 1)
    
    def dfs(self, node, maxDepth):
        if node == None:
            return maxDepth
        
        left_depth, right_depth = maxDepth, maxDepth
        if node.left:
            left_depth = self.dfs(node.left, left_depth + 1)
        if node.right:
            right_depth = self.dfs(node.right, right_depth + 1)
        return max(left_depth, right_depth)
        