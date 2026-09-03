# Raw facts: simple-answer-no-visual-overkill

Source project: General

Test fixture: полностью синтетический сценарий для model-forward проверки. Он не
описывает текущую Task или реально выпущенную функцию какого-либо проекта.

## Publication unit

Нужен прямой ответ пользователю на вопрос: «Теперь я могу прикреплять PDF?»
Читатель не просил технический доказательный след или разбор устройства.

## User-visible acceptance

### Scenario A — обычный PDF

- PDF размером 4 МБ прикреплён, повторно открыт и скачан без изменения имени.
- После обновления страницы вложение осталось доступно.

### Scenario B — крупный PDF

- Файлы больше 10 МБ в этой проверке не использовались.
- Текущая проверка не доказывает поведение для таких файлов.

## Knowledge and authority boundary

- Можно подтвердить возможность только в проверенной границе до 10 МБ.
- Нельзя утверждать, что любой PDF уже поддерживается.
- Действие пользователя не требуется.

## Audit-only evidence

- fixture path `/tmp/eval/brief.pdf`;
- run id `run-eval-simple-419`;
- command `python3 tests/upload_pdf.py`.

## Accepted product source

Для этого полностью синтетического case разделы `User-visible acceptance` и
`Knowledge and authority boundary` являются полным authoritative основанием.
Других принятых продуктовых утверждений нет.
