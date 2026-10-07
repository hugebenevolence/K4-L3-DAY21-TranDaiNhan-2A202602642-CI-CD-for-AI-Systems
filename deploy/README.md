# EC2 deployment for the lab

The deployed stack is `aitc-day21-income-api` in `us-east-1`. Its CloudFormation
template is [`ec2-lab.yml`](ec2-lab.yml). It creates a small Ubuntu 24.04 EC2
instance, a security group for SSH and TCP 8080, and an instance role limited to
reading this lab's S3 model and bootstrap files. The separate stopped `Thanks-app`
instance is unrelated to this lab.

Current public IP: `44.211.49.198`. EC2 assigns a new public IP after a stop/start;
if that happens, update the GitHub `SERVER_HOST` secret before rerunning CI.

The boot script installs the API environment, copies `bootstrap/serve.py` and
`bootstrap/income-api.service` from S3, and starts `income-api`. The Release job
publishes the newly approved model to `artifacts/current/`, copies `src/serve.py`
over SSH, restarts the service, and checks `/healthz`.

Required repository secrets: `AWS_ACCESS_KEY_ID`, `AWS_SECRET_ACCESS_KEY`,
`ARTIFACT_BUCKET`, `SERVER_HOST`, `SERVER_USER`, and `SERVER_SSH_KEY`. Secret values
must never be committed. The S3 writer key is used by GitHub Actions; the VM reads
S3 using its instance role.

To check the deployed VM:

```bash
curl http://44.211.49.198:8080/healthz
curl -X POST http://44.211.49.198:8080/score \
  -H 'Content-Type: application/json' \
  -d '{"features":[39,2,13,2,9,0,1,2174,0,40]}'
```

The VM, its public IPv4 address, and its 12 GiB gp3 disk can incur AWS charges
while it exists. After grading, delete the `aitc-day21-income-api` CloudFormation
stack and the imported `income-lab-deploy` EC2 key pair. Deleting the stack removes
the lab VM, disk, role, and security group. Keep the DVC/model S3 bucket until the
submission has been checked.
