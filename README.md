# Epidemic Disease Simulator

This is a clean, simple project that simulates how a virus spreads through a population of 10,000 people over 150 days. 

## How It Works
Instead of using rigid, perfect math formulas where the numbers are exactly the same every time, this simulator uses random dice rolls (Binomial Distribution). 

Every day of the simulation, the code calculates the chance of someone catching the virus or recovering, and then flips a bunch of virtual coins. Because it uses randomness, every single simulation run looks slightly different, which is exactly how real-world outbreaks work.

People in the simulation move through 4 stages:
- S (Susceptible): Healthy people who can catch the bug.
- E (Exposed): People who have the virus but are still in the incubation phase (not contagious yet).
- I (Infected): Sick people who are actively spreading it.
- R (Recovered): People who got better and are now completely immune.

## What It Proves (The Features)
The project runs a parameter sweep, which is just a fancy way of saying it tests different "what-if" scenarios:
1. No Interventions: Everyone acts normal. The virus spikes super fast and high.
2. Wearing Masks: The risk goes down, lowering the peak.
3. Strict Lockdown: The risk drops significantly, delaying the spike and completely flattening the curve.

By running each scenario 10 times, the graph shows both the messy individual random lines and the bold average trend.
