#!/usr/bin/env node

import * as cdk from '@aws-cdk/core';
import invariant from 'ts-invariant';
import { SagemakerStack } from './sagemaker';
import { context } from '../../cdk.json';

type Context = typeof context;

const app = new cdk.App({});

// Set the default environment with an environment variable.
// 
// Example 1:
// $ export CDK_DEFAULT_ENV_NAME=user-jdoe
// $ yarn cdk bootstrap
// $ yarn cdk synthesize --json
// $ yarn cdk deploy
// 
// Example 2:
// $ CDK_DEFAULT_ENV_NAME=user-jdoe yarn cdk bootstrap
// $ CDK_DEFAULT_ENV_NAME=user-jdoe yarn cdk synthesize --json
// $ CDK_DEFAULT_ENV_NAME=user-jdoe yarn cdk deploy
const defaultEnvironmentName = process.env.CDK_DEFAULT_ENV_NAME ?? '';
const defaultEnvironment = context.environments[defaultEnvironmentName as keyof Context['environments']];

if (defaultEnvironmentName !== '') {
  invariant(defaultEnvironment != null, `“process.env.CDK_DEFAULT_ENV_NAME=${defaultEnvironmentName}” not found in cdk.json`);
}

// Set the environment with a context argument.
//
// Example:
// $ yarn cdk bootstrap --context env-name=jdoe
// $ yarn cdk synthesize --json --context env-name=jdoe
// $ yarn cdk deploy --context env-name=jdoe
const contextEnvironmentName = app.node.tryGetContext('env-name') ?? '';
const contextEnvironment = context.environments[contextEnvironmentName as keyof Context['environments']];

if (contextEnvironmentName !== '') {
  invariant(contextEnvironment != null, `“--context env-name=${contextEnvironmentName}” not found in cdk.json`);
}

const env = contextEnvironment ?? defaultEnvironment;
invariant(env != null, '“process.env.CDK_DEFAULT_ENV” or “--context env-name=<ENV>” is required');

new SagemakerStack(app, 'hackTheMachineUnmannedTrack3', {
  description: 'HACKtheMACHINE: Unmanned — Track 3',
  env,
});
