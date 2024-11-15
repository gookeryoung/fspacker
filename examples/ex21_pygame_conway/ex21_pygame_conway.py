"""
康威生命游戏（Conway's Game of Life）是一种由英国数学家约翰·康威在1970年发明的细胞自动机。这个游戏使用一个二维的网格，每个
格子可以是“活”或者“死”状态。每个格子的状态根据周围格子的状态进行更新，遵循以下规则：

如果一个活细胞周围有少于两个活细胞，它将因为“孤独”而死去。
如果一个活细胞周围有两个或三个活细胞，它将保持活状态。
如果一个活细胞周围有超过三个活细胞，它将因为“拥挤”而死去。
如果一个死细胞周围正好有三个活细胞，它将变成活细胞。

使用 pygame 库设计康威生命游戏的基本步骤如下：

初始化 pygame：设置屏幕大小和颜色。
定义游戏参数：包括网格大小、细胞大小、更新速度等。
创建网格：随机生成初始状态的网格。
更新逻辑：根据康威生命游戏的规则更新网格状态。
绘制网格：将更新后的网格绘制到屏幕上。
事件处理：处理用户输入，如暂停、重启等。
"""

import numpy as np
import pygame as pg


class Cells:
    PREDICT_ARR = np.array([list("000100000"), list("001100000")], dtype=np.uint8)

    def __init__(self, nx: int, ny: int, screen_width: int):
        self.nx, self.ny = nx, ny
        self.size = screen_width // nx
        self.cells = np.random.choice((0, 1), (nx, ny))

    def count_neighbours(self, x: int, y: int):
        return sum(
            [
                self.cells[(x - 1) % self.nx, (y - 1) % self.ny],
                self.cells[(x - 1) % self.nx, y % self.ny],
                self.cells[(x - 1) % self.nx, (y + 1) % self.ny],
                self.cells[x % self.nx, (y - 1) % self.ny],
                self.cells[x % self.nx, (y + 1) % self.ny],
                self.cells[(x + 1) % self.nx, (y - 1) % self.ny],
                self.cells[(x + 1) % self.nx, y % self.ny],
                self.cells[(x + 1) % self.nx, (y + 1) % self.ny],
            ]
        )

    def predict_life(self, cell: int, neighbours: int) -> int:
        return self.PREDICT_ARR[cell][neighbours]

    def update_logic(self):
        new_cells = np.zeros((self.nx, self.ny), dtype=np.uint8)
        for row in range(len(self.cells)):
            for col in range(len(self.cells[0])):
                total = self.count_neighbours(col, row)
                new_cells[row][col] = self.predict_life(self.cells[row][col], total)
        self.cells = new_cells

    def draw(self, surface: pg.Surface):
        surface.fill("black")
        for row in range(len(self.cells)):
            for col in range(len(self.cells[0])):
                rect = [col * self.size, row * self.size, self.size, self.size]
                if self.cells[row][col] == 1:
                    pg.draw.rect(surface, "green", rect)
                pg.draw.rect(surface, "white", rect, 1)


def main():
    pg.init()
    sw, sh, fps = 800, 600, 60
    screen = pg.display.set_mode((sw, sh))
    clock = pg.time.Clock()
    cells = Cells(60, 80, screen_width=sw)

    # 主循环
    running = True
    while running:
        for event in pg.event.get():
            if event.type == pg.QUIT:
                running = False

        cells.update_logic()
        cells.draw(screen)
        pg.display.flip()
        clock.tick(fps)  # 控制更新速度
    pg.quit()


if __name__ == "__main__":
    main()
