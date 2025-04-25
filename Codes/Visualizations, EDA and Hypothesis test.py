import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import pearsonr, ttest_ind

# Load all four seasons of cleaned data
seasons = ['2000-2001', '2001-2002', '2020-2021', '2021-2022']
frames = []
for season in seasons:
    path = f"cleaned_{season}.csv"
    df = pd.read_csv(path, parse_dates=['Date'])
    frames.append(df)
all_data = pd.concat(frames, ignore_index=True)

# 1. Plot goal distributions for each season
for season, df in zip(seasons, frames):
    avg_goals = df['TotalGoals'].mean()
    plt.figure(figsize=(6, 4))
    plt.hist(df['TotalGoals'],
             bins=range(0, int(df['TotalGoals'].max()) + 2),
             color='skyblue', alpha=0.7)
    plt.title(f"{season}: Goals per Match (avg {avg_goals:.2f})")
    plt.xlabel("Goals in Match")
    plt.ylabel("Number of Matches")
    plt.grid(axis='y', alpha=0.5)
    plt.show()

# 2. Weather impact: average goals by precipitation type
print("Precipitation counts & average goals:")
precip_counts = all_data['preciptype'].fillna('None').value_counts()
precip_avgs   = all_data.groupby(all_data['preciptype'].fillna('None'))['TotalGoals']\
                        .mean().round(2)
print(precip_counts, "\n", precip_avgs, "\n")

for season in seasons:
    df = all_data[all_data['Season'] == season]
    avg_by_bin = df.groupby('PrecipBin')['TotalGoals']\
                   .mean().reindex(['Clear','Light','Moderate','Heavy'])
    # compute ordinal correlation
    mapping = {'Clear': 0, 'Light': 1, 'Moderate': 2, 'Heavy': 3}
    r, p = pearsonr(df['PrecipBin'].map(mapping), df['TotalGoals'])
    plt.figure(figsize=(6, 4))
    avg_by_bin.plot(kind='bar', color='salmon', alpha=0.8)
    plt.title(f"{season}: Avg Goals by Precipitation (r={r:.2f}, p={p:.3f})")
    plt.xlabel("Precipitation")
    plt.ylabel("Average Goals")
    plt.grid(axis='y', alpha=0.5)
    plt.show()

# 3. Temperature vs goals scatter with regression line
for season in seasons:
    df = all_data[all_data['Season'] == season]
    r, p = pearsonr(df['temp'], df['TotalGoals'])
    plt.figure(figsize=(6, 4))
    plt.scatter(df['temp'], df['TotalGoals'], color='C3', alpha=0.6)
    m, b = np.polyfit(df['temp'], df['TotalGoals'], 1)
    xs = np.linspace(df['temp'].min(), df['temp'].max(), 100)
    plt.plot(xs, m*xs + b, color='red', lw=1)
    plt.title(f"{season}: Temp vs Goals (r={r:.2f}, p={p:.3f})")
    plt.xlabel("Temperature (°C)")
    plt.ylabel("Goals Scored")
    plt.grid(alpha=0.5)
    plt.show()

# 4. Attendance effect if available
for season in seasons:
    df = all_data[all_data['Season'] == season]
    if 'Attendance' not in df.columns:
        continue
    subset = df.dropna(subset=['Attendance','TotalGoals'])
    subset['Attendance'] = pd.to_numeric(subset['Attendance'], errors='coerce')
    if len(subset) < 2:
        print(f"{season}: not enough attendance data\n")
        continue
    r, p = pearsonr(subset['Attendance'], subset['TotalGoals'])
    plt.figure(figsize=(6, 4))
    plt.scatter(subset['Attendance'], subset['TotalGoals'],
                color='green', alpha=0.6)
    m, b = np.polyfit(subset['Attendance'], subset['TotalGoals'], 1)
    xs = np.linspace(subset['Attendance'].min(), subset['Attendance'].max(), 100)
    plt.plot(xs, m*xs + b, color='black', lw=1)
    plt.title(f"{season}: Attendance vs Goals (r={r:.2f}, p={p:.3f})")
    plt.xlabel("Attendance")
    plt.ylabel("Goals Scored")
    plt.grid(alpha=0.5)
    plt.show()

# 5. Compare pre-VAR and post-VAR averages with t-test
pre = all_data.query("Season in ['2000-2001','2001-2002']")['TotalGoals']
post = all_data.query("Season in ['2020-2021','2021-2022']")['TotalGoals']
t_stat, p_val = ttest_ind(post, pre, equal_var=False)
print(f"Pre-VAR avg={pre.mean():.2f}, Post-VAR avg={post.mean():.2f}")
print(f"t={t_stat:.2f}, p={p_val:.3f}\n")
plt.figure(figsize=(5, 4))
plt.bar(['Pre-VAR','Post-VAR'], [pre.mean(), post.mean()],
        color=['navy','teal'], alpha=0.7)
plt.title("Avg Goals: Pre-VAR vs Post-VAR")
plt.ylabel("Avg Goals")
plt.grid(axis='y', alpha=0.5)
plt.show()

# 6. Time-of-day breakdown for recent seasons
recent = all_data.query("Season in ['2020-2021','2021-2022']")
if 'TimeBin' in recent:
    breakdown = recent[recent['TimeBin'].isin(['Afternoon','Evening'])] \
                .groupby('TimeBin')['TotalGoals'] \
                .agg(['mean','count'])
    print("Afternoon vs Evening (20/21 & 21/22):")
    print(breakdown, "\n")
    plt.figure(figsize=(6,4))
    breakdown['mean'].plot(kind='bar',
                           color=['#C0504D','#9BBB59'], alpha=0.8)
    plt.title("20/21 & 21/22: Avg Goals by Time of Day")
    plt.ylabel("Average Goals")
    plt.grid(axis='y', alpha=0.5)
    plt.show()

# 7. Test heavy rain vs clear weather
heavy = all_data.query("PrecipBin=='Heavy'")['TotalGoals']
clear = all_data.query("PrecipBin=='Clear'")['TotalGoals']
t_h, p_h = ttest_ind(heavy, clear, equal_var=False)
print("Heavy vs Clear rain:")
print(f"  Heavy games (n={len(heavy)}) avg={heavy.mean():.2f}")
print(f"  Clear games (n={len(clear)}) avg={clear.mean():.2f}")
print(f"  t={t_h:.2f}, p={p_h:.3f} ->",
      "Reject H₀" if p_h < 0.05 else "Fail to reject H₀")

# 8. Referee impact on scoring
ref_counts = all_data['Referee'].value_counts()
qualified = ref_counts[ref_counts >= 10].index
ref_table = (all_data[all_data['Referee'].isin(qualified)]
             .groupby('Referee')['TotalGoals']
             .agg(['mean','count'])
             .sort_values('count', ascending=False))
print("\nReferees with ≥10 matches:\n", ref_table, "\n")

# Plot top 5 by number of matches
top5 = ref_table.head(5)
plt.figure(figsize=(6,4))
plt.bar(top5.index, top5['mean'], color='purple', alpha=0.8)
plt.title("Avg Goals per Match – Top 5 Referees")
plt.xlabel("Referee")
plt.ylabel("Average Goals")
plt.xticks(rotation=45, ha='right')
plt.grid(axis='y', alpha=0.5)
plt.tight_layout()
plt.show()
