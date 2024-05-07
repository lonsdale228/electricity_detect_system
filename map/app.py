import datetime
import uvicorn
from fastapi import FastAPI
import folium
from starlette.responses import HTMLResponse
import aiohttp

app = FastAPI()
my_map = folium.Map(control_scale=True, location=(48.90793813554786, 31.393633712579252), zoom_start=6.5)


async def get_all_addresses():
    URL = "http://web/get_all_addresses"
    async with aiohttp.ClientSession() as session:
        params = {"api_key": "3TRRwA_-5l_xyEuWztGzww"}
        async with session.get(URL, params=params) as response:
            print(response)
            answer: list[dict] = await response.json()
            print(answer)
            return answer


async def add_markers(folium_map):
    format_string = "%Y-%m-%dT%H:%M:%S.%f"
    addr = await get_all_addresses()
    for point in addr:
        if point["last_update"] is not None:
            last_update = datetime.datetime.strptime(point["last_update"], format_string).strftime("%H:%M:%S")
        else:
            last_update = "Немає інформації"
        if point["electricity_status"]:
            iframe = folium.IFrame(f"Світло увімкнено <br>Останнє оновлення: <br>{last_update}")
            popup = folium.Popup(iframe, min_width=230, max_width=230)
            folium.Marker(location=[point['latitude'], point['longitude']],
                          icon=folium.Icon(color='green'),
                          popup=popup).add_to(folium_map)
        else:
            iframe = folium.IFrame(f"Світло вимкнено! <br>Останнє оновлення: <br>{last_update}")
            popup = folium.Popup(iframe, min_width=230, max_width=230)
            folium.Marker(location=[point['latitude'], point['longitude']],
                          icon=folium.Icon(color='red'),
                          popup=popup).add_to(folium_map)


@app.get("/", response_class=HTMLResponse)
async def root():
    my_map = folium.Map(control_scale=True, location=(48.90793813554786, 31.393633712579252), zoom_start=6.5)
    await add_markers(my_map)
    body_html = my_map.get_root()
    return body_html.render()


if __name__ == '__main__':
    uvicorn.run(app, port=8001, host='0.0.0.0')
