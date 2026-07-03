from collections import Counter
# First create a counter of words across each word
# Traverse the list with this approach and put each one into the map
# indexed by counter item's frozenset
class Solution:
    def groupAnagrams(self, strs: List[str]) -> List[List[str]]:
        anagram_hashmap = {}
        for word in strs:
            char_counter_frozenset = frozenset(Counter(word).items())
            if char_counter_frozenset in anagram_hashmap:
                anagram_hashmap[char_counter_frozenset].append(word)
            else: 
                anagram_hashmap[char_counter_frozenset] = [word]
        # need to output list from map
        output = []
        for word_list in anagram_hashmap.values():
            output.append(word_list)
        return output