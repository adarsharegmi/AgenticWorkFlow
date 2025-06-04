import pandas as pd
import numpy as np
from sklearn.preprocessing import StandardScaler, MinMaxScaler
from sklearn.impute import SimpleImputer
from sklearn.preprocessing import LabelEncoder

class DataFrameAgent:
    def __init__(self, dataframe):
        """
        Initialize the agent with the dataframe.
        
        :param dataframe: The input pandas DataFrame to operate on.
        """
        self.df = dataframe

    def handle_missing_data(self, strategy='mean', columns=None):
        """
        Handle missing data by imputing with a specified strategy.

        :param strategy: The imputation strategy ('mean', 'median', 'most_frequent').
        :param columns: List of columns to apply imputation, or None to apply to all.
        """
        imputer = SimpleImputer(strategy=strategy)
        if columns:
            self.df[columns] = imputer.fit_transform(self.df[columns])
        else:
            self.df = pd.DataFrame(imputer.fit_transform(self.df), columns=self.df.columns)
        print(f"Missing data handled using {strategy} strategy.")

    def remove_duplicates(self):
        """
        Remove duplicate rows from the dataframe.
        """
        initial_shape = self.df.shape
        self.df.drop_duplicates(inplace=True)
        print(f"Removed {initial_shape[0] - self.df.shape[0]} duplicate rows.")

    def remove_outliers(self, z_threshold=3):
        """
        Remove rows where numerical columns have outliers beyond a certain Z-score threshold.
        
        :param z_threshold: Z-score threshold to consider as outliers.
        """
        from scipy.stats import zscore
        numerical_cols = self.df.select_dtypes(include=[np.number]).columns
        z_scores = np.abs(zscore(self.df[numerical_cols]))
        self.df = self.df[(z_scores < z_threshold).all(axis=1)]
        print(f"Outliers removed based on Z-score threshold {z_threshold}.")

    def encode_categorical(self, columns=None):
        """
        Encode categorical columns using label encoding.
        
        :param columns: List of columns to encode, or None to apply to all categorical columns.
        """
        if columns:
            for col in columns:
                encoder = LabelEncoder()
                self.df[col] = encoder.fit_transform(self.df[col].astype(str))
                print(f"Column '{col}' encoded.")
        else:
            categorical_cols = self.df.select_dtypes(include=[object]).columns
            for col in categorical_cols:
                encoder = LabelEncoder()
                self.df[col] = encoder.fit_transform(self.df[col].astype(str))
                print(f"Column '{col}' encoded.")

    def normalize_numerical_columns(self, columns=None):
        """
        Normalize numerical columns using Min-Max scaling.

        :param columns: List of columns to normalize, or None to apply to all numerical columns.
        """
        scaler = MinMaxScaler()
        if columns:
            self.df[columns] = scaler.fit_transform(self.df[columns])
        else:
            numerical_cols = self.df.select_dtypes(include=[np.number]).columns
            self.df[numerical_cols] = scaler.fit_transform(self.df[numerical_cols])
        print("Numerical columns normalized.")

    def standardize_numerical_columns(self, columns=None):
        """
        Standardize numerical columns to have zero mean and unit variance.
        
        :param columns: List of columns to standardize, or None to apply to all numerical columns.
        """
        scaler = StandardScaler()
        if columns:
            self.df[columns] = scaler.fit_transform(self.df[columns])
        else:
            numerical_cols = self.df.select_dtypes(include=[np.number]).columns
            self.df[numerical_cols] = scaler.fit_transform(self.df[numerical_cols])
        print("Numerical columns standardized.")

    def filter_columns_by_valid_data(self, threshold=0.2):
        """
        Filter out columns with more than a certain percentage of missing data.
        
        :param threshold: Percentage of missing data allowed (e.g., 0.4 means 40% missing data).
        """
        valid_cols = self.df.columns[self.df.isnull().mean() <= threshold]
        self.df = self.df[valid_cols]
        print(f"Columns with more than {threshold*100}% missing data filtered out.")

    def generate_feature_interaction(self, col1, col2, new_col_name):
        """
        Create a new feature based on interaction between two columns.
        
        :param col1: The first column for interaction.
        :param col2: The second column for interaction.
        :param new_col_name: The name of the new interaction column.
        """
        self.df[new_col_name] = self.df[col1] * self.df[col2]
        print(f"New interaction feature '{new_col_name}' created between {col1} and {col2}.")

    def handle_imbalance(self, method='undersample'):
        """
        Handle class imbalance if applicable (for classification tasks).
        
        :param method: Either 'oversample' or 'undersample'.
        """
        from imblearn.over_sampling import SMOTE
        from imblearn.under_sampling import RandomUnderSampler
        
        if method == 'oversample':
            smote = SMOTE()
            X_res, y_res = smote.fit_resample(self.df.drop(columns='target'), self.df['target'])
            self.df = pd.concat([X_res, y_res], axis=1)
            print("Data oversampled to handle imbalance.")
        elif method == 'undersample':
            undersampler = RandomUnderSampler()
            X_res, y_res = undersampler.fit_resample(self.df.drop(columns='target'), self.df['target'])
            self.df = pd.concat([X_res, y_res], axis=1)
            print("Data undersampled to handle imbalance.")

    def get_dataframe(self):
        """
        Return the processed DataFrame.
        """
        return self.df


