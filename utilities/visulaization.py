import matplotlib.pyplot as plt
import numpy as np

# Data extracted from the image
labels = ['HNSWLib', 'ChromaDB']
query_time = [0.00000020, 0.001983]
memory_before = [35.66, 92.56]
memory_after = [35.70, 92.95]
index_size = [0.06, 0.00]

x = np.arange(len(labels))  # label locations
width = 0.25  # width of the bars

# Create subplots
fig, ax = plt.subplots(3, 1, figsize=(8, 10))

# Plot query time
ax[0].bar(labels, query_time, color=['skyblue', 'lightcoral'])
ax[0].set_title('Average Query Time (100 queries, k=10)')
ax[0].set_ylabel('Time (seconds)')

# Plot memory usage before and after
ax[1].bar(x - width/2, memory_before, width, label='Before Query', color='orange')
ax[1].bar(x + width/2, memory_after, width, label='After Query', color='green')
ax[1].set_title('Memory Usage Comparison')
ax[1].set_ylabel('Memory (MB)')
ax[1].set_xticks(x)
ax[1].set_xticklabels(labels)
ax[1].legend()

# Plot index size
ax[2].bar(labels, index_size, color=['purple', 'gray'])
ax[2].set_title('Index Size')
ax[2].set_ylabel('Size (MB)')

plt.tight_layout()
plt.show()
