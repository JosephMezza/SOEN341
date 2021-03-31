import smtplib


def sendemail(receiver, link):
    sender_email = "binstagram341@gmail.com"
    rec_email = receiver
    password = "Binstagram_341!"
    link = link
    subject = "Password Reset Link"
    body = "Hello, in order to reset your email please use the link below. Please keep this new password secret and don't forget it again. This link will expire after 5 min. Press here: "+link                
    message = f'Subject: {subject}\n\n{body}'

    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.ehlo()
    server.starttls()
    server.ehlo()
    server.login(sender_email, password)
    print("Login success")
    server.sendmail(sender_email, rec_email, message)

# sendemail("alexandrubara2000@gmail.com","http://127.0.0.1:5000/resetPassword/alex")