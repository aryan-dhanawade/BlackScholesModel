import streamlit as st
import numpy as np

def get_user_input():
    st.sidebar.header('Input Parameters')

    S = st.sidebar.number_input('Spot Price (S)', min_value=0.01, value=300.0)
    K = st.sidebar.number_input('Strike Price (K)', min_value=0.01, value=250.0)
    T = st.sidebar.number_input('Expiry Time (T) in Years', min_value=0.01, value=1.0)
    r = st.sidebar.number_input('Interest Rate (r)', min_value=0.0, max_value=1.0, value=0.03)
    v = st.sidebar.number_input('Volatility (v)', min_value=0.01, max_value=1.0, value=0.15)
    option_type = st.sidebar.radio('Option Type', ('Call', 'Put'))

    x_variable_label = st.sidebar.selectbox(
        'Choose the variable for the x-axis',
        ('Spot Price', 'Strike Price', 'Volatility', 'Expiry Time', 'Interest Rate')
    )

    variable_mapping = {
        'Spot Price': 'S',
        'Strike Price': 'K',
        'Volatility': 'v',
        'Expiry Time': 'T',
        'Interest Rate': 'r'
    }
    x_variable = variable_mapping[x_variable_label]

    range_defaults = {
        'S': (50.0, 350.0),
        'K': (50.0, 350.0),
        'v': (0.1, 1.0),
        'T': (0.1, 5.0),
        'r': (0.01, 0.15)
    }
    range_from = st.sidebar.number_input(f'{x_variable_label} Range: From', value=range_defaults[x_variable][0])
    range_to = st.sidebar.number_input(f'{x_variable_label} Range: To', value=range_defaults[x_variable][1])
    x_values = np.linspace(range_from, range_to, 100)

    st.sidebar.header('Select Greeks to Plot')
    show_delta = st.sidebar.checkbox('Delta')
    show_gamma = st.sidebar.checkbox('Gamma')
    show_theta = st.sidebar.checkbox('Theta')
    show_vega = st.sidebar.checkbox('Vega')
    show_rho = st.sidebar.checkbox('Rho')

    show_greeks = {'delta': show_delta, 'gamma': show_gamma, 'theta': show_theta, 'vega': show_vega, 'rho': show_rho}

    return S, K, T, r, v, option_type, x_variable, x_values, show_greeks
