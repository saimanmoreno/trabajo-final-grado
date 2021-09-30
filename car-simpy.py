import simpy

def car(env):
    while True:
        print('Start parking at %d' % env.now)
        parking_duration = 5
        yield env.timeout(parking_duration)

        print('Start driving at %d' % env.now)
        trip_duration = 2
        yield env.timeout(trip_duration)

env  = simpy.Environment()
env.process(car(env))

env.run(until=15)

# OUTPUT:
# Start parking at 0
# Start driving at 5 
# Start parking at 7 
# Start driving at 12
# Start parking at 14
