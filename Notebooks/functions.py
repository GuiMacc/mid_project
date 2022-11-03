
import numpy as np
import pandas as pd 

def clean_col_names(df):
    """
        Takes our dataframe and changes the column names into ones that better represent the contents of that column
        Input -> df Dataframe needing column name cleaning
        Output -> df1 Dataframe with columns renamed
    """
    
    df1 = df.copy()
    df1.rename(columns = {'name' : 'game', 'platform' : 'console', 'r-date' : 'release_date',
                         'score' : 'critic_score', 'user score' : 'user_score',
                         'developer' : 'dev', 'players' : 'player_support',
                         'critics' : 'num_critics', 'users' : 'num_users'}, inplace = True )
    return df1
def weird_rows(df):
    """
        Takes our dataframe and eliminates rows with values in the numerical columns that are simply no good
        Input -> df Dataframe needing row cleaning
        Output -> df1 Dataframe with no strange rows
    """
    
    df1 = df.copy()
    df1 = df1[ (df['user_score'] != 'tbd') & (df['num_users'] != 0) & (df['num_critics'] != 0) ]
    return df1
def support_fill(df):
    """
        Takes our dataframe and fills the values in the "player_support" column with reasonable ones
        Input -> df Dataframe with a few null values in the "player_support" column
        Output -> df1 Dataframe cleaned of null values
    """
    
    df1 = df.copy()
    df1['player_support'].fillna('No info', inplace=True)
    return df1
def fix_user_score(x):
    """
        Simply multiplies a number by 10 an returns the result as an integer
        Input -> any numeric value x, even if it's not cast as a numerical type
        Output -> produc y cast as an integer
    """
    
    y = float(x) * 10
    return int(y)
def score_diff_col(df):
    """
        Takes our dataframe and adds a new column with the difference between the two score columns
        Input -> df Dataframe
        Output -> df1 Dataframe with the newly created column
    """
    
    df1 = df.copy()
    df1['score_diff'] = df['user_score']-df['critic_score']
    return df1
def date_fix(df):
    """
        Takes our dataframe, changes the date column to the correct type and adds 2 new columns
        Input -> df Dataframe
        Output -> df1 Dataframe with the 2 new columns
    """
    
    df1 = df.copy()
    df1['release_date'] = pd.to_datetime(df['release_date'])
    df1['release_year'] = pd.DatetimeIndex(df1['release_date']).year
    df1['release_month'] = pd.DatetimeIndex(df1['release_date']).month
    return df1
def console_groupping(row):
    """
        Takes a string an aggregates it into a group based on it's value
        Input -> any possible string
        Output -> string whose value depends on the input
    """
    
    if "PlayStation" in row or row == "PSP":
        return "PS"
    elif "Xbox" in row:
        return "Xbox"
    elif row == "Dreamcast":
        return "Sega"
    elif row == "Stadia":
        return "Google"
    elif row == "PC":
        return "PC"
    else:
        return "Nintendo"
def fix_player_count(row):
    """
        Takes a string and aggregates it into a group based on it's value
        Input -> any possible string
        Output -> string whose value depends on the input
    """
    
    if row == "No info":
        return "No info"
    elif row == "1 Player" or row == "No Online Multiplayer":
        return "Singleplayer"
    elif row=="1-2 " or row=="1-3 " or row=="1-4 " or row=="2 " or row=="Up to 3 " or row=="Up to 4 " or row=="2  Online"  or row=="3  Online"  or row=="4  Online" :
        return "Co-op"
    else:
        return "Multiplayer"
def genre_cleaning(row):
    """
        Takes a string with a comma, and returns the substring prior the first comma
        Input -> any possible string as long as it has a comma
        Output -> everything before the first comma
    """
    
    g=row.split(",")
    return g[0]
def genre_cleaning_sec(row):
    """
        Takes a string with a comma, and returns the substring between the first and second commas
        Input -> any possible string as long as it has a comma
        Output -> everything between the first and second commas; if there is no second comma, returns "No secondary genre"
    """
    
    g=row.split(",")
    if len(g)>1:
        return g[1]
    else:
        return 'No secondary genre'
def narrow_genres(df):
    """
        Takes our dataframe and agregates most of the main and secondary genres while retaining the 10 or so with highest count
        Input -> df Dataframe
        Output -> df1 Dataframe with aggregated main and secondary genres
    """
    
    df1 = df.copy()
    df1['main_genre'] = np.where( df['main_genre'].isin( ['Action', 'Action Adventure', 'Role-Playing', 'Sports', 'Strategy', 'Miscellaneous', 'Adventure', 'Driving', 'Simulation'] ) , df['main_genre'], 'Other')
    df1['sec_genre'] = np.where( df['sec_genre'].isin( ['General', 'Shooter', 'Platformer', 'Traditional', 'Racing', 'Action RPG', 'Real-Time', 'Miscellaneous', 'Fighting', 'Turn-Based', 'Beat-\'Em-Up'] ) , df['sec_genre'], 'Other')
    return df1
def dev_mess(row):
    """
        Takes a string and aggregates it into a specific group
        Input -> any possible string
        Output -> string whose value depends on the input
    """
    
    if "Capcom" in row:
        return "Capcom"
    elif "TelltaleGames" in row:
        return "Telltale"
    elif row.startswith("EA") or "ElectronicArts" in row:
        return "EA"
    elif "Konami" in row:
        return "Konami"
    elif "Nintendo" in row:
        return "Nintendo"
    elif "Ubisoft" in row:
        return "Ubisoft"
    elif "Bandai" in row or "Namco" in row:
        return "BandaiNamco"
    elif "SquareEnix" in row or "SquareSoft" in row:
        return "SquareEnix"
    else:
        return "Other"
def yearly_reviews(df):
    """
        Takes our dataframe and adds a new column containing the amount of user reviews that game gets per year
        Input -> df Dataframe
        Output -> df1 Dataframe with the new column
    """
    
    df1=df.copy()
    max_year = df1['release_year'].max()
    df1['yearly_num_reviews'] = ( ( df1['num_users']) / ( (max_year + 1) - df1['release_year'] ) )
    return df1
def arrange_col(df):
    """
        Takes our dataframe and changes the order in which the columns appear, as well as sorting rows by year and montgh
        Input -> df Dataframe
        Output -> df1 Dataframe with the column order changed
    """
    
    df1 = df.copy()
    df1 = df1[['game', 'console', 'console_brand', 'dev', 'main_genre', 'sec_genre', 'player_support',
               'critic_score', 'user_score', 'score_diff','num_critics', 'num_users' , 
               'yearly_num_reviews', 'release_date', 'release_month', 'release_year']]
    df1.sort_values(by=["release_year",'release_month'],ascending=True, inplace=True)
    df1.reset_index(drop=True, inplace=True)
    return df1
def clean_full_data(df):
    """
        Takes our dataframe and inputs all the necessary functions to fully clean it
        Input -> df Dataframe raw and yet untreated
        Output -> f_data Dataframe fully cleaned
    """
    
    df1 = df.copy()
    
    # start by changing column names
    col_change = clean_col_names(df1)
    
    # need to get rid of rows with nonsensical values
    fixed_rows = weird_rows(col_change)
    
    # time to fill the null values in the player_support column
    no_nulls = support_fill(fixed_rows)
    
    # apply the correct function that scales the values in user_score
    no_nulls['user_score'] = no_nulls['user_score'].apply(fix_user_score)
    
    # adding the new column
    score_diff_df = score_diff_col(no_nulls)
    
    # changing date column type and adding month and year columns
    data = date_fix(score_diff_df)
    
    # begin applying the functions that clean categorical data
    # first, is adding the console_brand column
    data['console_brand'] = data['console'].apply(console_groupping)
    
    # second is grouping the values from player_support so we don't have 50 unique values
    data['player_support'] = data['player_support'].apply(fix_player_count)
    
    # third is collecting the main and secondary genres
    data['main_genre']=data['genre'].apply(genre_cleaning)
    data['sec_genre']=data['genre'].apply(genre_cleaning_sec)
    
    # fourth is reducing the amount of each genre type by grouping most of the unique values
    data_narrow = narrow_genres(data)

    # fifth is cleaning up the dev column by group the vast majority of them while keeping the most common values
    data_narrow['dev'] = data_narrow['dev'].apply(dev_mess)
    
    # sixth is adding a new column which computes the amount of reviews per year a game gets
    data_yearly = yearly_reviews(data_narrow)
    
    # finally we change the order of columns and sort by release year and month
    f_data = arrange_col(data_yearly)
    
    return f_data
