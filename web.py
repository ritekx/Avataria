import asyncio
import base64
import configparser
import redis
from aiohttp import web
import aiohttp_session
import aiohttp_jinja2
import jinja2
from cryptography import fernet
from aiohttp_session.cookie_storage import EncryptedCookieStorage
import utils.bot_common

routes = web.RouteTableDef()
routes.static("/files", "files")

xml = """<?xml version="1.0" ?>
<cross-domain-policy>
    <allow-access-from domain="*" />
</cross-domain-policy>"""

config = configparser.ConfigParser()
config.read("web.ini")
registation = config["webserver"]["allow_reg"].lower() == "true"


def get_level(exp):
    expSum = 0
    i = 0
    while expSum <= exp:
        i += 1
        expSum += i * 50
    return i


@routes.get("/")
async def index(request):
    session = await aiohttp_session.get_session(request)
    context = {}
    if "token" not in session:
        context["logged_in"] = False
    else:
        context["logged_in"] = True
        context["token"] = session["token"]
        context["update_time"] = config["webserver"]["update_time"]
    return aiohttp_jinja2.render_template("index.html", request, context=context)


@routes.post("/login")
async def login(request):
    session = await aiohttp_session.new_session(request)
    data = await request.post()
    password = data["password"]
    uid = app["redis"].get(f"auth:{password}")
    if uid == data["login"]:
        session["uid"] = uid
        session["token"] = password
    raise web.HTTPFound("/")


@routes.get("/logout")
async def logout(request):
    session = await aiohttp_session.get_session(request)
    if "token" in session:
        del session["token"]
        del session["uid"]
    raise web.HTTPFound("/")


@routes.get("/kayitol")
async def register(request):
    if not registation:
        return web.Response(text="Регистрация отключена")
    uid, password = utils.bot_common.new_account(app["redis"])
    return web.Response(text=f"Avataria PVP Hesap Bilgileriniz; ID: - {uid}, Şifreniz: - {password}")


@routes.get("/prelogin")
async def prelogin(request):
    if "sid" not in request.query:
        raise web.HTTPClientError()
    try:
        uid = int(request.query["sid"])
    except ValueError:
        raise web.HTTPClientError()
    exp = int(app["redis"].get(f"uid:{uid}:exp"))
    return web.json_response({
        "user": {
            "bannerNetworkId": None,
            "reg": 0,
            "paymentGroup": "",
            "preloginModuleIds": "",
            "id": uid,
            "avatariaLevel": get_level(exp)
        }
    })


@routes.post("/social")
async def social(request):
    data = await request.post()
    if not data["method"]:
        raise web.HTTPClientError()
    if data["method"] == "getTestUsers":
        return web.json_response({"uids": [str(data["user_id"])]})
    elif data["method"] in ["getFriends", "getAppFriends"]:
        return web.json_response([])
    elif data["method"] == "getProfiles":
        return web.json_response([{"id": data["uids"]}])


@routes.get("/appconfig.xml")
async def appconfig(request):
    session = await aiohttp_session.get_session(request)
    if "token" not in session:
        raise web.HTTPUnauthorized()
    context = {
        "token": session["token"],
        "uid": session["uid"],
        "ip": config["webserver"]["server_ip"],
        "address": config["webserver"]["web_address"]
    }
    return aiohttp_jinja2.render_template("appconfig.xml", request, context=context)


@routes.get("/crossdomain.xml")
async def crossdomain(request):
    return web.Response(text=xml)


async def main():
    global app
    app = web.Application()
    app.add_routes(routes)
    app["redis"] = redis.Redis(decode_responses=True)

    fernet_key = fernet.Fernet.generate_key()
    secret_key = base64.urlsafe_b64decode(fernet_key)
    aiohttp_session.setup(app, EncryptedCookieStorage(secret_key))
    aiohttp_jinja2.setup(app, loader=jinja2.FileSystemLoader("templates"))

    runner = web.AppRunner(app)
    await runner.setup()
    site = web.TCPSite(runner, "127.0.0.1", int(config["webserver"]["web_port"]))
    await site.start()

    print(f"Serwer działa na http://127.0.0.1:{config['webserver']['web_port']}")

    while True:
        await asyncio.sleep(3600)


if __name__ == "__main__":
    asyncio.run(main())
