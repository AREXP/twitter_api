# twitter_api

Нужно разработать консольное приложение для работы с [tmdb](https://www.themoviedb.org) v3, которое умеет выполнять две операции:

* Выводить N(задается параметром в консоли) самых популярных фильмов в формате «id/Название/место в рейтинге/дата релиза/рейтинг/страна производства». NB: страна производства это не оригинальный язык фильма
* По id указанного фильма(id из предыдущего фильма) вывести информацию о пяти актерах(первые пять в ответе API) фильма в формате «имя актера/роль в этом фильме/место рождения/дата рождения»лаев

Технические ограничения:
* python3.7
* библиотеки requests или aiohttp
* без готовых SDK

Прочие ограничения:
* Решение должно быть оформлено в виде пулл-реквеста к этому репозиторию
* К решению отдельным файлом должна быть приложена инструкция по запуску
* Весь ввод-вывод через терминал
