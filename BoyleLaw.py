from BACON import *

# record the data
volumes = np.array([1.0, 1.5, 2.0, 3.0, 4.0, 5.0, 6.0, 7.0, 8.0, 9.0, 10.0,
    12.0, 14.0, 16.0, 18.0, 20.0, 24.0, 28.0, 32.0])

V = Term('V', volumes)

pressures = np.array([29.750, 19.125, 14.375, 9.500, 7.125, 5.625, 4.875, 4.250,
    3.750, 3.375, 3.000, 2.625, 2.250, 2.000, 1.875, 1.750, 1.500, 1.375,
    1.250])

P = Term('P', pressures)

data = Table([V, P])

# introduce the rules to use
constant = Constant(0.20)
linear = Linear(0.10)
increasing = Increasing()
decreasing = Decreasing()

rules = [constant, linear, increasing, decreasing]

# have BACON search for laws

laws = data.find_laws(rules)

# output results
print("**** \nHere's what I found: ")

while len(laws) > 0:
    print(laws.pop())
