# AWS VM setup for this lab

The workflow deploys to an existing Ubuntu VM over SSH. The current AWS identity
can access S3 but cannot create or inspect EC2 instances, so this setup must be
run when an EC2-capable identity or an existing VM is available.

1. Give the VM an instance role with `s3:GetObject` for
   `arn:aws:s3:::aitc-day21-trandainhan-2a202602642/artifacts/current/*`.
   Allow SSH from the GitHub runner and TCP 8080 for the API in the security group.
2. On the VM, prepare the service environment:

   ```bash
   sudo apt update
   sudo apt install -y python3-venv
   python3 -m venv ~/income-api-venv
   ~/income-api-venv/bin/pip install fastapi==0.111.0 uvicorn==0.29.0 scikit-learn==1.4.2 pandas==2.2.2 joblib==1.4.2 'boto3>=1.34,<2'
   mkdir -p ~/src ~/models
   ```

3. Copy `src/serve.py` to `~/src/serve.py` and `deploy/income-api.service` to
   `/etc/systemd/system/income-api.service`. Replace `ubuntu` in the service file
   if the VM uses another user. Run `sudo systemctl daemon-reload` and
   `sudo systemctl enable --now income-api`.
4. Add six GitHub Actions repository secrets:

   | Secret | Value |
   |---|---|
   | `AWS_ACCESS_KEY_ID` | S3 writer access key for the CI runner |
   | `AWS_SECRET_ACCESS_KEY` | Matching secret key |
   | `ARTIFACT_BUCKET` | `aitc-day21-trandainhan-2a202602642` |
   | `SERVER_HOST` | VM public IP or DNS name |
   | `SERVER_USER` | VM SSH user, normally `ubuntu` |
   | `SERVER_SSH_KEY` | Private key whose public key is in VM `authorized_keys` |

The model is already available in S3. The workflow downloads DVC data during
Train, checks positive-class F1, then publishes and deploys only after the gate
passes. Test the VM with `GET /healthz` and `POST /score` on port 8080.
