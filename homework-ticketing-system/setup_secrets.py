"""
One-time setup script: creates the Databricks secret scope and stores the
Lakebase URL. Run this locally (with the Databricks CLI configured) or from
a notebook - never commit the resulting secret value anywhere.

If you already ran this for Day 1/2/3 against the same workspace and secret
scope ("database" / "lakebase-url"), you can skip this and reuse that secret.

Usage:
    python setup_secrets.py
"""
from databricks.sdk import WorkspaceClient
from databricks.sdk.service import workspace
import getpass

w = WorkspaceClient()

w.secrets.create_scope(scope="database")
w.secrets.put_secret(
    scope="database",
    key="lakebase-url",
    string_value=getpass.getpass("Paste your Lakebase URL: ")
)

w.secrets.put_acl(
    scope="database",
    principal="users",
    permission=workspace.AclPermission.READ,
)
