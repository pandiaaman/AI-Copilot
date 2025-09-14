# Documentation Title: Delete Assets (Bulk)

#### Summary:
The Interplay Web Services method DeleteAssets is used to delete assets, associated media, and/or empty folders. It accepts parameters that define what exactly to delete:

- DeleteMetadata: If true, the metadata of the asset is deleted from the folder.
- DeleteMedia: If true, the media files referenced by the asset are deleted.
- If DeleteMedia is true:
    - Resolutions: Defines the resolutions of the media files to delete. If not given, media files of all resolutions are deleted.
    - FileType: Defines the type of the media files to delete (AMA, NATIVE or ALL).
The method also allows to only simulate the deletion. In this case, the result is a list of the assets and media files that would be deleted.

## Deleting empty folders in CTMS
>> CTMS currently doesn't allow deleting empty folders in  Avid Production Management.

## Deleting assets in CTMS

###### Parameter:
- A list of asset references in folders. An asset reference consists of the path in the folder structure, followed by the MOB ID of the asset. Example: "/Catalogs/IPWS/060a2b340101010101010f0013-000000-6dda7dad08c24cfd-b581d7f05b5b-51fb".
- The CTMS deletion mode:

| Deletion mode  | Description | 
| ------------- |:-------------:|
| all      | Delete items in a folder and the referenced assets (if the item is the last reference to the asset), including the media files. Equivalent to DeleteMetadata=true, DeleteMedia=true in IPWS.     |
| metadata      | Delete items in a folder and the referenced assets (if the item is the last reference to the asset). This is the default if "mode" is not given in the deletion request. Equivalent to DeleteMetadata=true, DeleteMedia=false in IPWS.    |
| media      | Delete all (online) media files of the referenced assets. Items and referenced assets are not deleted, but will become offline. Equivalent to DeleteMetadata=false, DeleteMedia=true in IPWS.    |

> CTMS doesn't support selecting only specific resolutions or file types. The deletion modes "media" and "all" will delete all media files (if the last reference to the asset is deleted).

> CTMS doesn't support simulating the deletion.

###### Steps:
1. Use the cached CTMS Registry information or fetch it as shown in Using the CTMS API.
2. Find the link [loc:locations](https://developer.avid.com/ctms/api/loc/linkrels/locations.html)  for the  Avid Production Management and make an HTTP GET request.
3. Find the link [loc:delete-item-by-id-bulk-command](https://developer.avid.com/ctms/api/loc/linkrels/delete-item-by-id-bulk-command.html).
    - The request body is a JSON array with the IDs of the asset references to delete. Example
    ```
    [
    "/Catalogs/IPWS/060a2b340101010101010f0013-000000-6dda7dad08c24cfd-b581d7f05b5b-51fb",
    "/Catalogs/IPWS/060a2b340101010101010f0013-000000-070812007d070018-060e2b347f7f-d080"
    ]
    ```
    - Set the URI query parameter "mode" to the desired deletion mode.
    - Make an HTTP POST request to start a long-running command that deletes the assets. The response is a command:command resource that represents the command. Example (abbreviated):

    ```
    {
    "version": "1.0",
    "command": {
        "type": "loc:delete-item-by-id-bulk-command",
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
    - “finished”: The deletion process was finished. It's possible that only a subset of the assets was really deleted. See below for evaluating the result.
    - “error”: The entire deletion command failed. The response contains a property "error" within the "command" property with error details. See command:command for details.

If the final value of "lifecycle" is "finished", the property "result" in "payload" contains an array with the deletion result for each requested ID, in the same order as in the request body:

    ```
    {
    "version": "1.0",
    "command": {
        "type": "loc:delete-item-by-id-bulk-command",
        "lifecycle": "finished"
    },
    "payload": {
        "command-parameters": {
        "ids": [
            "/Catalogs/IPWS/060a2b340101010101010f0013-000000-6dda7dad08c24cfd-b581d7f05b5b-51fb",
            "/Catalogs/IPWS/060a2b340101010101010f0013-000000-070812007d070018-060e2b347f7f-d080"
        ]
        },
        "result": [
        {
            "success": true,
            "data": "/Catalogs/IPWS/060a2b340101010101010f0013-000000-6dda7dad08c24cfd-b581d7f05b5b-51fb"
        },
        {
            "success": false,
            "httpStatus": 400,
            "errorCode": "avid.mam.assets.access/BAD_ARGUMENT",
            "errorMessage": "Invalid item ID"
        }
        ]
    }
    }
    ```

Each result item has the following properties:

- success: true if the deletion was successful.
- Only if success is false:
    - httpStatus: the HTTP status code that a non-bulk call would return.
    - errorCode: the CTMS error code.
    - errorMessage: the error message.

#### How to use this collection:
This collection involves the process of following the above steps, as provided in the summary, in your postman application.
Open your postman, import the collection "Delete Asset/CTMS Delete bulk Assets.postman_collection.json", and follow the steps as given below:

###### Postman API Calls
(Hit Send on the "ROPC Login" API call to login in the system. View the project-level ReadMe to understand how it works.)

> **GET** 1_CTMS Registry information: avid.ctms.registry
- This GET call hits the service roots URL for CTMS registry, fetching the resources, systems and the links associated to the system.
- In the **Scripts** section: We check if the  Avid Production Management is avaialable with the registry. If yes, we fetch "[loc:locations](https://developer.avid.com/ctms/api/loc/linkrels/locations.html) " link present inside the "resources", and store the variable globally as selected_system_locLocationsHref.

> **GET** 2_loc location href
- Hitting the above fetched selected_system_locLocationsHref, to get the location or folder information of the system we are in.
- In the **Scripts** section: From the response, we fetch the "[loc:delete-item-by-id-bulk-command](https://developer.avid.com/ctms/api/loc/linkrels/delete-item-by-id-bulk-command.html)", which is used to delete the items in bulk using this one command, and store it globally as selected_system_locDeleteItemByIdBulkCommandHref.

> **POST** 3 delete assets in bulk
- Hitting the above selected_system_locDeleteItemByIdBulkCommandHref URL, we run the deletion process.
- In the **Body** section: **You as a user have to provide the list of assets or asset paths inside the array that you want to delete in your system.**
- In the **Scripts** section: We fetch the "self" link from "_links", that point to the long running command and we can poll the command status using this link.

    <mark>🔶 At this step, you need to insert the appropriate **asset paths** in the request body array</mark>

> **GET** 4 poll command status (pending/finished)
- Here we poll the status of the long running command that shows if the assets have been deleted or not.


#### Precautions/Recommendations:
- Please **select and put** the right asset/masterclip IDs in the environment required for this example.
- It is suggested to have a separate folder with assets you want to delete and only perform this action with caution on those selected assets. Once deleted, assets can not be retrieved back.