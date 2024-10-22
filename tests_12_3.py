import unittest
from tests_12_2 import RunnerTest, TournamentTest


class RunnerTest(RunnerTest):
    is_frozen = False

    def run(self, result=None):
        if self.is_frozen:
            print("Тесты в этом кейсе заморожены")
            return
        super().run(result)


class TournamentTest(TournamentTest):
    is_frozen = True

    def run(self, result=None):
        if self.is_frozen:
            print("Тесты в этом кейсе заморожены")
            return
        super().run(result)


if __name__ == "__main__":
    unittest.main()
