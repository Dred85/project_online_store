import smtplib
from email.header import Header
from email.mime.text import MIMEText


def send_email(blog):
    # Учетные данные для отправки письма
    login = "olonovaleksandar"
    password = "wpaqnubuejmchlrk"
    email_to = ["adrolv@rambler.ru"]  # Список получателей

    # Создание содержимого письма
    msg = MIMEText(
        f"Поздравляю, ваша статья {blog.title} набрала {blog.views_count} просмотров",
        "plain",
        "utf-8",
    )
    msg["Subject"] = Header("Поздравляю !!!", "utf-8")
    msg["From"] = f"{login}@yandex.ru"
    msg["To"] = ", ".join(email_to)

    # Установление соединения с SMTP сервером
    s = None  # Инициализируем s как None
    try:
        s = smtplib.SMTP("smtp.yandex.ru", 587, timeout=10)
        s.starttls()  # Начинаем TLS для безопасности
        s.login(login, password)  # Входим на сервер
        s.sendmail(msg["From"], email_to, msg.as_string())  # Отправляем письмо
    except Exception as e:
        print(f"Ошибка при отправке email: {e}")
    finally:
        if s:  # Проверяем, что s был создан
            s.quit()  # Завершаем соединение с сервером.
