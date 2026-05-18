---
name: Infrastructure as Code
description: CDK/CloudFormation design principles for immutable infrastructure, environment parity, least privilege, tagging strategy, and cost optimization. Infrastructure is code—it deserves the same rigor as application code.
leadership_principles:
  - Ownership
  - Insist on the Highest Standards
  - Frugality
  - Dive Deep
  - Bias for Action
---

# Infrastructure as Code

## Overview

Infrastructure as Code (IaC) means every piece of infrastructure—compute, storage, networking, permissions, monitoring—is defined in version-controlled code that can be reviewed, tested, and deployed through the same pipeline as application code. There is no "clicking in the console." There are no snowflake environments. The code IS the infrastructure, and the infrastructure IS the code.

Immutable infrastructure means you never patch in place. You replace. A server is never SSH'd into and modified; it is destroyed and rebuilt from the code. This eliminates configuration drift, makes deployments predictable, and ensures every environment is reproducible.

## When to Use

- Always. All infrastructure must be defined in code. There are no exceptions.
- When creating a new service or microservice
- When modifying any infrastructure component (networking, IAM, storage, compute)
- When setting up a new environment (dev, staging, production)
- When responding to an incident that requires infrastructure changes
- When optimizing costs (changes must be in code so they're reproducible and reviewable)

## Amazon Context

At Amazon, teams own their infrastructure end-to-end. There is no separate "ops team" that provisions resources. The team that builds the service provisions, deploys, monitors, and operates the infrastructure. CDK (Cloud Development Kit) and CloudFormation are the primary tools, with CDK preferred for new projects because it provides type safety, composition, and testing capabilities that raw CloudFormation templates lack.

Infrastructure changes go through the same code review and deployment pipeline as application code. A CDK change that modifies IAM permissions gets the same scrutiny as a code change that handles authentication. In many ways, it deserves MORE scrutiny—a bad IAM policy can expose the entire account.

## The Process

### 1. Immutable Infrastructure

#### Principles

- **Never modify running infrastructure.** To change a server's configuration, create a new server with the new configuration and destroy the old one.
- **No SSH in production.** If you need to SSH in, your automation is incomplete. Fix the automation.
- **Identical artifacts across environments.** The same AMI/container image deployed to dev is deployed to production. Only configuration (env vars, secrets references) differs.
- **Rebuild from scratch regularly.** If you can't destroy and recreate your entire environment from code in under an hour, your IaC is incomplete.

#### Implementation

```typescript
// CDK Example: Immutable deployment via Auto Scaling Group
const asg = new autoscaling.AutoScalingGroup(this, 'ServiceASG', {
  instanceType: ec2.InstanceType.of(ec2.InstanceClass.M5, ec2.InstanceSize.LARGE),
  machineImage: ec2.MachineImage.lookup({
    name: `service-ami-${props.buildId}`, // New AMI per build
  }),
  updatePolicy: autoscaling.UpdatePolicy.rollingUpdate({
    maxBatchSize: 1,
    minInstancesInService: 2,
    pauseTime: Duration.minutes(5),
  }),
});
```

### 2. Environment Parity

#### The Rule

Production, staging, and development environments must be structurally identical. They differ only in:
- Scale (instance count, storage size)
- Configuration values (endpoints, account IDs)
- Data (production has real data; lower environments have synthetic data)

They must NOT differ in:
- Architecture (same services, same topology)
- Security posture (same IAM structure, same encryption)
- Networking model (same VPC design, same security groups)
- Monitoring (same metrics, same alarms—different thresholds are acceptable)

#### Implementation

```typescript
// CDK Example: Environment parity through parameterization
interface EnvironmentConfig {
  readonly envName: string;
  readonly instanceCount: number;
  readonly instanceType: ec2.InstanceType;
  readonly alarmThreshold: number;
  readonly retentionDays: number;
}

const environments: Record<string, EnvironmentConfig> = {
  dev: {
    envName: 'dev',
    instanceCount: 1,
    instanceType: ec2.InstanceType.of(ec2.InstanceClass.T3, ec2.InstanceSize.MEDIUM),
    alarmThreshold: 5000,
    retentionDays: 7,
  },
  staging: {
    envName: 'staging',
    instanceCount: 2,
    instanceType: ec2.InstanceType.of(ec2.InstanceClass.M5, ec2.InstanceSize.LARGE),
    alarmThreshold: 2000,
    retentionDays: 30,
  },
  production: {
    envName: 'production',
    instanceCount: 6,
    instanceType: ec2.InstanceType.of(ec2.InstanceClass.M5, ec2.InstanceSize.XLARGE),
    alarmThreshold: 1000,
    retentionDays: 365,
  },
};

// Same stack, different config — structural parity guaranteed
new ServiceStack(app, `Service-${config.envName}`, { config });
```

### 3. Least Privilege

#### IAM Design Principles

1. **Start with zero permissions.** Add only what's needed, one permission at a time.
2. **Scope to specific resources.** Never use `Resource: "*"` unless there is no alternative.
3. **Use conditions.** Restrict by source IP, time, MFA, tags, or organization.
4. **Prefer managed policies for AWS services.** Custom policies for application-specific access.
5. **Separate read and write roles.** A service that reads from DynamoDB and writes to S3 should have separate role assumptions if possible.
6. **Time-bound elevated access.** Admin access should be temporary (STS assume-role with session duration).

#### Common Violations and Fixes

```typescript
// ❌ WRONG: Overly broad permissions
const badPolicy = new iam.PolicyStatement({
  actions: ['dynamodb:*'],
  resources: ['*'],
});

// ✅ RIGHT: Least privilege
const goodPolicy = new iam.PolicyStatement({
  actions: [
    'dynamodb:GetItem',
    'dynamodb:PutItem',
    'dynamodb:Query',
  ],
  resources: [
    table.tableArn,
    `${table.tableArn}/index/*`,
  ],
  conditions: {
    'ForAllValues:StringEquals': {
      'dynamodb:LeadingKeys': ['${aws:PrincipalTag/TenantId}'],
    },
  },
});
```

#### IAM Review Checklist

- [ ] No `Action: "*"` (wildcard actions)
- [ ] No `Resource: "*"` without documented justification
- [ ] No inline policies on IAM users (use roles)
- [ ] Cross-account access uses external ID condition
- [ ] Service roles have trust policy scoped to specific service principal
- [ ] Admin access requires MFA and has session time limit
- [ ] Permissions boundaries are applied to delegated admin roles

### 4. Tagging Strategy

#### Mandatory Tags

Every resource must have these tags (enforced by Service Control Policy):

| Tag Key | Description | Example Values |
|---------|-------------|---------------|
| `service` | Service name (matches repo name) | `payment-processing` |
| `environment` | Deployment environment | `dev`, `staging`, `production` |
| `team` | Owning team name | `payments-core` |
| `cost-center` | Finance cost allocation code | `CC-12345` |
| `data-classification` | Data sensitivity level | `public`, `internal`, `confidential`, `restricted` |
| `managed-by` | IaC tool managing this resource | `cdk`, `cloudformation`, `terraform` |

#### Enforcement

```typescript
// CDK Example: Enforce tags at the stack level
Tags.of(app).add('service', props.serviceName);
Tags.of(app).add('environment', props.environment);
Tags.of(app).add('team', props.teamName);
Tags.of(app).add('cost-center', props.costCenter);
Tags.of(app).add('managed-by', 'cdk');

// CDK Nag: Fail deployment if tags are missing
Aspects.of(app).add(new TagEnforcementAspect(REQUIRED_TAGS));
```

#### Tag-Based Policies

- **Cost allocation**: All cost reports filter by `service` and `team` tags
- **Access control**: IAM policies use `aws:ResourceTag` conditions
- **Automation**: Auto-shutdown of dev resources uses `environment: dev` tag
- **Compliance**: Audit queries use `data-classification` tag to verify encryption

### 5. Cost Optimization

#### Design-Time Cost Decisions

| Decision | Cost Impact | Guideline |
|----------|-------------|-----------|
| Instance type | 40-60% of compute cost | Right-size based on actual metrics, not guesses. Start small, scale up. |
| Storage class | 20-50% of storage cost | Use lifecycle policies: hot → warm → cold → archive |
| Reserved vs. On-Demand | 30-60% savings | Reserve steady-state baseline; On-Demand for burst |
| Region selection | 10-30% variation | Use cheapest region that meets latency requirements |
| Data transfer | Often overlooked | Keep data in same AZ/region where possible; use VPC endpoints |

#### Cost Guardrails in Code

```typescript
// CDK Example: Cost guardrails
class CostGuardrailAspect implements IAspect {
  visit(node: IConstruct) {
    // Prevent expensive instance types in non-prod
    if (node instanceof ec2.CfnInstance) {
      if (props.environment !== 'production') {
        const instanceType = node.instanceType;
        if (EXPENSIVE_INSTANCE_TYPES.includes(instanceType)) {
          Annotations.of(node).addError(
            `Instance type ${instanceType} not allowed in ${props.environment}. Use t3/t4g family.`
          );
        }
      }
    }

    // Ensure DynamoDB tables use on-demand in dev, provisioned in prod
    if (node instanceof dynamodb.CfnTable) {
      if (props.environment === 'production' && !node.billingMode) {
        Annotations.of(node).addWarning(
          'Production DynamoDB tables should use PROVISIONED billing with auto-scaling for cost predictability.'
        );
      }
    }
  }
}
```

#### Cost Monitoring

- **Budget alarms**: Set per-service monthly budget with alerts at 50%, 80%, 100%
- **Anomaly detection**: AWS Cost Anomaly Detection enabled per-service tag
- **Weekly review**: Automated cost report per team, compared to previous week
- **Unused resource detection**: Automated scan for unattached EBS, idle EC2, empty S3 buckets

### 6. CDK Best Practices

#### Project Structure

```
infrastructure/
├── bin/
│   └── app.ts                    # Entry point, environment selection
├── lib/
│   ├── constructs/               # Reusable L3 constructs
│   │   ├── monitored-lambda.ts   # Lambda + alarms + dashboard
│   │   ├── secure-bucket.ts      # S3 + encryption + lifecycle
│   │   └── api-gateway.ts        # APIGW + WAF + logging
│   ├── stacks/
│   │   ├── networking-stack.ts   # VPC, subnets, security groups
│   │   ├── data-stack.ts         # DynamoDB, S3, ElastiCache
│   │   ├── compute-stack.ts      # Lambda, ECS, ASG
│   │   └── monitoring-stack.ts   # Dashboards, alarms, SNS
│   └── config/
│       ├── dev.ts
│       ├── staging.ts
│       └── production.ts
├── test/
│   ├── unit/                     # Snapshot + fine-grained tests
│   └── integration/              # Deployed stack verification
└── cdk.json
```

#### Testing Infrastructure Code

```typescript
// Snapshot test: Detect unintended changes
test('infrastructure matches snapshot', () => {
  const app = new App();
  const stack = new ServiceStack(app, 'TestStack', { config: testConfig });
  expect(Template.fromStack(stack)).toMatchSnapshot();
});

// Fine-grained assertion: Verify specific properties
test('DynamoDB table has encryption enabled', () => {
  const template = Template.fromStack(stack);
  template.hasResourceProperties('AWS::DynamoDB::Table', {
    SSESpecification: {
      SSEEnabled: true,
      SSEType: 'KMS',
    },
  });
});

// Security assertion: No public S3 buckets
test('no public S3 buckets', () => {
  const template = Template.fromStack(stack);
  template.hasResourceProperties('AWS::S3::Bucket', {
    PublicAccessBlockConfiguration: {
      BlockPublicAcls: true,
      BlockPublicPolicy: true,
      IgnorePublicAcls: true,
      RestrictPublicBuckets: true,
    },
  });
});
```

#### Construct Composition

- **L1 (Cfn)**: Raw CloudFormation. Use only when L2 doesn't exist.
- **L2**: AWS-opinionated defaults. Use as building blocks.
- **L3 (Custom)**: Your team's opinionated constructs. Encode your standards.

```typescript
// L3 Construct: Encodes team standards
export class MonitoredService extends Construct {
  constructor(scope: Construct, id: string, props: MonitoredServiceProps) {
    super(scope, id);

    // Creates: ECS service + ALB + auto-scaling + dashboard + alarms + SNS topic
    // All with team-standard configurations baked in
    // Individual overrides available but defaults are production-ready
  }
}
```

### 7. Drift Detection and Reconciliation

- **Automated drift detection**: Schedule CloudFormation drift detection weekly
- **Alert on drift**: Any detected drift triggers a ticket to the owning team
- **Resolution**: Drift must be resolved within 1 sprint (either update code to match reality, or re-deploy code to fix reality)
- **Prevention**: Restrict console access in production accounts. All changes through pipeline.

## Mechanisms Over Good Intentions

| Intention | Mechanism |
|-----------|-----------|
| "I'll define everything in code" | Service Control Policies deny resource creation without `managed-by` tag; console access is read-only in production |
| "I'll follow least privilege" | CDK Nag rules fail the build on overly broad IAM policies |
| "I'll tag everything" | SCP denies resource creation without mandatory tags |
| "I'll keep costs under control" | Budget alarms auto-notify; cost anomaly detection pages on-call |
| "I'll keep environments consistent" | Same CDK stack with different configs; structural drift detection alerts |

## Common Rationalizations

| What They Say | Why It's Wrong | What To Do Instead |
|---------------|---------------|-------------------|
| "I'll just make this change in the console quickly" | Console changes cause drift. Drift causes incidents. The next deployment will either fail or overwrite your change. | Make the change in code. Deploy through the pipeline. If it's truly urgent, make the console change AND immediately commit the IaC change. |
| "This is just a dev environment, it doesn't need the same rigor" | Dev environments that differ from production hide bugs until production. Every "works in dev, breaks in prod" incident traces to environment divergence. | Use the same stack with different scale parameters. Dev is smaller but architecturally identical. |
| "Least privilege is too hard to get right upfront" | Broad permissions today become the permissions you're stuck with forever. Tightening later breaks things. Starting broad is technical debt with security interest. | Start with zero permissions. Add each permission as you need it. Use IAM Access Analyzer to identify unused permissions. |
| "We'll add tags later" | Later never comes. Untagged resources are unowned resources. Unowned resources are never cleaned up, never optimized, and never secured. | Enforce tags at creation time via SCP. No tag, no resource. Period. |
| "Reserved instances are a commitment we're not ready for" | On-Demand pricing for stable workloads is paying a 40% premium for flexibility you're not using. | Use Savings Plans (more flexible than RIs). Commit to your minimum steady-state usage. Use On-Demand only for burst. |

## Red Flags

- Resources exist that aren't in any IaC template (shadow infrastructure)
- Production changes are made via console and "backfilled" into code later
- Dev and production use different architectures (dev uses single-AZ, prod uses multi-AZ)
- IAM policies use `*` for actions or resources without documented justification
- No drift detection running; team doesn't know if reality matches code
- Infrastructure tests don't exist or only test "it deploys successfully"
- No tagging strategy; cost allocation is impossible
- Cost reports are never reviewed; no budget alarms configured
- Secrets are hardcoded in IaC templates (even in parameter store references, review what's in plain text)
- Infrastructure changes don't go through code review
- Different team members use different IaC tools for the same service

## Verification

- [ ] All infrastructure is defined in version-controlled CDK/CloudFormation code
- [ ] No resources exist in production that aren't in IaC (verified by drift detection)
- [ ] Same stack/template deploys to all environments with configuration parameters
- [ ] IAM policies follow least privilege (verified by CDK Nag or equivalent)
- [ ] All resources have mandatory tags (enforced by SCP)
- [ ] Infrastructure code has tests (snapshot + fine-grained assertions)
- [ ] Infrastructure changes go through code review in the same pipeline as app code
- [ ] Cost budgets and anomaly detection are configured per-service
- [ ] Console access is read-only in production accounts
- [ ] Drift detection runs weekly with alerts on detected drift
- [ ] Secrets are never in plain text in IaC code (use Secrets Manager/Parameter Store references)
- [ ] Environments can be destroyed and recreated from code within defined time target

## Tenets

1. **If it's not in code, it doesn't exist.** Console changes are ephemeral. Code is truth. If the code doesn't describe it, it will be destroyed on next deployment.
2. **Immutable over mutable.** Replace, don't patch. Every deployment is a fresh creation from a known-good template. Drift is impossible when you replace instead of modify.
3. **Same architecture, different scale.** Environments differ in size, not shape. A bug that only manifests in production's architecture is a bug in your environment parity.
4. **Least privilege is non-negotiable.** Every wildcard permission is a blast radius multiplied. Start with nothing; add the minimum needed.
5. **Cost is a feature.** Infrastructure cost is as much a design consideration as latency or availability. Optimize it in code, measure it continuously, alert when it deviates.
