from enum import Enum
from math import floor
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


class TransactionParser:
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
        parses transactions by combining 
        """
        # init all merchants to 0
        transactions = {
            merchant_code: 0.0 for merchant_code in self._defined_merchants
        }

        print("trans: ", self._raw_transactions)
        print("raw trans: ", list(self._raw_transactions.values()))

        for transaction in list(self._raw_transactions.values()):
            merchant = transaction["merchant_code"]
            if merchant not in self._defined_merchants:
                merchant = MerchantCode.OTHER.value
            # immediately conver to dollar
            amount = transaction["amount_cents"] / 100
            
            self._total_transaction_amount += amount
            transactions[merchant] += amount

        print("paresed transactions: ", transactions)

        self._parsed_transactions = transactions


    def maximum_reward_per_transaction(self) -> Dict[str, int]:
        """
        """

    def maximum_reward_for_month_backtrack(self) -> int:
        """

        * This current algo is only applicable to the DEFAULT_RULES
           above (given in assesment), but this method can be updated
           to return max reward points for different sets of rules
        """
        # I will be taking the backtracking approach for this algo: 
        # attempt to apply every rule and check which gives the max 
        max_reward = 0
        max_rules_used = []

        def backtrack(transactions: Dict[str, float], rules_used: List[str], total_amount: int, reward: int):
            nonlocal max_reward
            nonlocal max_rules_used

            print("============================================= Starting new Backtrack")
            print("transactions: ", transactions)
            print("rules: ", rules_used)
            print("total amount: ", total_amount)
            print("reward: ", reward)

            # special case: check if any rules other than Rule 7 can be applied
            #  if not, then put everything into 'other' and calculate left over
            #  reward points using Rule 7
            if self._must_merge_to_other(transactions):
                print("MUST MERGE TO OTHER")
                for merchant, amount in transactions.items():
                    if merchant != MerchantCode.OTHER.value:
                        transactions[MerchantCode.OTHER.value] += amount
                amount = floor(transactions[MerchantCode.OTHER.value])
                total_amount -= amount
                reward += amount
                rules_used.append(7) # will only append 7 once to keep it clean

            if total_amount < 1:
                print("FOUND AMOUNT < 1")
                print("reward: ", reward)
                if max_reward < reward:
                    max_reward = reward
                    max_rules_used = rules_used
                return

            for rule_num, rule in enumerate(self._rules):
                rule_num += 1 # rules are 0 indexed
                print("trying rule: ", rule_num)
                reqs = rule["Reqs"]
                transactions_copy = transactions.copy()
                new_total = total_amount
                new_reward = reward + rule["Points"]
                new_rules_used = rules_used.copy() + [rule_num]
                if self._rule_applicable(transactions_copy, reqs):
                    print("new_reward: ", new_reward)
                    print("rule: ", rule_num, " applicable")
                    new_total -= self._apply_rule(transactions_copy, reqs)
                    backtrack(transactions_copy, new_rules_used, new_total, new_reward)

        backtrack(self._parsed_transactions, [], self._total_transaction_amount, 0)

        print("max_reward:", max_reward)
        print("rules_used:", max_rules_used)

        return max_reward


    def _rule_applicable(self, transactions: Dict[str, float], reqs: List[Tuple[str, int]]) -> bool:
        """
        checks if rule is applicable
        """
        for merchant, amount in reqs:
            if transactions[merchant] < amount:
                return False
        return True
    
    def _apply_rule(self, transactions: Dict[str, float], reqs: List[Tuple[str, int]]) -> int:
        """
        modifies transaction in place to decrement ammounts
        returns total decremented
        """
        total = 0
        for merchant, amount in reqs:
            transactions[merchant] -= amount
            total += amount

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
        return transactions[MerchantCode.SPORTCHECK.value] < 20



sample = {
"T01": {"date": "2021-05-01", "merchant_code" : "sportcheck", "amount_cents": 21000}, "T02": {"date": "2021-05-02", "merchant_code" : "sportcheck", "amount_cents": 8700}, "T03": {"date": "2021-05-03", "merchant_code" : "tim_hortons", "amount_cents": 323}, "T04": {"date": "2021-05-04", "merchant_code" : "tim_hortons", "amount_cents": 1267}, "T05": {"date": "2021-05-05", "merchant_code" : "tim_hortons", "amount_cents": 2116}, "T06": {"date": "2021-05-06", "merchant_code" : "tim_hortons", "amount_cents": 2211}, "T07": {"date": "2021-05-07", "merchant_code" : "subway", "amount_cents": 1853}, "T08": {"date": "2021-05-08", "merchant_code" : "subway", "amount_cents": 2153}, "T09": {"date": "2021-05-09", "merchant_code" : "sportcheck", "amount_cents": 7326}, "T10": {"date": "2021-05-10", "merchant_code" : "tim_hortons", "amount_cents": 1321}
}

tricky = {
    "T01": {"date": "2021-05-01", "merchant_code" : "sportcheck", "amount_cents": 7500},
    "T02": {"date": "2021-05-10", "merchant_code" : "tim_hortons", "amount_cents": 2000},
    "T03": {"date": "2021-05-10", "merchant_code" : "subway", "amount_cents": 2000},
} # 1x Rule 3 gives less than 2x Rule 4

t = TransactionParser(sample)

# t.parse_transactions()


"""

TRY tricky WITHOUT TIMS CUS IT SEEMED LIKE IT BROKE

"""
t.maximum_reward_for_month()

# print("rule applicable: ", t._rule_applicable(DEFAULT_RULES[0]["Reqs"]))
