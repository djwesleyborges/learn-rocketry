from rocketry import Rocketry
from rocketry.conds import minutely, every

app = Rocketry()


@app.task('every 1 second')
def a_cada_segundo():
    print('Todo segundo')


@app.task(every('1s'))
def a_cada_segundo_():
    print('Todo segundo')


@app.task(minutely)
def a_cada_minuto():
    print('Estou sendo executado a cada minuto')


@app.task('hourly')
def a_cada_hora():
    print('Estou sendo executado a cada hora')


if __name__ == "__main__":
    print('rodando')
    app.run()
