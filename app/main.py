import bottle
import os


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
    snakes = data['snakes']
    head = None
    tail = None
    food_list = data['food']

    for snake in snakes:
        if snake['id'] == MY_SNAKE_ID:
            head = snake['coords'][0]
            tail = snake['coords']

    print "HEAD POSITION: %s" % head
    print "Food List: %s" % food_list

    if food_list and len(food_list) > 1:
        food_position = get_closest_food_position(head, food_list)
        action = decide_action(head, food_position, tail)
    elif food_list:
        action = decide_action(head, food_list[0], tail)
    else:
        action = 'north'

    return {
        'move': action,
        'taunt': 'You won\'t catch me. I am too fabulous!'
    }


def decide_action(head, food_position, tail):
    if head[0] < food_position[0]:
        new_position = [head[0] + 1, head[1]]
        if is_safe(new_position, tail):
            return 'east'

    elif head[0] > food_position[0]:
        new_position = [head[0] - 1, head[1]]
        if is_safe(new_position, tail):
            return 'west'

    elif head[1] < food_position[1]:
        new_position = [head[0], head[1] + 1]
        if is_safe(new_position, tail):
            return 'south'

    return 'north'


def is_safe(new_position, tail):
    return new_position not in tail


def get_closest_food_position(head, food_list):
    closest_food = None
    smallest_result = 999
    for food in food_list:
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
