# Definition for a binary tree node.
# class TreeNode:
#     def __init__(self, val=0, left=None, right=None):
#         self.val = val
#         self.left = left
#         self.right = right
class Solution:
    def inorderTraversal(self, root: Optional[TreeNode]) -> List[int]:
        output = []

        def dfs(node):
            if not node:
                return
            if node.left:
                dfs(node.left)
            if node:
                output.append(node.val)
            if node.right:
                dfs(node.right)
        dfs(root)
        return output