# Rollback-kit для review wave owner

Статус: подготовлен 2026-09-03, **не применён**.

## Что откатывается

- ShipTask commit:
  `bed44ba954313f7f4a26f8c02e45e616fa367a19`;
- Marketplace publish commit:
  `293d5fa0f57d8c749e6ced789335d2e0951d2e50`;
- установленный snapshot:
  `issue-grinder/0.1.0+codex.20260903010612`.

Причина и evidence находятся в
[benchmark report](2026-09-03-issue-grinder-review-wave-owner-benchmark.md).

## Безопасная последовательность

Команды ниже — подготовленный runbook, а не выполненные действия.

### 1. Вернуть source contract

```bash
cd '/workspace/ShipTask'
git fetch origin main
git status --short
git revert --no-edit bed44ba954313f7f4a26f8c02e45e616fa367a19
python3 scripts/validate_repo.py
python3 -B -m unittest discover -s tests -p 'test_*.py'
python3 ~/.codex/skills/.system/skill-creator/scripts/quick_validate.py issue-grinder
ruby ~/.codex/skills/project-docs/scripts/validate_docs.rb . --strict-navigation
git diff --check
git push origin main
```

Перед `git revert` нужно убедиться, что текущий `main` содержит указанный
commit и новые пользовательские изменения не пересекаются с его 17 файлами.
Существующие незакоммиченные файлы пользователя нельзя очищать, stash-ить или
включать в revert.

### 2. Пересобрать Marketplace из восстановленного source

Не следует просто делать `git revert 293d5fa`: возврат старого cachebuster
создаст неоднозначный downgrade. Нужно синхронизировать восстановленный source
и выпустить новый monotonically fresh snapshot.

```bash
cd '/workspace/Srez Marketplace'
git fetch origin main
git status --short
rsync -a --delete \
  '/workspace/ShipTask/issue-grinder/' \
  'plugins/issue-grinder/skills/issue-grinder/'
python3 ~/.codex/skills/.system/plugin-creator/scripts/update_plugin_cachebuster.py \
  plugins/issue-grinder
python3 -m unittest discover -s tests -p 'test_*.py' -v
python3 ~/.codex/skills/.system/skill-creator/scripts/quick_validate.py \
  plugins/issue-grinder/skills/issue-grinder
python3 ~/.codex/skills/.system/plugin-creator/scripts/validate_plugin.py \
  plugins/issue-grinder
diff -qr \
  '/workspace/ShipTask/issue-grinder' \
  'plugins/issue-grinder/skills/issue-grinder'
git diff --check
git add plugins/issue-grinder
git commit -m 'Roll back Issue Grinder review wave ownership'
git push origin main
```

### 3. Обновить installed snapshot

```bash
codex plugin marketplace upgrade srez-marketplace --json
codex plugin add issue-grinder@srez-marketplace --json
codex plugin list --json
```

После установки нужно подтвердить:

- новый rollback cachebuster установлен и enabled;
- cache byte-identical Marketplace source;
- `ship-tasks@srez-marketplace` остаётся не установлен;
- Task Manager остаётся adapter-only;
- standalone-каталоги Issue Grinder отсутствуют;
- свежая Codex-сессия видит новый snapshot.

## Точка остановки

Если source revert конфликтует, Marketplace не clean или новый snapshot не
появился после `plugin add`, остановиться без ручного удаления cache и без
частичного отката. Сохранить `git status`, exact SHA и вывод валидатора для
пользователя.
