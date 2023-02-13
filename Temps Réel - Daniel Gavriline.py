import datetime
import time

class Pump:
    def __init__(self, period, execution_time, production_quantity_oil):
        self.period = period
        self.execution_time = execution_time
        self.production_quantity_oil = production_quantity_oil
        self.last_execution = -period

    def is_ready(self, current_time):
        return current_time - self.last_execution >= self.period

    def produce_oil(self, tank):
        time.sleep(self.execution_time)
        tank.add_oil(self.production_quantity_oil)
        self.last_execution = time.time()


class Tank:
    def __init__(self, max_quantity_oil):
        self.quantity_oil = 0
        self.max_quantity_oil = max_quantity_oil

    def add_oil(self, quantity):
        if self.quantity_oil + quantity > self.max_quantity_oil:
            self.quantity_oil = self.max_quantity_oil
        else:
            self.quantity_oil += quantity


class Machine:
    def __init__(self, name, required_oil_quantity, execution_time, period, stock):
        self.name = name
        self.required_oil_quantity = required_oil_quantity
        self.execution_time = execution_time
        self.period = period
        self.stock = stock
        self.last_execution = -period

    def is_ready(self, current_time):
        return current_time - self.last_execution >= self.period

    def run_machine(self, tank):
        if tank.quantity_oil >= self.required_oil_quantity:
            tank.quantity_oil -= self.required_oil_quantity
            self.stock += 1
            time.sleep(self.execution_time)
            self.last_execution = time.time()


def main():
    #Start production
    print(f"Production started at {datetime.datetime.now()}")

    # Initialize the pump and machine objects
    pump1 = Pump(5, 2, 10)
    pump2 = Pump(period=15, execution_time=3, production_quantity_oil=20)
    machine1 = Machine(name='Machine 1', required_oil_quantity=25, stock=0, period=5, execution_time=5)
    machine2 = Machine(name='Machine 2', required_oil_quantity=5, stock=0, period=5, execution_time=3)
    tank = Tank(50)

    # Initialize the counters for motors and wheels
    nb_motors = 0
    nb_wheels = 0
    nb_engines = 0

    # Start the 2-minute simulation
    for t in range(120):
        if tank.quantity_oil == tank.max_quantity_oil:
            # If the tank is full, give low priority to pumps
            if t % pump1.period == 0:
                pump1.produce_oil(tank)
            elif t % pump2.period == 0:
                pump2.produce_oil(tank)
        else:
            # If the tank is not full, give priority to pumps
            if t % pump1.period == 0:
                pump1.produce_oil(tank)
            elif t % pump2.period == 0:
                pump2.produce_oil(tank)

            # Check if Machine 1 should be prioritized
            if nb_wheels // 4 > nb_motors:
                if t % machine1.period == 0 and tank.quantity_oil >= machine1.required_oil_quantity:
                    nb_motors += 1
                    tank.quantity_oil -= machine1.required_oil_quantity
            # Check if either Machine 1 or Machine 2 can run
            elif t % machine1.period == 0 and tank.quantity_oil >= machine1.required_oil_quantity:
                nb_motors += 1
                tank.quantity_oil -= machine1.required_oil_quantity
            elif t % machine2.period == 0 and tank.quantity_oil >= machine2.required_oil_quantity:
                nb_wheels += 1
                tank.quantity_oil -= machine2.required_oil_quantity

        if nb_motors >= 1 and nb_wheels >= 4:
            print(f"1 engine created at {datetime.datetime.now()}")
            nb_engines += 1
            nb_motors -= 1
            nb_wheels -= 4
    print(f"Engines created: {nb_engines} with {nb_motors} remaning motors and {nb_wheels} remaining wheels")

if __name__ == "__main__":
    main()
