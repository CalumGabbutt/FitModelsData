import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.ticker import MaxNLocator
import stan
import arviz as az
import os

plt.ion()

# If an output directory to store the plots in doesn't exist,
# create it
if ~os.path.exists('plots'):
    os.mkdir('plots')

try:
     os.mkdir('plots')
except FileExistsError as e:
    print(e)

# Read in Lynx - Hare dataset
df = pd.read_csv('hudson-bay-lynx-hare.csv')

# Put the data into a dictionary that Stan can read
stan_data = {"N": np.shape(df)[0],
            "ts":df["Year"].values,
            "y":df[["Hare", "Lynx"]].values}

# Load the Stan code for the model
with open('LotkaVolterraHMC.stan') as f:
    model_code = f.read()

# Build the Stan model
posterior = stan.build(model_code, data=stan_data, random_seed=1)

# Fit the model to the data
fit = posterior.sample(num_chains=4, num_samples=1000)

# Convert the Stan output to arviz iData for plotting
idata_kwargs = {
    "posterior_predictive": "y_rep",
    "observed_data": "y",
    "log_likelihood": "log_lik"
}
inference = az.from_pystan(fit, posterior_model=posterior, **idata_kwargs)

# Print a summary of the statistics
print(az.summary(inference, var_names=["alpha", "beta", "gamma", "delta", "z_init", "sigma"]))

# Plot a trace plot of the variables to check that there are no divergences
# and the model has compiled
az.plot_trace(inference, var_names=["alpha", "beta", "gamma", "delta", "z_init", "sigma"])
plt.savefig("plots/LotkaVolterraTrace.png", dpi=600)
plt.close()

# Plot a pairs plot to check for strong correlations in the posterior
az.plot_pair(inference, var_names=["alpha", "beta", "gamma", "delta"])
plt.savefig("plots/LotkaVolterraPair.png", dpi=600)
plt.close()

# Plot Leave-One-Out probability integral transformation (PIT) predictive 
# checks to check that the model adequetly represents the data
az.plot_loo_pit(inference, y="y", y_hat="y_rep")
plt.savefig("plots/LotkaVolterraLooPit.png", dpi=600)
plt.close()


# Extract the posterior predictive 
y_hat = fit["y_rep"]

y_hat_lb = np.percentile(y_hat, 2.5, axis=2)
y_hat_ub = np.percentile(y_hat, 97.5, axis=2)
y_hat_med = np.median(y_hat, axis=2)

# Overlay the posterior predictive 95% CI atop the data
fig, axes = plt.subplots(2, 1, sharex=True)
axes[0].plot(df["Year"], df["Hare"], 'blue')
axes[0].fill_between(df["Year"], y_hat_lb[:, 0], y_hat_ub[:, 0], alpha=0.2)
axes[0].set_ylabel("Hare Population\n(Thousands)")

axes[1].plot(df["Year"].values, df["Lynx"].values, 'orange')       
axes[1].fill_between(df["Year"], y_hat_lb[:, 1], y_hat_ub[:, 1], alpha=0.2)
axes[1].set_ylabel("Lynx Population\n(Thousands)")
axes[1].set_xlabel("Date")
axes[1].xaxis.set_major_locator(MaxNLocator(integer=True))
fig.savefig("plots/LotkaVolterraPosteriorPredictive.png", dpi=600)
plt.close()

# Plot 50 of the posterior predictive samples in phase space
fig, ax = plt.subplots()
for i in range(50):
    plt.plot(y_hat[:, 0, i], y_hat[:, 1, i], alpha=0.2, color='blue')
plt.scatter(df["Hare"], df["Lynx"], color='k')
plt.xlabel("Hare Population\n(Thousands)")
plt.ylabel("Lynx Population\n(Thousands)")
plt.tight_layout()
fig.savefig("plots/LotkaVolterraPhasePlots.png", dpi=600)
plt.close()
