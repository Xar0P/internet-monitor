import matplotlib.pyplot as plt
from matplotlib import animation
import json


def read_data_from_json(filename):
    x = []
    y1 = []
    y2 = []
    y3 = []

    with open(filename, 'r') as file:
        data = json.loads(file.read())

    for d in data:
        y1.append(d['download_speed'])
        y2.append(d['upload_speed'])
        y3.append(d['ping'])
        fulltime = f"{d['hour']}"
        hour = fulltime.split(":")[0] + ":" + fulltime.split(":")[1]
        x.append(hour)

    return x, y1, y2, y3


def update_graph(frame):
    # Atualizar dados a partir do arquivo
    x, y1, y2, y3 = read_data_from_json('limited_report.json')

    # Limpar os gráficos existentes
    for ax in axes.flatten():
        ax.cla()

    # Plotar os novos dados
    axes[0].plot(x, y1)
    axes[0].set_title('Download')
    axes[1].plot(x, y2)
    axes[1].set_title('Upload')
    axes[2].plot(x, y3)
    axes[2].set_title('Ping')

    for ax in axes.flatten():
        ax.set_xticklabels(ax.get_xticklabels(), rotation=45)

    for ax in axes:
        ax.spines['top'].set_visible(False)
        ax.spines['right'].set_visible(False)

    # Ajustar o tamanho do gráfico
    fig.tight_layout()


fig, axes = plt.subplots(nrows=3, ncols=1, figsize=(8, 6))

ani = animation.FuncAnimation(fig, update_graph, interval=1000)

plt.subplots_adjust(hspace=5.0)

plt.show()
