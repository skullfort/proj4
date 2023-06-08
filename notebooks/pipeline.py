import pandas as pd
from sklearn.preprocessing import StandardScaler
from imblearn.over_sampling import RandomOverSampler
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, classification_report
from sklearn.model_selection import train_test_split

def preprocess(df):
    '''
    This function applies preprocessing specific to the HR dataset with missing values filled.
    The details are adapted from the same preprocessing process used in preliminary data exploration.
    '''
    # `city`: create a bin for cities with fewer than `threshold` instances.
    threshold = 200
    city_counts = df['city'].value_counts()
    cities_to_replace = city_counts[city_counts<threshold].index
    for city in cities_to_replace:
        df['city'] = df['city'].replace(city, 'Other')

    # `relevent_experience`: convert having and not having relevant experience to 1's and 0's.
    df['relevent_experience'].replace('Has relevent experience', 1, inplace=True)
    df['relevent_experience'].replace('No relevent experience', 0, inplace=True)

    # `enrolled_university`: update values for better readability.
    df['enrolled_university'].replace('no_enrollment', 'none', inplace=True)
    df['enrolled_university'].replace('Full time course', 'full_time', inplace=True)
    df['enrolled_university'].replace('Part time course', 'part_time', inplace=True)

    # `experience`: create bins for boarder categorization of experience.
    for exp in ['<1', '1', '2']:
        df['experience'].replace(exp, '0-2', inplace=True)
    for exp in ['3', '4']:
        df['experience'].replace(exp, '3-4', inplace=True)
    for exp in ['5', '6', '7', '8', '9']:
        df['experience'].replace(exp, '5-9', inplace=True)
    for exp in ['10', '11', '12', '13', '14', '15', '16', '17', '18', '19', '20', '>20']:
        df['experience'].replace(exp, '>=10', inplace=True)
    df['experience'].value_counts(dropna=False)

    # `company_size`: correct a typo.
    df['company_size'].replace('10/49', '10-49', inplace=True)

    return df

def lrmodel(df):
    '''
    This function prints out the performance metrics of using a logistic regression model on the preprocessed data.
    '''
    # Use `get_dummies` to encode all categorical features.
    df = pd.get_dummies(df)
    
    # Split the data into a training set and a testing set.
    y = df.target
    X = df.drop(columns='target')
    X_train, X_test, y_train, y_test = train_test_split(X, y, random_state=42, stratify=y)

    # Instantiate a StandardScaler instance.
    scaler = StandardScaler()

    # Fit the training data to the standard scaler.
    X_scaler = scaler.fit(X_train)

    # Transform the training data using the scaler.
    X_train_scaled = X_scaler.transform(X_train)

    # Transform the testing data using the scaler.
    X_test_scaled = X_scaler.transform(X_test)

    # Due to imbalanced target values, instantiate the random oversampler model.
    ros = RandomOverSampler(random_state=42)
    X_res, y_res = ros.fit_resample(X_train_scaled, y_train)

    # Implement a logistic regression classifier.
    classifier = LogisticRegression(solver='lbfgs', random_state=42)
    classifier.fit(X_res, y_res)
    predictions = classifier.predict(X_test_scaled)

    # Display the accuracy score for the test dataset.
    print(f'Accuracy score: {accuracy_score(y_test, predictions):.2f}')

    # Display the classification report.
    target_names = ['stay', 'leave']
    print(classification_report(y_test, predictions, target_names=target_names))