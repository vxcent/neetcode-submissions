# Definition for a binary tree node.
# class TreeNode:
#     def __init__(self, val=0, left=None, right=None):
#         self.val = val
#         self.left = left
#         self.right = right

class Solution:
    def diameterOfBinaryTree(self, root: Optional[TreeNode]) -> int:
        self.diameter = 0
        self.dfs(root)
        return self.diameter

    def dfs(self, node):
        if not node:
            return 0

        left_diameter = self.dfs(node.left)
        right_diameter = self.dfs(node.right)
        curr_diameter = left_diameter + right_diameter
        self.diameter = max(self.diameter, curr_diameter)
        return 1 + max(left_diameter, right_diameter)
        