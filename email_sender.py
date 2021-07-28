import smtplib


def send_mail(url):
    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.ehlo()
    server.starttls()
    server.ehlo()

    server.login('valorcool@gmail.com', INSERT_CODE_HERE)

    subject = 'Videocard price!'
    body = 'The price is lower than 500 Eur ' + url

    msg = f"Subject: {subject}\n\n{body}"

    server.sendmail(
        "valorcool@gmail.com",
        "valorcool@gmail.com",
        msg
    )

    print("EMAIL HAS BEEN SENT!")
    server.quit()
