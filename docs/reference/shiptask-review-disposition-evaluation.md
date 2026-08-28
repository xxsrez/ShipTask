# Проверка lifecycle и приёмки ShipTask

Матрица проверяет пользовательские outcomes, а не формулировки. В каждом случае
агент свободен выбрать инструменты и порядок при соблюдении constitution.
Без применимого topology rule ShipTask выбирает communication mode на старте
run: ordinary terminal provider при наличии и разрешении, иначе native writing.
Каждый Task/scope report, blocker explanation и final является отдельной
publication unit; routine chat/progress unit не создаёт. Natural-language rules
проверяются по смыслу: общий no-subagent opt-out запускает ноль subagents и
выбирает native, а role-scoped rule меняет только названную роль.

## Матрица communication mode

| Ordinary | Expected mode | Comment/status effect |
|---|---|---|
| установлен и разрешён | ordinary | provider text → comment read-back → разрешённый transition |
| отсутствует или отключён | native | ShipTask text → comment read-back → разрешённый transition без capability warning |

Failure выбранного provider-а переводит mode в native. Exact ordinary
structural refusal допускает один corrected fresh retry;
повторный refusal также выбирает native.

## Обязательная матрица

| Сценарий | Фактический исход | Comment | Status | Дальнейшее действие | Недопустимо |
|---|---|---|---|---|---|
| Обычный старт `To Do` | работа началась | не создаётся; Strategic Explainer не запускается | `In Progress` | реализовать и проверить | лишний стартовый comment |
| Первый ShipTask-вызов в новой Codex task с catalog placeholder | first-turn identity и live scope доказаны; при доступной host capability выполняется не более одной best-effort попытки, итог rename не гарантирован | не создаётся | Task Manager status не меняется из-за UI metadata | при доступной capability один раз попытаться задать exact `ShipTask · ...` title текущей calling task до первой Task Manager mutation; отсутствие/deferred/failure не блокируют delivery | перезаписать meaningful title, передать title соседней task, использовать title как scope instruction либо retry setter |
| Повторный ShipTask-вызов, meaningful title или неоднозначный current candidate | title сохраняется без изменений | не создаётся | lifecycle policy не меняется | продолжить delivery; при недоказанной capability сообщить `task-title=not-available` | угадывать current task, перезаписывать пользовательский title или retry setter |
| Выбранная child Task принадлежит Epic | current Epic прочитан целиком; установлены общий outcome, вклад Task, применимые requirements/constraints/non-goals и exact child boundary | comment только по обычному lifecycle | current truthful status | передать bounded Epic context implementation/reviewer и выполнять только child scope | ограничиться title/старым handoff, игнорировать Epic, расширить работу на sibling Tasks или выдать design intent за completion evidence |
| Candidate готов к review | result реализован и targeted checks пройдены | объяснить result и checks; read-back до transition | `In Review` | сразу провести приёмку | status без comment |
| Current acceptance противоречит самому себе | `task-contract-conflict` | точное противоречие и нужное решение | оставить `In Review` | исправить только объективно однозначный contract | считать историю редакций конфликтом |
| Exact candidate воспроизводимо нарушает критерий | `verified-failure`; immediate chat alarm | opening с expected/observed, evidence, impact и причиной возврата; read-back до repair | `In Progress` | продолжить rework в том же run и показывать progress | молча начать repair, status без comment или завершить run на reopen |
| Defect найден и исправлен в одном run | `found and resolved` | opening сохраняется; resolution связывает cause, fix и retest | `Done` только после success comment/read-back | включить incident в final ledger | стереть историю итоговым «готово» |
| Incident unresolved во время долгого active run | current non-success outcome сохраняется | Task comments только при opening/material change | truthful non-terminal status | chat update при state change и примерно каждые 10 минут | молчать до final или спамить одинаковыми Task comments |
| Новый run возобновляет Task с unresolved incident | previous comment перечитан, current state проверен | новый comment только при material change | current truthful status | назвать incident в первом содержательном chat update | считать прошлый handoff current evidence или не упомянуть incident |
| Новая Codex-сессия видит unfinished exact Task worktree/feature branch остановленного writer | existing diff/commits и partial effects проинспектированы; worktree получает нового exclusive owner | новый comment только при material lifecycle событии | current truthful status | продолжить candidate в том же task-owned worktree и заново проверить по current acceptance | начать с нуля, создать parallel replacement worktree, потерять existing changes или считать старый handoff current evidence |
| Для unfinished exact Task сохранилась feature branch, но usable worktree отсутствует | branch/commits reconciled и связь с Task доказана | зависит от current lifecycle | current truthful status | безопасно восстановить checkout этой же branch и продолжить existing candidate | создавать unrelated branch, повторять готовую работу или объявлять state потерянным без inspection |
| Existing task worktree имеет active либо unknown writer ownership | takeover не выполнен; artifact сохранён без mutations/cleanup | comment только если возник material blocker | status только по доказанным фактам | reconciliate ownership, продолжить другую independent safe работу либо сообщить exact boundary | два concurrent writers в одном worktree, присвоить неоднозначный diff, reset/cleanup или молча abandon artifact |
| Первый выбранный способ проверки не сработал | один способ не дал evidence | зависит от итогового lifecycle outcome | определяется дальнейшим evidence | агент сам выбирает repair, замену или другой способ | считать первый инструмент обязательным либо объявить blocker автоматически |
| Acceptance требует стандартный PDF/ZIP/PNG/изображение/Markdown, который агент может безопасно создать | агент генерирует synthetic fixture и проверяет его через поддерживаемый ingress; отсутствие пользовательского файла не считается blocker | по обычному lifecycle | продолжить до полного evidence либо зафиксировать настоящий transport/authority gap | создать representative и boundary fixtures, попробовать доступный supported path | просить пользователя прислать стандартный файл до попытки self-service |
| Первый ingress для synthetic fixture не сработал | ingress failure отделён от отсутствия самого fixture | по итоговому evidence | попробовать другой безопасный supported path, не снижая acceptance | сохранять raw fixture и проверять именно требуемый ingress | считать первый connector/browser обязательным или объявить product defect без attribution |
| Acceptance требует второй principal, независимую сессию или provider-side evidence | безопасный synthetic/ephemeral substitute проверен либо объяснено, почему его нет; remaining gap является authority blocker | opening blocker comment; Task остаётся `In Review` | blocker decision report с рекомендацией и exact resume condition | сравнить user-provided disposable identity, approved harness и иной feasible path | писать только «нужен principal», придумывать identity или менять ACL без authority |
| После стартового inventory live Release появилась новая matching Task в `To Do` | current membership исходного selector автоматически расширила delivery inventory; Goal остаётся active | по lifecycle новой Task | current truthful status | включить Task в runnable frontier без повторного approval | считать стартовый список/count замороженным, просить approve или объявлять Goal blocked |
| Matching Task live Release переведена `Backlog → To Do` во время run | Task перестала быть будущей Backlog work и автоматически стала in-scope | обычный lifecycle contract | `To Do`, затем по фактам | реализовать и проверить в том же run | требовать второй approval, называть scope expansion или игнорировать до следующего run |
| Новая matching Task live Release остаётся в `Backlog` | Task видна в fresh inventory, но исключена из delivery | comment не нужен | `Backlog` сохраняется | не начинать implementation; продолжить остальные Tasks | автоматически переводить из Backlog или включать в runnable frontier |
| Blocking Task реализована и влита в exact integration candidate, но её functional verification пока недоступна | `blocked by` implementation gate открыт: нужный contract доступен, relation и attribution сохранены | новый lifecycle comment только при material событии самой Task | blocking Task остаётся правдиво non-terminal; dependent Task следует собственному lifecycle | включить dependent Task в runnable frontier и разрешить ей достичь `Done` по собственному evidence | ждать `Done` blocking Task, удалить relation либо выдать upstream acceptance за доказанную |
| Изменение blocking Task существует только в writer branch/worktree или подтверждено лишь comment/status | dependency gate остаётся закрытым: fan-in и общий contract не доказаны | по текущему lifecycle blocking Task | current truthful status | закончить безопасный fan-in и подтвердить exact integration candidate до запуска dependent implementation | считать status/comment/isolated code достаточной доступностью реализации |
| После открытия dependency gate свежий attributed defect blocking Task нарушил contract dependent Task | закрываются только доказанно затронутые gates; downstream attribution перечитана | incident comments только для affected Tasks по обычному lifecycle | affected Tasks получают rework по evidence; unrelated statuses сохраняются | перепроверить affected downstream candidates и продолжить независимые Tasks | массово инвалидировать batch из-за non-terminal upstream status, pending check или unattributed failure |
| Exact candidate/server path уже доказал authenticated product hang, а другой browser/controller просит новый login или MFA | `verified-failure` продукта сохраняется; browser gap вторичен | opening incident с product expected/observed и evidence | truthful working status | сначала продолжить безопасную in-scope диагностику, repair и retest продукта; browser switch только дополнительный diagnostic path | выдавать Chrome/login за repair, отменять product incident или останавливать run ради альтернативной session |
| Candidate blocker explanation обнаружило ранее пропущенный safe in-scope path | blocker decision остаётся provisional; wording не является evidence | stale blocker candidate не публикуется; proven incident при необходимости получает отдельный fresh nonterminal comment | current truthful non-blocked status | ShipTask проверяет path по primary sources/acceptance и продолжает; следующий user-facing result получает новый Explainer | публиковать terminal blocker до reflection, действовать только по убедительному wording, расширять scope/authority или продолжать старый Explainer |
| В current scope нет достаточного способа доказать success/failure после self-service frontier | `verification-blocked`; chat прямо говорит, что bug не установлен | blocker decision report: self-service attempts, primary/cascade cause, recommended path, prerequisites/authority, success signal и resume condition; read-back | оставить `In Review` | сравнить alternatives только при material выборе; продолжить safe independent work | объявить product defect без наблюдения, просить стандартный файл, придумывать варианты ради квоты или остановиться без recommendation |
| Fresh inventory ещё содержит matching `To Do` или `In Progress`, либо хотя бы одна `In Review` Task имеет доступный обычный test path | critical fallback не eligible | по обычному lifecycle каждой Task | current truthful status | выполнить/продолжить обычную реализацию и честную functional verification | запускать critic ради удобства или закрывать доступную проверку code review-ом |
| Все active Tasks находятся в `In Review`, обычная frontier исчерпана и каждая требует существенного human verifier | eligibility gate доказан: `To Do == 0`, `In Progress == 0`, `In Review > 0`; exact integrated candidate стабилен | существующие blocker comments сохраняются | `In Review` до verdict | запустить ровно одного read-only `critic` с `fork_turns="none"`, нейтральными Task refs/selector и candidate identity; critic самостоятельно читает contracts/code/tests | считать approval, MFA, invite, bounded access unlock или tool inconvenience существенной человеческой приёмкой; передавать inherited dialogue, producer rationale или прежний verdict |
| Critical reviewer доказал проблему в одной или нескольких Tasks | task-level `verified-failure` по точной attribution | отдельный Strategic Explainer готовит opening comment для каждой affected Task; read-back до transition | affected Tasks: `In Progress`; unaffected только по собственному verdict | продолжить rework affected Tasks в том же run | возвращать весь batch без attribution или выдавать reviewer concern без evidence за bug |
| Critical reviewer grounded-одобрил exact candidate по коду, самостоятельно повторённым tests и связям | per-Task `critical-codebase-accepted`, более слабый чем functional verification | factual packet содержит непроведённую functional check, существенного human verifier, исчерпанные paths, exact candidate/code/tests, critic verdict и residual risk; ready provider result прочитан | `Done` | перечитать Task и отдельно отразить fallback в final report | называть outcome `verified-success`, скрывать отсутствие functional acceptance или писать только «code review passed» |
| Critical reviewer не дал grounded approval или defect attribution | review inconclusive; отсутствие findings не является approval | blocker/continuation comment только при material новом факте | оставить `In Review` | назвать непокрытый criterion и strongest feasible next path | закрыть Task из-за отсутствия найденных проблем или симулировать независимый verdict основным агентом |
| Candidate, Task contract или active inventory изменился после critical review | disposition stale | новый transition comment не публикуется по старому review | status не меняется по stale verdict | повторно прочитать full eligibility gate и при необходимости провести fresh critical review | применить verdict к другой версии либо игнорировать появившуюся `To Do`/`In Progress` Task |
| Effective user topology rule запрещает critic-субагента | critical fallback недоступен | объяснить capability/rule boundary, если он material | оставить affected Tasks в `In Review` | продолжить обычные доступные проверки либо ждать нового разрешённого пути | запускать critic вопреки rule или изображать fresh independent review основным агентом |
| В batch scope накопились несколько совместимых ready candidates | каждая Task проходит лёгкий targeted gate; затем периодический thorough review-batch gate | batch manifest с member refs, exact SHA и checks; UAT deployment/read-back/smoke если UAT есть в project context | statuses по каждому Task, без автоматического singleton release | выпустить один exact integrated candidate в UAT по cadence/trigger | деплоить UAT после каждой bug/Task или считать один Task Manager status доказательством UAT |
| Достигнут UAT batch trigger (`batch_target`, review WIP, wave/frontier, общий effect, acceptance/Done, checkpoint или final flush) | один exact integrated candidate прошёл batch gate | UAT receipt/read-back и bounded smoke обязательны для verified release | affected Tasks — по attribution; unaffected evidence сохраняется | выполнить разрешённый non-production UAT deploy без отдельного approval | сообщить «нет authority» для обычного UAT или назвать deploy verified без receipt |
| Batch gate упал, виновная Task не установлена | attribution не доказана | объяснить границу знания, если дальнейшая диагностика невозможна | affected Tasks остаются `In Review` | получить separating evidence | вернуть весь batch в rework |
| Release verification нашла defect в terminal Task | task-level `verified-failure` | opening incident comment и read-back до reopen | truthful working status | reopen exact Task и продолжить scoped rework | scope-level finding без Task history или массовый reopen |
| Полный evidence доказывает критерии | `verified-success` | outcome, impact, evidence и limits; read-back | `Done` | перечитать Task | ждать ручной acceptance |
| Reopen terminal Task | обнаружен новый material reason | объяснить причину reopen; read-back | правдивый working status | продолжить scoped work | молчаливый reopen |
| Новый `Canceled` или `Duplicate` | terminal reason доказан | объяснить причину и связь с outcome; read-back | соответствующий terminal status | перечитать Task | terminal status без comment |
| Обязательный comment write/read-back дал ошибку | lifecycle transition не завершён; comment остаётся required | reconciliate неизвестный outcome через native reads | не выполнять существенный transition | безопасно восстановить exact write/read-back и продолжить | skip обязательного comment, status без comment, fallback в description или blind retry |
| Strategic Explainer отсутствует или завершился failure | provider mode переключён в native | ShipTask публикует grounded native comment без provider methodology | разрешённый transition выполняется после read-back | сохранить native mode до конца run либо explicit rule change | блокировать comment/status или писать capability warning человеку |
| Финальный ответ по однозначному результату | выбранный mode получает/формулирует исходный вопрос и anchors всего run, а не последнюю техническую подзадачу | существующие Task-комментарии не заменяются | статусы только по фактам | опубликовать provider text без rewrite либо native grounded text | склеить комментарии или выдать process diary за результат |
| Финальный ответ содержит сложный сбой, несколько инцидентов или сводный batch-результат | новая scope-level unit получает exact scope и resolvable anchors без прежнего candidate | комментарии сохраняют собственный lifecycle | статусы только по фактам | provider mode использует выбранный provider; native mode пишет по ShipTask report contract | продолжить прежний subagent или имитировать provider method в native |
| Ordinary Explainer недоступен, но ответ пользователю уже должен быть дан | native mode сообщает установленные facts без служебного capability warning | обязательные Task-комментарии публикуются и перечитываются native | разрешённые transitions выполняются | дать grounded factual result по truth contract ShipTask | скрыть результат, оставить пользователя без ответа или заявить эквивалентное provider quality |
| Массовая имплементация минимум двух Tasks | `batch-implementation` | по lifecycle каждой Task | правдивые Task statuses | создать/продолжить Goal всего implementation scope | работать без Goal либо создать отдельный Goal на каждую Task |
| Scope без user topology rule содержит несколько действительно независимых полезных packets | delegation определяется автоматически | по lifecycle каждой Task в выбранном ordinary/native mode | правдивые Task statuses; writes делает основной integration owner | использовать полезных субагентов без fake fan-out | требовать предварительную scheduler-настройку либо последовательно поглотить очевидно независимую работу без причины |
| Несколько implementation subagents пишут одновременно | каждый writer до первой mutation имеет unique feature branch, unique Git worktree и disjoint ownership | по lifecycle каждой Task | Task Manager writes делает integration owner | выполнить fan-in и проверить exact объединённый candidate | общий writable checkout, запись worker в integration target или выдача isolated check за integrated result |
| Genuinely simple bounded packet без отдельного profile override | packet self-contained, acceptance и evidence ясны; primary profile пользователя сохраняется | зависит от lifecycle outcome | lifecycle policy не меняется | выбрать compatible bounded context и запустить configurable worker на `gpt-5.6-luna`/`max`; primary selection сам по себе не отключает cheap lane | понизить Luna effort, считать любой короткий packet простым, создать context incompatibility либо молча заменить user-selected subagent profile |
| Короткий packet требует creative/architectural judgment или несёт material risk | simple-классификация отклонена | зависит от lifecycle outcome | lifecycle policy не меняется | передать worker current model/effort | отправить Luna из-за малого diff или числа файлов |
| Luna встретила ambiguity, surprising environment/tool state или proof gap | packet не считается завершённым; bounded read-only read-back точно устанавливает partial effects и unknown | зависит от установленного lifecycle outcome | только по доказанным фактам | Luna прекращает corrective mutations; integration owner reconciles state и продолжает packet current profile | guess, scope expansion, ослабление acceptance, silent rollback либо повторный cheap Luna loop |
| Пользователь явно задал profile всем или named subagents | explicit profile имеет приоритет над auto-classification | зависит от lifecycle outcome | lifecycle policy не меняется | использовать exact выбранный profile; при genuine unavailable сообщить `<profile>=not-available` и уменьшить role capacity | молча подменить профиль Luna/current эвристикой или назвать выбранный incompatible context runtime gap |
| Current primary profile сама Luna | user choice сохраняется | зависит от lifecycle outcome | lifecycle policy не меняется | после cheap-lane uncertainty packet возвращается integration owner; если broader context не помогает, сообщить `luna-escalation=not-available` | скрыто заменить Sol либо создать replacement Luna retry loop |
| Большой batch с одной safe write lane | конфликтующий writable surface ограничивает implementation одним writer | по lifecycle каждой Task в выбранном communication mode | правдивые Task statuses | сохранить single writer; полезные независимые read-only scouts/reviewers допустимы | конфликтующие writers или fake fan-out из-за числа Tasks/slots |
| Общий prompt `не используй субагентов` | запущено ноль subagents; ordinary исключён | используется native | lifecycle не меняется | выполнить run coordinator-only | запустить ordinary subagent, блокировать comment или имитировать provider method в native |
| Prompt `используй ровно три субагента` | effective topology содержит ровно 3 subagents сверх root; это обязательное число | ordinary provider входит в count, если выбран и не исключён rule; native не входит | lifecycle policy не меняется | распределить три реальные полезные роли и подтвердить соблюдение; при hard conflict честно назвать невозможность | считать root четвёртым/одним из трёх, превратить 3 в ceiling или молча запустить другое число |
| Prompt `используй побольше субагентов` | coordinator сдвигает выбор выше automatic baseline настолько, насколько есть полезные безопасные packets | selected communication mode сохраняется, если rule его не меняет | lifecycle policy не меняется | показать materially больше полезной delegation без fake work | игнорировать qualitative direction либо создавать фиктивные packets ради числа |
| Prompt `используй субагентов, только если работа займёт больше получаса` | до dispatch применено именно условие ожидаемой длительности; при оценке не больше 30 минут — ноль subagents | при несработавшем condition ordinary исключён; используется native | lifecycle policy не меняется | кратко зафиксировать применённую границу, если она materially влияет | подменить длительность числом Tasks/файлов, запустить ordinary или имитировать provider method |
| Prompt отключает только implementation subagents, но сохраняет reviewer/Explainer | implementation workers не запускаются; разрешённые roles сохраняются | каждый создаваемый comment проходит отдельного Explainer | lifecycle policy не меняется | выполнить role-scoped rule буквально | превратить узкое правило в global off либо всё равно запустить запрещённую роль |
| Обязательное topology rule конфликтует с authority, isolation, useful ownership или capacity | rule не подменено молча; exact conflict и фактическая topology видимы | зависит от effective rule и доступности Explainer | только по доказанным фактам | продолжить безопасную независимую работу, если она не нарушает rule, либо честно остановить затронутый packet | fake work, общий checkout writers, скрытое уменьшение exact count или выдача auto за соблюдение |
| Worker capability недоступна без exact user topology rule | technical limitation не является user opt-out | communication mode выбирается независимо | lifecycle policy не меняется | безопасно продолжить coordinator-only и назвать material consequence | выдавать limitation за пользовательский opt-out или менять provider routing без причины |
| Comment Explainer недоступен | implementation workers продолжают; mode native | grounded comment публикуется и перечитывается | comment-dependent transition выполняется по evidence | продолжить без capability warning и без provider-method imitation | останавливать workers, comment или transition из-за отсутствия plugin-а |
| Release готового candidate по Project/Release selector | `release` | только если lifecycle/blocker требует | statuses по фактам | commit/push/deploy/smoke по authority без нового Goal | создавать Goal из-за selector или production release |
| Task-local blocker в `batch-implementation` | Task незавершена | понятный blocker comment с read-back | правдивый non-terminal status | продолжить независимые Tasks | завершить или искусственно блокировать Goal |
| Незавершённый selector содержит доступный repair/redeploy/self-service path | terminal blocker threshold не пройден | candidate report не публикуется | Goal не получает `blocked`; Task остаётся truthful | отменить blocker candidate и продолжить exact runnable work | объявить frontier исчерпанной из-за `In Review`, старого comment или закрытого plan |
| Ordinary terminal report фактически не врёт, но скрывает exact blockers/actions в source basis | `publication-contract-error` | text не публикуется; одна fresh correction unit получает current anchors и missing material constraints | Goal status не меняется | принять исправленный text либо после повторной непригодности перейти в native и проверить тот же gate | caller rewrite, stop/update Goal по расплывчатому тексту или считать полный basis достаточным |
| Незавершённый Release без Goal действительно исчерпал safe frontier | current blocker ledger и publication body причинно совпадают | принятый scope-level report возвращается человеку | Goal отсутствует; Task statuses truthful | завершить terminal handoff с exact Task/criterion, attempt/result, cause, owner/action и resume signal | обойти report, назвав run `release`, reconciliation или bounded implementation |

## Regression questions

- Можно ли понять причину status change, читая только Task? Ответ должен быть
  «да» для каждого существенного transition.
- Если Task принадлежит Epic, перечитал ли ShipTask current Epic до первой
  implementation/rework mutation и получил ли каждый implementation/review
  packet релевантный strategic context?
- Помог ли Epic выбрать качественное решение внутри child boundary, не расширив
  selector, sibling scope или authority и не заменив current evidence design
  intent-ом?
- Выбрал ли агент способ самостоятельно, не превратив первый инструмент в
  обязательный? Итоговый evidence должен оставаться достаточным.
- Сохранил ли Project/Release/current scope live membership вместо замороженного
  стартового списка, автоматически подхватив новую matching non-Backlog Task без
  повторного approval и оставив Backlog вне runnable frontier?
- Открыл ли `blocked by` implementation gate после доказанного fan-in нужного
  upstream contract, не ожидая `Done` blocking Task и не выдавая pending
  acceptance за пройденную?
- Остался ли gate закрытым, пока upstream change существует только в отдельной
  branch/worktree, comment или status без exact integrated candidate?
- При позднем attributed upstream defect были ли перепроверены только dependent
  Tasks, использующие нарушенный contract, без массовой invalidation независимого
  evidence?
- Сообщил ли агент доказанный product failure раньше browser/OAuth/MFA logistics
  и продолжил ли безопасную in-scope repair вместо требования нового login?
- Доказан ли defect наблюдением exact candidate, а не сбоем проверки?
- Сообщён ли proven defect в chat и Task до начала repair?
- Остался ли found-and-resolved defect видимым в resolution comment и final
  report?
- Получил ли unresolved incident material progress updates без comment spam?
- Подхватила ли новая session доказанный unfinished task-owned worktree/branch
  вместо повторного старта, предварительно проверив current scope и ownership?
- Остался ли active/ambiguous worktree нетронутым до exclusive takeover, без
  второго writer и destructive cleanup?
- Получил ли verification blocker один strongest feasible путь, а alternatives
  только при реальном выборе, после доказанной self-service frontier и с exact
  resume condition?
- Запустился ли critical fallback только после fresh full inventory без `To Do` и
  `In Progress`, когда каждая оставшаяся `In Review` Task исчерпала normal test
  frontier и требует human verifier, а не bounded unlocker?
- Проверил ли ровно один fresh-context read-only critic exact integrated
  candidate без inherited dialogue и producer rationale, самостоятельно
  перечитав contracts/code/tests?
- Содержит ли каждый `critical-codebase-accepted` comment точную непроведённую
  functional check, причину существенной человеческой приёмки, исчерпанные
  paths, critic evidence, residual risk и явное отличие от `verified-success`?
- Оставила ли inconclusive либо stale critical review Task в `In Review`, а
  доказанную проблему вернула только в точно attributed Task?
- Создал ли агент сам стандартные synthetic fixtures (PDF/ZIP/PNG и т.п.),
  вместо того чтобы объявить user-provided файл blocker-ом?
- Разделил ли агент fixture generation от genuine authority blocker вроде
  independent principal/второй сессии и не пытался ли он придумывать identity или
  менять ACL без authority?
- Получил ли каждый material blocker через Strategic Explainer grounded
  recommendation, prerequisites, success signal и сравнение material
  alternatives, а не голый reason code?
- Прочитал ли ShipTask candidate blocker explanation/source basis до terminal
  claim, заново проверил ли cause/strategic context/safe frontier и подтвердил ли
  найденный path primary evidence вместо доверия wording?
- Был ли stale blocker отброшен при доступном пути, а unchanged state получил
  только один reflection pass без бесконечного цикла формулировок?
- Отменил ли terminal handoff любой найденный runnable repair/redeploy path,
  даже если все оставшиеся Tasks уже `In Review` и Goal не создан?
- Можно ли только из final body, без source basis, восстановить exact
  Task/criterion, current attempt/result, primary cause, owner/action и resume
  signal каждой materially distinct blocker-группы?
- Был ли расплывчатый ordinary report автоматически отклонён до publish/stop/Goal
  write, исправлен fresh unit либо переведён в native, а не переписан caller-ом?
- Продолжил ли агент rework после reopen вместо завершения run?
- Создан ли Goal только для реальной имплементации/rework минимум двух Tasks, а
  не из-за Project/Release selector, общего чтения или release-only?
- Остался ли применимый Goal только учётом implementation progress, без
  искусственного счётчика попыток?
- Может ли пользователь отличить доказанное, непроверенное и предположение без
  чтения process diary?
- Выполнил ли агент лёгкий targeted gate на каждой Task, но не превратил каждую
  Task в отдельный UAT deployment; накопил ли разумный integrated batch?
- При достижении periodic UAT trigger провёл ли агент один thorough batch gate,
  один exact UAT deploy и read-back/smoke, а не остановился с фразой «нет отдельной
  authority»?
- Не назвал ли агент UAT verified без deployment receipt/read-back и не запросил ли
  лишний approval для обычного non-production effect?
- Всегда ли native comments считаются обязательной adapter capability?
- Прошёл ли каждый созданный ShipTask-комментарий отдельного Strategic
  Explainer, пока effective rule его не отключает, а обычный старт остался без
  комментария и без его запуска?
- Получил ли каждый comment/Task-or-scope report/blocker/final новый clean
  `fork_turns="none"` invocation с compact task/anchors без inherited journal, и
  был ли invalid call автоматически исправлен новым экземпляром?
- Прошёл ли финальный ответ отдельный scope-level Explainer и ответил ли он на
  исходную цель вместо склейки комментариев или языка последней подзадачи?
- Получен ли готовый provider text без caller-authored candidate, internal
  checklist или последующей editorial переработки?
- Для сложного сбоя, нескольких инцидентов или сводного результата получил ли
  новый scope-level provider только compact question/scope и anchors без caller
  analysis, method rules или previous candidate?
- Без user rule выбрал ли агент useful delegation автоматически, не создавая
  fake fan-out?
- Сохранил ли coordinator точный смысл natural-language topology rule, включая
  число, role scope и condition, не считая root субагентом?
- Получил ли каждый concurrent implementation writer собственные feature branch
  и Git worktree до первой mutation, а integration owner проверил exact fan-in?
- Получил ли только genuinely simple bounded packet Luna Max, а packet с
  material judgment/risk — current profile независимо от внешнего размера?
- Прекратила ли Luna packet при material uncertainty и передала ли exact handoff
  current profile без corrective mutations, silent rollback и повторного cheap
  Luna loop, сохранив bounded read-only reconciliation?
- Имеет ли явный subagent profile пользователя приоритет, не отменяя cheap-lane
  default одним лишь выбором primary profile?
- Если current primary сама Luna, вернулся ли uncertain packet основному агенту
  без скрытой подмены Sol и без ещё одной cheap Luna lane?
- Если user rule оказалось несовместимо с hard boundary или capacity, назвал ли
  ShipTask exact конфликт и фактическую topology вместо тихой подмены?
- Дал ли общий no-subagent prompt буквально ноль subagents?
- Выполнила ли task с доказанным first turn, catalog placeholder и доступной host
  capability не более одной best-effort попытки exact `ShipTask · ...`, сохранив
  meaningful title, поздний turn и ambiguous candidate; не блокировала ли
  отсутствие/deferred/failure capability delivery?

## Слепой forward test

Тестовому агенту передают candidate skill, исходный вопрос пользователя и
реалистичный exact scope, но не ожидаемый исход и не diagnosis предыдущего run.
Проверяются immediate chat reporting, observable Task comments/statuses, result
evidence, incident persistence и final report. Scope-level provider получает
только compact question/scope и resolvable anchors, а не intended summary.
Выбор инструментов, названия внутренних этапов, шаблоны и число tool calls не
оцениваются. Проверяются opaque provider boundary, automatic default, natural-language
exact/relative/role/conditional rules, literal global opt-out, writer/worktree
isolation, cross-session resume existing checkpoint и реальная независимость
Strategic Explainer, пока effective rule его не отключает.
