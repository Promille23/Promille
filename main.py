from aiohttp import web

async def handle(request):
    return web.Response(text="🔥 Ich bin online, Bro!")

app = web.Application()
app.router.add_get('/', handle)
app.router.add_post('/', handle)
app.router.add_route('*', '/{tail:.*}', handle)

if __name__ == '__main__':
    web.run_app(app, host='0.0.0.0', port=443)
