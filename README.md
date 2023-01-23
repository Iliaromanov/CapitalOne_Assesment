# CapitalOne_Assesment
My implementation of the Credit Card Reward Points Calculator Technical Assesment for Capital One

## File Structure
I wrote a class - `RewardPointsCalculator` - that implements methods to find the max reward points for the month and max reward points per transaction. This class is located in `IliaRomanov.py` and the methods are `maximum_reward_for_month` and `maximum_reward_per_transaction` respectively.

The `transactionParserCDKApp` directory contains the AWS CDK (infrastructure as code tool) code I used to deploy an AWS Lambda + API Gateway based API to utilize the aforementioned class through the web, using HTTP POST requests (located in `transactionParserCDKApp/lib`), as well as my code for the lambda handler that imports and calls my `RewardPointsCalculator` class methods (located in `transactionParserCDKApp/lambda/rewardPointsCalculator/lambda_handler.py`).

(I have a copy of the code in `IliaRomanov.py` in  `transactionParserCDKApp/lambda/rewardPointsCalculator/rewardPointsCalculator.py` for the lambda handler to import; the `IliaRomanov.py` is just there to make it easier for you to review my code for the main logic of the assesment solution)

## API
I deployed an AWS Lambda + API Gateway based API to accept HTTP POST requests providing a dictionary of transactions for a month in the format specified by the assesment documentation and return a response containing the max reward points for the month and max reward points per transaction information.

URL: `https://ycyx8q4m03.execute-api.us-east-2.amazonaws.com/prod/`

methods: `POST`

Sample Request Body:
```javascript
{"transactions": 
  {
    "T01": {"date": "2021-05-01", "merchant_code" : "sportcheck", "amount_cents": 21000},
    "T02": {"date": "2021-05-02", "merchant_code" : "sportcheck", "amount_cents": 8700},
    "T03": {"date": "2021-05-03", "merchant_code" : "tim_hortons", "amount_cents": 323},
    "T04": {"date": "2021-05-04", "merchant_code" : "tim_hortons", "amount_cents": 1267},
    "T05": {"date": "2021-05-05", "merchant_code" : "tim_hortons", "amount_cents": 2116},
    "T06": {"date": "2021-05-06", "merchant_code" : "tim_hortons", "amount_cents": 2211},
    "T07": {"date": "2021-05-07", "merchant_code" : "subway", "amount_cents": 1853},
    "T08": {"date": "2021-05-08", "merchant_code" : "subway", "amount_cents": 2153},
    "T09": {"date": "2021-05-09", "merchant_code" : "sportcheck", "amount_cents": 7326},
    "T10": {"date": "2021-05-10", "merchant_code" : "tim_hortons", "amount_cents": 1321}
  }
}
```
Sample Response:

(the `max_reward_per_transaction` field provides the max reward points for transaction `i` at index `i - 1`; eg. the max reward points for T01 is 400 which is achieved through applying Rule 3 twice.)

```javascript
{
    "max_reward_per_transaction": [
        [
            400,
            {
                "rules_used": [3,3]
            }
        ],
        [
            200,
            {
                "rules_used": [3]
            }
        ],
        [
            3,
            {
                "rules_used": [7]
            }
        ],
        [
            12,
            {
                "rules_used": [7]
            }
        ],
        [
            21,
            {
                "rules_used": [7]
            }
        ],
        [
            22,
            {
                "rules_used": [7]
            }
        ],
        [
            18,
            {
                "rules_used": [7]
            }
        ],
        [
            21,
            {
                "rules_used": [7]
            }
        ],
        [
            225,
            {
                "rules_used": [6,6,6]
            }
        ],
        [
            13,
            {
                "rules_used": [7]
            }
        ]
    ],
    "rewards_for_month": {
        "max_reward": 1657,
        "rules_used": [1,2,4,6,6,6,6,6,6,6,6,6,7]
    }
}
```
