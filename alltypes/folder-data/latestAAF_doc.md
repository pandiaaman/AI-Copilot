# Documentation Title: Get Latest AAF

#### Summary:
The Interplay Web Services method GetLatest returns the latest version of the AAF of an asset.

###### Parameter:
- The MOB ID of the asset.

###### Steps:
1. Use the cached CTMS Registry information or fetch it as shown in Using the CTMS API.
2. Find the link [aa:asset-by-id](https://developer.avid.com/ctms/api/aa/linkrels/asset-by-id.html) for the  Avid Production Management. The "href" is an   URI template.
    1. Set the URI template variable "id" to the ID of the asset and expand the URI template.
    2. Make an HTTP GET request to get the [aa:asset](https://developer.avid.com/ctms/api/aa/linkrels/asset.html) resource for the asset
3. Make an HTTP GET request to the pa:export-asset-command link to start a long-running command that exports the AAF. The response is a command:command resource representing the command. Example response (abbreviated):

```
{
  "version": "1.0",
  "command": {
    "type": "aa:export-asset-command",
    "lifecycle": "pending"
  },
  "_links": {
    "self": {
      "href": "https://..."
    }
  }
}
```

4. Poll the command status (with a small delay of, for example, 200 milliseconds between calls) by making an HTTP GET call to the "self" link until "lifecycle" in "command" is either "finished" or "error".
5. The result depends on the final value of the "lifecycle" property:
    1. “finished”: The export process was completed successfully. In this case, the response contains a pa:download-file link:

    ```
    "version": "1.0",
    "command": {
        "type": "aa:export-asset-command",
        "progress": 100,
        "lifecycle": "finished"
    },
    "_links": {
        "self": {
            "href": "https://..."
        },
        "pa:download-file": {
            "href": "http://..."
        }
    }
    ```
    2. “error”: The call failed. The response contains a property "error" within the "command" property with error details. See command:command for details.

6. If the command was successful, make an HTTP GET call on the pa:download-file link to download the AAF.

    The aa:export-asset-command and pa:download-file links will be part of the release version of  Avid Production Management and will be documented on developer.avid.com at that point in time.

#### How to use this collection:
This collection involves the process of following the above steps, as provided in the summary, in your postman application.
Open your postman, import the collection "Latest AAF/CTMS Get Latest AAF.postman_collection.json", and follow the steps as given below:

###### Postman API Calls
(Hit Send on the "ROPC Login" API call to login in the system. View the project-level ReadMe to understand how it works.)

> **GET** 1_CTMS Registry information: avid.ctms.registry
- This GET call hits the service roots URL for CTMS registry, fetching the resources, systems and the links associated to the system.
- In the **Scripts** section: We check if the  Avid Production Management is avaialable with the registry. If yes, we fetch "[aa:asset-by-id](https://developer.avid.com/ctms/api/aa/linkrels/asset-by-id.html)" link present inside the "resources", and store the variable globally as selected_system_aaAssetByIdHref.

    <mark>🔶 At this step, you need to insert the appropriate **asset ID** in the environment variable named: assetMobId</mark>

> **GET** 2_aa asset by id
- Hitting the above fetched selected_system_aaAssetByIdHref, to get the asset by id.
- In the **Scripts** section: From the response, we fetch the "aa:export-asset-command", which is used to get the export link for the given asset, and store it globally as selected_system_aaExportAssetCommandHref.

> **POST** 3 export AAFs
- Hitting the above selected_system_aaExportAssetCommandHref URL, to export the latest AAF file.
- The response starts a long running command that exports the file, with lifecyle initially as pending, and once completed, turns to finished.
- In the **Scripts** section: We fetch the "self" link from "_links", that point to the long running command and we can poll the command status using this link.

> **GET** 4 poll command status (pending/finished)
- Here we poll the status of the long running command that shows if the thumbnail has been set for the asset or not.


#### Precautions/Recommendations:
- Please **select and put** the right asset/masterclip IDs in the environment required for this example.