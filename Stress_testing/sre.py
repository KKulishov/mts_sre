from locust import HttpUser, SequentialTaskSet, task, between

class SreApp(SequentialTaskSet):
    @task(1)
    def cities_route(self):
        with self.client.get("/Cities", catch_response=True) as response:
            if response.status_code != 200:
                response.failure("Failed to get all Cities items, StatusCode: " + str(response.status_code))
                self.on_stop

    @task(2)
    def Forecast(self):
        with self.client.get("/Forecast", catch_response=True) as response:
            if response.status_code != 200:
                response.failure("Failed to get all Forecast items, StatusCode: " + str(response.status_code)) 
                self.on_stop

    def on_stop(self):
        self.user.stop()             

class WeatherForecast(SequentialTaskSet):
    @task()
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
    wait_time = between(1, 3)
    # указания веса для распредление нагрузки
    tasks = {
            SreApp: 8,
            WeatherForecast: 2
        }