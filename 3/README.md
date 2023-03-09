Поддерживаются запросы вида:

```
word1 & word2 | word3		
word1 & ~word2 | ~str3
word1 | word2 | word3		
word1 | ~word2 | ~word3
```

- `&` - операция AND
- `|` - операция OR
- `~` - операция NOT 

Запуск происходит через команду:
- `python search_inverted_index.py "query"`

Пример команды:
- `python search_inverted_index.py "~это & она"`

**Результат:
Номера страниц, подходящие под запрос**