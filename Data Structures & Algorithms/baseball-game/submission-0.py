class Solution:
    def calPoints(self, operations: List[str]) -> int:
        stack = []
        output = 0
        for c in operations:
            if c  == "+" and stack:
                prev = stack[-1]
                prev_prev = stack[-2]
                stack.append(prev + prev_prev)
            elif c == "D":
                stack.append(2 * stack[-1])
            elif c == "C":
                stack.pop()
            else:
                stack.append(int(c))
        for i in stack:
            output += i
        return output