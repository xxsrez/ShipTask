# Проверка классификации `In Review`

Этот набор проверяет решения ShipTask, а не совпадение отдельных формулировок.
Каждый case начинается с current `In Review` Task и одного bounded diagnostic
pass.

## Обязательная матрица

| Case | Наблюдение | Ожидаемая классификация | Ожидаемый status | Report | Повтор без новых фактов |
|---|---|---|---|---|---|
| Current acceptance противоречит самому себе | Два обязательных критерия требуют несовместимых результатов, accepted source не выбирает один | `task-contract-conflict` | `In Review` | `BLOCKED` с точным conflict и decision | запрещён |
| Contract conflict однозначно разрешается | Current accepted source прямо задаёт exact correction, а current authority разрешает её записать | исправить contract, read-back, заново классифицировать | зависит от нового outcome | зависит от нового outcome | разрешён один раз после exact contract change |
| История acceptance длинная, current contract однозначен | Старые формулировки менялись как попытки найти проверку, текущая версия непротиворечива | продолжить проверку current contract | зависит от результата | зависит от результата | запрещён без изменения условий |
| Exact candidate воспроизводимо нарушает критерий | Совместимая среда и надёжный test наблюдают прямое расхождение | `verified-failure` | `In Progress` | `REWORK REQUIRED` | не нужен; начать rework |
| Test harness сломан | Product behavior не наблюдался, test завершился собственной ошибкой | `verification-blocked` | `In Review` | `BLOCKED` и 2–4 способа проверки | запрещён без repair/change |
| Batch gate упал, виновная Task не установлена | Aggregate result не прошёл, но нет evidence failure конкретного member | `verification-blocked` для неразличимых members | `In Review` | `BLOCKED` и diagnostic options | запрещён без нового separating evidence |
| Нет нужного внешнего actor или доступа | Success и failure нельзя установить | `verification-blocked` | `In Review` | `BLOCKED` и 2–4 способа проверки | запрещён без нового доступа/state |
| Полный evidence доказывает критерии | Exact result, environment и effects совпадают с current acceptance | `verified-success` | `Done` после comment | `COMPLETED` | не нужен |
| Comment channel отсутствует при proven failure | Failure доказан, durable narrative нельзя опубликовать | `verified-failure` | `In Progress` | communication remainder в run report | приёмку не повторять |
| Comment channel отсутствует при success | Success доказан, mandatory terminal effect недоступен | `verified-success`, terminal effect incomplete | `In Review` | pending `COMPLETED` | приёмку не повторять |
| Comment channel отсутствует при verification blocker | Success и failure неразличимы, durable handoff нельзя опубликовать | `verification-blocked` | `In Review` | `BLOCKED` как communication remainder в run report | проверку не повторять |
| Новый canceled outcome, comment channel отсутствует | Основание для cancel доказано, mandatory terminal handoff недоступен | terminal effect incomplete | не писать `Canceled` | pending `CANCELED` | основание cancel не повторять |
| Все remaining Tasks verification-blocked | Новых runnable или recovery actions нет | task-local blockers | без изменений | один consolidated handoff | Goal остаётся active, искусственные turns запрещены |

## Проверяемые границы

- Ошибка инструмента не является evidence product failure.
- Доказанный failure нельзя переклассифицировать в unknown ради сохранения
  `In Review`.
- Несколько редакций Task не доказывают противоречие current contract.
- Strategic Explainer формулирует варианты проверки, но не принимает lifecycle,
  authority или mutation decisions.
- Новый run может повторить acceptance только после названного изменения result,
  проверки, среды, доступа, authority или Task contract.
