import resend

resend.api_key = "re_J8nuULie_vtxfvv3QmZ9zgjUmyWsRZULA"

params = {
    "from": "Acme <onboarding@resend.dev>",
    "to": ["delivered@resend.dev"],
    "subject": "hello world",
    "html": "<strong>it works!</strong>",
}

email = resend.Emails.send(params)