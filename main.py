from aiohttp import web

async def handle(request):
    print(f"🔥 Incoming request: {request.method} {request.path}")
    return web.Response(text="🔥 Ich bin online, Bro! Ich sehe dich.")

app = web.Application()
app.router.add_route('*', '/{tail:.*}', handle)  # fängt ALLE Routen, ALLE Methoden

if __name__ == '__main__':
    web.run_app(app, host='0.0.0.0', port=443)
