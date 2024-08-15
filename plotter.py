import os
import re
import matplotlib.pyplot as plt
from scipy.stats import linregress

def read_capture_rates(file_path):
    rates = []
    with open(file_path, 'r') as file:
        for line in file:
            try:
                # Extract the float value from the line
                rate = float(line.strip().split(',')[-1].strip(')'))
                rates.append(rate)
            except ValueError:
                # Skip lines that cannot be converted to float
                continue
    return rates

def calculate_average(rates):
    return sum(rates) / len(rates) if rates else 0

def plot_average_capture_rates(directory):
    if not os.path.exists(directory):
        raise FileNotFoundError(f"The directory '{directory}' does not exist.")
    
    averages = {}
    hp_values = []

    for filename in os.listdir(directory):
        if filename.endswith('.txt'):
            hp = int(re.search(r'\d+', filename).group())
            file_path = os.path.join(directory, filename)
            rates = read_capture_rates(file_path)
            average = calculate_average(rates)
            averages[hp] = average
            hp_values.append(hp)

    # Sort hp_values and corresponding averages
    hp_values.sort()
    sorted_averages = [averages[hp] for hp in hp_values]

    # Perform linear regression
    slope, intercept, r_value, p_value, std_err = linregress(hp_values, sorted_averages)
    print(f"Slope of the linear regression line: {slope}")

    # Plot the original data
    plt.plot(hp_values, sorted_averages, marker='o', label='Original Data')
    plt.xlabel('HP')
    plt.ylabel('Average Capture Rate')
    plt.title('Snorlax, health state = none: Average Capture Rate vs HP')
    plt.xticks(range(10, max(hp_values) + 10, 10))
    plt.grid(True, axis='y')

    # Plot the regression line
    regression_line = [slope * x + intercept for x in hp_values]
    plt.plot(hp_values, regression_line, color='red', label='Regression Line')

    plt.legend()
    plt.tight_layout()
    plt.show()

# Example usage
plot_average_capture_rates('Data')