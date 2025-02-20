import json
import time
var1 = json.loads("1")

var2 = json.loads("3")

result = ""

text = "7141561AC3C8E335855D9EB5627B42E1"

json_var = json.loads("{\"name\": \"Elton\"}")

array = json.loads("[\"1\",\"2\",\"3\"]")

optional = True

status = "{'status': 'True', 'message': \"setvar  b'6'.decode()\", 'img': '', 'vars': [{'name': 'var1', 'data': '6', 'type': 'string', 'collapse': True, '$$hashKey': 'object:5607'}, {'name': 'var2', 'data': '3', 'type': 'string', 'collapse': True, '$$hashKey': 'object:5608'}, {'name': 'result', 'data': \"b'6'\", 'type': 'string', 'collapse': True, '$$hashKey': 'object:5609'}, {'name': 'text', 'data': 'Bienvenido', 'type': 'string', 'collapse': True, '$$hashKey': 'object:5610'}, {'name': 'json_var', 'data': '{\"name\": \"Elton\"}', 'type': 'string', 'collapse': True, '$$hashKey': 'object:5611'}, {'name': 'array', 'data': '[\"1\",\"2\",\"3\"]', 'type': 'string', 'collapse': True, '$$hashKey': 'object:5612'}, {'name': 'optional', 'data': 'True', 'type': 'string', 'collapse': True, '$$hashKey': 'object:5613'}, {'name': 'status', 'data': '', 'type': 'string', 'collapse': True, '$$hashKey': 'object:5614'}], 'ifs': [], 'extra': []}"

esperar = True

bot.scrap.load_url("https://www.mercadolibre.com.ni/#from=homecom")

time.sleep(4)
esperar = bot.scrap.wait_for_object("visible","id","cb1-edit",5)

bot.scrap.click_and_wait_if_neccesary("cb1-edit",0,"id")

bot.scrap.send_key_web("","cb1-edit","id","Mause")

bot.scrap.send_key_web("ENTER","cb1-edit","id","")

time.sleep(float(5))

bot.scrap.kill_driver()

