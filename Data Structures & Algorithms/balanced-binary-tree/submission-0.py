# Definition for a binary tree node.
# class TreeNode:
#     def __init__(self, val=0, left=None, right=None):
#         self.val = val
#         self.left = left
#         self.right = right

class Solution:
    def isBalanced(self, root: Optional[TreeNode]) -> bool:
        # heightMap = {}
        if not root:
            return True
        
        left = self.getHeight(root.left)
        right = self.getHeight(root.right)
        if abs(left - right) > 1:
            return False
        return self.isBalanced(root.left) and self.isBalanced(root.right)

    def getHeight(self, node):
        if not node:
            return 0
        left_height = self.getHeight(node.left)
        right_height = self.getHeight(node.right)
        return 1 + max(left_height, right_height)

            