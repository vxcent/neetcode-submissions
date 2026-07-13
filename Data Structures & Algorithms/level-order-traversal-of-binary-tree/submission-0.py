# Definition for a binary tree node.
# class TreeNode:
#     def __init__(self, val=0, left=None, right=None):
#         self.val = val
#         self.left = left
#         self.right = right
from collections import deque
class Solution:
    def levelOrder(self, root: Optional[TreeNode]) -> List[List[int]]:
        output = []
        q = deque()
        
        if root:
            q.append(root)



        while q:
            level_output = []
            for i in range(len(q)):
                
                curr_node = q.popleft()
                level_output.append(curr_node.val)
                if curr_node.left:
                    q.append(curr_node.left)
                if curr_node.right:
                    q.append(curr_node.right)

            output.append(level_output)
        return output




    