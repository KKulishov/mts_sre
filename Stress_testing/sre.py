from locust import HttpUser, SequentialTaskSet, task, between
import json
import random
class SreApp(SequentialTaskSet):
    @task(30)
    def get_cities_and_fetch_id(self):
        # Шаг 1: Получаем JSON с /Cities
        response = self.client.get("/Cities")
        try:
            cities_data = response.json()
        except json.JSONDecodeError:
            # Если ответ не является JSON, завершаем тест
            self.on_stop
        # Проверяем, что ответ был успешным
        if response.status_code != 200:
            self.on_stop
        # Шаг 2: Выбираем случайный id из полученных данных
        selected_id = None
        if cities_data:
            city = random.choice(cities_data)
            selected_id = city.get("id")

        if selected_id is not None:
            # Шаг 3: Делаем запрос на /Cities/{selected_id}
            response = self.client.get(f"/Cities/{selected_id}")
            # Обработка результата в соответствии с вашими требованиями
            if response.status_code == 200:
                print(f"Successfully fetched data for city with id {selected_id}")
            else:
                print(f"Failed to fetch data for city with id {selected_id}")

    @task(20)
    def Forecast(self):
        with self.client.get("/Forecast", catch_response=True) as response:
            if response.status_code != 200:
                response.failure("Failed to get all Forecast items, StatusCode: " + str(response.status_code)) 
                self.on_stop

    def on_stop(self):
        self.user.stop()             


class Random_change(SequentialTaskSet):
    @task(5)
    def cities_id_change(self):
        # Шаг 1: Получаем текущие данные с /Forecast
        response = self.client.get("/Forecast")
        try:
            forecast_data = response.json()
        except json.JSONDecodeError:
            # Если ответ не является JSON, завершаем тест
            self.on_stop

        # Проверяем, что ответ был успешным
        if response.status_code != 200:
            self.on_stop

        # Шаг 2: Выбираем случайный элемент из полученных данных
        selected_forecast = None
        if forecast_data:
            city = random.choice(forecast_data)
            selected_id = city.get("id")
            selected_forecast = random.choice(forecast_data)

        # Шаг 3: Изменяем значение temperature и отправляем PUT-запрос
        if selected_forecast:
            random_temperaure = random.uniform(1, 30)  # новая случайная температура

            body = {
                "id": int(selected_id),
                "cityId": int(selected_id),
                "dateTime": 11111,
                "temperature": int(random_temperaure), # новая случайная температура,
                "summary": "warm"
            }

            # Отправляем PUT-запрос с обновленными данными
            put_response = self.client.put(f"/Forecast/{selected_id}", json=body)

            # Обработка результата в соответствии с вашими требованиями
            if put_response.status_code == 200:
                print(f"Successfully updated temperature for forecast with id {selected_id}")
            else:
                print(f"Failed to update temperature for forecast with id {selected_id} ")

class WeatherForecast(SequentialTaskSet):
    @task(10)
    def cities_route(self):
        endpoint = "/WeatherForecast"
        response = self.client.get(endpoint)
        self.handle_response(response, endpoint)

    def handle_response(self, response, endpoint):
        if response.status_code != 200:
            response.failure("Failed to get items for {endpoint}, StatusCode: " + str(response.status_code))
            #quit()  выход полный из locust
            #self.environment.runner.quit() остановка всех runner
            self.on_stop
            #self.user.stop() # остановка тока тек. task  проверки 
            #self.interrupt() #  останавливает только текущую задачу пользователя, не влияя на выполнение других задач.

    def on_stop(self):
        self.user.stop()    


class MyUser(HttpUser):
    wait_time = between(2, 6)
    # указания веса для распредление нагрузки
    tasks = {
            SreApp: 10,
            WeatherForecast: 2,
            Random_change: 1
        }