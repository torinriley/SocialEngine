import pandas as pd
from sklearn.preprocessing import MinMaxScaler


def preprocess_dataset(dataset):
    """
    Preprocesses the dataset.
    """
    numeric_columns = [
        'Impressions', 'From Home', 'From Hashtags', 'From Explore', 'From Other',
        'Saves', 'Comments', 'Shares', 'Likes', 'Profile Visits', 'Follows'
    ]
    dataset[numeric_columns] = dataset[numeric_columns].apply(pd.to_numeric, errors='coerce')
    dataset[numeric_columns] = dataset[numeric_columns].fillna(0)
    dataset['Caption'].fillna("", inplace=True)
    dataset['Hashtags'].fillna("", inplace=True)
    dataset['Engagement'] = (
        dataset['Likes'] + dataset['Comments'] +
        dataset['Shares'] + dataset['Saves']
    )
    scaler = MinMaxScaler()
    dataset['Engagement Norm'] = scaler.fit_transform(dataset[['Engagement']])
    return dataset