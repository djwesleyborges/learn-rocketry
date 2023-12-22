from datetime import date
from pathlib import Path
from random import randint
from os import makedirs, listdir
from httpx import get, stream
from rocketry import Rocketry
from rocketry.args import Arg, Return
from rocketry.conds import after_success, after_finish, after_fail

API = 'https://pokeapi.co/api/v2/pokemon'
DOLAR = 'https://economia.awesomeapi.com.br/json/daily/USD-BRL/?start_date={}&end_date={}'

app = Rocketry()


@app.param('date')
def date_today() -> str:
    date_today = date.today()
    formated_date = date_today.strftime('%Y%m%d')
    return formated_date


@app.task('every 5s', name='Pega cotação do dolar')
def get_dolar(date=Arg('date')) -> str:
    # def get_dolar(date=Arg('dater')) -> str:
    response = get(DOLAR.format(date, date)).json()[0]['high']
    return response.replace('.', '')[:3]


@app.task(after_fail(get_dolar))
def get_dolar_fail(date=Arg('date')):
    print(f'Erro no dia {date}')
    print('Enviando email para o responsavel')


@app.task(after_success(get_dolar))
def get_pokemon_json(number=Return(get_dolar)):
    response = get(f'{API}/{number}').json()
    return response


@app.task(after_success(get_pokemon_json))
def get_pokemon_sprite_url(poke_json=Return(get_pokemon_json)):
    return (
        poke_json['sprites']['front_default'],
        poke_json['name']
    )


@app.task(after_success(get_pokemon_sprite_url))
def download_sprite(
        poke_data=Return(get_pokemon_sprite_url),
        poke_number=Return(get_dolar),
        download=Arg('download')
):
    url, name = poke_data
    file = Path(f'{poke_number}_{name}.png')
    if not download:
        return file
    with open(file, 'wb') as download_file:
        with stream('GET', url) as s:
            for chunk in s.iter_bytes():
                download_file.write(chunk)
    return file


@app.task(after_finish(download_sprite))
def move_sprite(path: Path = Return(download_sprite)):
    makedirs('sprites', exist_ok=True)
    pasta = Path('sprites')
    path.rename(pasta / path)


@app.param('download')
def download(val=Return(get_dolar)):
    sprites: list[str] = listdir('sprites')
    for sprite in sprites:
        if sprite.startswith(val):
            print(f'{val=} é repetido')
            return False
    else:
        return True


app.run()
