import numpy as np
import matplotlib.pyplot as plt

POPULATION = 10000
DAYS = 150
INIT_INFECTED = 5

INCUBATION_RATE = 1 / 5.0  
RECOVERY_RATE = 1 / 10.0  

def run_seir_simulation(transmission_rate):
    S = np.zeros(DAYS)  
    E = np.zeros(DAYS)  
    I = np.zeros(DAYS)  
    R = np.zeros(DAYS)  
    
    I[0] = INIT_INFECTED
    E[0] = 0
    R[0] = 0
    S[0] = POPULATION - INIT_INFECTED

    for t in range(1, DAYS):
        S_past = S[t-1]
        E_past = E[t-1]
        I_past = I[t-1]
        R_past = R[t-1]
        
        prob_get_sick = (transmission_rate * I_past) / POPULATION
        prob_get_contagious = INCUBATION_RATE
        prob_get_well = RECOVERY_RATE
        
        new_exposed = np.random.binomial(S_past, prob_get_sick) if S_past > 0 else 0
        new_infected = np.random.binomial(E_past, prob_get_contagious) if E_past > 0 else 0
        new_recovered = np.random.binomial(I_past, prob_get_well) if I_past > 0 else 0
        
        S[t] = S_past - new_exposed
        E[t] = E_past + new_exposed - new_infected
        I[t] = I_past + new_infected - new_recovered
        R[t] = R_past + new_recovered
        
    return I  

scenarios = {
    "No Interventions": {"beta": 0.40, "color": "red"},
    "Wearing Masks": {"beta": 0.25, "color": "orange"},
    "Strict Lockdown": {"beta": 0.12, "color": "green"}
}

plt.figure(figsize=(10, 5))

for name, settings in scenarios.items():
    all_runs = []
    for trial in range(10):
        infected_curve = run_seir_simulation(settings["beta"])
        all_runs.append(infected_curve)
        plt.plot(infected_curve, color=settings["color"], alpha=0.15)
    
    mean_curve = np.mean(all_runs, axis=0)
    plt.plot(mean_curve, color=settings["color"], linewidth=2.5, label=name)
    
    peak_value = int(np.max(mean_curve))
    peak_day = np.argmax(mean_curve)
    print(f"{name} -> Average Peak: {peak_value} people sick on Day {peak_day}")

plt.title("Stochastic SEIR Simulator: Flattening the Curve", fontsize=12)
plt.xlabel("Days")
plt.ylabel("Active Cases (Infected)")
plt.grid(True, linestyle=":", alpha=0.6)
plt.legend()
plt.tight_layout()
plt.show()
