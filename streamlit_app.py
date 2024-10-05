import streamlit as st
import numpy as np
import plotly.graph_objects as go
from option_analysis import BlackScholesModel, OptionPlotter, run_sensitivity_analysis, plot_sensitivity_analysis
from user_input import get_user_input
from description import description_page, about_me
from monte_carlo import MonteCarloOptionPricing  # Import the Monte Carlo class
import pandas as pd



st.set_page_config(
    page_title="Black Scholes Option Model",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded",
)



st.sidebar.header("📊Black Scholes Option Model")


def main_page():
    st.title('Black-Scholes Option Pricing')
    S, K, T, r, v, option_type, x_variable, x_values, show_greeks = get_user_input()

    plotter = OptionPlotter(S, K, T, r, v, option_type, x_variable, x_values)
    prices, greeks_vals = plotter.generate_values()

    model = BlackScholesModel(S, K, T, r, v, option_type)
    st.write(f"### Option Price: ${model.option_price():.2f}")

    greeks = model.greeks()
    greeks_labels = ['Delta', 'Gamma', 'Theta', 'Vega', 'Rho']

    greeks_data = {
        'Greek': greeks_labels,
        'Value': [f"{value:.4f}" for value in greeks]
    }

    greeks_df = pd.DataFrame(greeks_data)

    # Create tabs for Greeks, Plot, Sensitivity Analysis, and Monte Carlo Simulation
    tab_selection = st.tabs(['Option Greeks', 'Option Plot', 'Sensitivity Analysis', 'Monte Carlo Simulation'])

    with tab_selection[0]:  # Greeks Tab
        st.write("### Option Greeks")
        st.table(greeks_df)

    with tab_selection[1]:  # Plot Tab
        st.write("### Option Value and Greeks Graph")
        fig = plotter.plot(prices, greeks_vals, show_greeks)
        st.plotly_chart(fig)

    with tab_selection[2]:  # Sensitivity Analysis Tab
        st.subheader('Sensitivity Analysis')
        sensitivity_variable = st.selectbox(
            'Select Variable for Sensitivity Analysis',
            ('Spot Price', 'Strike Price', 'Volatility', 'Expiry Time', 'Interest Rate')
        )
        if sensitivity_variable:
            sensitivity_values, sensitivity_prices, sensitivity_greeks = run_sensitivity_analysis(S, K, T, r, v, option_type, sensitivity_variable)
            st.subheader(f'Sensitivity Analysis for {sensitivity_variable}')
            fig_price, fig_greeks = plot_sensitivity_analysis(sensitivity_values, sensitivity_prices, sensitivity_greeks, sensitivity_variable)
            st.plotly_chart(fig_price)
            st.plotly_chart(fig_greeks)

    with tab_selection[3]:  # Monte Carlo Simulation Tab
        st.subheader('Monte Carlo Simulation for Option Pricing')
        num_simulations = st.number_input('Number of Simulations', min_value=1000, max_value=50000, value=10000, step=1000)
        mc_pricing = MonteCarloOptionPricing(S, K, T, r, v, option_type, num_simulations)
        
        # Get option price and paths
        option_price_mc, final_prices, _ = mc_pricing.simulate()  # No need for antithetic in the main price
        price_paths = mc_pricing.generate_paths()  # Generate paths for graphing
        
        st.write(f"### Monte Carlo Estimated Option Price: ${option_price_mc:.2f}")
        
        # Plot simulated paths
        st.write("### Simulated Asset Price Paths")
        fig_paths = go.Figure()
        
        for i in range(min(5, num_simulations)):  # Plot a maximum of 5 paths for clarity
            path = [S * np.exp((r - 0.5 * v ** 2) * (j / num_simulations) + v * np.sqrt(j / num_simulations) * np.random.normal()) for j in range(num_simulations)]
            fig_paths.add_trace(go.Scatter(x=list(range(num_simulations)), y=path, mode='lines', name=f'Path {i + 1}', line=dict(width=1)))

        fig_paths.update_layout(title='Simulated Asset Price Paths',
                                 xaxis_title='Time Steps',
                                 yaxis_title='Asset Price',
                                 height=400)

        st.plotly_chart(fig_paths)

        # Plot histogram of final prices
        st.write("### Distribution of Option Prices")
        fig_hist = go.Figure(data=[go.Histogram(x=final_prices, nbinsx=30)])
        fig_hist.update_layout(title='Distribution of Option Prices',
                               xaxis_title='Option Price',
                               yaxis_title='Frequency')

        st.plotly_chart(fig_hist)

# Main App
tab_selection = st.tabs(['Option Pricing Model', 'Glossary', 'About Me'])

with tab_selection[0]:
    main_page()

with tab_selection[1]:
    description_page()

with tab_selection[2]:
    about_me()