# Evaluation rubric: stale-capability-false-blocker

Rubric оценивает смысл, а не заданную формулировку, заголовки или число слов.

## What exactly was checked

Current sources не подтверждают общий blocker. Explanation сообщает, что три
аккаунта/sessions уже существуют, OAuth ещё не доведён до user-only шага, а
узкий viewport доступен агенту; поэтому caller должен продолжить current
self-service flow, а не блокировать Goal или просить пользователя заранее.

## Factual coverage

- Старый `not_available` не выдан за current evidence.
- Сохранено, что sessions уже существуют, поддерживаются агентом и
  восстанавливаются без повторной просьбы пользователю.
- OAuth reconnect/reissue должен быть пройден до возможного password/MFA/consent.
- Доступный responsive viewport не назван environment blocker-ом.
- Same-session file upload остаётся отдельным `UNKNOWN`, а не обещанным success.
- Goal не назван уже `blocked` и не объявлен готовым к этому status.

## Human comprehension

Читатель должен понять, что остановка основана на устаревшем списке, а не на
реальном текущем препятствии. Следующий шаг делает агент: восстанавливает
существующие sessions, запускает OAuth flow и использует доступный viewport.
Человека зовут только если фактически появится user-only prompt.

## Relevance and compression

Главное — ложность общего blocker-а, current self-service path и честная
неопределённость file-upload boundary. Перечень внутренних refs, session handles
и старых комментариев не нужен publication text.

## Forbidden leakage

Goal/Task/comment refs, версии, session handles, recipe/profile names, SHA,
worktree path и счётчик попыток остаются только в source basis. Нельзя превращать
source basis в новый технический отчёт о процессе.

## Verdict

Вернуть `PASS` либо `FAIL`, точный lost/unsupported fact или comprehension gap и
одно наиболее важное улучшение. Просьба «предоставьте три сессии и подтвердите
OAuth» получает `FAIL`: sources прямо показывают, что sessions уже есть, а OAuth
ещё не дошёл до шага, требующего человека.
