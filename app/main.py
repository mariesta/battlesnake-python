import bottle
import os


MY_SNAKE_ID = '3c7ea45f-9741-4324-8071-6cadd06b5307'
MY_SNAKE_NAME = 'unicorn snake'


@bottle.route('/static/<path:path>')
def static(path):
    return bottle.static_file(path, root='static/')


@bottle.get('/')
def index():
    head_url = '%s://%s/static/head.png' % (
        bottle.request.urlparts.scheme,
        bottle.request.urlparts.netloc
    )

    return {
        'color': '#00ff00',
        'head': head_url
    }


@bottle.post('/start')
def start():
    return {
        'taunt': 'Unicorn snake here!'
    }


@bottle.post('/move')
def move():
    data = bottle.request.json
    snakes = data['snakes']
    head = None
    tail = None
    food_list = data['food']
    gold_position = []
    if 'gold' in data:
        gold_position = data['gold']
    ncols = data['width']
    nrows = data['height']

    for snake in snakes:
        if snake['name'] == MY_SNAKE_NAME:
            head = snake['coords'][0]
            tail = snake['coords']

    if food_list:
        food_position = get_closest_food_position(head, food_list, gold_position)
        action = decide_action(head, food_position, tail, ncols, nrows, snakes)
    else:
        action = 'north'

    return {
        'move': action,
        'taunt': 'You won\'t catch me. I am too fabulous!'
    }


def decide_action(head, food_position, tail, ncols, nrows, snakes):
    if head[0] < food_position[0]:
        new_position = [head[0] + 1, head[1]]
        if is_safe(new_position, tail, ncols, nrows, snakes):
            return 'east'

    elif head[0] > food_position[0]:
        new_position = [head[0] - 1, head[1]]
        if is_safe(new_position, tail, ncols, nrows, snakes):
            return 'west'

    elif head[1] < food_position[1]:
        new_position = [head[0], head[1] + 1]
        if is_safe(new_position, tail, ncols, nrows, snakes):
            return 'south'

    return 'north'


def is_safe(new_position, tail, ncols, nrows, snakes):
    x = new_position[0]
    y = new_position[1]
    occupied_tiles = []

    # Check the walls
    if x >= ncols or x < 1:
        return False

    if y >= nrows or y < 1:
        return False

    # Check other snakes
    for snake in snakes:
        if snake['id'] != MY_SNAKE_ID:
            occupied_tiles = occupied_tiles + snake['coords']

    return new_position not in tail and new_position not in occupied_tiles


def get_closest_food_position(head, food_list, gold_position):
    closest_food = None
    smallest_result = 999
    snack_list = food_list + gold_position
    for food in snack_list:
        print food
        print head
        x_dis = abs(food[0] - head[0])
        y_dis = abs(food[1] - head[1])
        result = x_dis + y_dis
        if smallest_result > result:
            smallest_result = result
            closest_food = food

    return closest_food


@bottle.post('/end')
def end():
    return {
        'taunt': 'I will be back!'
    }


# Expose WSGI app (so gunicorn can find it)
application = bottle.default_app()
if __name__ == '__main__':
    bottle.run(application, host=os.getenv('IP', '0.0.0.0'), port=os.getenv('PORT', '8080'))
