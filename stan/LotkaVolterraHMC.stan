functions{
    vector LotkaVolterra(real t, vector z, real alpha, real beta, real gamma, real delta) {
    vector[2] dz_dt;

    dz_dt[1] = (alpha - beta * z[2]) * z[1];
    dz_dt[2] = (-gamma + delta * z[1]) * z[2];

    return dz_dt;
    }
}
data {
    int<lower = 0> N;                 // num measurements
    array[N] real ts;                 // measurement times > 0
    array[N, 2] real<lower = 0> y;    // measured population at measurement times
}
transformed data{
    real t_init=ts[1];                      // initial time
}
parameters {
    real<lower=0> alpha;
    real<lower=0> beta;
    real<lower=0> gamma;
    real<lower=0> delta;
    vector<lower = 0>[2] z_init;  // initial population
    array[2] real<lower = 0> sigma;   // error scale
}
transformed parameters {
    array[N-1] vector[2] z;

    z = ode_rk45(LotkaVolterra, z_init, t_init, ts[2:N], alpha, beta, gamma, delta);
}
model {
    // Priors
    alpha ~ std_normal();
    beta ~ normal(0, 0.05);
    gamma ~ std_normal();
    delta ~ normal(0, 0.05);

    sigma ~ lognormal(-1, 1);
    z_init ~ lognormal(log(10), 1);

    // likelihood
    for (k in 1:2) {
        y[1, k] ~ lognormal(log(z_init[k]), sigma[k]);
        y[2:N, k] ~ lognormal(log(z[:, k]), sigma[k]);

    }
}
generated quantities {
    array[N, 2] real y_rep;
    array[N, 2] real log_lik;

    for (k in 1:2) {
        y_rep[1, k] = lognormal_rng(log(z_init[k]), sigma[k]);
        log_lik[1, k] = lognormal_lpdf(y[1, k] | log(z_init[k]), sigma[k]);
        for (n in 2:N){
            y_rep[n, k] = lognormal_rng(log(z[n-1, k]), sigma[k]);
            log_lik[n, k] = lognormal_lpdf(y[n, k] | log(z[n-1, k]), sigma[k]);
        }
    }
}