class Solution:

    def getBoxNumber(self, num):
        box_index = 0
        while num > 0:
            box_index += num % 10
            num = num // 10
        return box_index

    def countBalls(self, lowLimit: int, highLimit: int) -> int:
        box_map = {}
        for i in range(lowLimit, highLimit + 1):
            box_num = self.getBoxNumber(i)
            if box_num in box_map:
                box_map[box_num] += 1
            else:
                box_map[box_num] = 1
        return max(box_map.values())
