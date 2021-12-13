# HACKtheMACHINE: Unmanned Track 3

See the mission description at [HACKtheMACHINE: Unmanned Track 3](https://www.hackthemachine.ai/track3).

# Requirements

It's recommended to use VSCode. A dev environment is already configured to run in VSCode terminal.

Add a `.env` file to the project with your AWS credentials:

```env
AWS_ACCESS_KEY_ID=…
AWS_SECRET_ACCESS_KEY=…
CDK_DEFAULT_ENV_NAME=user-…
```

If you prefer another editor then checkout `.devcontainer/Dockerfile` for instructions on setting up a dev environment.

# Installation

Install Node.js dependencies:

```sh
yarn install
```

Install Python dependencies:

```sh
poetry install
poetry run python model/ray/patch.py
```

## Login to AWS ECR

Run the following command with your {ACCOUNT_ID}:

`aws ecr get-login-password --region us-east-1 | docker login --username AWS --password-stdin 763104351884.dkr.ecr.us-east-1.amazonaws.com`
`aws ecr get-login-password --region us-east-1 | docker login --username AWS --password-stdin {ACCOUNT_ID}.dkr.ecr.us-east-1.amazonaws.com`

# CDK (infrastructure)

The `cdk.json` file tells the CDK Toolkit how to execute your app.

If this is the first time a CDK project has been deployed to this particular account, run:

```
yarn cdk bootstrap
```

At this point you can now synthesize the CloudFormation template for this code.

```
yarn cdk synth
```

To add additional dependencies, for example other CDK libraries, just add
them to your `package.json` file and rerun the `yarn install` command.

## Useful commands

- `yarn cdk ls`                                         list all stacks in the app
- `yarn cdk synth`                                      emits the synthesized CloudFormation template
- `yarn cdk deploy --outputs-file cdk.outputs.json`     deploy this stack to your default AWS account/region
- `yarn cdk diff`                                       compare deployed stack with current state
- `yarn cdk docs`                                       open CDK documentation
- `yarn cdk destroy`                                    destroy stack
- `yarn sagemaker:algorithm:create`                     create Sagemaker training algorithm
- `yarn sagemaker:algorithm:describe`                   describe Sagemaker training algorithm

# Model

Add a `.wandb_api_key` to the root of the project.
Register for an API key at [Weights & Biases](https://wandb.ai/site).

### Commands

Commands are stored in the scripts section of `./package.json`:

- `poetry run python model/server/Forge.py generate` Generate model environments
- `poetry run python model/server/Forge.py train --RENDER=True` Train model
- `./model/client/run.sh` Visualize model training

### Getting started

Training for the original Neural MMO competition config:

```sh
poetry run python model/server/Forge.py generate --config=CompetitionRound1 --TERRAIN_RENDER=True
poetry run python model/server/Forge.py train --config=CompetitionRound1 --RENDER=True
```

Training for HACKtheMACHINE:

```sh
poetry run python model/server/Forge.py train --config=EastPacificOcean --RENDER=True
```

Running the UI client:

```sh
./model/client/run.sh
```

## Website

The website’s source code and README is located in the `./site` directory.
It's build is output to the `./docs` directory and hosted using GitHub Pages.

## Contributors

<a href="https://www.compositeenergytechnologies.com/">
  <img src="" title="Composite Energy Technologies" width="80" height="80">
</a>

<a href="https://www.current-lab.com">
  <img src="https://i.imgur.com/shj7hNd.png" title="Current Lab" width="80" height="80">
</a>

<a href="https://github.com/spear-ai">
  <img src="https://avatars.githubusercontent.com/u/89326455" title="Spear AI" width="80" height="80">
</a>

<a href="https://github.com/psirenny">
  <img src="https://avatars.githubusercontent.com/u/463178" title="Dennis Torres" width="80" height="80">
</a>

<a href="https://github.com/captainjackcity">
  <img src="https://avatars.githubusercontent.com/u/32316343" title="Jackson Koehler" width="80" height="80">
</a>

<a href="https://github.com/JaimCoddington">
  <img src="https://avatars.githubusercontent.com/u/94637237" title="Jaim Coddington" width="80" height="80">
</a>

<a href="https://github.com/jobeid1">
  <img src="https://avatars.githubusercontent.com/u/80070004" title="Joseph Obeid" width="80" height="80">
</a>

<a href="https://github.com/kevinrosa">
  <img src="https://avatars.githubusercontent.com/u/13137098" title="Kevin Rosa" width="80" height="80">
</a>

<a href="https://github.com/mike-spear">
  <img src="https://avatars.githubusercontent.com/u/89326447" title="Michael Hunter" width="80" height="80">
</a>

## Special thanks to

<a href="https://github.com/aws">
  <img src="https://avatars.githubusercontent.com/u/2232217" title="Michael Hunter" width="80" height="80">
</a>
