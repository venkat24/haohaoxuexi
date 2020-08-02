# 好好学习 ⛽

This is a command line power tool for generating and exporting Chinese language learning flashcards into Anki.

Requirements:
- Python v3.6 or above
- Anki installed and running with the [AnkiConnect](https://ankiweb.net/shared/info/2055492159) plugin installed (Visit http://localhost:8765 to test AnkiConnect)

## Motivation

The [Zhongwen Chrome extension](https://chrome.google.com/webstore/detail/zhongwen-chinese-english/kkmlkkjojmombglmlpbpapmhcaljjkde?hl=en) is fantastic for quickly finding character pinyin with a simple mouse hover, saving it to a word list, and exporting it to a text file.

![Zhongwen Plugin](images/zhongwenScrot.png)

Saving the above card would generate a text file with:

`冠状病毒	冠狀病毒	guān zhuàng bìng dú	coronavirus`

However, these text exports aren't in the right format for Anki imports, and doing it manually is laborious. There is also little room for customizing the card format.

This script converts Zhongwen, Pleco, and any other text files containing Chinese content and definitions into ANKI Cards with custom formatting.

## Usage

Use like:

```
hhxx 
--input ../path/to/Zhongwen-Words.txt
--type "zhongwen"
--front "{content}"
--back "<h2>({{pinyin}})</h2> <br /> {{translation}} <br /> Traditional: {{oppositeCharacters}}"
--deck "Vocabulary"
```

If you have a custom list that may or may not have all the required columns, hhxx can generate these columns for you. For example, if you have simple list of sentences like:

```
我知道如果要写很漂亮的字, 应该多练习。
我认为认识汉字不太难，可是记着怎么写字特别难。
繁体字有很多历史和文化，但是写着不容易。
```

You can import this text file with a custom input format with a single `{content}` column, and auto generate the remaining fields in HTML.
```
hhxx
--input sentences.txt
--format "{content}"
--front "<h2>{content}</h2>"
--back "<h4>({pinyin})</h4> <br /> {translation}<br /> 繁体字: {oppositeCharacters}"
--deck "Sentences"
--no-delete
```

The translation will be generated through Google translate, and pinyin and traditional characters will be added. If you prefer traditional characters on the front, pass the `--traditional` flag, and the opposite character set will be simplified characters. Note that the script also converts words into your preferred character set - if you pass an input with traditional character content but prefer simplified chinese, it will be converted to simplified.

The above will generate a card that looks like:

![ANKI Sentence Card](images/sentenceExample.png)

好吧，去好好学习! ⛽