import matplotlib.pyplot as plt
import random


def draw_graph(item_id):
    fig, ax = plt.subplots()
    x_ax = range(1, 284)
    y_ax = [x * random.randint(436, 875) for x in x_ax]
    ax.plot(x_ax, y_ax)
    plt.savefig('main/static/graph/item{}.png'.format(item_id))
    return
