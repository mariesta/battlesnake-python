import bottle
import os
import math


MY_SNAKE_ID = '3c7ea45f-9741-4324-8071-6cadd06b5307'


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
    snakes, board_sizes = data['snakes'], data['board']
    width = board_sizes['width']
    height = board_sizes['height']
    head_position = None
    health = None
    food_list = data['food']

    for snake in snakes:
        if snake['id'] == MY_SNAKE_ID:
            head_position = snake['coords'][0]
            health = snake['health']

    food_position = get_closest_food_position(head_position, food_list)
    action = decide_action(head_position, food_position)

    # TODO: Do things with data

    return {
        'move': action,
        'taunt': 'battlesnake-python!'
    }


def decide_action(head_position, food_position):
    head_x = head_position[0]
    head_y = head_position[1]
    food_x = food_position[0]
    food_y = food_position[1]

    if head_x < food_x:
        return 'east'

    elif head_x > food_x:
        return 'west'

    elif head_y < food_y:
        return 'south'

    return 'north'


def get_closest_food_position(head_position, food_list):
    closest_food = None
    smallest_result = 100
    for food in food_list:
        food_x = food[0]
        food_y = food[1]
        head_x = head_position[0]
        head_y = head_position[1]
        result = math.sqrt(math.pow((food_x - head_x), 2) + math.pow((food_y - head_y), 2))
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
