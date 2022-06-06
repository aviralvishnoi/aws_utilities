from msilib.schema import Directory
from urllib import response
import boto3
import os

directory_id = os.environ["directory_id"]
workspace_client = boto3.client("workspaces")

def determine_dfpoc_id():
    user_name = ""
    return user_name


def get_workspace_id(user_name):
    response = workspace_client.describe_worspaces(
        DirectoryId = directory_id,
        UserName = user_name
    )
    workspaces = response.get("Workspaces", None)
    if workspaces:
        for workspace in workspaces:
            workspace_id = workspace.get("WorkspaceId", None)
    return workspace_id


def reboot_workspace(workspace_id):
    response = workspace_client.reboot_workspaces(
        RebootWorkspaceRequests=[
            {
                "WorkspaceId": workspace_id
            }
        ]
    )
    error_response = response.get("FailedRequests", None)
    if error_response:
        for item in error_response:
            error_message = "Not able to reboot workspace {} due to error code {} with error message".format(str(item["WorkspaceId"]), str(item["ErrorCode"]), str(item["ErrorMessage"]))
        return
    else:
        return True

    
def lambda_handler(event, context):
    user_name = determine_dfpoc_id()
    workspace_id = get_workspace_id(user_name)
    response = reboot_workspace(workspace_id)
