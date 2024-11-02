import logging
import unittest

# Настройка логирования
logging.basicConfig(
    level=logging.INFO,
    filename='runner_tests.log',
    filemode='w',
    encoding='utf-8',
    format='%(levelname)s: %(message)s'
)

class RunnerTest(unittest.TestCase):
    def test_walk(self):
        try:
            # Попробуем создать объект Runner с отрицательной скоростью
            runner = Runner('Вося', speed=-5)
        except ValueError:
            logging.warning("Неверная скорость для Runner")
        else:
            self.fail("Expected ValueError for negative speed not raised")
            logging.info('"test_walk" выполнен успешно')

    def test_run(self):
        try:
            # Попробуем создать объект Runner с неправильным типом для name
            runner = Runner(1234)  # Это число, а не строка
        except TypeError:
            logging.warning("Неверный тип данных для объекта Runner")
        else:
            self.fail("Expected TypeError for non-string name not raised")
            logging.info('"test_run" выполнен успешно')

if __name__ == '__main__':
    unittest.main()
