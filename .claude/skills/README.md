# Claude Code skills

Скиллы для Claude Code, скопированные из открытых репозиториев. Claude подхватывает их автоматически из `.claude/skills/`; вызвать вручную можно через `/<name>`.

| # | Скилл(ы) | Что делает | Источник | Лицензия |
|---|----------|------------|----------|----------|
| 01 | `reverse-engineer-anything` | Реверс-инжиниринг приложений с помощью REA (нужен сам REA) | github.com/morluto/rea | MIT |
| 02 | `ponytail`, `ponytail-review`, `ponytail-audit`, `ponytail-debt`, `ponytail-gain`, `ponytail-help` | «Старший разработчик»: ревью, аудит, техдолг | github.com/DietrichGebert/ponytail | MIT |
| 03 | `hallmark` | Убирает шаблонный «ИИ-дизайн» из интерфейсов | github.com/nutlope/hallmark | MIT |
| 04 | `humanizer` | Делает ИИ-тексты человечными | github.com/blader/humanizer | MIT |
| 05 | `taste` | Разбирает дизайн-вкус любого сайта (нужен Playwright MCP) | github.com/senlindesign/taste-skill | — |
| 06 | `impeccable` | Шлифовка интерфейсов командами для дизайнеров | github.com/pbakaus/impeccable | Apache-2.0 |
| 07 | `ui-ux-pro-max`, `design`, `design-system`, `ui-styling`, `brand`, `banner-design`, `slides` | Единый стиль интерфейсов, дизайн-система | github.com/nextlevelbuilder/ui-ux-pro-max-skill | MIT |
| 08 | `last30days` | Тренды из обсуждений за последние 30 дней | github.com/mvanhorn/last30days-skill | MIT |
| 09 | `scrapling-official` | Сбор данных с сайтов через Scrapling (`pip install scrapling`) | github.com/D4Vinci/Scrapling | BSD-3-Clause |
| 10 | `diagram-design` | Интерактивные технические схемы | github.com/cathrynlavery/diagram-design | MIT |

Демо-медиа (видео/картинки) и документация из исходных репозиториев не копировались.

## Скиллы для тендеров

15 скиллов для участия в тендерах и госзакупках, взяты из открытых репозиториев (все MIT, файл `LICENSE` лежит в папке каждого скилла). Скиллы написаны на английском, но работают и с запросами на русском, и с документацией на русском или казахском.

| # | Скилл | Что делает | Источник |
|---|-------|------------|----------|
| T01 | `rfp-responder` | Разбор тендера: обязательные и оценочные требования, решение «участвовать или нет», оценка шансов на победу (скрипты на Python без внешних библиотек) | github.com/alirezarezvani/claude-skills |
| T02 | `cowork-rfp-response` | Матрица соответствия «требование → наше подтверждение» по папке с прошлыми заявками и документами, черновик ответа | github.com/onewave-ai/claude-skills |
| T03 | `rfp-response` | Полная заявка на государственный или коммерческий тендер (RFP/RFQ/ITT) | github.com/mohitagw15856/pm-claude-skills |
| T04 | `bid-tender-review` | Проверка тендерного пакета (стройка): пробелы в объёме работ, перенос рисков, подозрительные расценки | github.com/mohitagw15856/pm-claude-skills |
| T05 | `rfp-scoring-matrix` | Взвешенная оценочная матрица: как комиссия будет оценивать заявки | github.com/mohitagw15856/pm-claude-skills |
| T06 | `01-cover-letter` | Сопроводительное письмо к заявке | github.com/peterbamuhigire/proposal-skills |
| T07 | `05-relevant-experience` | Раздел об опыте: аналогичные договоры, референции, результаты | github.com/peterbamuhigire/proposal-skills |
| T08 | `06-methodology` | Техническое предложение и методология, распределение объёма по баллам | github.com/peterbamuhigire/proposal-skills |
| T09 | `07-team-composition` | Состав команды, роли, резюме специалистов | github.com/peterbamuhigire/proposal-skills |
| T10 | `08-work-plan` | План-график работ, этапы, вехи | github.com/peterbamuhigire/proposal-skills |
| T11 | `10-financial-proposal` | Ценовое предложение: смета, график платежей, допущения | github.com/peterbamuhigire/proposal-skills |
| T12 | `bid-red-team-dual-review` | Двойная проверка заявки перед подачей («красная команда») | github.com/peterbamuhigire/proposal-skills |
| T13 | `submission-proof-and-receipt-discipline` | Контроль подачи: что, когда и куда отправлено, подтверждение получения | github.com/peterbamuhigire/proposal-skills |
| T14 | `contract-review` | Проверка проекта договора: невыгодные условия, правки | github.com/evolsb/claude-legal-skill |
| T15 | `cowork-vendor-comparison` | Сравнение коммерческих предложений поставщиков, полная стоимость | github.com/onewave-ai/claude-skills |

Ссылки на другие скиллы в T06–T13 ведут в исходный репозиторий proposal-skills и здесь не работают. Скиллы работают и без них.
