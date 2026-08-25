# 0028. Интегрированная реализация удовлетворяет `blocked by` до terminal acceptance

Статус: accepted, 2026-08-25.

## Контекст

Task Manager хранит structural dependency между Tasks, а lifecycle отдельно
показывает состояние реализации и приёмки. Если ShipTask считает `blocked by`
снятым только после `Done` блокирующей Task, временно недоступная проверка
upstream-результата искусственно останавливает downstream-работу, хотя нужная
реализация уже доступна в общем integration candidate.

Такое смешение превращает acceptance одной Task в глобальный scheduler gate,
сужает runnable frontier и заставляет ждать lifecycle-церемонию вместо
продолжения полезной реализации. При этом простой перевод upstream Task в
`Done` без её собственной проверки был бы неправдивым.

## Решение

- Разделить structural relation, implementation readiness и terminal
  acceptance.
- Считать dependency gate открытым, когда изменение blocking Task влито в exact
  общий integration candidate, связано с этой Task и предоставляет контракт,
  необходимый dependent Task.
- Не требовать terminal status blocking Task. Pending verification или effect
  сохраняет её в правдивом `In Progress`/`In Review`, но не удерживает dependent
  Tasks вне runnable frontier.
- Сохранять `blocked by` relation как provenance; открытый gate не означает
  acceptance upstream Task или готовность Release/Goal.
- Повторно закрывать gate только по свежему attributed evidence, что дефект или
  изменение upstream действительно нарушает используемый downstream contract.
  Rework и invalidation ограничиваются доказанно затронутыми Tasks/evidence.

## Наблюдаемое поведение

- Код blocking Task только в отдельной branch/worktree не разблокирует dependent
  Task.
- Тот же код после подтверждённого fan-in в integration target разблокирует
  dependent Task, даже если blocking Task остаётся non-terminal из-за
  `verification-blocked`.
- Dependent Task может достичь `Done` по собственному evidence, пока blocking
  Task честно остаётся в `In Review`.
- Unattributed batch failure или отсутствие одной upstream-проверки не закрывают
  уже открытый gate.
- Поздний attributed defect upstream возвращает только затронутые downstream
  Tasks к повторной проверке или rework.

## Последствия

Планировщик использует dependency-ready frontier по exact integrated candidate,
а не вычисляет его из `status == Done`. Координатор хранит Task-to-candidate и
contract attribution, поэтому поздний upstream defect можно локализовать без
массового отката. Lifecycle и release acceptance остаются правдивыми: ускорение
downstream-работы не ослабляет критерии самой blocking Task и всего Release.
