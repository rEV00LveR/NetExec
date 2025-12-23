from csv import reader
from nxc.helpers.misc import CATEGORY


class NXCModule:
    name = "wmware_workspace_discover"
    description = "Search for vmware workspace private connection files"
    supported_protocols = ["smb"]
    category = CATEGORY.ENUMERATION

    def __init__(self):
        pass
    def options(self, context, module_options):
        pass
    def on_admin_login(self, context, connection):
        search_keepass_files_payload = f"Get-ChildItem -Path 'C:\\Users\\*\\AppData\\Roaming\\VMware\\' -Recurse -Force -Filter 'preferences-private.ini' -ErrorAction SilentlyContinue | Select-Object FullName -ExpandProperty FullName"
        search_keepass_files_cmd = f'powershell.exe "{search_keepass_files_payload}"'
        search_keepass_files_output = connection.execute(search_keepass_files_cmd, True).split("\r\n")
        found = False
        for file in search_keepass_files_output:
            if ".ini" in file:
                found = True
                context.log.highlight(f"Found {file}")
        if not found:
            context.log.display("No wmware workspace-related file were found")
