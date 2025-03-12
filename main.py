from random import randint

import pygame as pg
from pygame import Vector2


class Agent:
    objects: list = []

    def __init__(self, x: int, y: int, color: tuple[int, int, int] = (128, 128, 128)):
        self.pos: Vector2 = Vector2(x, y)
        self.color: tuple[int, int, int] = color

        self.__class__.objects.append(self)

    def move(self, screen):
        separation_vector = self.get_separation_vector(screen)
        self.pos += separation_vector / 10

    def get_separation_vector(self, screen) -> Vector2:
        separation_vector: Vector2 = Vector2()

        for neighbour in list[self.__class__](self.__class__.objects):
            if neighbour == self:
                continue
            distance: float = self.pos.distance_to(neighbour.pos)
            diff: Vector2 = (self.pos - neighbour.pos).normalize()
            diff /= distance
            separation_vector += diff

            pg.draw.line(screen, (128, 0, 0), (self.pos.x, self.pos.y),
                         (self.pos.x + diff.x * 10000, self.pos.y + diff.y * 10000), 1)

        if len(self.__class__.objects) - 1 > 0:
            separation_vector /= len(self.__class__.objects) - 1
            separation_vector = separation_vector.normalize()

        pg.draw.line(screen, (0, 255, 0), (self.pos.x, self.pos.y),
                     (self.pos.x + separation_vector.x * 100, self.pos.y + separation_vector.y * 100), 2)

        return separation_vector

    def draw(self, screen):
        pg.draw.circle(screen, (128, 128, 128), (self.pos.x, self.pos.y), 10)


def main():
    pg.init()
    screen = pg.display.set_mode((1920, 1080))

    agents: list[Agent] = []
    for i in range(5):
        agents.append(Agent(randint(300, 800), randint(300, 800)))

    while True:
        for event in pg.event.get():
            if event.type == pg.QUIT:
                pg.quit()
        screen.fill((32, 32, 32))

        for agent in agents:
            agent.draw(screen)
            agent.move(screen)

        pg.display.flip()


if __name__ == '__main__':
    main()
