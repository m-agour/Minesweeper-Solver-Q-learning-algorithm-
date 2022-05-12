from matplotlib import pyplot as plt


def graph_stats(stats, name):
    # episode - win_rate
    episodes = stats['episode']
    win_rate = stats['win_rate']
    plt.plot(episodes, win_rate, color='red')
    plt.title('Win Rate', fontsize=14)
    plt.xlabel('Episode', fontsize=14)
    plt.ylabel('Winning rate', fontsize=14)
    plt.grid(True)
    plt.savefig(f"data/{name}_win_rate.png")

    plt.clf()

    epsilon = stats['epsilon']
    plt.plot(episodes, epsilon, color='brown')
    plt.title('Epsilon value', fontsize=14)
    plt.xlabel('Episode', fontsize=14)
    plt.ylabel('Epsilon', fontsize=14)
    plt.grid(True)
    plt.savefig(f"data/{name}_epsilon.png")

    plt.clf()

    progress = stats['m_progress']
    plt.plot(episodes, progress, color='blue')
    plt.title('Median Progress', fontsize=14)
    plt.xlabel('Episode', fontsize=14)
    plt.ylabel('Progress', fontsize=14)
    plt.grid(True)
    plt.savefig(f"data/{name}_progress.png")

    plt.clf()

    reward = stats['m_reward']
    plt.plot(episodes, reward, color='green')
    plt.title('Median Reward', fontsize=14)
    plt.xlabel('Episode', fontsize=14)
    plt.ylabel('Reward', fontsize=14)
    plt.grid(True)
    plt.savefig(f"data/{name}_reward.png")

    plt.clf()

    moves = stats['m_moves']
    plt.plot(episodes, moves, color='teal')
    plt.title('Median number of moves to win a game', fontsize=14)
    plt.xlabel('Episode', fontsize=14)
    plt.ylabel('No. moves to win', fontsize=14)
    plt.grid(True)
    plt.savefig(f"data/{name}_moves.png")

    plt.clf()