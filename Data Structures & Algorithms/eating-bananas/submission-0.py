# Need a "estimateConsumption" for getting output of h
# If h is too low, see if we can find a good higher middle ground
# if h is too high, vice versa
class Solution:
    def minEatingSpeed(self, piles: List[int], h: int) -> int:
        l = 1
        r = max(piles)
        output = r

        while l <= r:
            k = (l + r) // 2

            timeRequired = self.estimateConsumption(piles, k)

            if timeRequired <= h:
                output = k
                r = k - 1
            else:
                l = k + 1
        return output

        

    def estimateConsumption(self, piles, k) -> int:
        estimate = 0
        for p in piles:
            estimate += math.ceil(float(p / k))
        return estimate