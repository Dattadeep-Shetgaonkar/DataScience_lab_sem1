
import pandas as pd
import matplotlib.pyplot as plt

df = pd.read_csv(r"C:\Users\shetg\OneDrive\Desktop\Data Science\Q11_netflix_matplotlip\netflix_titles.csv")

movies = df[df['type'] == 'Movie']
movies['duration'] = movies['duration'].str.replace(' min', '').astype(float)
avg_duration = movies.groupby('country')['duration'].mean().head(10)

avg_duration.plot(kind='bar')
plt.xlabel('Country')
plt.ylabel('Average Duration (minutes)')
plt.title('Average Movie Duration (First 10 Countries)')
plt.show()