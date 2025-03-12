from time import sleep
from random import randint, random, uniform

import pygame as pg
from pygame import Vector2

visual_length: int = 20

pg.init()
pg.font.init()

my_font = pg.font.SysFont('Comic Sans MS', 30)


class Log:
    logs: list[str] = []
    stop: bool = False

    @classmethod
    def log(cls, text: any):
        if cls.stop:
            return
        cls.logs.append(str(text))
        cls.logs = cls.logs[-3:]


def random_vector(length=1):
    angle = uniform(0, 2 * 3.14159)
    vector = Vector2(length, 0).rotate_rad(angle)
    return vector


class Agent:
    objects: list = []

    def __init__(self, x: int, y: int, color: tuple[int, int, int] = (128, 128, 128)):
        self.pos: Vector2 = Vector2(x, y)
        self.color: tuple[int, int, int] = color
        self.velocity: Vector2 = Vector2()

        self.__class__.objects.append(self)

    def move(self, screen):
        self.velocity = Vector2()
        self.velocity += self.get_cohesion_vector(screen) * 1
        self.velocity += self.get_separation_vector(screen) * 1
        self.velocity += self.get_alignment_vector(screen) * 0.1

        self.pos += self.velocity

        Log.log(self.velocity)

    def get_separation_vector(self, screen) -> Vector2:
        separation_vector: Vector2 = Vector2()

        for neighbor in list[self.__class__](self.__class__.objects):
            if neighbor == self:
                continue
            distance: float = self.pos.distance_to(neighbor.pos)
            if distance < 50:
                diff: Vector2 = self.pos - neighbor.pos
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

        for neighbor in list[self.__class__](self.__class__.objects):
            center_of_mass += neighbor.pos

        if len(self.__class__.objects) > 0:
            center_of_mass /= len(self.__class__.objects)
            desired_direction = center_of_mass - self.pos
            if desired_direction.length() != 0:
                desired_direction = desired_direction.normalize()

        pg.draw.circle(screen, (0, 0, 255), (center_of_mass.x, center_of_mass.y), 5)

        pg.draw.line(screen, (255, 255, 0), (self.pos.x, self.pos.y),
                     (self.pos.x + desired_direction.x * visual_length,
                      self.pos.y + desired_direction.y * visual_length), 2)

        return desired_direction

    def get_alignment_vector(self, screen):
        average_velocity = Vector2(0, 0)
        count = 0

        for neighbor in list[self.__class__](self.__class__.objects):
            if neighbor == self:
                continue
            average_velocity += neighbor.velocity
            count += 1

        if count > 0:
            average_velocity /= count
            if average_velocity.length() != 0.0:
                average_velocity.normalize()

        pg.draw.line(screen, (255, 255, 255), (self.pos.x, self.pos.y),
                     (self.pos.x + average_velocity.x * 10, self.pos.y + average_velocity.y * 10), 2)

        return average_velocity

    def draw(self, screen):
        pg.draw.circle(screen, (128, 128, 128), (self.pos.x, self.pos.y), 10)


def draw_logs(screen: pg.Surface):
    offset: int = 0
    for log in Log.logs:
        text_surface = my_font.render(log, False, (255, 0, 0))
        screen.blit(text_surface, (0, 10 + offset))
        offset += text_surface.get_size()[1]


def main():
    screen = pg.display.set_mode((1920, 1080))

    agents = []
    for i in range(10):
        agents.append(Agent(randint(0, 1920), randint(0, 1080)))

    while True:
        for event in pg.event.get():
            if event.type == pg.QUIT:
                pg.quit()
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_SPACE:
                    Log.stop = not Log.stop
        screen.fill((32, 32, 32))

        for agent in agents:
            agent.draw(screen)
            agent.move(screen)

        draw_logs(screen)

        pg.display.flip()


if __name__ == '__main__':
    main()
