# Тест-кейсы API — Avito QA Internship

**Base URL:** `https://qa-internship.avito.com`

**Заголовки запросов:** `Content-Type: application/json`, `Accept: application/json`

**Severity:**
- `Blocker` — основной сценарий сломан полностью
- `Critical` — ключевая функция не работает
- `Major` — важная функция работает некорректно
- `Minor` — мелкое несоответствие контракту

> В автотестах данные генерируются через Faker, конкретные значения в шагах — для примера.

---

## POST /api/1/item — Создание объявления

### TC-001 — Успешное создание объявления

**Severity:** Blocker | **Функция:** `test_create_item_success`

**Шаги:**
1. POST `/api/1/item`:
```json
{
  "sellerID": 123456,
  "name": "Стол",
  "price": 5000,
  "statistics": {"likes": 1, "viewCount": 2, "contacts": 1}
}
```
2. Проверить статус ответа.
3. Проверить что в теле есть поле `id` с валидным UUID.
4. Проверить наличие полей `name`, `price`, `sellerId`, `statistics`, `createdAt`.

**Ожидаемый результат:** `200 OK`, все поля контракта присутствуют в ответе.

**Фактический результат (баг):** возвращает `{"status": "Сохранили объявление - {uuid}"}` — см. BUG-001.

**Постусловие:** DELETE `/api/2/item/{id}` (UUID из поля `status`)

---

### TC-002 — price = 0

**Severity:** Major | **Функция:** `test_create_item_price_zero`

**Шаги:**
1. POST `/api/1/item` с `price: 0`, остальные поля валидные.
2. Проверить статус ответа.

**Ожидаемый результат:** `200 OK` — нулевая цена допустима (бесплатное объявление).

**Постусловие:** DELETE `/api/2/item/{id}` если получен 200, иначе не требуется.

---

### TC-003 — price = -1

**Severity:** Major | **Функция:** `test_create_item_negative_price`

**Шаги:**
1. POST `/api/1/item` с `price: -1`.
2. Проверить статус и тело ответа.

**Ожидаемый результат:** `400 Bad Request`, в теле — описание ошибки валидации.

**Постусловие:** если вернул 200 (баг) — DELETE `/api/2/item/{id}`.

---

### TC-004 — нет поля name

**Severity:** Critical | **Функция:** `test_create_item_without_name`

**Шаги:**
1. POST `/api/1/item` без поля `name`.
2. Проверить статус и тело ответа.

**Ожидаемый результат:** `400 Bad Request` с описанием ошибки по полю `name`.

---

### TC-005 — нет поля price

**Severity:** Critical | **Функция:** `test_create_item_without_price`

**Шаги:**
1. POST `/api/1/item` без поля `price`.
2. Проверить статус и тело ответа.

**Ожидаемый результат:** `400 Bad Request` с описанием ошибки по полю `price`.

---

### TC-006 — нет поля sellerID

**Severity:** Critical | **Функция:** `test_create_item_without_seller`

**Шаги:**
1. POST `/api/1/item` без поля `sellerID`.
2. Проверить статус и тело ответа.

**Ожидаемый результат:** `400 Bad Request` с описанием ошибки по полю `sellerID`.

---

### TC-007 — нет поля statistics

**Severity:** Critical | **Функция:** `test_create_item_without_statistics`

**Шаги:**
1. POST `/api/1/item` без поля `statistics`.
2. Проверить статус ответа.

**Ожидаемый результат:** `400 Bad Request`.

**Постусловие:** если вернул 200 (баг) — DELETE `/api/2/item/{id}`.

---

### TC-008 — пустое тело запроса

**Severity:** Critical | **Функция:** `test_create_item_without_body`

**Шаги:**
1. POST `/api/1/item` с телом `{}`.
2. Проверить статус ответа.

**Ожидаемый результат:** `400 Bad Request`, не `500`.

---

### TC-009 — name из одного символа

**Severity:** Minor | **Функция:** `test_create_item_short_name`

**Шаги:**
1. POST `/api/1/item` с `name: "S"`.
2. Проверить статус ответа.

**Ожидаемый результат:** `200 OK`.

**Постусловие:** DELETE `/api/2/item/{id}`.

---

### TC-010 — name = пустая строка

**Severity:** Major | **Функция:** `test_create_item_with_empty_name`

**Шаги:**
1. POST `/api/1/item` с `name: ""`.
2. Проверить статус ответа.

**Ожидаемый результат:** `400 Bad Request`.

---

### TC-011 — XSS в поле name

**Severity:** Critical | **Функция:** `test_create_item_with_special_chars_name`

**Шаги:**
1. POST `/api/1/item` с `name: "<script>alert(\"hack\")</script>"`.
2. Проверить статус и тело ответа.

**Ожидаемый результат:** `400 Bad Request` либо `200 OK` с экранированным значением `name`. Хранить JS-код как есть нельзя.

**Постусловие:** если вернул 200 (баг) — DELETE `/api/2/item/{id}`.

---

### TC-012 — sellerID передан строкой

**Severity:** Major | **Функция:** `test_create_item_with_string_seller_id`

**Шаги:**
1. POST `/api/1/item` с `sellerID: "десять тысяч сто двадцать один"`.
2. Проверить статус и тело ответа.

**Ожидаемый результат:** `400 Bad Request` с понятным сообщением об ошибке.

---

### TC-013 — два одинаковых запроса дают разные id (идемпотентность)

**Severity:** Critical | **Функция:** `test_create_items_with_same_body`

**Шаги:**
1. POST `/api/1/item` с телом A, сохранить `id_1`.
2. POST `/api/1/item` с тем же телом A, сохранить `id_2`.
3. Сравнить `id_1` и `id_2`.

**Ожидаемый результат:** оба запроса вернули `200 OK`, `id_1 ≠ id_2`.

**Постусловие:** DELETE для обоих id.

---

### TC-014 — price = 99.99 (дробное число)

**Severity:** Major | **Функция:** `test_create_item_with_float_price`

**Шаги:**
1. POST `/api/1/item` с `price: 99.99`.
2. Проверить статус ответа.

**Ожидаемый результат:** `400 Bad Request` — price принимает только целые числа.

**Постусловие:** если вернул 200 (баг) — DELETE `/api/2/item/{id}`.

---

### TC-015 — очень большой price (граничное значение)

**Severity:** Minor | **Функция:** `test_create_item_with_very_large_price`

**Шаги:**
1. POST `/api/1/item` с `price: 9999999999`.
2. Проверить статус ответа.

**Ожидаемый результат:** `200 OK` или `400`, главное — не `500`.

**Постусловие:** DELETE `/api/2/item/{id}` если получен 200.

---

### TC-016 — очень длинный name (10000 символов)

**Severity:** Minor | **Функция:** `test_create_item_with_very_long_name`

**Шаги:**
1. POST `/api/1/item` с `name` из 10000 символов `"a"`.
2. Проверить статус ответа.

**Ожидаемый результат:** `200 OK` или `400`, не `500`.

**Постусловие:** DELETE `/api/2/item/{id}` если получен 200.

---

### TC-017 — sellerID = 0

**Severity:** Minor | **Функция:** `test_create_item_with_seller_id_zero`

**Шаги:**
1. POST `/api/1/item` с `sellerID: 0`.
2. Проверить статус ответа.

**Ожидаемый результат:** `400 Bad Request`.

**Постусловие:** если вернул 200 (баг) — DELETE `/api/2/item/{id}`.

---

### TC-018 — отрицательное значение в statistics (параметризованный)

**Severity:** Minor | **Функция:** `test_create_item_with_negative_statistics`

Проверяются три варианта: `likes: -1`, `viewCount: -1`, `contacts: -1`.

**Шаги:**
1. POST `/api/1/item` с одним из полей statistics = -1, остальные = 0.
2. Проверить статус ответа.

**Ожидаемый результат:** `400 Bad Request` — отрицательные значения в statistics недопустимы.

**Постусловие:** если вернул 200 (баг) — DELETE `/api/2/item/{id}`.

---

### TC-019 — отсутствует одно поле внутри statistics (параметризованный)

**Severity:** Minor | **Функция:** `test_create_item_with_missing_statistics_field`

Проверяются три варианта: нет `likes`, нет `viewCount`, нет `contacts`.

**Шаги:**
1. POST `/api/1/item` с `statistics` без одного из обязательных полей.
2. Проверить статус ответа.

**Ожидаемый результат:** `400 Bad Request`.

**Постусловие:** если вернул 200 (баг) — DELETE `/api/2/item/{id}`.

---

## GET /api/1/item/:id — Получение объявления по ID

### TC-020 — получение существующего объявления

**Severity:** Blocker | **Функция:** `test_get_item`

**Предусловие:** объявление создано фикстурой `create_and_delete_item`.

**Шаги:**
1. GET `/api/1/item/{id}`.
2. Проверить статус ответа.
3. Проверить что ответ — непустой массив.
4. Сверить поля `id`, `name`, `price`, `sellerId`, `statistics`, `createdAt` с данными из фикстуры.

**Ожидаемый результат:** `200 OK`, все поля совпадают с переданными при создании.

**Постусловие:** фикстура удаляет объявление автоматически.

---

### TC-021 — несуществующий UUID

**Severity:** Major | **Функция:** `test_get_item_with_non_existent_id`

**Шаги:**
1. GET `/api/1/item/00000000-0000-0000-0000-000000000000`.
2. Проверить статус ответа.

**Ожидаемый результат:** `404 Not Found`.

---

### TC-022 — невалидный формат id

**Severity:** Major | **Функция:** `test_get_item_with_invalid_id`

**Шаги:**
1. GET `/api/1/item/abcd`.
2. Проверить статус ответа.

**Ожидаемый результат:** `400` или `404`, не `500`.

---

## GET /api/1/:sellerID/item — Объявления продавца

### TC-023 — получение всех объявлений продавца

**Severity:** Blocker | **Функция:** `test_get_seller_items`

**Шаги:**
1. Сгенерировать `sellerID` в диапазоне 111111–999999.
2. Создать два объявления с этим `sellerID`, сохранить `id_1` и `id_2`.
3. GET `/api/1/{sellerID}/item`.
4. Проверить статус и структуру ответа.
5. Проверить что `id_1` и `id_2` есть в списке.
6. Проверить что у всех элементов `sellerId` совпадает с запрошенным.

**Ожидаемый результат:** `200 OK`, список содержит оба объявления, у всех элементов правильный `sellerId` и поля `id`, `name`, `price`, `statistics`, `createdAt`.

**Постусловие:** DELETE для `id_1` и `id_2`.

---

### TC-024 — продавец без объявлений

**Severity:** Major | **Функция:** `test_get_seller_items_empty`

**Предусловие:** для `sellerID = 12412421` объявлений нет.

**Шаги:**
1. GET `/api/1/12412421/item`.
2. Проверить статус и тело ответа.

**Ожидаемый результат:** `200 OK` с пустым массивом `[]` или `404`.

---

### TC-025 — sellerID строкой в пути

**Severity:** Major | **Функция:** `test_get_items_with_string_seller_id`

**Шаги:**
1. GET `/api/1/skakskdkds/item`.
2. Проверить статус ответа.

**Ожидаемый результат:** `400` или `404`, не `500`.

---

### TC-026 — объявление продавца A не попадает в список продавца B

**Severity:** Critical | **Функция:** `test_item_not_in_another_seller_list`

**Шаги:**
1. Создать объявление для `seller_a`, сохранить `id_a`.
2. GET `/api/1/{seller_b}/item` (другой продавец).
3. Проверить что `id_a` отсутствует в ответе.

**Ожидаемый результат:** объявление `seller_a` не появляется в выдаче `seller_b`.

**Постусловие:** DELETE `/api/2/item/{id_a}`.

---

## GET /api/1/statistic/:id и /api/2/statistic/:id

### TC-027 — статистика по существующему объявлению v1

**Severity:** Blocker | **Функция:** `test_get_statistic`

**Предусловие:** объявление создано фикстурой `create_and_delete_item`.

**Шаги:**
1. GET `/api/1/statistic/{id}`.
2. Проверить статус и тело ответа.
3. Сверить `likes`, `viewCount`, `contacts` с данными из фикстуры.

**Ожидаемый результат:** `200 OK`, непустой массив, значения совпадают с переданными при создании.

**Постусловие:** фикстура удаляет объявление автоматически.

---

### TC-028 — статистика по существующему объявлению v2

**Severity:** Blocker | **Функция:** `test_get_statistic_v2`

**Предусловие:** объявление создано фикстурой `create_and_delete_item`.

**Шаги:**
1. GET `/api/2/statistic/{id}`.
2. Проверить статус и тело ответа.
3. Сверить `likes`, `viewCount`, `contacts` с данными из фикстуры.

**Ожидаемый результат:** `200 OK`, значения совпадают с переданными при создании.

**Постусловие:** фикстура удаляет объявление автоматически.

---

### TC-029 — данные v1 и v2 совпадают

**Severity:** Major | **Функция:** `test_compare_statistic_v1_v2`

**Предусловие:** объявление создано фикстурой `create_and_delete_item`.

**Шаги:**
1. GET `/api/1/statistic/{id}` → `response_v1`.
2. GET `/api/2/statistic/{id}` → `response_v2`.
3. Сравнить `likes`, `viewCount`, `contacts` между v1 и v2.

**Ожидаемый результат:** оба вернули `200 OK`, значения идентичны.

**Постусловие:** фикстура удаляет объявление автоматически.

---

### TC-030 — статистика по несуществующему id v1

**Severity:** Major | **Функция:** `test_get_statistic_non_existent_id_v1`

**Шаги:**
1. GET `/api/1/statistic/00000000-0000-0000-0000-000000000000`.
2. Проверить статус ответа.

**Ожидаемый результат:** `404 Not Found`.

---

### TC-031 — статистика по несуществующему id v2

**Severity:** Major | **Функция:** `test_get_statistic_non_existent_id_v2`

**Шаги:**
1. GET `/api/2/statistic/00000000-0000-0000-0000-000000000000`.
2. Проверить статус ответа.

**Ожидаемый результат:** `404 Not Found`.

---

## Нефункциональные проверки

### TC-032 — Content-Type в ответе

**Severity:** Minor | **Функция:** `test_content_type_header`

**Предусловие:** объявление создано фикстурой `create_and_delete_item`.

**Шаги:**
1. GET `/api/1/item/{id}`.
2. Проверить заголовок `Content-Type`.

**Ожидаемый результат:** `Content-Type: application/json`.

---

### TC-033 — время ответа POST /api/1/item

**Severity:** Major | **Функция:** `test_post_response_item`

**Шаги:**
1. Замерить время выполнения POST `/api/1/item` с валидным телом.

**Ожидаемый результат:** ответ приходит быстрее 2000 мс.

**Постусловие:** DELETE `/api/2/item/{id}` если получен 200.

---

### TC-034 — время ответа GET /api/1/item/:id

**Severity:** Minor | **Функция:** `test_get_response_time`

**Предусловие:** объявление создано фикстурой `create_and_delete_item`.

**Шаги:**
1. Замерить время выполнения GET `/api/1/item/{id}`.

**Ожидаемый результат:** ответ приходит быстрее 2000 мс.

---

## E2E

### TC-E01 — полный жизненный цикл объявления

**Severity:** Blocker | **Функция:** `test_full_item_lifecycle`

**Шаги:**
1. POST `/api/1/item` с валидным телом → сохранить `item_id`.
2. GET `/api/1/item/{item_id}` → проверить что поля `id`, `name`, `price`, `sellerId` совпадают с созданными.
3. GET `/api/1/statistic/{item_id}` → проверить `likes`, `viewCount`, `contacts`.
4. Проверить что статистика из `/item/{id}` и `/statistic/{id}` совпадает между собой.

**Ожидаемый результат:** все три запроса вернули `200 OK`, данные консистентны на всех ручках.

**Постусловие:** DELETE `/api/2/item/{item_id}`.