import bisect
import sys
from collections import deque
from pathlib import Path
from random import choice
from time import perf_counter as tpc
from typing import Dict, NamedTuple, Tuple

import pygame as pg

SnakeProps = NamedTuple(
    "SnakeProps",
    [
        ("pos", Tuple[int, int]),
        ("length", int),
        ("direction", str),
        ("speed", int),
    ],
)

GameSettings = NamedTuple(
    "GameSettings",
    [
        ("caption", str),  # 标题
        ("geometry", dict),  # 窗口设置
        ("fps", int),  # fps 设置
        ("fontsize", Dict[str, int]),  # 字体大小
        ("colors", Dict[str, int]),  # 颜色列表
        ("snake_init", SnakeProps),  # 贪吃蛇初始状态
        ("scores", Tuple[int, ...]),  # 不同等级对应分数划分点
        ("motions", Dict[str, Tuple[int, int]]),  # 移动规则
        ("operations", Dict[str, int]),  # 按键与方向映射关系
    ],
)

GS = GameSettings(
    caption="Snake Game v1.0",
    geometry=dict(width=720, height=480, grid=24, nx=20, ny=20),
    fps=60,
    fontsize=dict(large=30, normal=20),
    colors=dict(
        snake=0x00CCCC,
        food=0xFFFF00,
        bg=0x0,
        border=0xFFFFFF,
        info=0x00FF00,
        warn=0xFF0000,
        food_border=0xFF00FF,
    ),
    snake_init=SnakeProps(
        pos=(8, 5),
        length=3,
        direction=choice(["up", "down", "left", "right"]),
        speed=4,
    ),
    scores=(150, 300, 500, 750, 1100, 1500, 2000, 2500),
    motions=dict(right=(1, 0), left=(-1, 0), up=(0, -1), down=(0, 1)),
    operations=dict(
        left=pg.K_a,
        right=pg.K_d,
        up=pg.K_w,
        down=pg.K_s,
        quit=pg.K_ESCAPE,
    ),
)


def convert_color(x: int) -> Tuple[int, int, int]:
    """转化 hex 格式为 tuple 格式."""
    return (x & 0xFF0000) >> 16, (x & 0xFF00) >> 8, (x & 0xFF)


def pos_to_rect(pos: Tuple[int, int], size: int) -> Tuple[int, int, int, int]:
    """转化x, y位置为矩形格式."""
    return pos[0] * size, pos[1] * size, size, size


class Snake:
    __slots__ = ["grids", "speed", "direction"]

    def __init__(self, pos: Tuple[int, int], length: int, speed: int, direction: str) -> None:
        self.speed: int = speed
        self.direction: str = direction

        motion = GS.motions[direction]
        if direction in ("left", "right"):
            self.grids = deque([(x, pos[1]) for x in range(pos[0], pos[0] - length * motion[0], -motion[0])])
        else:
            self.grids = deque([(pos[0], y) for y in range(pos[1], pos[1] - length * motion[1], -motion[1])])

    def draw(self, screen: pg.surface.Surface) -> None:
        for grid in self.grids:
            pg.draw.rect(
                screen,
                GS.colors["snake"],
                pos_to_rect(grid, size=GS.geometry["grid"]),
            )
            pg.draw.rect(
                screen,
                GS.colors["border"],
                pos_to_rect(grid, size=GS.geometry["grid"]),
                width=2,
            )

        if not self.alive:
            pg.draw.rect(
                screen,
                GS.colors["warn"],
                pos_to_rect(self.grids[0], size=GS.geometry["grid"]),
            )

    def move(self) -> None:
        x, y = self.target
        if 0 <= x < GS.geometry["nx"] and 0 <= y < GS.geometry["ny"]:
            self.grids.appendleft((x, y))
            self.grids.pop()
        else:
            self.grids.appendleft(self.grids[0])

    @property
    def target(self) -> Tuple[int, int]:
        motion = GS.motions[self.direction]
        return self.grids[0][0] + motion[0], self.grids[0][1] + motion[1]

    def eat(self) -> None:
        self.grids.appendleft(self.target)

    def set_direction(self, direction: str) -> None:
        neck_direction = [self.grids[0][i] - self.grids[1][i] for i in range(2)]
        if any(neck_direction[i] + GS.motions[direction][i] for i in range(2)):
            self.direction = direction

    @property
    def alive(self) -> bool:
        return len(set(self.grids)) == len(self.grids)


class Game:
    def __init__(self) -> None:
        pg.init()
        pg.display.set_caption(GS.caption)
        self.ttf_large = pg.font.SysFont("simhei", GS.fontsize["large"])
        self.ttf = pg.font.SysFont("simhei", GS.fontsize["normal"])
        self.screen = pg.display.set_mode((GS.geometry["width"], GS.geometry["height"]))
        self.snake: Snake = Snake(**GS.snake_init._asdict())
        self.food: Tuple[int, int] = (0, 0)
        self.score: int = 0
        self.alive: bool = True
        self.reset()

    def reset(self) -> None:
        self.snake, self.score = Snake(**GS.snake_init._asdict()), 0
        self.alive = True
        self.generate_food()

    def generate_food(self) -> None:
        foods = [
            (x, y)
            for x in range(GS.geometry["nx"])
            for y in range(GS.geometry["ny"])
            if (x, y) not in self.snake.grids
            and any(
                [
                    x not in (0, GS.geometry["nx"] - 1),
                    y not in (0, GS.geometry["ny"] - 1),
                ]
            )
        ]
        self.food = choice(foods)

    def run(self) -> None:
        clock = pg.time.Clock()
        start_time = tpc()
        bg, border, food, info, warn, food_border = [
            convert_color(GS.colors[x]) for x in "bg border food info warn food_border".split()
        ]
        boundary_x, boundary_y = (
            GS.geometry["grid"] * GS.geometry["nx"],
            GS.geometry["height"],
        )

        if pg.mixer:
            music = Path(__file__).parent / "assets" / "music" / "snake.wav"
            pg.mixer.music.load(str(music))
            pg.mixer.music.play(-1)

        while self.alive:
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    return
                elif event.type == pg.KEYDOWN:
                    self.check_keydown_events(event)

            self.screen.fill(bg)
            pg.draw.line(self.screen, border, (boundary_x, 0), (boundary_x, boundary_y))
            pg.draw.line(
                self.screen,
                border,
                (boundary_x, 110),
                (GS.geometry["width"], 110),
            )
            self.snake.draw(self.screen)
            pg.draw.rect(self.screen, food, pos_to_rect(self.food, GS.geometry["grid"]))
            pg.draw.rect(
                self.screen,
                food_border,
                pos_to_rect(self.food, GS.geometry["grid"]),
                width=2,
            )

            if self.snake.alive:
                if tpc() - start_time > 1.0 / self.snake.speed:
                    self.snake.move()
                    start_time = tpc()
            else:
                self.screen.blit(self.ttf_large.render("游戏结束!", True, warn), (180, 150))
                self.screen.blit(
                    self.ttf_large.render("输入 '回车' 继续", True, warn),
                    (140, 200),
                )

            self.screen.blit(
                self.ttf.render(f"当前得分: {self.score}", True, info),
                (535, 20),
            )
            self.screen.blit(
                self.ttf.render(f"速度等级: {self.snake.speed}", True, info),
                (535, 60),
            )

            self.screen.blit(self.ttf_large.render(f"操作提示", True, border), (535, 140))
            self.screen.blit(self.ttf.render(f"方向: W/A/S/D", True, info), (535, 200))
            self.screen.blit(self.ttf.render(f"退出: ESC", True, info), (535, 240))

            if self.snake.grids[0] == self.food:
                self.snake.eat()
                self.score += 50
                self.snake.speed = bisect.bisect(GS.scores, self.score) + GS.snake_init.speed
                self.generate_food()

            pg.display.flip()
            clock.tick(GS.fps)

        if pg.mixer:
            pg.mixer.music.fadeout(1000)
        pg.time.wait(1000)

    def check_keydown_events(self, event: pg.event.Event) -> None:
        dirs = dict((v, k) for k, v in GS.operations.items())

        if event.key == GS.operations["quit"]:
            self.alive = False
        elif event.key in GS.operations.values():
            self.snake.set_direction(dirs[event.key])
        elif event.key == pg.K_RETURN and not self.snake.alive:
            self.reset()


def main():
    Game().run()
    pg.quit()


if __name__ == "__main__":
    main()
