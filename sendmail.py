import smtplib

def send_mail(student_name, student_email, student_year, student_rating, student_comment):
  login = '542d502793b750'
  password = 'dc471b73bb3f2f'

  sender = f"{student_name} <{student_email}>"
  receiver = "Feedback Collector <feedback@example.com>"

  message = f"""\
  Subject: New Feedback Submission
  To: {receiver}
  From: {sender}

  New Feedback received:

  Name: {student_name}
  Email: {student_email}
  Year: {student_year}
  Rating: {student_rating} / 5
  Comments: {student_comment}
  """
  message = f"""\
Subject: New Feedback Submission
To: {receiver}
From: {sender}

New Feedback received:
Name: {student_name}
Email: {student_email}
Year: {student_year}
Rating: {student_rating} / 5
Comments: {student_comment}"""

  with smtplib.SMTP("smtp.mailtrap.io", 2525) as server:
    server.login(login, password)
    server.sendmail(sender, receiver, message)