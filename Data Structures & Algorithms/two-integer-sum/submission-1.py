class Solution:
    def twoSum(self, nums: List[int], target: int) -> List[int]:
        hash_map = {}
        output_list = []
        for index, num in enumerate(nums):
            difference_to_target = target - num
            if difference_to_target in hash_map:
                return [hash_map[difference_to_target], index]
            hash_map[num] = index
        return output_list