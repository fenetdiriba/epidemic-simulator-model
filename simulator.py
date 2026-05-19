#include <iostream>
#include <vector>
#include <random>
#include <string>
#include <numeric>
#include <algorithm>
#include <iomanip>

// --- Constants ---
const int    POPULATION      = 10000;
const int    DAYS            = 150;
const int    INIT_INFECTED   = 5;
const double INCUBATION_RATE = 1.0 / 5.0;
const double RECOVERY_RATE   = 1.0 / 10.0;
const int    NUM_TRIALS      = 10;

// --- Result struct ---
struct SimResult {
    std::vector<double> infected_curve;
    double peak_value;
    int    peak_day;
};

// --- Scenario struct ---
struct Scenario {
    std::string name;
    double      beta;
};

// --- SEIR Simulator class ---
class SEIRSimulator {
public:
    SEIRSimulator() : rng_(std::random_device{}()) {}

    SimResult run(double transmission_rate) {
        std::vector<double> S(DAYS), E(DAYS), I(DAYS), R(DAYS);

        S[0] = POPULATION - INIT_INFECTED;
        E[0] = 0;
        I[0] = INIT_INFECTED;
        R[0] = 0;

        for (int t = 1; t < DAYS; ++t) {
            double prob_infection   = (transmission_rate * I[t-1]) / POPULATION;

            int new_exposed   = sample_binomial(static_cast<int>(S[t-1]), prob_infection);
            int new_infected  = sample_binomial(static_cast<int>(E[t-1]), INCUBATION_RATE);
            int new_recovered = sample_binomial(static_cast<int>(I[t-1]), RECOVERY_RATE);

            S[t] = S[t-1] - new_exposed;
            E[t] = E[t-1] + new_exposed  - new_infected;
            I[t] = I[t-1] + new_infected - new_recovered;
            R[t] = R[t-1] + new_recovered;
        }

        auto peak_it = std::max_element(I.begin(), I.end());

        return SimResult{
            I,
            *peak_it,
            static_cast<int>(std::distance(I.begin(), peak_it))
        };
    }

private:
    std::mt19937 rng_;

    int sample_binomial(int n, double p) {
        if (n <= 0 || p <= 0.0) return 0;
        std::binomial_distribution<int> dist(n, p);
        return dist(rng_);
    }
};

// --- Aggregate helper: compute element-wise mean across runs ---
std::vector<double> compute_mean(const std::vector<std::vector<double>>& runs) {
    std::vector<double> mean(DAYS, 0.0);
    for (const auto& run : runs)
        for (int d = 0; d < DAYS; ++d)
            mean[d] += run[d];
    for (auto& v : mean) v /= static_cast<double>(runs.size());
    return mean;
}

// --- Main ---
int main() {
    std::vector<Scenario> scenarios = {
        {"No Interventions", 0.40},
        {"Wearing Masks",    0.25},
        {"Strict Lockdown",  0.12}
    };

    SEIRSimulator simulator;

    std::cout << "\nStochastic SEIR Simulator — Flattening the Curve\n";
    std::cout << std::string(52, '-') << "\n";
    std::cout << std::fixed << std::setprecision(0);

    for (const auto& scenario : scenarios) {
        std::vector<std::vector<double>> all_runs;
        all_runs.reserve(NUM_TRIALS);

        for (int trial = 0; trial < NUM_TRIALS; ++trial)
            all_runs.push_back(simulator.run(scenario.beta).infected_curve);

        auto mean_curve = compute_mean(all_runs);

        auto peak_it  = std::max_element(mean_curve.begin(), mean_curve.end());
        int  peak_day = static_cast<int>(std::distance(mean_curve.begin(), peak_it));

        std::cout << std::left << std::setw(22) << scenario.name
                  << "-> Avg Peak: " << std::setw(6) << *peak_it
                  << " people on Day " << peak_day << "\n";
    }

    std::cout << std::string(52, '-') << "\n";
    return 0;
}
