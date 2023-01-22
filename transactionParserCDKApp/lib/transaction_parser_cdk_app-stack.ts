import * as cdk from 'aws-cdk-lib';
import * as lambda from 'aws-cdk-lib/aws-lambda';
import * as apigw from 'aws-cdk-lib/aws-apigateway';
import { Construct } from 'constructs';
// import * as sqs from 'aws-cdk-lib/aws-sqs';

export class TransactionParserCdkAppStack extends cdk.Stack {
  constructor(scope: Construct, id: string, props?: cdk.StackProps) {
    super(scope, id, props);

    // Define AWS Lambda resource
    const my_lambda = new lambda.Function(this, 'TransactionHandler', {
      runtime: lambda.Runtime.PYTHON_3_9,
      code: lambda.Code.fromAsset(__dirname + '/../lambda',),
      handler: 'rewardPointsCalculator.lambda_handler.handler'
    });

    // Defines API Gateway REST API resource backed by our "hello" func
    new apigw.LambdaRestApi(this, 'Endpoint', {
      handler: my_lambda
    });
  }
}
