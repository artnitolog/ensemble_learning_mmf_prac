# Третье практическое задание

#### Предметный указатель!
* [Реализации ансамблей](https://github.com/artnitolog/mmf_prac_2020_task_3/tree/main/ensembles)
* [Отчет об экспериментах](https://github.com/artnitolog/mmf_prac_2020_task_3/blob/main/experiments/report.pdf)
* [Ноутбук с экспериментами](https://github.com/artnitolog/mmf_prac_2020_task_3/blob/main/experiments/experiments.ipynb)
* [Реализация веб-сервера](https://github.com/artnitolog/mmf_prac_2020_task_3/tree/main/app)

### Инструкция для [готовой сборки](https://hub.docker.com/r/artnitolog/server_ens) сервера
* `docker run --rm -p 5000:5000 -i artnitolog/server_ens`

### Команды для самостоятельной сборки 
1. `docker build -t server_ens .`
2. `docker run --rm -p 5000:5000 -i server_ens`
