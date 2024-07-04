from pprint import pprint

from aquarius.creation import create_chat_results
from aquarius.smtp import send_mail

res = create_chat_results()
pprint(res)
send_mail("this week in LLM news", body=res)
