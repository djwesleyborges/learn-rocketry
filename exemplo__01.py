from rocketry import Rocketry
from rocketry.conds import minutely, every

app = Rocketry()


@app.task('minutely after 10')
def restrições():
    print('Minuto depois do 10')


if __name__ == "__main__":
    print('rodando')
    app.run()
