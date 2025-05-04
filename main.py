from aiohttp import web

async def handle(request):
    return web.Response(text="🔥 Ich bin online, Bro!")

app = web.Application()
app.router.add_get('/{tail:.*}', handle)  # fängt ALLE GETs ab
app.router.add_post('/{tail:.*}', handle)  # fängt ALLE POSTs ab

if __name__ == '__main__':
    web.run_app(app, host='0.0.0.0', port=443)
