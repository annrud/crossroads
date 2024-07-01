import random
import threading
import time
from collections import defaultdict
from queue import Queue
from time import sleep

from event import Event


class TrafficLight:
    """Класс для всех светофоров,
    содержит методы для измерения длины очереди,
    обработки движения, отправки и получения событий.
    """
    def __init__(
            self, id_, controller, base_green_time,
            max_green_time, min_green_time
    ):
        self.id_ = id_
        self.state = "red"
        self.queue_length = 0

        self.events_queue = Queue()
        self.objects_queue = Queue()

        self.lock = threading.Lock()
        self.controller = controller
        self.base_green_time = base_green_time
        self.max_green_time = max_green_time
        self.min_green_time = min_green_time
        self.green_time = self.base_green_time
        self.counts_objects = defaultdict(int)

    def measure_queue_length(self):
        """Метод рандомного измерения длины очереди."""
        return self.queue_length + random.randint(0, 10)

    def update_objects_queue(self):
        """Метод обновления количества объектов в очереди."""
        current_size = self.objects_queue.qsize()
        new_size = self.queue_length

        while current_size < new_size:
            self.objects_queue.put(1)
            current_size += 1

        while current_size > new_size:
            self.objects_queue.get()
            current_size -= 1

    def process_moving(self, green_time):
        """Метод для извлечения объектов из очереди,
        пока горит зеленый сигнал светофора.
        """
        start_time = time.time()
        print(
            self,
            f"количество объектов в очереди перед передвижением: "
            f"{self.objects_queue.qsize()}"
        )
        while time.time() - start_time < green_time:
            with self.lock:
                if self.state != 'green':
                    break
                if not self.objects_queue.empty():
                    self.objects_queue.get()
                else:
                    break
            time.sleep(1)
        self.queue_length = self.objects_queue.qsize()
        self.counts_objects[self.id_] = self.queue_length
        print(
            self,
            f"количество объектов в очереди после передвижения: "
            f"{self.objects_queue.qsize()}"
        )
        event = Event(
            sender_id=self.id_,
            data={"queue_length": self.queue_length, "state": self.state}
        )
        self.send_event(event)

    def send_event(self, event):
        """Отправка события в контроллер."""
        self.controller.receive_event(event)

    def receive_event(self, event):
        """Добавление события в очередь."""
        self.events_queue.put(event)

    def handle_event(self):
        """Метод обработки очереди событий -
        получения среднего количества объектов в очереди
        для автомобильных и пешеходных светофоров.
        """
        while not self.events_queue.empty():
            event = self.events_queue.get()
            self.counts_objects[event.sender_id] = event.data["queue_length"]
        average_cars_ns = (self.counts_objects[1] + self.counts_objects[3]) / 2
        average_cars_we = (self.counts_objects[2] + self.counts_objects[4]) / 2
        average_pedestrians = sum(
            value for key, value in self.counts_objects.items()
            if 5 <= key <= 12
        )/8

        return average_cars_ns, average_cars_we, average_pedestrians

    def increase_green_light_duration(self, average):
        """Метод увеличение длительности зеленого сигнала светофора."""
        self.green_time = min(
            self.max_green_time,
            self.base_green_time + round(average/self.base_green_time)
        )

    def decrease_green_light_duration(self, average):
        """Метод уменьшения длительности зеленого сигнала светофора."""
        self.green_time = max(self.min_green_time, round(average))

    def run(self):
        """Отправка события другим светофорам."""
        while True:
            if self.state != "green":
                self.queue_length = self.measure_queue_length()
                self.update_objects_queue()
                event = Event(
                    sender_id=self.id_,
                    data={"queue_length": self.queue_length,
                          "state": self.state}
                )
                self.events_queue.put(event)
                self.send_event(event)
                sleep(20)

    def __str__(self):
        return f"Светофор id={self.id_}"


class CarTrafficLightNorthSouth(TrafficLight):

    def adjust_green_time(self):
        """Метод регулировки зелёного сигнала автомобильных
        светофоров направления север-юг
        на основе средней длины очереди.
        """
        average_cars_ns, average_cars_we, average_pedestrians = self.handle_event()
        if not average_cars_ns:
            self.green_time = 0
        elif (
                average_cars_ns > average_cars_we and
                average_cars_ns > average_pedestrians and
                average_cars_ns > self.base_green_time
        ):
            self.increase_green_light_duration(average_cars_ns)
        elif (
                average_cars_ns < self.base_green_time
        ):
            self.decrease_green_light_duration(average_cars_ns)
        return self.green_time

    def __str__(self):
        return f"Светофор id={self.id_}"


class CarTrafficLightWestEast(TrafficLight):

    def adjust_green_time(self):
        """Метод регулировки зелёного сигнала автомобильных
        светофоров направления запад-восток
        на основе средней длины очереди.
        """
        average_cars_ns, average_cars_we, average_pedestrians = self.handle_event()
        if not average_cars_we:
            self.green_time = 0
        elif (
                average_cars_we > average_cars_ns and
                average_cars_we > average_pedestrians and
                average_cars_we > self.base_green_time
        ):
            self.increase_green_light_duration(average_cars_we)
        elif (
                average_cars_we < self.base_green_time
        ):
            self.decrease_green_light_duration(average_cars_we)
        return self.green_time

    def __str__(self):
        return f"Светофор id={self.id_}"


class PedestrianTrafficLight(TrafficLight):

    def adjust_green_time(self):
        """Метод регулировки зелёного сигнала пешеходных
        светофоров на основе средней длины очереди.
        """
        average_cars_ns, average_cars_we, average_pedestrians = self.handle_event()
        if not average_pedestrians:
            self.green_time = 0
        elif (
                average_pedestrians > average_cars_ns and
                average_pedestrians > average_cars_we and
                average_pedestrians > self.base_green_time
        ):
            self.increase_green_light_duration(average_pedestrians)
        elif (
                average_pedestrians < self.base_green_time
        ):
            self.decrease_green_light_duration(average_pedestrians)
        return self.green_time

    def __str__(self):
        return f"Светофор id={self.id_}"
