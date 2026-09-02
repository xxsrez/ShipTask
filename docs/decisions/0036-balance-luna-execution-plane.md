# 0036. Luna execution plane для режима «Баланс»

Статус: принято, 2026-09-02.

Уточняет Balance-specific части
[ADR-0025](0025-cost-aware-subagent-profiles.md): после узкого решения
проверяющего профиля отделимое исполнение возвращается Luna, а не остаётся у
дорогого integration owner. Общие user-profile, authority, worktree и
single-effect-owner границы сохраняются.

## Контекст

`Классический` режим доказал способность автономно доводить сложные Release до
результата, но в пользовательском тарифном контексте может за один день
израсходовать почти всю недельную квоту. Luna наблюдаемо расходует примерно в
25 раз меньше этого лимита, поэтому несколько целевых Luna-проходов могут быть
существенно дешевле одного длинного Sol-прохода. Это практическая мотивация, а
не постоянная ценовая константа либо доказательство качества любой Luna-wave.

Первый сравнительный прогон не проверил предполагаемую экономику `Баланса`:
основную содержательную работу продолжали выполнять Sol descendants, Luna была
занята преимущественно публикационным текстом, а отсутствие обязательной связи
между packet, routing receipt и фактическим dispatch позволило режиму формально
продолжиться. Функционально успешный результат поэтому не доказал соблюдение
режима.

Простая замена одного Sol несколькими одинаковыми Luna также недостаточна.
Одинаковые prompts создают коррелированные ошибки, голосование скрывает
конкретные дефекты, а root Sol может потратить прежнюю квоту на пошаговое
управление и чтение полных transcripts дешёвых агентов.

## Решение

`Баланс` использует один дорогой control plane и экономичный execution plane.

Проверяющий профиль:

- один раз строит full-scope strategy, acceptance, risk map и package
  boundaries;
- принимает только неделимые material decisions и integration decisions;
- получает узкие escalation questions, а не весь ordinary packet;
- проводит final review точного интегрированного результата.

Luna Max по умолчанию:

- владеет полным внутренним циклом ограниченного пакета: research,
  implementation, tests, independent critique и rework;
- при доступной nested delegation может использовать одного packet lead,
  который координирует дешёвую проверку и возвращает coordinator-у один
  компактный result; без неё тот же цикл выполняется direct Luna lanes;
- возвращает exact candidate, checks, source anchors, findings, known defects,
  unknowns и один узкий escalation question при необходимости;
- после принятого дорогого решения получает новый bounded contract и продолжает
  отделимое исполнение.

Избыточность адаптивна. Обычный пакет получает одну реализацию и независимую
экономичную проверку, когда она возможна. Несколько кандидатов создаются только
при реальной развилке, слабом oracle, провале прежнего подхода либо высокой
ценности отдельной попытки. Это не голосование: каждый material finding должен
иметь evidence и disposition `исправлено`, `опровергнуто` или `передано на
решение`.

Root/coordinator остаётся единственным владельцем Goal, Task Manager mutations,
fan-in, publication unit и точной интегрированной версии. Packet lead не
создаёт второго effect owner. Reviewer получает compact review packet с
resolvable anchors и raw check evidence, но не обязан читать сырой transcript
всех дешёвых waves.

Bundled routing guard связывает receipt с packet identity и точными dispatch
args, а observed profile либо внешняя recursive telemetry подтверждают
фактический маршрут. Этот guard не перехватывает raw platform spawn: пропуск
его является наблюдаемым protocol violation и делает прогон невалидным
`Балансом`. Физически непропускаемый gate возможен только в platform dispatcher,
который одновременно валидирует и создаёт child.

## Последствия

- Число Luna и общие токены не становятся самостоятельной метрикой успеха.
- Основная экономия возникает не только от дешёвой реализации, но и от дешёвого
  повседневного управления внутри пакета.
- Независимая критика снижает риск коррелированной self-review ошибки, но не
  заменяет final exact-result gate.
- Реальный расход проверяется по полной thread-tree telemetry; один
  стохастический run и account-level quota delta при параллельной активности не
  создают итоговый ranking.
- Luna Max остаётся current economical baseline. Переход на меньший reasoning
  effort требует отдельного изменения Requirements и сопоставимой оценки.

## Проверка

- static contract связывает Requirements, Architecture, runtime mode и
  evaluation cases;
- model-routing receipt содержит packet identity и fingerprint точных dispatch
  args;
- deterministic tests отвергают Sol/GPT-5.4 для Balance packet lead,
  implementation, research, tests, verifier, critic, reducer и rework;
- fresh Balance smoke наблюдает Luna-owned ordinary packet loop до первой
  source mutation, независимую economical verification, compact finding ledger,
  узкий material escalation и повторный Luna dispatch после решения;
- полный повторный benchmark отдельно сравнивает terminal outcome, escaped
  defects, user interruptions, wall time и расход дефицитного профиля с
  `Классическим`.
