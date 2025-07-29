from backtesting import Strategy
from backtesting.lib import crossover
import pandas as pd
import numpy as np

class EmaVolumeStrategy(Strategy):
    # Definir parámetros ajustables
    ema_short = 9    # EMA rápida
    ema_medium = 21  # EMA media
    ema_long = 50    # EMA lenta
    
    volume_factor = 1.5  # Factor de volumen por encima del promedio
    volume_period = 20   # Período para calcular el volumen promedio

    def init(self):
        # Calcular las EMAs usando cálculo manual
        close = self.data.Close
        self.ema_s = self.I(self._calculate_ema, close, self.ema_short)
        self.ema_m = self.I(self._calculate_ema, close, self.ema_medium)
        self.ema_l = self.I(self._calculate_ema, close, self.ema_long)

        # Calcular el volumen promedio móvil
        volume = self.data.Volume
        self.volume_sma = self.I(self._calculate_sma, volume, self.volume_period)
        
    def _calculate_ema(self, data, period):
        alpha = 2.0 / (period + 1)
        result = [data[0]]  # Initialize with first value
        
        for i in range(1, len(data)):
            ema = alpha * data[i] + (1 - alpha) * result[-1]
            result.append(ema)
            
        return result
        
    def _calculate_sma(self, data, period):
        return pd.Series(data).rolling(period).mean()
        
    def next(self):
        # Verificar si tenemos suficientes datos
        if len(self.volume_sma) < 2:
            return

        # Comprobar si el volumen actual es alto
        current_volume = self.data.Volume[-1]
        avg_volume = self.volume_sma[-1]
        high_volume = current_volume > (avg_volume * self.volume_factor)

        # Si no hay suficiente volumen, no operar
        if not high_volume:
            return

        # Verificar la alineación de EMAs para tendencia
        ema_s = self.ema_s[-1]
        ema_m = self.ema_m[-1]
        ema_l = self.ema_l[-1]

        # Condiciones anteriores para comparar
        prev_ema_s = self.ema_s[-2]
        prev_ema_m = self.ema_m[-2]
        prev_ema_l = self.ema_l[-2]

        # Detectar cambio a tendencia alcista
        bullish = (
            ema_s > ema_m > ema_l and  # EMAs alineadas en orden alcista
            not (prev_ema_s > prev_ema_m > prev_ema_l)  # Confirmar el cambio
        )

        # Detectar cambio a tendencia bajista
        bearish = (
            ema_s < ema_m < ema_l and  # EMAs alineadas en orden bajista
            not (prev_ema_s < prev_ema_m < prev_ema_l)  # Confirmar el cambio
        )

        # Tomar posiciones
        if bullish and not self.position:
            # Calcular el stop loss y take profit
            entry_price = self.data.Close[-1]
            stop_loss = entry_price * 0.98  # 2% stop loss
            take_profit = entry_price * 1.04  # 4% take profit
            
            self.buy(sl=stop_loss, tp=take_profit)
            
        elif bearish and self.position:
            self.sell()
