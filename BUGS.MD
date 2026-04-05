# Баг-репорты

## Сводная таблица

| ID | Краткое описание | Severity | Priority | Связанный тест |
|---|---|---|---|---|
| BUG-001 | Некорректная структура ответа POST /api/1/item | Major | High | test_create_item_success |
| BUG-002 | 400 при price = 0 | Major | Medium | test_create_item_price_zero |
| BUG-003 | XSS-скрипт принимается в поле name | Critical | High | test_create_item_with_special_chars_name |
| BUG-004 | Отрицательный price принимается без ошибки | Major | High | test_create_item_negative_price |

---

## BUG-001 — POST /api/1/item возвращает некорректную структуру ответа

**Краткое описание:** Сервис возвращает id созданного объявления внутри строки поля `status` вместо отдельного поля `id`.

**Шаги воспроизведения:**
1. Отправить POST на `https://qa-internship.avito.com/api/1/item` с телом:
```json
{
  "sellerID": 123456,
  "name": "Стол",
  "price": 5000,
  "statistics": {"likes": 1, "viewCount": 2, "contacts": 1}
}
```
2. Получить ответ.

**Фактический результат:**
```json
{"status": "Сохранили объявление - d0638546-c750-4c1f-b41b-60161710b544"}
```

**Ожидаемый результат** (по контракту Postman):
```json
{"id": "d0638546-...", "name": "Стол", "price": 5000, "sellerId": 123456, ...}
```

**Связанный тест:** `test_create_item_success` — падает из-за данного бага  
**Severity:** Major  
**Priority:** High  
**Воспроизводимость:** Всегда  
**Окружение:** https://qa-internship.avito.com, Python 3.13, pytest 9.0.2

---

## BUG-002 — POST /api/1/item возвращает 400 при price = 0

**Краткое описание:** Сервис отклоняет создание объявления с нулевой ценой, хотя `price = 0` является бизнес-корректным сценарием (бесплатное объявление). Документация не ограничивает минимальную цену значением выше нуля.

**Шаги воспроизведения:**
1. Отправить POST на `https://qa-internship.avito.com/api/1/item` с телом:
```json
{
  "sellerID": 123456,
  "name": "Бесплатный товар",
  "price": 0,
  "statistics": {"likes": 0, "viewCount": 0, "contacts": 0}
}
```
2. Получить ответ.

**Фактический результат:** `400 Bad Request`

**Ожидаемый результат:** `200 OK`, объявление создаётся с `price = 0`

**Связанный тест:** `test_create_item_price_zero` — падает из-за данного бага  
**Severity:** Major  
**Priority:** Medium  
**Воспроизводимость:** Всегда  
**Окружение:** https://qa-internship.avito.com, Python 3.13, pytest 9.0.2

---

## BUG-003 — POST /api/1/item принимает XSS-скрипт в поле name

**Краткое описание:** Сервис создаёт объявление с полем `name`, содержащим исполняемый JavaScript-код, вместо возврата ошибки валидации или экранирования значения.

**Шаги воспроизведения:**
1. Отправить POST на `https://qa-internship.avito.com/api/1/item` с телом:
```json
{
  "sellerID": 123456,
  "name": "<script>alert(\"hack\")</script>",
  "price": 5000,
  "statistics": {"likes": 0, "viewCount": 0, "contacts": 0}
}
```
2. Получить ответ.

**Фактический результат:**
```
200 OK
{"status": "Сохранили объявление - 476aec65-2d01-4220-bfdb-2a1a9e05ce84"}
```

**Ожидаемый результат:** Сервис должен вернуть `400 Bad Request` либо `200 OK` с экранированным значением поля `name`. Хранение исполняемого JS-кода as-is является потенциальной угрозой XSS при отображении данных на фронтенде.

**Связанный тест:** `test_create_item_with_special_chars_name` — падает из-за данного бага  
**Severity:** Critical  
**Priority:** High  
**Воспроизводимость:** Всегда  
**Окружение:** https://qa-internship.avito.com, Python 3.13, pytest 9.0.2

---

## BUG-004 — POST /api/1/item принимает отрицательный price

**Краткое описание:** Сервис создаёт объявление с `price = -1` вместо возврата ошибки валидации.

**Шаги воспроизведения:**
1. Отправить POST на `https://qa-internship.avito.com/api/1/item` с телом:
```json
{
  "sellerID": 123456,
  "name": "Стол",
  "price": -1,
  "statistics": {"likes": 0, "viewCount": 0, "contacts": 0}
}
```
2. Получить ответ.

**Фактический результат:**
```
200 OK
{"status": "Сохранили объявление - 476aec65-2d01-4220-bfdb-2a1a9e05ce84"}
```

**Ожидаемый результат:** `400 Bad Request` — поле `price` не может быть отрицательным.

**Связанный тест:** `test_create_item_negative_price` — падает из-за данного бага  
**Severity:** Major  
**Priority:** High  
**Воспроизводимость:** Всегда  
**Окружение:** https://qa-internship.avito.com, Python 3.13, pytest 9.0.2
