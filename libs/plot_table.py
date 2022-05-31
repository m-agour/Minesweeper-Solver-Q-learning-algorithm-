import numpy as np
import seaborn as sns; sns.set()
import matplotlib.pyplot as plt

name = f"{3}x{1}_{1}"

Q_table = np.load(f'../data/{name}_Q_table.npz')['q_table']
# Q_table = np.zeros((27, 3), dtype='float16')
ax = sns.heatmap(Q_table, annot=True, cbar=False, vmin=-1, vmax=1)


plt.title("Q-Table ", fontsize=22)
plt.gcf().set_size_inches(4, 10)
plt.tight_layout()
plt.savefig("visualize_numpy_array_01.png",  dpi=700)

plt.show()