import matplotlib.pyplot as plt
import numpy as np

# Create initial data
N = 5
values1 = np.random.rand(N)
values2 = np.random.rand(N)
labels = ['Category 1', 'Category 2', 'Category 3', 'Category 4', 'Category 5']

# Create grouped bar chart
fig, ax = plt.subplots()
ax.set_title('Grouped Bar Chart')
ax.set_xlabel('X Label')
ax.set_ylabel('Y Label')
ax.set_xticks(np.arange(N))
ax.set_xticklabels(labels)
bar_width = 0.35
opacity = 0.8
for i in range(1,145):
    bar1 = ax.bar(np.arange(N), values1, bar_width, alpha=opacity, color='b', label='Group 1')
    bar2 = ax.bar(np.arange(N) + bar_width, values2, bar_width, alpha=opacity, color='g', label='Group 2')
ax.legend()

# Update data every one second
while True:
    # Generate new data
    values1 = np.random.rand(N)
    values2 = np.random.rand(N)
    
    # Update grouped bar chart
    for i, rect in enumerate(bar1):
        rect.set_height(values1[i])
    for i, rect in enumerate(bar2):
        rect.set_height(values2[i])
    
    fig.canvas.draw()
    plt.pause(1)  # Pause for one second to update the plot
