from chalice import Chalice
from core.dao.entities import Sensor, SensorData
from core.models.request import Request
from core.dao import dao
from core.utilities import utils
from typing import List
import json

app = Chalice(app_name='PyChalice01')


@app.route('/test', methods=['GET'])
def get_sensor_data():
    query_params: dict = app.current_request.query_params or {}
    req: Request = Request(query_params)
    response: List[SensorData] = dao.get_sensor_data(req)
    return json.dumps(response, default=utils.as_dict)


@app.route('/', methods=['GET'])
def get_foo():
    response = dao.get_sensor_data2()
    return json.dumps(response, default=utils.as_dict)
    # return response
