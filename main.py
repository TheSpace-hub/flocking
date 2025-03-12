from random import randint, random, uniform

import pygame as pg
from pygame import Vector2


def random_vector(length=1):
    angle = uniform(0, 2 * 3.14159)
    vector = Vector2(length, 0).rotate_rad(angle)
    return vector


class Agent:
    objects: list = []

    def __init__(self, x: int, y: int, color: tuple[int, int, int] = (128, 128, 128)):
        self.pos: Vector2 = Vector2(x, y)
        self.color: tuple[int, int, int] = color

        self.__class__.objects.append(self)

    def move(self, screen):
        self.pos += random_vector() * 0.1
        self.pos += self.get_cohesion_vector(screen) * 0.5
        self.pos += self.get_separation_vector(screen) * 1

    def get_separation_vector(self, screen) -> Vector2:
        separation_vector: Vector2 = Vector2()

        for neighbour in list[self.__class__](self.__class__.objects):
            if neighbour == self:
                continue
            distance: float = self.pos.distance_to(neighbour.pos)
            if distance < 50:
                diff: Vector2 = self.pos - neighbour.pos
                diff = diff.normalize()
                diff /= distance
                separation_vector += diff

        if len(self.__class__.objects) - 1 > 0:
            separation_vector /= len(self.__class__.objects) - 1
            if separation_vector.length() != 0:
                separation_vector = separation_vector.normalize()

        pg.draw.line(screen, (0, 255, 0), (self.pos.x, self.pos.y),
                     (self.pos.x + separation_vector.x * 10, self.pos.y + separation_vector.y * 10), 2)

        return separation_vector

    def get_cohesion_vector(self, screen):
        center_of_mass: Vector2 = Vector2(0, 0)

        for neighbour in list[self.__class__](self.__class__.objects):
            center_of_mass += neighbour.pos

        if len(self.__class__.objects) > 0:
            center_of_mass /= len(self.__class__.objects)
            desired_direction = center_of_mass - self.pos
            if desired_direction.length() != 0:
                desired_direction = desired_direction.normalize()

        pg.draw.circle(screen, (0, 0, 255), (center_of_mass.x, center_of_mass.y), 5)

        pg.draw.line(screen, (255, 255, 0), (self.pos.x, self.pos.y),
                     (self.pos.x + desired_direction.x * 10, self.pos.y + desired_direction.y * 10), 2)

        return desired_direction

    def draw(self, screen):
        pg.draw.circle(screen, (128, 128, 128), (self.pos.x, self.pos.y), 10)


def main():
    pg.init()
    screen = pg.display.set_mode((1920, 1080))

    agents: list[Agent] = []
    for i in range(50):
        agents.append(Agent(randint(0, 1920), randint(0, 1080)))

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
