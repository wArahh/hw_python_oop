from dataclasses import dataclass


@dataclass
class InfoMessage:
    """Информационное сообщение о тренировке."""
    training_type: str
    duration: float
    distance: float
    speed: float
    calories: float

    def get_message(self):
        return (f'Тип тренировки: {self.training_type}; '
                f'Длительность: {self.duration:.3f} ч.; '
                f'Дистанция: {self.distance:.3f} км; '
                f'Ср. скорость: {self.speed:.3f} км/ч; '
                f'Потрачено ккал: {self.calories:.3f}.')


@dataclass
class Training:
    """Базовый класс тренировки."""
    action: int
    duration: float
    weight: float
    LEN_STEP = 0.65
    M_IN_KM = 1000
    H_IN_MIN = 60

    def get_distance(self) -> float:
        """Получить дистанцию в км."""
        return self.action * self.LEN_STEP / self.M_IN_KM

    def get_mean_speed(self) -> float:
        """Получить среднюю скорость движения."""
        return self.get_distance() / self.duration

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
    CALORIES_MEAN_SPEED_MULTIPLIER = 18
    CALORIES_MEAN_SPEED_SHIFT = 1.79

    def get_spent_calories(self) -> float:
        mean_speed = super().get_mean_speed()
        duration_in_min = self.duration * self.H_IN_MIN
        return ((self.CALORIES_MEAN_SPEED_MULTIPLIER * mean_speed
                + self.CALORIES_MEAN_SPEED_SHIFT)
                * self.weight / self.M_IN_KM * duration_in_min)


@dataclass
class SportsWalking(Training):
    """Тренировка: спортивная ходьба."""
    KMH_IN_MS = 0.278
    M_IN_SM = 100
    FIRST_COEFF = 0.035
    SECOND_COEFF = 0.029
    height: int

    def get_spent_calories(self) -> float:
        mean_speed_in_ms = (super().get_mean_speed()) * self.KMH_IN_MS
        height_in_m = self.height / self.M_IN_SM
        duration_in_min = self.duration * self.H_IN_MIN
        return ((self.FIRST_COEFF * self.weight
                + (mean_speed_in_ms**2 / height_in_m)
                * self.SECOND_COEFF * self.weight)
                * duration_in_min)


@dataclass
class Swimming(Training):
    """Тренировка: плавание."""
    FIRST_COEFF = 1.1
    SECOND_COEFF = 2
    LEN_STEP = 1.38
    length_pool: int
    count_pool: int

    def get_mean_speed(self) -> float:
        """Получить среднюю скорость движения."""
        return (self.length_pool * self.count_pool
                / self.M_IN_KM / self.duration)

    def get_spent_calories(self) -> float:
        swim_avg = self.get_mean_speed()
        return ((swim_avg + self.FIRST_COEFF)
                * self.SECOND_COEFF * self.weight * self.duration)


def read_package(workout_type: str, data: list) -> Training:
    """Прочитать данные полученные от датчиков."""
    workout: dict = {'SWM': Swimming,
                     'RUN': Running,
                     'WLK': SportsWalking}
    if workout_type in workout.keys():
        return workout[workout_type](*data)
    else:
        print('Данная тренировка недоступна')


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
