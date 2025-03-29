import matplotlib.pyplot as plt
import numpy as np

def generate_gradient(value):
    if value > 60:
        colors = [0.3, 0, 0, 1]
    elif 30 <= value <= 60:
        colors = [value / 60, value / (2 * 60), 0, 1]
    elif 0 <= value < 30:
        colors = [value / (2 * 30), 0, value / 30, 1]

    return colors

value = float(input("Enter a value: "))

if 0 <= value <= 100:
    color = generate_gradient(value)

    fig, ax = plt.subplots(figsize=(6, 1))
    gradient = np.linspace(0, 1, 256).reshape(1, -1)
    ax.imshow(gradient, aspect='auto', cmap='RdYlBu', vmin=0, vmax=1)
    ax.set_axis_off()
    plt.show()
else:
    print("Invalid input. Please enter a value between 0 and 100.")