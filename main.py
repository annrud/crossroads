import threading
import time

from controller import TrafficLightController
from traffic_light import (CarTrafficLightNorthSouth, CarTrafficLightWestEast,
                           PedestrianTrafficLight)

if __name__ == '__main__':
    controller = TrafficLightController()
    cars_tl_ns = [CarTrafficLightNorthSouth(
        i, controller, base_green_time=30, max_green_time=60, min_green_time=15
    ) for i in (1, 3)]
    cars_tl_we = [CarTrafficLightWestEast(
        i, controller, base_green_time=30, max_green_time=60, min_green_time=15
    ) for i in (2, 4)]
    pedestrian_tl = [PedestrianTrafficLight(
        i, controller, base_green_time=15, max_green_time=40, min_green_time=10
    ) for i in range(5, 13)]

    for light in cars_tl_ns + cars_tl_we + pedestrian_tl:
        controller.add_traffic_light(light)

    def run_controller():
        """Бесконечный цикл, который поочередно активирует
        светофоры для автомобилей и пешеходов.
        """
        while True:
            print("Запускаем автомобильные светофоры север-юг c id=1 и id=3")
            controller.run_car_traffic_lights(cars_tl_ns)
            print(
                "Запускаем автомобильные светофоры запад-восток c id=2 и id=4"
            )
            controller.run_car_traffic_lights(cars_tl_we)
            print(
                "Запускаем пешеходные светофоры с "
                "id=5, id=6, id=7, id=8, id=9, id=10, id=11, id=12"
            )
            controller.run_pedestrian_traffic_lights(pedestrian_tl)
            time.sleep(1)

    threads = []
    for light in controller.traffic_lights.values():
        t = threading.Thread(target=light.run)
        threads.append(t)
        t.start()

    controller_thread = threading.Thread(target=run_controller)
    controller_thread.start()
    threads.append(controller_thread)

    for thread in threads:
        thread.join()
