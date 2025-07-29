import pandas as pd
from sklearn.preprocessing import MinMaxScaler
from typing import List

class DataPreprocessor:
    def __init__(self):
        self.scalers = {}

    def preprocess_data(self, df: pd.DataFrame, columns_to_scale: List[str] = None) -> pd.DataFrame:
        """
        Clean and scale the data.
        
        Args:
            df: DataFrame with OHLCV and indicator data
            columns_to_scale: List of columns to scale (excluding price data)
        """
        # 1. Handle missing values
        df = self._handle_missing_values(df)
        
        # 2. Scale features if specified
        if columns_to_scale:
            df = self._scale_features(df, columns_to_scale)
        
        return df

    def _handle_missing_values(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        Handle missing values in the DataFrame.
        """
        # Forward fill missing values
        df = df.fillna(method='ffill')
        
        # Backward fill any remaining missing values at the start
        df = df.fillna(method='bfill')
        
        return df

    def _scale_features(self, df: pd.DataFrame, columns: List[str]) -> pd.DataFrame:
        """
        Scale specified features using MinMaxScaler.
        """
        df_scaled = df.copy()
        
        for col in columns:
            if col in df.columns:
                # Create a new scaler for each feature if it doesn't exist
                if col not in self.scalers:
                    self.scalers[col] = MinMaxScaler()
                
                # Reshape data for scaling
                values = df[col].values.reshape(-1, 1)
                
                # Fit and transform
                scaled_values = self.scalers[col].fit_transform(values)
                
                # Add scaled column to DataFrame
                df_scaled[f'{col}_scaled'] = scaled_values
        
        return df_scaled

    def inverse_scale_feature(self, col: str, scaled_values) -> pd.Series:
        """
        Inverse scale a feature using its stored scaler.
        """
        if col in self.scalers:
            return pd.Series(
                self.scalers[col].inverse_transform(scaled_values.reshape(-1, 1)).flatten()
            )
        return scaled_values
