import random
import time

# --- Configuration ---
# You can modify these parameters to change the simulation's behavior.
TOTAL_TIME_STEPS = 50  # Number of simulation steps to run
ROAD_LENGTH = 1000     # Length of the road in meters
TRAFFIC_SIGNAL_POSITION = 500  # Position of the traffic signal
TRAFFIC_SIGNAL_CYCLE = 10      # Number of steps for a full light cycle (green then red)
INITIAL_CAR_COUNT = 3  # Number of cars to start the simulation

class Car:
    """
    Represents a single car in the simulation.
    Each car has a unique ID, position, and speed.
    """
    def __init__(self, car_id, position=0, max_speed=5):
        self.id = car_id
        self.position = position
        self.max_speed = max_speed
        self.current_speed = random.uniform(1, max_speed)
        self.state = "driving"
        print(f"Car {self.id} initialized at position {self.position} with speed {self.current_speed:.2f} m/s.")

    def update(self, delta_time, cars, traffic_signal):
        """
        Updates the car's state for a single time step.
        Checks for traffic signals and other cars to adjust its speed and state.
        """
        if self.state == "driving":
            # Check for traffic signal
            if self.position >= traffic_signal.position - 10 and traffic_signal.state == "red":
                if self.current_speed > 0:
                    self.current_speed = max(0, self.current_speed - 1)  # Slow down
                if self.current_speed == 0:
                    self.state = "stopped"
                    print(f"Car {self.id} stopped at signal.")

            # Check for cars ahead
            for other_car in cars:
                if self.id != other_car.id and other_car.position > self.position:
                    distance = other_car.position - self.position
                    # Simple collision avoidance: slow down if too close to the car ahead
                    if distance < 15:
                        if self.current_speed > other_car.current_speed:
                            self.current_speed = max(1, self.current_speed - 2)
                        print(f"Car {self.id} is slowing down due to Car {other_car.id} ahead.")
                    
            # Move the car
            self.position += self.current_speed * delta_time
            if self.position >= ROAD_LENGTH:
                self.state = "finished"
                print(f"Car {self.id} has finished the road.")
            
        elif self.state == "stopped":
            # Check if the traffic signal has turned green
            if traffic_signal.state == "green":
                self.state = "driving"
                self.current_speed = random.uniform(1, self.max_speed)
                print(f"Car {self.id} started driving again (signal is green).")

    def __repr__(self):
        """
        Provides a string representation of the car for easy logging.
        """
        return f"Car({self.id}): pos={self.position:.2f}m, speed={self.current_speed:.2f}m/s, state='{self.state}'"

class TrafficSignal:
    """
    Manages the state of a traffic signal.
    """
    def __init__(self, position, cycle_time):
        self.position = position
        self.cycle_time = cycle_time
        self.state = "green"  # Initial state
        self.time_in_state = 0
        print(f"Traffic signal initialized at position {self.position}m.")

    def update(self, delta_time):
        """
        Switches the light state based on the cycle time.
        """
        self.time_in_state += delta_time
        if self.time_in_state >= self.cycle_time:
            self.time_in_state = 0
            self.state = "red" if self.state == "green" else "green"
            print(f"Traffic signal at {self.position}m is now {self.state.upper()}.")

class Simulation:
    """
    The main simulation orchestrator.
    Manages all cars and signals and runs the simulation loop.
    """
    def __init__(self):
        self.cars = [Car(i, position=random.uniform(0, 50)) for i in range(INITIAL_CAR_COUNT)]
        self.traffic_signal = TrafficSignal(TRAFFIC_SIGNAL_POSITION, TRAFFIC_SIGNAL_CYCLE)
        self.time_step = 1  # 1 second per step
        self.current_step = 0

    def run(self):
        """
        Main simulation loop.
        """
        print("\n--- Starting Simulation ---\n")
        while self.current_step < TOTAL_TIME_STEPS:
            print(f"\n--- Time Step {self.current_step} ---")

            # Update traffic signal
            self.traffic_signal.update(self.time_step)

            # Update each car
            for car in self.cars:
                car.update(self.time_step, self.cars, self.traffic_signal)

            # Print current status of all cars
            for car in self.cars:
                print(car)
            
            self.current_step += 1
            time.sleep(0.5)  # Pause to make the simulation visible in the console

        print("\n--- Simulation Finished ---\n")

# Run the simulation
if __name__ == "__main__":
    sim = Simulation()
    sim.run()
