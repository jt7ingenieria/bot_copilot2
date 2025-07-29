import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from datetime import datetime

class Dashboard:
    def __init__(self):
        st.set_page_config(
            page_title="Crypto Trading Bot Dashboard",
            page_icon="📈",
            layout="wide"
        )

    def render(self, data=None, balance=None, open_positions=None, 
               backtest_results=None, trade_history=None):
        """
        Render the dashboard with real-time data and backtest results.
        """
        st.title("Crypto Trading Bot Dashboard")

        # Create tabs for different views
        tab1, tab2 = st.tabs(["Real-time Monitor", "Backtest Results"])

        with tab1:
            self._render_realtime_view(data, balance, open_positions, trade_history)

        with tab2:
            self._render_backtest_view(backtest_results)

    def _render_realtime_view(self, data, balance, open_positions, trade_history):
        """Render the real-time monitoring view."""
        # Account Overview
        st.subheader("Account Overview")
        cols = st.columns(3)
        
        if balance:
            with cols[0]:
                st.metric("Total Balance (USDT)", 
                         f"{balance.get('total', 0):,.2f}",
                         f"{balance.get('pnl_24h', 0):+,.2f}")
            with cols[1]:
                st.metric("Available Balance (USDT)", 
                         f"{balance.get('free', 0):,.2f}")
            with cols[2]:
                st.metric("In Position (USDT)", 
                         f"{balance.get('used', 0):,.2f}")

        # Price Chart
        if data is not None and not data.empty:
            st.subheader("Price Chart")
            fig = self._create_price_chart(data)
            st.plotly_chart(fig, use_container_width=True)

        # Open Positions
        st.subheader("Open Positions")
        if open_positions:
            st.dataframe(pd.DataFrame(open_positions))
        else:
            st.info("No open positions")

        # Trade History
        st.subheader("Recent Trades")
        if trade_history:
            st.dataframe(pd.DataFrame(trade_history))
        else:
            st.info("No trade history available")

    def _render_backtest_view(self, results):
        """Render the backtest results view."""
        if not results:
            st.info("No backtest results available")
            return

        st.subheader("Backtest Results")
        
        # Key Metrics
        cols = st.columns(4)
        with cols[0]:
            st.metric("Total Return", f"{results.get('Return [%]', 0):.2f}%")
        with cols[1]:
            st.metric("Sharpe Ratio", f"{results.get('Sharpe Ratio', 0):.2f}")
        with cols[2]:
            st.metric("Max Drawdown", f"{results.get('Max. Drawdown [%]', 0):.2f}%")
        with cols[3]:
            st.metric("Win Rate", f"{results.get('Win Rate [%]', 0):.2f}%")

        # Detailed Metrics Table
        st.subheader("Detailed Metrics")
        metrics_df = pd.DataFrame([results])
        st.dataframe(metrics_df)

        # Equity Curve
        if 'equity_curve' in results:
            st.subheader("Equity Curve")
            fig = go.Figure(data=[
                go.Scatter(x=results['equity_curve'].index, 
                          y=results['equity_curve'].values,
                          mode='lines',
                          name='Equity')
            ])
            st.plotly_chart(fig, use_container_width=True)

    def _create_price_chart(self, data):
        """Create an interactive price chart with indicators."""
        fig = go.Figure()

        # Candlestick chart
        fig.add_trace(go.Candlestick(
            x=data.index,
            open=data['open'],
            high=data['high'],
            low=data['low'],
            close=data['close'],
            name='Price'
        ))

        # Add indicators if available
        if 'sma_50' in data.columns:
            fig.add_trace(go.Scatter(
                x=data.index,
                y=data['sma_50'],
                name='SMA 50',
                line=dict(color='blue')
            ))

        if 'bb_upper' in data.columns and 'bb_lower' in data.columns:
            fig.add_trace(go.Scatter(
                x=data.index,
                y=data['bb_upper'],
                name='BB Upper',
                line=dict(color='gray', dash='dash')
            ))
            fig.add_trace(go.Scatter(
                x=data.index,
                y=data['bb_lower'],
                name='BB Lower',
                line=dict(color='gray', dash='dash'),
                fill='tonexty'
            ))

        # Update layout
        fig.update_layout(
            title='Price and Indicators',
            yaxis_title='Price',
            xaxis_title='Date',
            template='plotly_dark'
        )

        return fig
