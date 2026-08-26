# Raw facts: redeploy-persistence-failure

Test fixture: полностью синтетический сценарий для model-forward проверки. Он не
описывает текущую Task или реально выполненный релиз Example Notes.

Source project: ExampleNotes

## Publication unit

Нужен один rework comment для вымышленной Task `MD-EVAL-421`. Task проверяет,
что файлы остаются доступными после повторной публикации UAT candidate. Она пока
находится в `In Review`; после comment должна вернуться в `In Progress`.

## User-visible acceptance

### Scenario A — изображение

- JPEG размером 40 МиБ загрузился, сохранился и открылся в preview.
- После повторной публикации UAT candidate изображение осталось доступно для
  preview и download.

### Scenario B — большой документ

- PDF размером 250 МиБ до повторной публикации загрузился, сохранился и
  скачался byte-identical.
- После повторной публикации запись о PDF осталась в списке файлов, но download
  вернул `404`, а deterministic export не включил PDF bytes.
- Повторная попытка дала тот же результат.
- Это нарушает исходную цель Task: большой файл нельзя считать надёжно
  сохранённым.

## Knowledge and authority boundary

- CI, manifest validation и local tests зелёные, но они не опровергают
  наблюдаемый UAT regression.
- Причина потери PDF bytes пока не установлена.
- JPEG path продолжает работать; его результат нельзя объявлять сломанным из-за
  отдельного PDF failure.
- Без исправления persistence и повторной проверки Task не готова к закрытию.
- Пользовательское действие не требуется; repair принадлежит команде продукта.
- Production не затрагивался.

## Audit-only evidence

- product candidate `4a38ab5386a5be3d4390c68bf4a5e579ca09f285`;
- CI run `44198272477`;
- Sites versions `v-eval-106` и `v-eval-107`;
- deployments `appgdep_eval_421_before` и `appgdep_eval_421_after`;
- revision `rev_eval_421_13`, parent `rev_eval_421_12`;
- JPEG digest suffix `1caa73`;
- PDF digest suffix `2f0e19`;
- observed request correlation `req_eval_421_pdf_download_02`.

## Accepted product source

Требование сохранять exact bytes при download/export описано в read-only source:
`/workspace/ExampleNotes/docs/specs/bundle-files.md`.
