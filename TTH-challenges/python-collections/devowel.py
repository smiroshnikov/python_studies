"""
build a script that removes the vowels from whatever words we give it.
It should take a list of words, which you can just write into the script.
Then it should remove, all of the vowels in each of those words, and
give them back in a new list, with the first letter capitalized.
"""
vowel_list = list('aeiuyo')
full_word_list = ['MMmm', 'FFGDs', 'Momo', 'Sasi', 'Kuki', 'Burgen', 'Oblamandovevshauyapizdroushina']
vowelless_word_list = []


def remove_single_vowel(word):
    modified_word = list(word)
    for letter in word:  # for should run on unmodified word
        if (letter in vowel_list) or (letter.lower() in vowel_list):
            # modified_word.remove(letter) # remove is not dependent on index , works as well
            del (modified_word[modified_word.index(letter)])  # this also works
    return "".join(modified_word).title()  # converting back to string


def process_full_word_list(word_list):
    for word in word_list:
        remove_single_vowel(word)
        vowelless_word_list.append(remove_single_vowel(word))
    return vowelless_word_list
