from aquarius.smtp import send_mail

res = send_mail("title", "results")
print(f"{res=}")
