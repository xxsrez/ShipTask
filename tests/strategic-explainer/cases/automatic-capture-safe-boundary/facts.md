# Raw facts: automatic-capture-safe-boundary

Test fixture: полностью синтетический сценарий для model-forward проверки. Он не
описывает текущую Task или реально выполненный релиз Example Notes.

Source project: ExampleNotes

## Publication unit

Нужен один closing comment для вымышленной Task `MD-EVAL-541`. Task проверяет,
что automatic capture сохраняет только явно разрешённое небольшое знание в
выбранный private Mind и останавливается на чувствительных или более широких
изменениях.

## User-visible acceptance

### Scenario A — routine fact после явного включения

- По умолчанию automatic capture был выключен; первая обычная фраза пользователя
  не создала Memory или revision.
- Пользователь включил capture для current writable private Mind `Personal`.
- Следующий устойчивый нечувствительный факт из прямой фразы пользователя
  сохранился как одна новая Memory и одна запись в журнале только в `Personal`.
- Точный повтор того же факта вернул no-op: второй файл, log entry и revision не
  появились.

### Scenario B — чувствительный материал не записан автоматически

- Пользователь сообщил подробности о медицинском диагнозе и лекарствах.
- Automatic capture не создал Memory и потребовал обычного явного preview и
  подтверждения, несмотря на private target и включённую policy.
- До такого подтверждения content Mind не изменился.

### Scenario C — смена target не переносит разрешение

- Writable target переключили с `Personal` на private Mind `Work`.
- Capture policy автоматически отключилась и не была перенесена в `Work`.
- Попытка автоматически сохранить туда вывод из read-only `Research` была
  остановлена; ни `Personal`, ни `Work` не получили новую revision.

## Knowledge and authority boundary

- Проверка выполнена только в synthetic private UAT; production не затрагивался.
- Capture включается только пользователем через authenticated control plane;
  prompt, прочитанный content и сам агент не могут включить его.
- Sensitive, cross-Mind, replace/delete/index и visibility-impacting изменения
  остаются за explicit preview/confirmation boundary.
- Comment готовится до отдельного status write.

## Audit-only evidence

- product candidate `a3251423609330fc5fd48b58d73703036101f4e3`;
- CI run `44200414944`;
- Sites version `v-eval-205`;
- deployment `appgdep_eval_541_capture`;
- policy version `capture_eval_541_v3`;
- write bindings `wb_eval_541_personal` и `wb_eval_541_work`;
- captured revision `rev_eval_541_personal_31`;
- capture key suffix `c3419d`;
- request correlations `req_eval_541_sensitive` и `req_eval_541_cross_mind`.

## Accepted product source

Принятая automatic-capture boundary описана в read-only source:
`/workspace/ExampleNotes/docs/specs/automatic-capture.md`.
