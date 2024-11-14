import pandas as pd
import matplotlib.pyplot as plt
import numpy as np


def main():
    # 创建一个示例数据集
    np.random.seed(0)
    data = {
        "A": np.random.randn(100),
        "B": np.random.randn(100) + 2,
        "C": np.random.randn(100) - 2,
    }

    df = pd.DataFrame(data)

    # 绘制箱线图
    df.plot(kind="box", title="Box Plot")
    plt.ylabel("Value")
    plt.show()


if __name__ == "__main__":
    main()
