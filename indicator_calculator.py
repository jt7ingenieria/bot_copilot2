import pandas as pd
import pandas_ta as ta

def calculate_indicators(df: pd.DataFrame) -> pd.DataFrame:
    """
    Calculate technical indicators and add them to the DataFrame.
    """
    # Create a copy of the DataFrame with lowercase column names for indicators
    df_lower = df.copy()
    df_lower.columns = df_lower.columns.str.lower()
    
    # Add RSI
    df_lower.ta.rsi(length=14, append=True)
    
    # Add Simple Moving Averages
    df_lower.ta.sma(length=50, append=True)
    df_lower.ta.sma(length=200, append=True)
    
    # Add Bollinger Bands
    df_lower.ta.bbands(length=20, append=True)
    
    # Add ATR for volatility
    df_lower.ta.atr(length=14, append=True)
    
    # Add MACD
    df_lower.ta.macd(append=True)
    
    # Add Volume indicators
    df_lower.ta.obv(append=True)  # On Balance Volume
    df_lower.ta.mfi(append=True)  # Money Flow Index
    
    # Copy indicators to original DataFrame
    for col in df_lower.columns:
        if col not in ['open', 'high', 'low', 'close', 'volume']:
            df[col] = df_lower[col]
    
    # Rename columns for clarity
    df.rename(columns={
        'RSI_14': 'rsi',
        'SMA_50': 'sma_50',
        'SMA_200': 'sma_200',
        'BBL_20_2.0': 'bb_lower',
        'BBM_20_2.0': 'bb_middle',
        'BBU_20_2.0': 'bb_upper',
        'ATRr_14': 'atr',
        'OBV': 'obv',
        'MFI_14': 'mfi'
    }, inplace=True)
    
    return df
