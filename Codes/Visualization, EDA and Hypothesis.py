# eda_analysis.py

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import pearsonr, ttest_ind

# 1) Load cleaned CSVs
season_labels = ['2000-2001','2001-2002','2020-2021','2021-2022']
dfs = []
for lbl in season_labels:
    df = pd.read_csv(f"cleaned_{lbl}.csv", parse_dates=['Date'])
    dfs.append(df)
all_df = pd.concat(dfs, ignore_index=True)

# 2) Histograms of goals per season
for lbl in season_labels:
    df = all_df[all_df['Season'] == lbl]
    avg_g = df['TotalGoals'].mean()
    plt.figure(figsize=(6,4))
    plt.hist(df['TotalGoals'],
             bins=range(0, int(df['TotalGoals'].max())+2),
             color='skyblue', alpha=0.7)
    plt.title(f"{lbl}: Goals Distribution (avg={avg_g:.2f})")
    plt.xlabel("Goals per Match"); plt.ylabel("Frequency")
    plt.grid(axis='y', alpha=0.5)
    plt.show()

# 3) Weather Impact
print("Raw preciptype counts & avg goals:")
print(all_df['preciptype'].fillna('None').value_counts(), "\n")
print(all_df.groupby(all_df['preciptype'].fillna('None'))['TotalGoals']
               .mean().round(2), "\n")

for lbl in season_labels:
    df = all_df[all_df['Season'] == lbl]
    stats = df.groupby('PrecipBin')['TotalGoals'] \
              .mean().reindex(['Clear','Light','Moderate','Heavy'])
    # ordinal corr
    ord_map = {'Clear':0,'Light':1,'Moderate':2,'Heavy':3}
    r_o, p_o = pearsonr(df['PrecipBin'].map(ord_map),
                        df['TotalGoals'])
    plt.figure(figsize=(6,4))
    stats.plot(kind='bar', color='salmon', alpha=0.8)
    plt.title(f"{lbl}: Avg Goals by Precip\n(r={r_o:.2f}, p={p_o:.3f})")
    plt.xlabel("Precipitation"); plt.ylabel("Avg Goals")
    plt.grid(axis='y', alpha=0.5)
    plt.show()

# 4) Temperature vs Goals
for lbl in season_labels:
    df = all_df[all_df['Season'] == lbl]
    r_t, p_t = pearsonr(df['temp'], df['TotalGoals'])
    plt.figure(figsize=(6,4))
    plt.scatter(df['temp'], df['TotalGoals'],
                color='C3', alpha=0.6)
    m,b = np.polyfit(df['temp'], df['TotalGoals'],1)
    xs = np.linspace(df['temp'].min(), df['temp'].max(),100)
    plt.plot(xs, m*xs+b, color='red', lw=1)
    plt.title(f"{lbl}: Temp vs Goals (r={r_t:.2f}, p={p_t:.3f})")
    plt.xlabel("Temp (°C)"); plt.ylabel("Total Goals")
    plt.grid(alpha=0.5)
    plt.show()

# 5) Attendance vs Goals (with guard)
for lbl in season_labels:
    df = all_df[all_df['Season'] == lbl]
    if 'Attendance' not in df.columns:
        continue
    sub = df.dropna(subset=['Attendance','TotalGoals'])
    sub['Attendance'] = pd.to_numeric(sub['Attendance'],
                                      errors='coerce')
    if len(sub) < 2:
        print(f"{lbl}: not enough attendance data to compute correlation\n")
        continue
    r_a, p_a = pearsonr(sub['Attendance'], sub['TotalGoals'])
    plt.figure(figsize=(6,4))
    plt.scatter(sub['Attendance'], sub['TotalGoals'],
                color='green', alpha=0.6)
    m,b = np.polyfit(sub['Attendance'], sub['TotalGoals'],1)
    xs = np.linspace(sub['Attendance'].min(),
                     sub['Attendance'].max(),100)
    plt.plot(xs, m*xs+b, color='black', lw=1)
    plt.title(f"{lbl}: Attendance vs Goals\n(r={r_a:.2f}, p={p_a:.3f})")
    plt.xlabel("Attendance"); plt.ylabel("Total Goals")
    plt.grid(alpha=0.5)
    plt.show()

# 6) VAR Era Comparison & t-test
pre = all_df[all_df['Season'].isin(['2000-2001','2001-2002'])]['TotalGoals']
post= all_df[all_df['Season'].isin(['2020-2021','2021-2022'])]['TotalGoals']
t_v, p_v = ttest_ind(post, pre, equal_var=False)
print(f"Pre-VAR avg={pre.mean():.2f}, Post-VAR avg={post.mean():.2f}")
print(f"t={t_v:.2f}, p={p_v:.3f}\n")
plt.figure(figsize=(5,4))
plt.bar(['Pre-VAR','Post-VAR'], [pre.mean(),post.mean()],
        color=['navy','teal'], alpha=0.7)
plt.title("Pre-VAR vs Post-VAR Avg Goals")
plt.ylabel("Avg Goals")
plt.grid(axis='y', alpha=0.5)
plt.show()

# 7) Time-of-Day (Afternoon vs Evening) for 20/21 & 21/22
tdf = all_df[all_df['Season'].isin(['2020-2021','2021-2022'])]
if 'TimeBin' in tdf:
    sel = tdf[tdf['TimeBin'].isin(['Afternoon','Evening'])]
    stats_td = sel.groupby('TimeBin')['TotalGoals'] \
                 .agg(['mean','count'])
    print("Afternoon vs Evening (20/21 & 21/22):")
    print(stats_td, "\n")
    plt.figure(figsize=(6,4))
    stats_td['mean'].plot(kind='bar',
                         color=['#C0504D','#9BBB59'],
                         alpha=0.8)
    plt.title("20/21 & 21/22: Avg Goals by Time of Day")
    plt.ylabel("Avg Goals")
    plt.grid(axis='y', alpha=0.5)
    plt.show()

# 8) Hypothesis Test: Heavy vs Clear rain
heavy = all_df[all_df['PrecipBin']=='Heavy']['TotalGoals']
clear = all_df[all_df['PrecipBin']=='Clear']['TotalGoals']
t_hc, p_hc = ttest_ind(heavy, clear, equal_var=False)
print("Heavy vs Clear rain:")
print(f" Heavy(n={len(heavy)}) avg={heavy.mean():.2f}")
print(f" Clear(n={len(clear)}) avg={clear.mean():.2f}")
print(f"t={t_hc:.2f}, p={p_hc:.3f} → "
      f"{'Reject H₀' if p_hc<0.05 else 'Fail to reject H₀'}")
