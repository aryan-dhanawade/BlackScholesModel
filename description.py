import sympy as sp
from sympy.stats import Normal, cdf
import streamlit as st

def description_page():
    st.title('Greeks and Black-Scholes Model Explanation')

    # Brief explanation of the Black-Scholes Model
    st.write("### Black-Scholes Model Overview")
    st.write(
        "The Black-Scholes model is a mathematical model for pricing an options contract. "
        "It provides a formula for calculating the theoretical price of European-style options, "
        "which can only be exercised at expiration. The model takes into account the current "
        "price of the underlying asset, the strike price of the option, the time to expiration, "
        "the risk-free interest rate, and the volatility of the asset. "
        "The Black-Scholes formula is based on the assumption that the stock price follows a "
        "lognormal distribution and that markets are efficient, meaning that the option price reflects "
        "all available information."
    )

    # Black-Scholes Formula
    S, K, T, r, v = sp.symbols('S K T r v')
    d1 = (sp.log(S/K) + (r + 0.5 * v**2) * T) / (v * sp.sqrt(T))
    d2 = d1 - v * sp.sqrt(T)

    # Define a standard normal distribution
    X = Normal('X', 0, 1)

    # Black-Scholes Call and Put formulas
    BS_call = S * cdf(X)(d1) - K * sp.exp(-r * T) * cdf(X)(d2)
    BS_put = K * sp.exp(-r * T) * cdf(X)(-d2) - S * cdf(X)(-d1)

    # Display the Black-Scholes formulas symbolically
    st.write("### Black-Scholes Formula")
    st.latex(r"Call: \text{C} = S \cdot N(d_1) - K e^{-rT} N(d_2)")
    st.latex(r"Put: \text{P} = K e^{-rT} N(-d_2) - S \cdot N(-d_1)")

    # Variable Descriptions
    variable_descriptions = {
        'S': "Spot Price: The current price of the underlying asset.",
        'K': "Strike Price: The price at which the option can be exercised.",
        'T': "Time to Expiration: The time remaining until the option's expiration date, expressed in years.",
        'r': "Risk-Free Interest Rate: The theoretical return of an investment with zero risk, typically the yield of government bonds.",
        'v': "Volatility: A measure of the underlying asset's price fluctuations, indicating the degree of uncertainty."
    }

    # Greek Descriptions with Formulas
    greek_descriptions = {
        'Delta': (
            "Delta measures the rate of change of the option price with respect to changes in the underlying asset's price."
        ),
        'Gamma': (
            "Gamma measures the rate of change of delta with respect to changes in the underlying price."
        ),
        'Theta': (
            "Theta measures the sensitivity of the value of the derivative to the passage of time."
        ),
        'Vega': (
            "Vega measures the sensitivity of the option price to changes in volatility of the underlying asset."
        ),
        'Rho': (
            "Rho measures the sensitivity of the option price to changes in interest rates."
        )
    }

    # Formulas for Greeks
    greek_formulas = {
        'Delta': r"\Delta = N(d_1)",
        'Gamma': r"\Gamma = \frac{N'(d_1)}{S \sigma \sqrt{T}}",
        'Theta': r"\Theta = -\frac{S N'(d_1) \sigma}{2 \sqrt{T}} - rK e^{-rT} N(d_2)",
        'Vega': r"\nu = S N'(d_1) \sqrt{T}",
        'Rho': r"\rho = \begin{cases} K T e^{-rT} N(d_2) & \text{if Call} \\ -K T e^{-rT} N(-d_2) & \text{if Put} \end{cases}"
    }

    # Display Variable Descriptions
    st.write("### Variables in the Black-Scholes Formula")
    for var, description in variable_descriptions.items():
        st.write(f"**{var}:** {description}")

    # Display Greek Descriptions with LaTeX
    st.write("### Greek Descriptions")
    for greek, description in greek_descriptions.items():
        st.write(f"**{greek}:** {description}")
        st.latex(greek_formulas[greek])  # Display the formula for each Greek




def about_me():
    st.title("About Me")
    st.write("Hello! I'm Aryan Dhanawade. "
             "I'm a 2nd Year Computer Engineering Student at Mukesh Patel School of Technology Management and Engineering. "
             "I'm passionate about finance and programming.")
    st.write("You can connect with me on LinkedIn:")
    st.markdown("[LinkedIn Profile](https://www.linkedin.com/in/aryan-dhanawade)")