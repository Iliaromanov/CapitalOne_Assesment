from enum import Enum
from typing import Any, Dict, List, Set


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
        "Points": int, "Reqs": [
            {MerchantCode: int, ...}, ...
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
            {MerchantCode.SPORTCHECK.value: 75},
            {MerchantCode.TIM_HORTONS.value: 25},
            {MerchantCode.SUBWAY.value: 25}
        ]
    },
    # Rule 2
    {
        "Points": 300,
        "Reqs": [
            {MerchantCode.SPORTCHECK.value: 75},
            {MerchantCode.TIM_HORTONS.value: 25}
        ]
    },
    # Rule 3
    {
        "Points": 200,
        "Reqs": [
            {MerchantCode.SPORTCHECK.value: 75}
        ]
    },
    # Rule 4
    {
        "Points": 150,
        "Reqs": [
            {MerchantCode.SPORTCHECK.value: 25},
            {MerchantCode.TIM_HORTONS.value: 10},
            {MerchantCode.SUBWAY.value: 10}
        ]
    },
    # Rule 5
    {
        "Points": 75,
        "Reqs": [
            {MerchantCode.SPORTCHECK.value: 25},
            {MerchantCode.TIM_HORTONS.value: 10},
        ]
    },
    # Rule 6
    {
        "Points": 75,
        "Reqs": [
            {MerchantCode.SPORTCHECK.value: 20},
            {MerchantCode.TIM_HORTONS.value: 25},
            {MerchantCode.SUBWAY.value: 25}
        ]
    },
    # Rule 7
    {
        "Points": 1,
        "Reqs": [
            # Here OTHER encompasses the other defined MerchantCodes as 
            #  well as any non-defined merchant codes
            {MerchantCode.OTHER.value: 1}
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

    def parse_transactions(self) -> None:
        """
        parses transactions by combining 
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

            transactions[merchant] += amount

        self._parsed_transactions = transactions


    def maximize_reward_per_transaction(self) -> Dict[str, int]:
        """
        """




sample = {
"T01": {"date": "2021-05-01", "merchant_code" : "sportcheck", "amount_cents": 21000}, "T02": {"date": "2021-05-02", "merchant_code" : "sportcheck", "amount_cents": 8700}, "T03": {"date": "2021-05-03", "merchant_code" : "tim_hortons", "amount_cents": 323}, "T04": {"date": "2021-05-04", "merchant_code" : "tim_hortons", "amount_cents": 1267}, "T05": {"date": "2021-05-05", "merchant_code" : "tim_hortons", "amount_cents": 2116}, "T06": {"date": "2021-05-06", "merchant_code" : "tim_hortons", "amount_cents": 2211}, "T07": {"date": "2021-05-07", "merchant_code" : "subway", "amount_cents": 1853}, "T08": {"date": "2021-05-08", "merchant_code" : "subway", "amount_cents": 2153}, "T09": {"date": "2021-05-09", "merchant_code" : "sportcheck", "amount_cents": 7326}, "T10": {"date": "2021-05-10", "merchant_code" : "tim_hortons", "amount_cents": 1321}
}

t = TransactionParser(sample)

t.parse_transactions()
