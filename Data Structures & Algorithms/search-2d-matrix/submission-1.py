# vertical first, then horizontal
class Solution:
    def searchMatrix(self, matrix: List[List[int]], target: int) -> bool:
        HEIGHT = len(matrix) - 1
        LENGTH = len(matrix[0]) - 1
        row = self.verticalBinarySearch(matrix, target, 0, HEIGHT)
        if row:
            return self.horizontalBinarySearch(row, target, 0, LENGTH)
        else:
            return False
    
    def verticalBinarySearch(self, matrix, target, top, bottom):
        if top > bottom:
            return None
        middleRow= (top + bottom) // 2
        left = matrix[middleRow][0]
        right = matrix[middleRow][-1]
        if target >= left and target <= right:
            return matrix[middleRow]
        elif target < left:
            return self.verticalBinarySearch(matrix, target, top, middleRow - 1)
        else:
            return self.verticalBinarySearch(matrix, target, middleRow + 1, bottom)
        

    def horizontalBinarySearch(self, row, target, left, right):
        if left > right:
            return False
        middle = (left + right) // 2
        if row[middle] == target:
            return True
        elif row[middle] < target:
            return self.horizontalBinarySearch(row, target, middle + 1, right)
        else:
            return self.horizontalBinarySearch(row, target, left, middle - 1)
        