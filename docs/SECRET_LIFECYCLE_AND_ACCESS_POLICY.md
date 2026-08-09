# Secret Lifecycle and Access Policy

## Ownership and handoff

| Period | Responsible party | Handoff condition |
| --- | --- | --- |
| Current MVP preparation | Developer | Maintain the secret inventory by name only, select the MVP platform immediately before deployment, and approve access changes. |
| Long-term operation | DevOps/infrastructure or security owner | Transfer only after the recipient accepts the inventory, platform access model, rotation runbook, audit location, incident procedure, and current access list. |

No named DevOps, infrastructure, or security owner is present in repository evidence today; the receiving owner identity is **UNKNOWN**.

## Lifecycle rules

1. Create a value only in the approved local, CI, platform, or long-term secret facility for its environment.
2. Grant least-privilege access and avoid sharing values through source control or informal channels.
3. Rotate on scheduled policy set by the future platform/security owner, on role change, after suspected exposure, and before an owner handoff when risk warrants it.
4. Remove access when a person, workload, environment, or integration no longer needs it.
5. Retire values only after dependent workloads use a replacement and the rollback period has ended.

## Suspected exposure response

1. Stop further disclosure: do not paste the value into a ticket, PR, chat, or commit.
2. Notify the current responsible developer, then the designated security or platform owner when assigned.
3. Revoke or rotate the affected value in its actual storage facility.
4. Identify affected workloads and replace the value through the approved delivery path.
5. Review access/audit records, document the incident without the value, and add preventive controls in a separate approved change.

## CI rule

No CI files are currently evidenced. Therefore GitHub Secrets must not be used merely in anticipation of CI. A future CI implementation must define the job, required secret names, least-privilege repository/environment scope, and responsible maintainer before GitHub Secrets are introduced.

## Unknowns requiring a future decision

- Selected MVP platform and its exact role model.
- Current production injection path, service identities, and audit trail.
- Long-term AWS versus GCP secret-manager selection.
- Named receiving DevOps/infrastructure or security owner.
- Scheduled rotation interval and production incident contact path.
