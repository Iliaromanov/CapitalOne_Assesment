from enum import Enum
from typing import Any, Dict, List, Set, Tuple


class MerchantCode(Enum):
    SPORTCHECK = "sportcheck"
    TIM_HORTONS = "tim_hortons"
    SUBWAY = "subway"
    OTHER = "other"


# Defined merchants must include a value for OTHER
DEFAULT_DEFINED_MERCHANTS = {
    MerchantCode.SPORTCHECK.value,
    MerchantCode.TIM_HORTONS.value,
    MerchantCode.SUBWAY.value,
    MerchantCode.OTHER.value
}

"""
Rules format:
[
    {
        "Points": int, 
        "Reqs": [
            (MerchantCode: int), ...
        ]
    },
    ...
]
"""
DEFAULT_RULES = [
    # Rule 1
    {
        "Points": 500,
        "Reqs": [
            (MerchantCode.SPORTCHECK.value, 75),
            (MerchantCode.TIM_HORTONS.value, 25),
            (MerchantCode.SUBWAY.value, 25)
        ]
    },
    # Rule 2
    {
        "Points": 300,
        "Reqs": [
            (MerchantCode.SPORTCHECK.value, 75),
            (MerchantCode.TIM_HORTONS.value, 25)
        ]
    },
    # Rule 3
    {
        "Points": 200,
        "Reqs": [
            (MerchantCode.SPORTCHECK.value, 75)
        ]
    },
    # Rule 4
    {
        "Points": 150,
        "Reqs": [
            (MerchantCode.SPORTCHECK.value, 25),
            (MerchantCode.TIM_HORTONS.value, 10),
            (MerchantCode.SUBWAY.value, 10)
        ]
    },
    # Rule 5
    {
        "Points": 75,
        "Reqs": [
            (MerchantCode.SPORTCHECK.value, 25),
            (MerchantCode.TIM_HORTONS.value, 10),
        ]
    },
    # Rule 6
    {
        "Points": 75,
        "Reqs": [
            (MerchantCode.SPORTCHECK.value, 20),
        ]
    },
    # Rule 7
    {
        "Points": 1,
        "Reqs": [
            # Here OTHER encompasses the other defined MerchantCodes as 
            #  well as any non-defined merchant codes
            (MerchantCode.OTHER.value, 1)
        ]
    },
]


class RewardPointsCalculator:
    def __init__(
        self, 
        transactions: Dict[str, Dict[str, Any]],
        rules: List[Dict[str, Any]] = DEFAULT_RULES,
        defined_merchants: Set[str] = DEFAULT_DEFINED_MERCHANTS
    ) -> None:
        """Constructor"""
        self._raw_transactions = transactions
        self._rules = rules
        self._defined_merchants = defined_merchants
        self._total_transaction_amount = 0

        # sets self._parsed_transactions attr
        # and updates self._total_transaction_amount
        self.parse_transactions()

    def parse_transactions(self) -> None:
        """
        Parses raw transactions by summing values with same
        merchant_code and putting unknown merchants into 'other'

        sets self._parsed_transactions attribute
        """
        # init all merchants to 0
        transactions = {
            merchant_code: 0.0 for merchant_code in self._defined_merchants
        }

        for transaction in list(self._raw_transactions.values()):
            merchant = transaction["merchant_code"]
            if merchant not in self._defined_merchants:
                merchant = MerchantCode.OTHER.value
            # immediately conver to dollar
            amount = transaction["amount_cents"] / 100
            
            self._total_transaction_amount += amount
            transactions[merchant] += amount

        self._parsed_transactions = transactions


    def maximum_reward_per_transaction(
        self
    )-> List[Tuple[int, Dict[str, List[int]]]]:
        """
        Compute max reward points per transaction based on
        self._raw_transactions

        Returns:
            list of tuples -- (
                    max_reward_for_transaction, 
                    {"rules_used": [rules_used]}
                )
                index of each tuple denotes the transaction number
        """
        rewards = []
        for transaction in list(self._raw_transactions.values()):
            # add transaction for transsaction["merchant_code"]
            #  and a 0$ transaction for 'other' in case Rule 7 required
            parsed_transaction = {
                transaction[
                    "merchant_code"
                ]: transaction["amount_cents"] / 100,
                MerchantCode.OTHER.value: 0
            }

            # check if need to merge to 'other' for Rule 7
            if self._must_merge_to_other(parsed_transaction):
                rule_7_reward = self._merge_to_other(parsed_transaction)
                rewards.append((rule_7_reward, {"rules_used": [7]}))
                continue

            # iterate over all rules from highest reward to lowest
            #  break when an applicable rule is reached
            for rule_num, rule in enumerate(self._rules):
                reqs = rule["Reqs"]
                num_times_applicable = self._rule_applicable(
                    parsed_transaction, reqs
                )   
                if num_times_applicable:
                    # rules are 0 indexed
                    rewards.append((
                        rule["Points"] * num_times_applicable,
                        # use rule number num_times_applicable times
                        {"rules_used": [rule_num + 1] * num_times_applicable}
                    ))
                    break

        print("Rewards: ", rewards)

        return rewards

    def maximum_reward_for_month(self) -> Tuple[int, List[int]]:
        """
        Compute maximum reward for month based on self._parsed_transactions

        * This current algo is only applicable to the DEFAULT_RULES
           above (given in assesment), but this method can be updated
           to return max reward points for different sets of rules

        Returns:
            tuple -- (max_reward: int, rules_used: List[int])
        """

        # Will use the following logic (for DEFAULT_RULES):
        #  Rule 1 > Rule 2 > 2*Rule 4 > Rule 3 > Rule 6 > Rule 7
        #  Rule 5 should never be used since Rule 6 + Rule 7 can be used
        #   to produce bigger reward instead
        total_remainig = self._total_transaction_amount
        transactions = self._parsed_transactions.copy()
        rules_used = []
        reward = 0

        while total_remainig >= 1:
            # check if only Rule 7 is applicable
            # if so, then add all remaining transaction amounts
            #  into the 'other' category and apply Rule 7
            if self._must_merge_to_other(transactions):
                amount = self._merge_to_other(transactions)
                total_remainig -= amount
                reward += amount
                rules_used.append(7) # will only append 7 once to keep it clean
                break
            
            # Note that self._rules is 0 indexed

            # Rule 1
            if self._rule_applicable(transactions, self._rules[0]["Reqs"]):
                reward += self._rules[0]["Points"]
                rules_used.append(1)
                total_remainig -= self._apply_rule(
                    transactions, self._rules[0]["Reqs"]
                )
                continue
            # Rule 2
            elif self._rule_applicable(transactions, self._rules[1]["Reqs"]):
                reward += self._rules[1]["Points"]
                rules_used.append(2)
                total_remainig -= self._apply_rule(
                    transactions, self._rules[1]["Reqs"]
                )
                continue
            # 2 x Rule 4
            elif self._rule_applicable(transactions, self._rules[3]["Reqs"]) == 2:
                reward += self._rules[3]["Points"] * 2
                rules_used.append(4)
                rules_used.append(4)
                total_remainig -= self._apply_rule(
                    transactions, self._rules[3]["Reqs"], 2
                )
                continue
            # Rule 3 
            elif self._rule_applicable(transactions, self._rules[2]["Reqs"]):
                reward += self._rules[2]["Points"]
                rules_used.append(3)
                total_remainig -= self._apply_rule(
                    transactions, self._rules[2]["Reqs"]
                )
                continue
            # Rule 6
            elif self._rule_applicable(transactions, self._rules[5]["Reqs"]):
                reward += self._rules[5]["Points"]
                rules_used.append(6)
                total_remainig -= self._apply_rule(
                    transactions, self._rules[5]["Reqs"]
                )
                continue
        
        print("Maximum Reward Points For Month: ", reward)
        print("Rules Used: ", rules_used)

        return (reward, rules_used)


    @staticmethod
    def _rule_applicable(
        transactions: Dict[str, float], 
        reqs: List[Tuple[str, int]]
    ) -> int:
        """
        Checks how many times Rule with requirements == reqs
        can be applied

        Args:
            transactions -- a dict of parsed transactions 
                          (same format as self._parsed_transactions)
            reqs -- a list of requirements 
                    (see DEFAULT_RULES[i]["Reqs"] above for format)
        
        Returns:
            int -- number of times rule can be applied
        """
        # counts of how many times a req can be applied to a specific
        #  merchant within transaction
        number_of_applications = []
        for merchant, amount in reqs:
            if merchant not in transactions or \
               transactions[merchant] < amount:
                return 0
            else:
                number_of_applications.append(
                    transactions[merchant] // amount
                )
        
        # the max number of times a rule can be applied to a transaction is 
        #  limited by the number of times a req can be applied to any 
        #  specific merchant within the transaction
        return int(min(number_of_applications))
    
    @staticmethod
    def _apply_rule(
        transactions: Dict[str, float],
        reqs: List[Tuple[str, int]],
        times: int = 1
    ) -> int:
        """
        modifies transaction in place to decrement ammounts
        returns total decremented

        * Expects that _rule_applicable(transactions, reqs, times)
          has returned True

        Args:
            transactions -- a dict of parsed transactions 
                          (same format as self._parsed_transactions)
            reqs -- a list of requirements 
                    (see DEFAULT_RULES[i]["Reqs"] above for format)
            times -- the number of times the rule is applied
        
        Returns:
            the total amount deducted from transaction total to apply the Rule
        """
        total = 0
        for merchant, amount in reqs:
            transactions[merchant] -= amount * times
            total += amount * times

        return total

    @staticmethod
    def _must_merge_to_other(transactions: Dict[str, float]) -> bool:
        """
        This method is specific to the DEFAULT_RULES given in the assesment;
        it checks if none of the rules other than Rule 7 can be applied
        (if that is the case, then we must merge 'subway' and 'tim_hortons'
         into the other category to be used as left over amount)

        Args:
            transactions -- a dict of parsed transactions 
                          (same format as self._parsed_transactions)
        Returns:
            bool -- whether we need to merge the other merchants 
                     values into 'other' or not
        """
        return MerchantCode.SPORTCHECK.value not in transactions or \
            transactions[MerchantCode.SPORTCHECK.value] < 20

    @staticmethod
    def _merge_to_other(transactions: Dict[str, float]) -> int:
        """
        Merges all remaining transactions into the 'other'
        category and returns the total from applying Rule 7

        * requires a mechant_code of 'other' to be present in transactions

        Args:
            transactions -- a dict of parsed transactions 
                          (same format as self._parsed_transactions)
        Returns:
            int -- amount earned from applying rule 7
        """
        for merchant, amount in transactions.items():
            if merchant != MerchantCode.OTHER.value:
                transactions[MerchantCode.OTHER.value] += amount
        
        # using int cast on floats in Python is the same as floor
        return int(transactions[MerchantCode.OTHER.value])