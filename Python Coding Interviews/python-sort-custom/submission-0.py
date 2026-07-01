from typing import List


def get_word_length(word: str) -> int:
    return len(word)

def get_abs_val(num: int) -> int:
    return abs(num)

def sort_words(words: List[str]) -> List[str]:
    return sorted(words, key=get_word_length, reverse=True)


def sort_numbers(numbers: List[int]) -> List[int]:
    return sorted(numbers, key = get_abs_val)


# do not modify below this line
print(sort_words(["cherry", "apple", "blueberry", "banana", "watermelon", "zucchini", "kiwi", "pear"]))

print(sort_numbers([1, -5, -3, 2, 4, 11, -19, 9, -2, 5, -6, 7, -4, 2, 6]))
