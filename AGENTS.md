# ShipTask repository instructions

Инструкции действуют для всего репозитория.

## Назначение

- Репозиторий является source of truth для Task Manager-only Codex skills
  `$ship-tasks`, `$ship-tasks:task-composer` и общего communication skill
  `$strategic-explainer`.
- Исполнимые skills находятся в sibling-каталогах `ship-tasks/`,
  `task-composer/` и `strategic-explainer/`.
- Документация проекта находится в `docs/`; `docs/README.md` — её
  канонический индекс.
- Основной язык документации — русский. Точные protocol/state/tool names можно
  оставлять на английском.

## Документация как исходный код

Документация является исходным кодом всех трёх skills. Единица source —
отдельный skill: его Requirements и Architecture находятся только в
`docs/skills/<skill>/` и не смешиваются с контрактами соседних skills. Для
каждого source package обязательны три уровня с таким приоритетом:

1. **Level 1 — требования пользователя.**
   `docs/skills/<skill>/requirements.md` хранит полный current-набор
   высокоуровневых требований пользователя только для одного skill. Он задаёт
   обязательный результат, смысл, наблюдаемые признаки и жёсткие
   scope/truth/safety/authority boundaries. Skill не может ослабить, заменить
   или нарушить собственный Level 1 и не наследует скрытые требования из
   Requirements соседнего skill.
2. **Level 2 — архитектура достижения.**
   `docs/skills/<skill>/architecture.md` описывает, как этот skill сейчас
   достигает собственного Level 1. Это agent-owned инерционная память: агент
   может менять её, когда улучшает способ достижения требований, но не может
   через Level 2 переписать смысл Level 1 или выдать выбранный механизм за
   новое требование пользователя. Дополнительные локальные design/reference/
   evaluation документы допустимы, но не создают второй current contract.
3. **Level 3 — runtime skills.**
   `ship-tasks/SKILL.md`, `task-composer/SKILL.md` и runtime package
   `strategic-explainer/` являются компактной исполнимой проекцией Level 1 и
   применимой части Level 2. У Strategic Explainer caller-visible `SKILL.md`
   содержит только router/admission contract, а provider expertise находится в
   reference, который читает лишь admitted fresh subagent. Формулировка и
   структура могут отличаться от документации, но runtime package должен нести
   весь применимый смысл Level 1 без семантических потерь.

При конфликте всегда побеждает Level 1. Level 2 нельзя использовать как
основание удалить, сузить или молча переопределить пользовательское требование.
Level 1 меняется только из явного решения пользователя: редакционная правка
разрешена без повторного согласования лишь когда доказано, что смысл не
изменился. Неясность «это новое требование или изменение способа» не разрешает
тихую реклассификацию: сохраните current Level 1 и явно отделите вопрос от
agent-owned архитектурного решения.

Документы не обязаны повторяться дословно. Обязательна смысловая трасса
`Level 1 requirement → Level 2 design → runtime skill → observable evaluation`.
Validator проверяет наличие и связность этой трассы, но зелёный validator не
заменяет содержательную проверку полноты требований.

Каждый `docs/skills/<skill>/` должен быть самодостаточным source package: если
удалить соответствующий runtime skill и заново смыслово скомпилировать его из
локальных `requirements.md` и `architecture.md`, должен получиться примерно тот
же contract и наблюдаемое поведение. Компиляция стохастическая, поэтому
требуется semantic equivalence, а не дословный output. Cross-skill dependency
фиксируйте как локальный interface в каждом затронутом package, а не общим
смешанным Requirements. Shared ADR/reports могут хранить rationale и историю,
но не добавляют hidden current policy.

Plugin является общим distribution artifact независимых runtime skills. Общие
manifest/install/byte-identity правила остаются repository-level build policy,
но не объединяют Requirements или Architecture разных skills. Каноническая
схема source packages находится в [`docs/skills/README.md`](docs/skills/README.md).

## Границы

- `$ship-tasks` работает только через Task Manager connector. Не добавляйте
  fallback providers, generic task-source abstraction или альтернативный
  tracker workflow.
- `$ship-tasks:task-composer` остаётся Task Manager-only planning workflow: не добавляйте
  delivery, implementation, release, Goal lifecycle, fallback provider или
  право автоматически менять Label taxonomy.
- `$strategic-explainer` остаётся generic: не добавляйте в его runtime contract
  ShipTask, Task Manager, конкретный tracker, project lifecycle или право
  принимать решения/выполнять mutations.
- Requests сформулировать, создать, разложить или положить Task Manager работу
  в backlog направляйте через `$ship-tasks:task-composer`, когда он доступен. Это
  planning-only mutation и не запускает ShipTask delivery. Read/status/audit
  без постановки оставляйте техническому Task Manager adapter.
- Project и Release refs, repository path, branch, deployment provider,
  environment, URL, команды проекта и production policy брать из текущего
  project context, а не зашивать в skill.
- Каждый локальный `architecture.md` описывает один current workflow. Не
  создавайте параллельные поколения или альтернативные Requirements/
  Architecture одного runtime skill.
- Распространяйте все три runtime skills только через отдельный plugin
  `ship-tasks@srez-marketplace`. Task Manager connector устанавливается
  отдельно как adapter-only `task-manager@srez-marketplace`; не помещайте
  ShipTask внутрь его package. Не создавайте и не синхронизируйте
  standalone user-level копии `~/.codex/skills/ship-tasks`,
  `~/.codex/skills/task-composer` и
  `~/.codex/skills/strategic-explainer`.

## Изменения

- Если пользователь меняет обязательный outcome или boundary, сначала обновите
  `docs/skills/<skill>/requirements.md`. Если меняется только способ достижения,
  Level 1 не трогайте и обновите локальный `architecture.md`. После этого
  обновите соответствующий runtime `SKILL.md` и observable evaluation. Не
  начинайте с runtime и не восстанавливайте требования из памяти, старого ADR,
  соседнего skill или реализации, когда local current Level 1 им противоречит.
- Считайте current requirements конституцией для агентов: фиксируйте outcome,
  rationale, observable evidence и authority/safety boundaries, но не
  предписывайте agent topology, tool choreography, число попыток, форму context
  или внутренний reasoning, если только это не является явным требованием
  пользователя. Текущие явные исключения: без user rule ShipTask автоматически
  использует субагентов для действительно независимой полезной работы;
  однозначное правило пользователя свободным языком — exact/relative count,
  role scope, общий или узкий opt-out, duration/complexity condition — имеет
  приоритет и сохраняется по смыслу; root agent не входит в явно названное число
  субагентов; если effective rule не отключает comment Explainer, каждый
  комментарий проходит отдельного независимого Strategic Explainer; каждый
  Strategic Explainer publication unit — comment, Task/scope report, blocker
  explanation или final — получает нового built-in `default` subagent с
  `fork_turns="none"`, одной compact task и resolvable read-only anchors без
  inherited turns/tool transcript/process diary/caller candidate; Explainer до
  discovery проверяет invocation, invalid call получает automatic corrected
  fresh retry, а candidate blocker до публикации становится reflection input
  ShipTask для повторной проверки safe frontier без расширения scope/authority;
  caller знает только opaque client protocol, не читает provider-internal
  contract, не пишет candidate, не передаёт analysis/strategic summary/format
  rules, не применяет provider method при opt-out/unavailability и не
  переписывает ready result; только admitted fresh subagent читает внутренний
  provider reference;
  каждый
  одновременно пишущий implementation
  subagent получает собственные feature branch и Git worktree, не разделяемые с
  другим writer; после interruption или смены сессии доказанно task-owned
  unfinished worktree/branch подхватывается тем же coordinator или новым
  exclusive writer после проверки quiescence, а не дублируется; особо простые bounded packets
  без отдельного user override используют `gpt-5.6-luna`/`max`, остальные
  наследуют current model/effort, а Luna при material uncertainty прекращает
  packet и передаёт его current profile без Luna retry loop; доказанная первая
  Codex task с catalog placeholder при доступной host title capability после live
  scope resolution получает best-effort попытку `ShipTask · ...`, но meaningful
  title, later turn или ambiguous candidate не переименовываются, а
  отсутствие/failure capability не блокируют delivery; обычный переход
  `To Do → In Progress` комментария не создаёт. Точный порядок
  оставляйте только для доказуемого инварианта целостности, безопасности или
  внешнего эффекта.
- Сохраняйте `SKILL.md` компактным и переносите подробные объяснения в
  проектную документацию, а не в runtime context skill.
- Не создавайте пустые каталоги или placeholder-документы.
- Не добавляйте runtime state, secrets, private content или signed URLs в Git.

## Definition of done для изменения skill

Поведенческое или distribution-изменение любого runtime skill не завершено, пока
одновременно не выполнены все три критерия:

1. Exact repository scope закоммичен в этом репозитории.
2. Этот commit запушен в `origin/main`, а local `HEAD` совпадает с
   `origin/main`.
3. Отдельный Marketplace package является единственной runtime-дистрибуцией:
   `Srez Marketplace/plugins/ship-tasks/skills/ship-tasks`,
   `Srez Marketplace/plugins/ship-tasks/skills/task-composer` и
   `Srez Marketplace/plugins/ship-tasks/skills/strategic-explainer`
   byte-identical соответствующим repository sources, а installed cache
   byte-identical marketplace source и отображается installed/enabled. Если
   изменился runtime payload, manifest version или cachebuster обновлён,
   соответствующий marketplace commit запушен в `origin/main`, а plugin переустановлен из
   `ship-tasks@srez-marketplace`. Отдельно установленный
   `task-manager@srez-marketplace` остаётся adapter-only и не содержит
   `skills/ship-tasks`, `skills/task-composer` или
   `skills/strategic-explainer`.

Standalone user-level каталоги `~/.codex/skills/ship-tasks`,
`~/.codex/skills/task-composer` и
`~/.codex/skills/strategic-explainer` должны отсутствовать, а fresh
`skills/list` не должен возвращать отдельные user skills.
Plugin-managed marketplace snapshot и installed cache являются внутренними
копиями одной plugin installation и не удаляются вручную.

Не объявляйте изменение завершённым при частичном выполнении этого списка.
Проверку загрузки нового snapshot выполняйте в новой Codex-сессии; текущая
сессия может сохранять старые skill/tool instructions.

## Проверка перед commit

Перед commit выполните:

```bash
python3 scripts/validate_repo.py
python3 ~/.codex/skills/.system/skill-creator/scripts/quick_validate.py ship-tasks
python3 ~/.codex/skills/.system/skill-creator/scripts/quick_validate.py task-composer
python3 ~/.codex/skills/.system/skill-creator/scripts/quick_validate.py strategic-explainer
ruby ~/.codex/skills/project-docs/scripts/validate_docs.rb . --strict-navigation
git diff --check
```

Если системные skill paths недоступны на другой машине, обязательным остаётся
`python3 scripts/validate_repo.py`; остальные проверки укажите как
неисполненные, а не симулируйте.

## Plan discipline

- Используйте plan только для действительно многошаговой работы.
- Синхронизируйте plan с фактическим выполнением.
- Перед финальным ответом закройте, измените или явно объясните каждый пункт.
- Verification evidence сообщайте отдельно от статуса plan.
