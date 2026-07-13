
"# TikTok Auto Uploader

Автоматический загрузчик видео в TikTok с удобным графическим интерфейсом на PyQt6.

![Python](https://img.shields.io/badge/python-3.8+-blue.svg)
![PyQt6](https://img.shields.io/badge/PyQt6-6.6.1-green.svg)
![License](https://img.shields.io/badge/license-MIT-orange.svg)

## 🚀 Возможности

- ✅ Быстрый вход в аккаунты TikTok через undetected-chromedriver
- ✅ Загрузка видео на несколько аккаунтов одновременно
- ✅ Группировка аккаунтов по тегам
- ✅ Прогресс загрузки в реальном времени
- ✅ Современный темный интерфейс
- ✅ Управление прокси
- ✅ История загрузок

## 📋 Требования

- Python 3.8 или выше
- Google Chrome или Chromium

## 🔧 Установка

1. Клонируйте репозиторий:
```bash
git clone https://github.com/y1ki/TikTokAutoUploader.git
cd TikTokAutoUploader/tiktok
```

2. Установите зависимости:
```bash
pip install -r requirements.txt
```

3. Запустите приложение:
```bash
python main.py
```

## 📦 Зависимости

```
PyQt6==6.6.1
requests>=2.31.0
aiohttp>=3.9.0
playwright>=1.40.0
undetected-chromedriver>=3.5.0
```

## 🎯 Использование

### Добавление аккаунта

1. Нажмите **"Добавить аккаунт"**
2. Введите имя аккаунта и тег
3. Войдите в TikTok в открывшемся браузере
4. Браузер автоматически закроется после успешного входа

### Загрузка видео

1. Перейдите на вкладку **"Загрузка"**
2. Выберите видео файл
3. Введите название и описание
4. Выберите тег аккаунтов для загрузки
5. Нажмите **"Загрузить видео"**

Видео будет загружено на все аккаунты с выбранным тегом.

### Управление тегами

**Способ 1**: Выделите аккаунты и нажмите **"Установить тег"**

**Способ 2**: Дважды кликните на колонку "Тег" в таблице

**Способ 3**: Правый клик → "🏷️ Изменить тег"

## 📁 Структура проекта

```
tiktok/
├── src/
│   ├── core/           # Логика приложения
│   │   ├── app.py
│   │   ├── database.py
│   │   └── cookie_manager.py
│   └── ui/            # Интерфейс
│       ├── pages/     # Страницы приложения
│       ├── components/# UI компоненты
│       ├── dialogs/   # Диалоговые окна
│       └── windows/   # Главное окно
├── CookiesDir/        # Cookies аккаунтов
├── data/              # База данных
├── main.py            # Точка входа
└── requirements.txt   # Зависимости
```

## 🔐 Безопасность

- Все cookies хранятся локально в папке `CookiesDir/`
- Используется undetected-chromedriver для обхода защиты TikTok
- Данные аккаунтов хранятся в локальной SQLite базе данных

## ⚙️ Настройка

### Переменные окружения (.env)

```env
TIKTOK_LOGIN_URL=https://www.tiktok.com/login
```

## 🐛 Решение проблем

### Браузер не открывается

Убедитесь, что установлен Google Chrome:
```bash
google-chrome --version
```

### Ошибка при входе

1. Очистите cookies аккаунта
2. Попробуйте войти снова
3. Убедитесь, что интернет-соединение стабильно

### Видео не загружается

1. Проверьте формат видео (MP4, MOV, AVI, MKV)
2. Убедитесь, что аккаунт активен
3. Проверьте логи в `log.log`

## 📝 Changelog

### v1.0.0 (2026-07-13)
- Первый релиз
- Добавлен графический интерфейс
- Поддержка множественных аккаунтов
- Система тегов
- Прогресс загрузки

## 👨‍💻 Автор

**y1ki**

- Telegram: [@Y1kiLOLZ](https://t.me/Y1kiLOLZ)
- GitHub: [@y1ki](https://github.com/y1ki)

## 📄 Лицензия

MIT License - смотрите [LICENSE](LICENSE) для деталей

## ⚠️ Disclaimer

Этот инструмент предназначен только для образовательных целей. Используйте на свой страх и риск. Автор не несет ответственности за любые действия, предпринятые с использованием этого программного обеспечения.

## 🤝 Вклад

Contributions, issues и feature requests приветствуются!

1. Fork the Project
2. Create your Feature Branch (`git checkout -b feature/AmazingFeature`)
3. Commit your Changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the Branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## ⭐ Поддержка

Если проект был полезен, поставьте звезду ⭐

---

Made with ❤️ by [y1ki](https://github.com/y1ki)" 
=======
# TikTokAutoUploader
>>>>>>> 433b308e68ba3c5a8c3eb5d59c8ec80e704e0de8
