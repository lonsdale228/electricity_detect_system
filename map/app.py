import uvicorn
from fastapi import FastAPI
import folium
from starlette.responses import HTMLResponse
import aiohttp

app = FastAPI()
my_map = folium.Map(control_scale=True, location=(48.90793813554786, 31.393633712579252), zoom_start=6.5)

marker_list = [
    [46.33816492462972, 30.68647288837276],
    [46.47838217382792, 30.739875027100144],
    [46.51871580608107, 30.62395723920654],
    [46.473503400542356, 30.38451860038735]
]




async def get_all_addresses():
    URL = "http://web/posts/get_all_addresses"
    async with aiohttp.ClientSession() as session:
        params = {"api_key": "3TRRwA_-5l_xyEuWztGzww"}
        async with session.get(URL, params=params) as response:
            print(response)
            answer: list[dict] = await response.json()
            print(answer)
            return answer


async def add_markers(folium_map):
    addr = await get_all_addresses()
    for point in addr:
        if point["electricity_status"]:
            folium.Marker(location=[point['latitude'], point['longitude']], icon=folium.Icon(color='green'), popup="Світло увімкнено").add_to(folium_map)
        else:
            folium.Marker(location=[point['latitude'], point['longitude']], icon=folium.Icon(color='red'),
                          popup="Світло вимкнено").add_to(folium_map)


@app.get("/", response_class=HTMLResponse)
async def root():
    my_map = folium.Map(control_scale=True, location=(48.90793813554786, 31.393633712579252), zoom_start=6.5)
    await add_markers(my_map)

    body_html = my_map.get_root()
    return body_html.render()


if __name__ == '__main__':
    uvicorn.run(app, port=8001, host='0.0.0.0')
