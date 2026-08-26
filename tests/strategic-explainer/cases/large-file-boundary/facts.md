# Raw facts: large-file-boundary

Test fixture: полностью синтетический сценарий для model-forward проверки. Он не
описывает текущую Task или реально выполненный релиз Example Notes.

Source project: ExampleNotes

## Publication unit

Нужен один closing comment перед переводом вымышленной Task `MD-EVAL-401` из
`In Review` в `Done`. Цель Task — подтвердить, что человек может сохранить в
private Mind большой локальный файл, получить его обратно и увидеть понятное
ограничение по размеру. Закрытие Task разблокирует вымышленную `MD-EVAL-402`.

## User-visible acceptance

### Scenario A — файл внутри лимита

- Через установленный локальный помощник выбран PDF размером 262,144,000 bytes
  (250 МиБ).
- Файл загрузился в private Mind, сохранился в новой revision и появился в
  списке файлов под исходным именем `field-notes.pdf`.
- Скачанный файл byte-identical исходному.
- Deterministic export этого Mind содержит тот же файл с теми же bytes.
- После повторной публикации того же UAT candidate файл остался доступен для
  скачивания.

### Scenario B — файл выше лимита

- Через тот же пользовательский путь выбран PDF размером 268,435,457 bytes:
  на один byte больше принятого лимита 256 МиБ.
- Приложение отклонило файл до commit и показало: «Файл слишком большой.
  Максимальный размер — 256 МБ».
- Новая revision не появилась, ранее сохранённый `field-notes.pdf` не изменился.
- Это ожидаемая product boundary, а не найденный defect.

## Knowledge and authority boundary

- Проверка выполнена только в synthetic private UAT; production не затрагивался.
- Выбор файла с локального диска требует установленного локального помощника.
- Других проблем в этих двух сценариях не наблюдалось.
- Comment готовится до status write; Task ещё находится в `In Review`.

## Audit-only evidence

Эти значения нужны для проверяемости fixture, но сами по себе не объясняют
результат человеку:

- product candidate `7e4a2c9d6a3851f7e9cb2eef1a59b3e58d944f26`;
- companion candidate `2e91fa5c1dd8ef88e12698d7ad7cabf559f34841`;
- CI run `44198270031`;
- Sites version `v-eval-104`;
- deployments `appgdep_eval_401_primary` и `appgdep_eval_401_mirror`;
- revision `rev_eval_401_17`, parent `rev_eval_401_16`;
- manifest digest suffix `51d9c3`;
- file digest suffix `ab82f0`.

## Accepted product source

Принятая граница и поведение download/export описаны в read-only source:
`/workspace/ExampleNotes/docs/specs/bundle-files.md`.
