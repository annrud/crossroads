## CROSSROADS - система управления светофорами с использованием многопоточности и обработки событий для динамического регулирования времени работы сигналов.

### Задача: придумать и описать адаптивный алгоритм работы светофоров для оптимизации общей пропускной способности перекрестка в зависимости от ситуации на перекрестке.

### Основные компоненты:
1. Создаются списки объектов светофоров для направления "север-юг", "запад-восток" и пешеходных светофоров.<br>
2. Каждый светофор инициализируется с идентификатором, контроллером и временем работы зеленого сигнала (минимальным, базовым и максимальным).<br>
3. Каждый созданный светофор добавляется в контроллер, который управляет их состоянием.<br>

### Алгоритм:
- Инициализируются объекты светофоров и добавляются в контроллер.<br>
- Для каждого светофора создается отдельный поток.<br>
- Создается отдельный поток для запуска контроллера.<br>
- Светофоры отправляют события о своем состоянии и длине очереди в контроллер.<br>
- Контроллер пересылает эти события другим светофорам для координации их работы.<br>
- В бесконечном цикле поочередно активируются светофоры для автомобилей и пешеходов, с помощью методов контроллера для запуска соответствующих светофоров.<br>
- Все потоки запускаются и объединяются с использованием join, что обеспечивает синхронизацию потоков.<br>

### Особенности регулировки зеленого сигнала светофора:
- Временя зеленого сигнала регулируется на основе средней длины очереди.<br>
- Получаем среднюю длину очереди для всех направлений: север-юг, запад-восток и пешеходов.<br>
- Если нет автомобилей/пешеходов, зеленый сигнал не включается.<br>
- Если средняя длина очереди больше, чем в других направлениях и превышает базовое время зеленого сигнала, то время работы зеленого сигнала увеличивается.<br>
- Если средняя длина очереди меньше базового времени зеленого сигнала, то время работы зеленого сигнала уменьшается.<br>
- Время зеленого сигнала ограничено минимальным и максимальным значениями.<br>

## Разработчик:
<a href="https://github.com/annrud">*Попова Анна*</a>. 
