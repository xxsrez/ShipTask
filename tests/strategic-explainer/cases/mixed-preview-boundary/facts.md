# Raw facts: mixed-preview-boundary

Test fixture: полностью синтетический сценарий для model-forward проверки. Он не
описывает текущую Task или реально выполненный релиз Example Notes.

Source project: ExampleNotes

## Publication unit

Нужен один closing comment перед переводом вымышленной Task `MD-EVAL-411` из
`In Review` в `Done`. Цель Task — проверить, что Example Notes безопасно показывает
поддерживаемое изображение, но не пытается открыть архив как содержимое страницы.

## User-visible acceptance

### Scenario A — безопасное изображение

- PNG размером 12 МиБ загрузился в private Mind.
- После сохранения изображение открылось во встроенном preview.
- Его также удалось скачать; downloaded bytes совпали с исходными.
- После повторной публикации UAT candidate preview и download продолжили
  работать.

### Scenario B — архив

- ZIP размером 30 МиБ загрузился и сохранился в том же private Mind.
- Вместо preview интерфейс показал обычное сообщение: «Предпросмотр для этого
  типа файла недоступен. Файл можно скачать».
- ZIP скачался byte-identical и вошёл в deterministic export.
- Сервис не распаковывал и не исполнял содержимое ZIP. Это ожидаемая защитная
  граница, а не неполная реализация Task.

## Knowledge and authority boundary

- Проверка выполнена только в synthetic private UAT; production не затрагивался.
- Для этих двух форматов других проблем не наблюдалось.
- SVG, HTML, DOCX, audio/video и неизвестные форматы в этом fixture не
  проверялись; нельзя обобщать результат на них.
- Comment готовится до status write; Task ещё находится в `In Review`.

## Audit-only evidence

- product candidate `31f0b7c8f75b9e4ce3130d953593f678f3db4c75`;
- CI run `44198271104`;
- Sites version `v-eval-105`;
- deployment `appgdep_eval_411`;
- revision `rev_eval_411_09`, parent `rev_eval_411_08`;
- PNG digest suffix `69ee2a`;
- ZIP digest suffix `9b31d4`;
- export digest suffix `e17ca0`.

## Accepted product source

Принятая preview/download boundary описана в read-only source:
`/workspace/ExampleNotes/docs/specs/bundle-files.md`.
