import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

file_path = 'diabetes.csv'
df = pd.read_csv(file_path)

correlation_matrix = df.corr()

target_correlation = correlation_matrix['Diabetes_012'].sort_values(ascending=False)

print("korelacja")
print(target_correlation)

plt.figure(figsize=(20, 16))
sns.heatmap(correlation_matrix, annot=True, fmt=".2f", cmap='coolwarm', linewidths=0.5)
plt.title('mapa korelacji')
plt.show()