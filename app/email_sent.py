import resend

resend.api_key = "re_J8nuULie_vtxfvv3QmZ9zgjUmyWsRZULA"


def send_email(to,subject,msg):
    r = resend.Emails.send({
  "from": "digi-loans@resend.dev",
  "to": "{to}",
  "subject": subject
})


