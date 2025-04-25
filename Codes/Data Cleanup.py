import pandas as pd

# Define which teams belong to each city
LONDON_TEAMS = [
    'Arsenal', 'Chelsea', 'Crystal Palace',
    'Fulham', 'Tottenham Hotspur', 'West Ham United'
]
MANCHESTER_TEAMS = ['Man City', 'Man United']

def city_of(team):
    """Return city name for a given Premier League team."""
    if team in LONDON_TEAMS:
        return 'London'
    if team in MANCHESTER_TEAMS:
        return 'Manchester'
    return 'Other'

def classify_precip(mm):
    """Bucket rainfall amount into Clear/Light/Moderate/Heavy."""
    if pd.isna(mm) or mm == 0:
        return 'Clear'
    elif mm <= 1:
        return 'Light'
    elif mm <= 3:
        return 'Moderate'
    else:
        return 'Heavy'

def time_of_day(hour):
    """Classify match start hour into Afternoon (<17) or Evening."""
    return 'Afternoon' if hour < 17 else 'Evening'


# Configuration for each season
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

for season in seasons:
    # Load match data
    matches = pd.read_csv(season['prem'])
    matches['Date'] = pd.to_datetime(matches['Date'],
                                     format=season['fmt'],
                                     dayfirst=True)
    # Keep only London/Manchester home games
    matches['City'] = matches['HomeTeam'].apply(city_of)
    matches = matches[matches['City'].isin(['London', 'Manchester'])]

    # Load weather data
    lw = pd.read_csv(season['wl'])
    lw['Date'] = pd.to_datetime(lw['datetime'])
    mw = pd.read_csv(season['wm'])
    mw['Date'] = pd.to_datetime(mw['datetime'])

    # Merge by city
    london_matches = pd.merge(
        matches[matches['City'] == 'London'], lw,
        on='Date', how='left'
    )
    man_matches = pd.merge(
        matches[matches['City'] == 'Manchester'], mw,
        on='Date', how='left'
    )
    df = pd.concat([london_matches, man_matches], ignore_index=True)

    # Compute goals and drop rows missing key weather
    df['TotalGoals'] = df['FTHG'] + df['FTAG']
    df = df.dropna(subset=['temp', 'precip'])

    # Add new columns for EDA
    df['PrecipBin'] = df['precip'].apply(classify_precip)
    if 'Attendance' in df.columns:
        df['Attendance'] = pd.to_numeric(df['Attendance'],
                                         errors='coerce')
    if 'Time' in df.columns:
        times = pd.to_datetime(df['Time'], format='%H:%M', errors='coerce')
        df['Hour'] = times.dt.hour
        df['TimeBin'] = df['Hour'].apply(time_of_day)

    df['Season'] = season['label']

    # Select only the columns we need
    columns = [
        'Date', 'Season', 'City', 'Referee',
        'TotalGoals', 'temp', 'precip',
        'PrecipBin', 'preciptype'
    ]
    if 'Attendance' in df.columns:
        columns.append('Attendance')
    if 'TimeBin' in df.columns:
        columns.append('TimeBin')

    clean_df = df[columns]

    # Write out the cleaned CSV
    filename = f"cleaned_{season['label']}.csv"
    clean_df.to_csv(filename, index=False)
    print(f"Saved {filename}: {len(clean_df)} rows")
