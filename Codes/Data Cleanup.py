import pandas as pd

# 1) Helper functions
london_teams = [
    'Arsenal','Chelsea','Crystal Palace','Fulham',
    'Tottenham Hotspur','West Ham United'
]
manchester_teams = ['Man City','Man United']

def assign_city(team):
    """Map team to London/Manchester/Other."""
    if team in london_teams:
        return 'London'
    if team in manchester_teams:
        return 'Manchester'
    return 'Other'

def precip_category(mm):
    """Bin raw precip mm into Clear/Light/Moderate/Heavy."""
    if pd.isna(mm) or mm == 0:
        return 'Clear'
    if mm <= 1:
        return 'Light'
    if mm <= 3:
        return 'Moderate'
    return 'Heavy'

def tod_bin(hour):
    """Bin match start hour into Afternoon (<17) or Evening (>=17)."""
    return 'Afternoon' if hour < 17 else 'Evening'

# 2) Season configuration
seasons = [
    {
        'label': '2000-2001',
        'prem':  'Prem 2000-2001.csv',
        'wl':    'London Weather 2000-2001.csv',
        'wm':    'Manchester Weather 2000-2001.csv',
        'fmt':   '%d/%m/%y'
    },
    {
        'label': '2001-2002',
        'prem':  'Prem 2001-2002.csv',
        'wl':    'London Weather 2001-2002.csv',
        'wm':    'Manchester Weather 2001-2002.csv',
        'fmt':   '%d/%m/%y'
    },
    {
        'label': '2020-2021',
        'prem':  'Prem 2020-2021.csv',
        'wl':    'London Weather 2020-2021.csv',
        'wm':    'Manchester Weather 2020-2021.csv',
        'fmt':   '%d/%m/%Y'
    },
    {
        'label': '2021-2022',
        'prem':  'Prem 2021-2022.csv',
        'wl':    'London Weather 2021-2022.csv',
        'wm':    'Manchester Weather 2021-2022.csv',
        'fmt':   '%d/%m/%Y'
    }
]

# 3) Process each season
for s in seasons:
    # Load Premier League matches
    prem = pd.read_csv(s['prem'])
    prem['Date'] = pd.to_datetime(prem['Date'],
                                  format=s['fmt'], dayfirst=True)
    prem['HomeCity'] = prem['HomeTeam'].apply(assign_city)
    prem = prem[prem['HomeCity'].isin(['London','Manchester'])]

    # Load weather
    wl = pd.read_csv(s['wl'])
    wl['Date'] = pd.to_datetime(wl['datetime'])
    wm = pd.read_csv(s['wm'])
    wm['Date'] = pd.to_datetime(wm['datetime'])

    # Merge London and Manchester separately
    lon = pd.merge(prem[prem['HomeCity']=='London'], wl,
                   on='Date', how='left')
    man = pd.merge(prem[prem['HomeCity']=='Manchester'], wm,
                   on='Date', how='left')
    df = pd.concat([lon, man], ignore_index=True)

    # Compute total goals
    df['TotalGoals'] = df['FTHG'] + df['FTAG']

    # Drop any rows missing key weather
    df = df.dropna(subset=['temp','precip'])

    # Bin precipitation
    df['PrecipBin'] = df['precip'].apply(precip_category)

    # Parse attendance numeric
    if 'Attendance' in df.columns:
        df['Attendance'] = pd.to_numeric(df['Attendance'],
                                         errors='coerce')

    # Parse time-of-day if available
    if 'Time' in df.columns:
        df['Time'] = pd.to_datetime(df['Time'],
                                    format='%H:%M').dt.time
        df['Hour'] = df['Time'].apply(lambda t: t.hour)
        df['TimeBin'] = df['Hour'].apply(tod_bin)

    # Tag season
    df['Season'] = s['label']

    # Select only columns needed for EDA
    cols = [
        'Date','Season','HomeCity','TotalGoals',
        'temp','precip','PrecipBin','preciptype'
    ]
    if 'Attendance' in df.columns:
        cols.append('Attendance')
    if 'TimeBin' in df.columns:
        cols.append('TimeBin')

    cleaned = df[cols]

    # Save to cleaned CSV
    out_name = f"cleaned_{s['label']}.csv"
    cleaned.to_csv(out_name, index=False)
    print(f"Saved {out_name} ({len(cleaned)} records)")
