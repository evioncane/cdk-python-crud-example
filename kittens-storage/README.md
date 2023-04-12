
# Welcome to your CDK Python project!

This is a project for kitten management.

## Steps to create the project
1. Run: `cdk init --language python` to create project.
2. Add `boto3` to `requirements.txt`.
3. Run `pip install -r requirements.txt` to install dependencies.
4. Create layer folder: `layer/python/`.
5. Add DynamoDB shared code python file.
6. Create CRUD handler functions in separate packages.
7. Configure Stack.


### Create CRUD handler functions
1. Write create kitten handler.
2. Write list all kittens handler.
3. Write get kitten handler.
4. Write delete kitten handler.

### Configure Stack
1. Create DynamoDB table
    * Create key
    * Create table
2. Create a lambda layer. For the layer specify:
    * id
    * code
    * compatible_runtimes
    * description
3. Create Lambda functions. For each Lambda function specify:
    * id
    * code
    * handler
    * environment
    * runtime
    * layers
4. Grant all Lambda permission to access DynamoDB
5. Create a REST API Gateway
6. Create a Lambda integration
7. Add resource and method
    * For each resource add HTTP methods

## Useful commands

 * `cdk ls`          list all stacks in the app
 * `cdk synth`       emits the synthesized CloudFormation template
 * `cdk deploy`      deploy this stack to your default AWS account/region
 * `cdk diff`        compare deployed stack with current state
 * `cdk docs`        open CDK documentation

Enjoy!
