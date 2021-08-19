from velocity.velocity import Velocity, VelocityItem
from capacity.capacity import Capacity, Person, PresentItem
from datetime import datetime

def main():

    start_date = datetime.strptime("2021-07-19", "%Y-%m-%d")

    velocity_data = [
        VelocityItem("Sprint 1", 10, 42, 0.9),
        VelocityItem("Sprint 2", 10, 47, 0.85),
    ]
    velocity_calculations = Velocity(velocity_data)

    person0 = Person("M0", "K0", start_date, 14)
    person0.presences["2021-07-19"].presence = False
    person0.presences["2021-07-20"].presence = False
    person0.presences["2021-07-21"].presence = False
    person0.presences["2021-07-22"].presence = False
    person0.presences["2021-07-23"].presence = False
    person1 = Person("M1", "K1", start_date, 14)
    person2 = Person("M2", "K2", start_date, 14)
    person3 = Person("M3", "K3", start_date, 14)
    person3.presences["2021-07-19"].presence = False
    person3.presences["2021-07-20"].presence = False
    person3.presences["2021-07-21"].presence = False
    person3.presences["2021-07-22"].presence = False
    person3.presences["2021-07-23"].presence = False
    person4 = Person("M4", "K4", start_date, 14)

    capacity_data = [
        person0,
        person1,
        person2,
        person3,
        person4,
    ]
    capacity_calculations = Capacity(capacity_data)

    print(f"Velocity: {velocity_calculations.calculate_velocity()} sp")
    print(f"Presence: {capacity_calculations.calculate_presence() * 100} %")
    print(f"Capacity: {capacity_calculations.calculate_actual_capacity(velocity_calculations.calculate_velocity())} sp")

if __name__ == "__main__":
    main()
