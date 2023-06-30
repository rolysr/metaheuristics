from cProfile import label
from math import sqrt
from typing import Callable, Iterator, Optional, Tuple

import numpy as np
from attr import dataclass

# Weight constants
INITIAL_WEIGHT = 480.0  # Kg
FULL_TANK_WEIGHT = 105.0  # Kg
MIN_ENGIE_WEIGHT = 160.0  # Kg
KG_PER_CYLINDER = 15.0
BODYWORK_BEST_WEIGHT = 90  # Kg

# Cost constants
GAS_PRICE_PER_KG = 1.027
BODYWORK_COST_RANGE = (700.0, 1500.0)
WHEEL_PRICE = 100.0
ENGINE_BASE_PRICE = 3000.0

# Simulation
DT = 1e-2


@dataclass
class CarState:
    distance: float
    velocity: float
    time: float
    gas: float


class Car:
    def __init__(
        self,
        gas_ammount: float,
        aerodynamic: float,
        cylinder_count: int,
        cylinder_cc: float,
    ) -> None:
        assert 0 <= gas_ammount <= 1
        assert 0 <= aerodynamic <= 1
        assert 1 <= cylinder_count <= 8
        assert cylinder_cc > 0

        self.gas_ammount = gas_ammount
        self.aerodynamic = aerodynamic
        self.cylinder_count = cylinder_count
        self.cylinder_cc = cylinder_cc
        self.engine_size = self.cylinder_cc * self.cylinder_count
        self.max_hp = self.engine_size / 10
        self.gas = self.gas_ammount * FULL_TANK_WEIGHT
        self.gas_consumption_rate = (
            (0.5 * self.max_hp) * 0.0010515 / 6.1
        )  # Liters per sec

        self.engine_weight = MIN_ENGIE_WEIGHT + self.cylinder_count * KG_PER_CYLINDER
        self.bodywork_weight = BODYWORK_BEST_WEIGHT
        if self.aerodynamic < 1:
            self.bodywork_weight -= (BODYWORK_BEST_WEIGHT / 4) ** (1 - self.aerodynamic)

    def reset(self):
        self.gas = self.gas_ammount * FULL_TANK_WEIGHT

    @property
    def weight(self) -> float:
        return INITIAL_WEIGHT + self.gas + self.engine_weight + self.bodywork_weight

    @property
    def cost(self) -> float:
        bodywork_price = (
            BODYWORK_COST_RANGE[0]
            + (BODYWORK_COST_RANGE[1] - BODYWORK_COST_RANGE[0]) * self.aerodynamic
        )
        engine_price = (
            ENGINE_BASE_PRICE + 700 * self.cylinder_count + 0.4 * self.cylinder_cc
        )
        return (
            self.gas_ammount * FULL_TANK_WEIGHT * GAS_PRICE_PER_KG
            + bodywork_price
            + engine_price
        )

    @property
    def max_velocity(self):
        return 100 * sqrt(self.max_hp / self.weight)

    def _step(self, vel, dist) -> Tuple[float, float]:
        max_v = self.max_velocity
        max_hp = self.max_hp - (vel / max_v) * self.max_hp
        aerodyn_factor = 1 - (1 - self.aerodynamic) * (vel * 2 / max_v) ** 2
        d_vel = sqrt((2 * max_hp * DT) / self.weight) * aerodyn_factor
        if vel + d_vel > max_v:
            d_vel = (max_v - vel) * 0.2
        vel += d_vel
        dist += vel * DT
        self.gas -= self.gas_consumption_rate * DT
        return vel, dist

    def simulate_race(
        self,
        max_distance: float = np.inf,
        max_time: float = np.inf,
    ) -> Iterator[CarState]:
        self.reset()
        t = 0.0
        dist, vel = 0.0, 0.0
        yield CarState(gas=self.gas, distance=0.0, velocity=0.0, time=t)
        while t < max_time and dist < max_distance and self.gas > 0:
            vel, dist = self._step(vel, dist)
            yield CarState(gas=self.gas, distance=dist, velocity=vel, time=t)
            t += DT

    def race(
        self,
        max_time: float = np.inf,
        max_distance: float = np.inf,
    ) -> CarState:
        self.reset()
        t = 0.0
        dist, vel = 0.0, 0.0
        while t < max_time and dist < max_distance and self.gas > 0:
            vel, dist = self._step(vel, dist)
            t += DT
        return CarState(gas=self.gas, distance=dist, velocity=vel, time=t)
