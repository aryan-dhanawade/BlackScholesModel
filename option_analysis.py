import numpy as np
import scipy.stats as si
import numpy as np
import plotly.graph_objects as go


class BlackScholesModel:
    def __init__(self, S, K, T, r, v, option_type='put'):
        self.S = S
        self.K = K
        self.T = T
        self.r = r
        self.v = v
        self.option_type = option_type.lower()
        self.d1, self.d2 = self._calculate_d1_d2()

    def _calculate_d1_d2(self):
        d1 = (np.log(self.S/self.K) + (self.r + 0.5 * self.v**2) * self.T) / (self.v * np.sqrt(self.T))
        d2 = d1 - self.v * np.sqrt(self.T)
        return d1, d2

    def option_price(self):
        if self.option_type == 'call':
            price = self.S * si.norm.cdf(self.d1) - self.K * np.exp(-self.r * self.T) * si.norm.cdf(self.d2)
        else:
            price = self.K * np.exp(-self.r * self.T) * si.norm.cdf(-self.d2) - self.S * si.norm.cdf(-self.d1)
        return price

    def greeks(self):
        delta = si.norm.cdf(self.d1) if self.option_type == 'call' else si.norm.cdf(self.d1) - 1
        gamma = si.norm.pdf(self.d1) / (self.S * self.v * np.sqrt(self.T))
        theta = -(self.S * si.norm.pdf(self.d1) * self.v) / (2 * np.sqrt(self.T)) - \
                self.r * self.K * np.exp(-self.r * self.T) * si.norm.cdf(self.d2)
        vega = self.S * si.norm.pdf(self.d1) * np.sqrt(self.T)
        rho = self.K * self.T * np.exp(-self.r * self.T) * si.norm.cdf(self.d2) if self.option_type == 'call' \
            else -self.K * self.T * np.exp(-self.r * self.T) * si.norm.cdf(-self.d2)
        return delta, gamma, theta, vega, rho


class OptionPlotter:
    def __init__(self, S, K, T, r, v, option_type, x_variable, x_values):
        self.S = S
        self.K = K
        self.T = T
        self.r = r
        self.v = v
        self.option_type = option_type.lower()
        self.x_variable = x_variable
        self.x_values = x_values

    def calculate_option_price_and_greeks(self, x_val):
        params = {
            'S': self.S, 'K': self.K, 'T': self.T, 'r': self.r, 'v': self.v
        }
        params[self.x_variable] = x_val
        model = BlackScholesModel(**params, option_type=self.option_type)
        price = model.option_price()
        greeks = model.greeks()
        return price, greeks

    def generate_values(self):
        prices, delta_vals, gamma_vals, theta_vals, vega_vals, rho_vals = [], [], [], [], [], []
        
        for x_val in self.x_values:
            price, (delta, gamma, theta, vega, rho) = self.calculate_option_price_and_greeks(x_val)
            prices.append(price)
            delta_vals.append(delta)
            gamma_vals.append(gamma)
            theta_vals.append(theta)
            vega_vals.append(vega)
            rho_vals.append(rho)

        greeks_vals = {'delta': delta_vals, 'gamma': gamma_vals, 'theta': theta_vals, 'vega': vega_vals, 'rho': rho_vals}
        return prices, greeks_vals

    def plot(self, prices, greeks_vals, show_greeks):
        fig = go.Figure()

        # Plot Option Value
        fig.add_trace(go.Scatter(
            x=self.x_values, y=prices, mode='lines', name='Option Value', line=dict(color='red')
        ))

        # Plot selected Greeks
        for greek, show in show_greeks.items():
            if show:
                fig.add_trace(go.Scatter(
                    x=self.x_values, y=greeks_vals[greek], mode='lines', name=greek.capitalize()
                ))

        fig.update_layout(
            title=f'{self.option_type.capitalize()} Option Value and Greeks vs {self.x_variable}',
            xaxis_title=self.x_variable,
            yaxis_title='Option Value / Greeks',
            hovermode="x",
            template='plotly_white'
        )

        return fig



class OptionPlotter:
    def __init__(self, S, K, T, r, v, option_type, x_variable, x_values):
        self.S = S
        self.K = K
        self.T = T
        self.r = r
        self.v = v
        self.option_type = option_type.lower()
        self.x_variable = x_variable
        self.x_values = x_values

    def calculate_option_price_and_greeks(self, x_val):
        params = {
            'S': self.S, 'K': self.K, 'T': self.T, 'r': self.r, 'v': self.v
        }
        params[self.x_variable] = x_val
        model = BlackScholesModel(**params, option_type=self.option_type)
        price = model.option_price()
        greeks = model.greeks()
        return price, greeks

    def generate_values(self):
        prices, delta_vals, gamma_vals, theta_vals, vega_vals, rho_vals = [], [], [], [], [], []
        
        for x_val in self.x_values:
            price, (delta, gamma, theta, vega, rho) = self.calculate_option_price_and_greeks(x_val)
            prices.append(price)
            delta_vals.append(delta)
            gamma_vals.append(gamma)
            theta_vals.append(theta)
            vega_vals.append(vega)
            rho_vals.append(rho)

        greeks_vals = {'delta': delta_vals, 'gamma': gamma_vals, 'theta': theta_vals, 'vega': vega_vals, 'rho': rho_vals}
        return prices, greeks_vals

    def plot(self, prices, greeks_vals, show_greeks):
        fig = go.Figure()

        # Plot Option Value
        fig.add_trace(go.Scatter(
            x=self.x_values, y=prices, mode='lines', name='Option Value', line=dict(color='red')
        ))

        # Plot selected Greeks
        for greek, show in show_greeks.items():
            if show:
                fig.add_trace(go.Scatter(
                    x=self.x_values, y=greeks_vals[greek], mode='lines', name=greek.capitalize()
                ))

        fig.update_layout(
            title=f'{self.option_type.capitalize()} Option Value and Greeks vs {self.x_variable}',
            xaxis_title=self.x_variable,
            yaxis_title='Option Value / Greeks',
            hovermode="x",
            template='plotly_white'
        )

        return fig

def run_sensitivity_analysis(S, K, T, r, v, option_type, sensitivity_variable):
    num_points = 100  # Number of points to generate
    sensitivity_values = None
    
    # Generate sensitivity values based on the selected variable
    if sensitivity_variable == 'Spot Price':
        sensitivity_values = np.linspace(0.01, 1000.0, num_points)
    elif sensitivity_variable == 'Strike Price':
        sensitivity_values = np.linspace(0.01, 1000.0, num_points)
    elif sensitivity_variable == 'Volatility':
        sensitivity_values = np.linspace(0.01, 1.0, num_points)
    elif sensitivity_variable == 'Expiry Time':
        sensitivity_values = np.linspace(0.01, 5.0, num_points)
    else:  # Interest Rate
        sensitivity_values = np.linspace(0.0, 1.0, num_points)

    # Calculate option prices and Greeks for sensitivity analysis
    sensitivity_prices = []
    sensitivity_greeks = {greek: [] for greek in ['delta', 'gamma', 'theta', 'vega', 'rho']}

    for value in sensitivity_values:
        if sensitivity_variable == 'Spot Price':
            model = BlackScholesModel(value, K, T, r, v, option_type)
        elif sensitivity_variable == 'Strike Price':
            model = BlackScholesModel(S, value, T, r, v, option_type)
        elif sensitivity_variable == 'Volatility':
            model = BlackScholesModel(S, K, T, r, value, option_type)
        elif sensitivity_variable == 'Expiry Time':
            model = BlackScholesModel(S, K, value, r, v, option_type)
        else:  # Interest Rate
            model = BlackScholesModel(S, K, T, value, v, option_type)

        sensitivity_prices.append(model.option_price())
        greek_vals = model.greeks()
        for i, greek in enumerate(['delta', 'gamma', 'theta', 'vega', 'rho']):
            sensitivity_greeks[greek].append(greek_vals[i])

    return sensitivity_values, sensitivity_prices, sensitivity_greeks

def plot_sensitivity_analysis(sensitivity_values, sensitivity_prices, sensitivity_greeks, sensitivity_variable):
    # Create sensitivity analysis plots
    fig_price = go.Figure()
    fig_price.add_trace(go.Scatter(x=sensitivity_values, y=sensitivity_prices, mode='lines', name='Option Price'))
    fig_price.update_layout(title=f'Option Price Sensitivity to {sensitivity_variable}',
                            xaxis_title=sensitivity_variable,
                            yaxis_title='Option Price',
                            template='plotly_white')

    fig_greeks = go.Figure()
    for greek in sensitivity_greeks:
        fig_greeks.add_trace(go.Scatter(x=sensitivity_values, y=sensitivity_greeks[greek], mode='lines', name=greek.capitalize()))
    
    fig_greeks.update_layout(title=f'Greeks Sensitivity to {sensitivity_variable}',
                              xaxis_title=sensitivity_variable,
                              yaxis_title='Greeks',
                              template='plotly_white')

    return fig_price, fig_greeks
