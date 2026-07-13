# Definition for a binary tree node.
# class TreeNode:
#     def __init__(self, val=0, left=None, right=None):
#         self.val = val
#         self.left = left
#         self.right = right
from collections import deque
class Solution:
    def hasPathSum(self, root: Optional[TreeNode], targetSum: int) -> bool:
        if not root:
            return False
        
        queue = deque([(root, targetSum - root.val)])

        while queue:
            node, curr_target = queue.popleft()
            if not node.left and not node.right and curr_target == 0:
                return True
            if node.left:
                queue.append((node.left, curr_target - node.left.val))
            if node.right:
                queue.append((node.right, curr_target - node.right.val))
        return False


