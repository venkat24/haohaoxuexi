# 好好学习

This is a collection of tools for easy Chinese immersion on YouTube and flashcard generation with ANKI.

## Zhongwen-to-Anki

The [Zhongwen Chrome extension](https://chrome.google.com/webstore/detail/zhongwen-chinese-english/kkmlkkjojmombglmlpbpapmhcaljjkde?hl=en) is fantastic for quickly finding character pinyin with a simple mouse hover, saving it to aword list, and exporting it to a text file.

However, these text exports aren't in the right format for Anki imports, and doing it manually is laborious. This script converts Zhongwen exports into an Anki card friendly format, and uploads each card. The AnkiConnect plugin must be installed and Anki must running on your desktop.

Use like:

```
python3 zhongwen-to-anki.py ../path/to/Zhongwen-Words.txt
```

The source export will be deleted, but a local copy will be saved in the script directory in an Anki-importable format.

## All Chinese All the time

This is a TamperMonkey script that will remove any content that does not have Chinese characters in the title from your feed.

⛽加油！