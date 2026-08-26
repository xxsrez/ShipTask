# Evaluation rubric: ownership-transfer-one-owner

Rubric оценивает смысл, а не заданную формулировку, заголовки или число слов.

## What exactly was checked

Publication text должен различать:

- успешную атомарную передачу действующему Editor: новый единственный Owner и
  прежний Owner как Admin;
- отказ для pending invite и обычной role mutation без изменения существующих
  ролей и без второго владельца.

`FAIL`, если текст говорит лишь «ownership transfer работает» или не объясняет,
что случилось с прежним владельцем и почему приглашённый ещё не подходит.

Проверяемая ловушка: перечислить роли и permissions, но не назвать единственного
нового владельца, новую роль прежнего владельца и атомарный отказ для
неподходящей цели.

## Factual coverage

- Мария не объявлена вторым Owner рядом с прежним: после transfer Owner один.
- Прежний Owner не удалён из Mind и не лишён всего доступа; он стал Admin.
- Pending invitation не представлено как active membership.
- Отклонённые операции не изменили роли, content или history.
- Personal Mind и production не объявлены частью успешного сценария.

## Human comprehension

Читатель должен понять защищаемый инвариант обычными словами: владение переходит
одним целым действием к уже присоединившемуся человеку, а приглашение без
принятия и обычное назначение роли не могут создать второго владельца. Metadata
version, transaction и capability names не должны заменять этот смысл.

## Relevance and compression

Каждая фраза меняет понимание результата transfer, ролей, отказа или границы.
Полная таблица permissions и internal state machine считаются лишними, если они
не помогают ответить, кто теперь владелец и что сохранилось. Английские названия
ролей допустимы как точные product terms, но русский несёт основную мысль.

## Forbidden leakage

SHA, CI run, deployment, metadata versions, membership/invitation IDs и request
correlations не входят в publication text. Они могут находиться в отдельно
обозначенном source basis.

## Verdict

Вернуть `PASS` либо `FAIL`, точный lost/unsupported fact или comprehension gap и
одно наиболее важное улучшение. Корректный список ролей не компенсирует потерю
атомарной single-owner мысли.
