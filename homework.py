class InfoMessage:
    """Информационное сообщение о тренировке."""
    def __init__(self,
                 training_type,
                 duration,
                 distance,
                 speed,
                 calories):
        self.training_type = training_type
        self.duration = duration
        self.distance = distance
        self.speed = speed
        self.calories = calories

    def get_message(self):
        return (f'Тип тренировки: {self.training_type}; '
                f'Длительность: {self.duration:.3f} ч.; '
                f'Дистанция: {self.distance:.3f} км; '
                f'Ср. скорость: {self.speed:.3f} км/ч; '
                f'Потрачено ккал: {self.calories:.3f}.')


class Training:
    """Базовый класс тренировки."""
    def __init__(self,
                 action: int,
                 duration: float,
                 weight: float,
                 ) -> None:
        self.action = action
        self.duration = duration
        self.weight = weight
    LEN_STEP: float = 0.65
    M_IN_KM: int = 1000
    H_IN_M: int = 60

    def get_distance(self) -> float:
        """Получить дистанцию в км."""
        dist_in_km = self.action * self.LEN_STEP / self.M_IN_KM
        return dist_in_km

    def get_mean_speed(self) -> float:
        """Получить среднюю скорость движения."""
        avg_kmh_speed = self.get_distance() / self.duration
        return avg_kmh_speed

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий."""
        pass

    def show_training_info(self) -> InfoMessage:
        """Вернуть информационное сообщение о выполненной тренировке."""
        return InfoMessage(self.__class__.__name__, self.duration,
                           self.get_distance(), self.get_mean_speed(),
                           self.get_spent_calories())


class Running(Training):
    """Тренировка: бег."""
    M_IN_KM = 1000
    CALORIES_MEAN_SPEED_MULTIPLIER = 18
    CALORIES_MEAN_SPEED_SHIFT = 1.79
    H_IN_MIN = 60

    def __init__(self, action, duration, weight):
        super().__init__(action, duration, weight)

    def get_spent_calories(self) -> float:
        mean_speed = super().get_mean_speed()
        duration_in_min = self.duration * self.H_IN_MIN
        spent_calories = ((self.CALORIES_MEAN_SPEED_MULTIPLIER * mean_speed
                          + self.CALORIES_MEAN_SPEED_SHIFT)
                          * self.weight / self.M_IN_KM * duration_in_min)
        return spent_calories


class SportsWalking(Training):
    """Тренировка: спортивная ходьба."""
    M_IN_KM = 1000
    KMH_IN_MS = 0.278
    M_IN_SM = 100
    H_IN_MIN = 60
    FIRST_COEFF = 0.035
    SECOND_COEFF = 0.029

    def __init__(self, action, duration, weight, height):
        super().__init__(action, duration, weight)
        self.height = height

    def get_spent_calories(self) -> float:
        mean_speed_in_ms = (super().get_mean_speed()) * self.KMH_IN_MS
        height_in_m = self.height / self.M_IN_SM
        duration_in_min = self.duration * self.H_IN_MIN
        spent_calories = ((self.FIRST_COEFF * self.weight
                           + (mean_speed_in_ms**2 / height_in_m)
                           * self.SECOND_COEFF * self.weight)
                          * duration_in_min)
        return spent_calories


class Swimming(Training):
    """Тренировка: плавание."""
    FIRST_COEFF = 1.1
    SECOND_COEFF = 2
    LEN_STEP = 1.38
    M_IN_KM = 1000

    def __init__(self, action, duration, weight, length_pool, count_pool):
        super().__init__(action, duration, weight)
        self.length_pool = length_pool
        self.count_pool = count_pool

    def get_mean_speed(self) -> float:
        """Получить среднюю скорость движения."""
        swim_avg = (self.length_pool * self.count_pool
                    / self.M_IN_KM / self.duration)
        return swim_avg

    def get_spent_calories(self) -> float:
        swim_avg = self.get_mean_speed()
        spent_calories = ((swim_avg + self.FIRST_COEFF)
                          * self.SECOND_COEFF * self.weight * self.duration)
        return spent_calories


def read_package(workout_type: str, data: list) -> Training:
    """Прочитать данные полученные от датчиков."""
    workout: dict = {'SWM': Swimming,
                     'RUN': Running,
                     'WLK': SportsWalking}
    return workout[workout_type](*data)


def main(training: Training) -> None:
    """Главная функция."""
    info = training.show_training_info()
    print(info.get_message())


if __name__ == '__main__':
    packages = [
        ('SWM', [720, 1, 80, 25, 40]),
        ('RUN', [15000, 1, 75]),
        ('WLK', [9000, 1, 75, 180]),
    ]

    for workout_type, data in packages:
        training = read_package(workout_type, data)
        main(training)
