# Define standard formats for text file inputs from various known sources
# The formats are defined as a list, with the number of items corresponding to the columns in the input file
# See cards.py for the types of named fields that can be inputted

# Use $skip to ignore a column

# Zhongwen plugin for Google Chrome (https://chrome.google.com/webstore/detail/zhongwen-chinese-english/kkmlkkjojmombglmlpbpapmhcaljjkde?hl=en)
# Example: 情调    情調    qíng diào     sentiment; tone and mood; taste
Zhongwen = "{content} {oppositeCharacters} {pinyin} {definition}"

# Pleco dictionary app for mobile - skip the pinyin since it's in the numbered form instead of the preferred accented form
# Example: 桌子    zhuo1zi5        noun table; desk
Pleco = "{content} {skip} {definition}"