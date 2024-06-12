from typing import Callable
import numpy as np

INITIAL_INVESTMENT = 1


def invest(period_start_index: int, period_length: int, interest_leverage: float,
           possible_interests: np.array, initial_investment: float = INITIAL_INVESTMENT,
           commission: float = 1, years: int = 1):
    """
    Simulate investment for a given period of time.It receives an array of interest values and simulate
    an investment for a given period using those values.

    @param period_start_index: start index of the investing period
    @param period_length: length of the investing period
    @param interest_leverage: leverage of the interest
    @param possible_interests: possible interest values to use for the simulation, ordered chronologicaly
    @param initial_investment: initial investment value, defaulted to 1 to show total interest as decimal percentage
    @param commission: yearly commission rate
    @param years: number of years commission was taken
    """
    total_commission = commission ** years
    interests = possible_interests[period_start_index:period_start_index + period_length] * interest_leverage
    interests = np.where(interests + 1 < 0, 0, interests)
    cash = np.cumprod(np.insert(interests + 1, 0, initial_investment))
    cash[-1] = cash[-1] * total_commission
    return cash


def stats_per_period(possible_interests: np.array, period: int, leverage: float = 1,
                     commission: float = 1, years: int = 1,
                     *funcs: Callable[[np.array], float]):
    """
    Given an array of investment values, simulate an investment for a given period for each possible chronological
    time period within the possible_interests array and return an array of statistics for each possible time period
    each statistic is calculated with a function given in the *funcs argument

    @param period: length of the period of investing the period should not exceed the length of possible_interests

    @param possible_interests: used to produce cash values see explanation above in "invest" function
    @param leverage: used to produce cash values see explanation above in "invest" function
    @param commission: used to produce cash values see explanation above in "invest" function
    @param years: used to produce cash values see explanation above in "invest" function
    @param funcs: functions which receive the array of cash values and return a statistic for the period

    """
    if period > len(possible_interests):
        raise ValueError("period should not exceed the length of possible_interests")
    stats = [[] for _ in funcs]
    for start_index in range(len(possible_interests) - period):
        cash_array = invest(period_start_index=start_index,
                            period_length=period,
                            interest_leverage=leverage,
                            possible_interests=possible_interests,
                            commission=commission, years=years)
        for func in funcs:
            stats[funcs.index(func)].append(func(cash_array))
    return stats


def probabiliy_losing(percentage_lost: float, initial_investment: float = INITIAL_INVESTMENT):
    """
    a helper function which return a function which receives an array of cash values and return
     True if at any point the amount was less than percentage_lost*initial_investment

    @param percentage_lost: percentage of the  loss from the initial investment
    @param initial_investment:  value  of initial investment
    """

    def func(cash_array):
        return np.any(np.array(cash_array) <= percentage_lost * initial_investment)

    return func


def get_last(x):
    """returns the last value of an array
    @param x: the array"""
    return x[-1]
