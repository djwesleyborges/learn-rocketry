from rocketry import Rocketry
from rocketry.conds import minutely, every

app = Rocketry()


@app.task('every 1s', execution='async')
async def todo_segundo_a():
    print('A')


@app.task('every 1s', execution='async')
async def todo_segundo_b():
    print('B')


if __name__ == "__main__":
    print('rodando')
    app.run()
