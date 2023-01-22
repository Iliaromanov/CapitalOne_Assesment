import json

from .rewardPointsCalculator import RewardPointsCalculator


def handler(event, context):
    print("request: ", json.dumps(event))
    transactions = json.loads(event["body"])["transactions"]

    reward_pts_calc = RewardPointsCalculator(transactions)

    max_per_transaction = reward_pts_calc.maximum_reward_per_transaction()
    max_for_month, rules_used = reward_pts_calc.maximum_reward_for_month()

    return {
        'statusCode': 200,
        'headers': {
            'Context-Type': 'application/json'
        },
        'body': json.dumps({
            "max_reward_per_transaction": max_per_transaction,
            "rewards_for_month": {
                "max_reward": max_for_month,
                "rules_used": rules_used
            }
        })
    }