# Definition for a binary tree node.
# class TreeNode:
#     def __init__(self, val=0, left=None, right=None):
#         self.val = val
#         self.left = left
#         self.right = right

# id is that person can only see the tail of each level output
# so walk the tree, and get the outtermost
from collections import deque
class Solution:
    def rightSideView(self, root: Optional[TreeNode]) -> List[int]:
        q = deque()
        if root:
            q.append(root)
        output = []

        while q:
            level_observable = []
            for i in range(len(q)):
                node = q.popleft()
                level_observable.append(node.val)
                if node.left:
                    q.append(node.left)
                if node.right:
                    q.append(node.right)

            output.append(level_observable[-1])
        return output
