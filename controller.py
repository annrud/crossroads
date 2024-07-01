import threading
import time


class TrafficLightController:
    """Управляет светофорами, переключает сигналы светофора,
    запускает движение очередей, принимает события и
    пересылает их другим светофорам.
    """
    def __init__(self):
        self.traffic_lights = {}
        self.lock = threading.Lock()

    def add_traffic_light(self, traffic_light):
        self.traffic_lights[traffic_light.id_] = traffic_light

    def receive_event(self, event):
        for light in self.traffic_lights.values():
            if light.id_ != event.sender_id:
                light.receive_event(event)

    def run_car_traffic_lights(self, cycle_lights):
        """Метод управления автомобильными светофорами,
        активирует зеленый сигнал на расчётное время,
        запускает движение очереди,
        затем переключает светофоры на желтый и,
        через 2 секунды, на красный сигнал.
        """
        green_time = cycle_lights[0].adjust_green_time()
        if green_time:
            def activate_light(light):
                light.state = 'green'
                print(
                    light,
                    f"состояние={light.state}, "
                    f"время работы сигнала: {green_time} секунд"
                )
                light.process_moving(green_time)

            threads = []
            for light in cycle_lights:
                t = threading.Thread(target=activate_light, args=(light,))
                threads.append(t)
                t.start()

            for t in threads:
                t.join()

            for light in cycle_lights:
                light.state = 'yellow'
                print(light, f"состояние: {light.state}")
            time.sleep(2)

            for light in cycle_lights:
                light.state = 'red'
                print(light, f"состояние: {light.state}")

    def run_pedestrian_traffic_lights(self, cycle_lights):
        """Метод управления пешеходными светофорами,
        активирует зеленый сигнал на расчётное время,
        запускает движение очереди,
        затем переключает светофоры на красный сигнал.
        """
        green_time = cycle_lights[0].adjust_green_time()
        if green_time:
            def activate_light(light):
                light.state = 'green'
                light.process_moving(green_time)
                print(
                    light,
                    f"состояние={light.state}, "
                    f"время работы сигнала: {green_time} секунд"
                )

            threads = []
            for light in cycle_lights:
                t = threading.Thread(target=activate_light, args=(light,))
                threads.append(t)
                t.start()

            for t in threads:
                t.join()

            for light in cycle_lights:
                light.state = 'red'
                print(light, f"состояние: {light.state}")
