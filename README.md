# CapitalOne_Assesment
My implementation of the Credit Card Reward Points Calculator Technical Assesment for Capital One

## File Structure
I wrote a class that implements methods to find the max reward points for the month and max reward points per transaction. This class is located in `IliaRomanov.py` and the methods are `maximum_reward_for_month` and `maximum_reward_per_transaction` respectively.

The `transactionParserCDKApp` directory contains the AWS CDK code I used to deploy an AWS Lambda + API Gateway based API to utilize the aforementioned class through the web, using HTTP POST requests.

