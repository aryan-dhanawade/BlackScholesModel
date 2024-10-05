import numpy as np
import streamlit as st 

@st.cache_resource
class MonteCarloOptionPricing:
    def __init__(self, S, K, T, r, v, option_type='put', num_simulations=10000):
        self.S = S          # Spot Price
        self.K = K          # Strike Price
        self.T = T          # Time to Expiry (in years)
        self.r = r          # Risk-Free Interest Rate
        self.v = v          # Volatility
        self.option_type = option_type.lower()
        self.num_simulations = num_simulations

    def simulate(self):
        # Generate random price paths
        np.random.seed(42)  # For reproducibility
        
        # Generate standard normal random variables for two sets (regular and antithetic)
        z = np.random.normal(0, 1, self.num_simulations)
        z_antithetic = -z  # Antithetic variates

        # Simulated final stock prices
        ST = self.S * np.exp((self.r - 0.5 * self.v**2) * self.T + self.v * np.sqrt(self.T) * z)
        ST_antithetic = self.S * np.exp((self.r - 0.5 * self.v**2) * self.T + self.v * np.sqrt(self.T) * z_antithetic)

        # Calculate payoffs
        if self.option_type == 'call':
            payoffs = np.maximum(ST - self.K, 0)
            payoffs_antithetic = np.maximum(ST_antithetic - self.K, 0)
        else:  # put option
            payoffs = np.maximum(self.K - ST, 0)
            payoffs_antithetic = np.maximum(self.K - ST_antithetic, 0)

        # Calculate the present value of the expected payoff using both sets of payoffs
        option_price = np.exp(-self.r * self.T) * (np.mean(payoffs) + np.mean(payoffs_antithetic)) / 2

        return option_price, ST, ST_antithetic  # Return the option price and both sets of final stock prices

    def generate_paths(self):
        # Generate multiple price paths
        price_paths = np.zeros((self.num_simulations, 2))  # Store initial and final prices
        price_paths[:, 0] = self.S
        
        for i in range(self.num_simulations):
            z = np.random.normal(0, 1)  # One random sample for each path
            ST = self.S * np.exp((self.r - 0.5 * self.v**2) * self.T + self.v * np.sqrt(self.T) * z)
            price_paths[i, 1] = ST

        return price_paths
