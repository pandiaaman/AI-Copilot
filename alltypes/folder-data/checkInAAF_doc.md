# Documentation Title: Check in AAF

#### Summary:
The Interplay Web Services method CheckInAAF accepts a binary AAF file (Advanced Authoring Format) and checks-in the AAF to a given folder. If an asset with the MOB ID in the AAF already exists, the asset is updated, otherwise a new asset is created. The asset is added to the target folder if required.

## Check-in an AAF in CTMS

###### Parameters:
- A byte array with the content of an AAF file.
- The ID of the target folder, consisting of the path with leading and trailing slashes. Example: "/Projects/Example/".

###### Steps:
1. Use the cached CTMS Registry information or fetch it as shown in Using the CTMS API.
2. Find the link [loc:item-by-id](https://developer.avid.com/ctms/api/loc/linkrels/item-by-id.html) for the  Avid Production Management. The "href" is an  URI template.
    1. Set the URI template variable "id" to the ID of the target folder and expand the URI template.
    2. Make an HTTP GET request to get the [loc:item](https://developer.avid.com/ctms/api/loc/linkrels/item.html) resource of the folder.
3. Make an HTTP POST request to the pa:upload-file link.
    1. Set header Content-Type: application/octet-stream.
    2. Send the bytes of the AAF in the request body.
    3. The response is a JSON with two properties: name is the file name of the uploaded file, downloadLink is a URI that can be used to download the file again:

    ```
    {
    "name": "a4a43ca8-17c8-4983-a52e-56878c8d4f72.dat",
    "downloadLink": "https://.../a4a43ca8-17c8-4983-a52e-56878c8d4f72.dat"
    }
    ```

4. Make an HTTP POST call to the pa:import-asset-command link of the [loc:item](https://developer.avid.com/ctms/api/loc/linkrels/item.html) resource from step 2 to start a long-running command that checks-in the AAF.
    1. The request body is a JSON with a property "filename" that contains the value of the received "name" property from step 3:

    ```
    {
        "filename": "a4a43ca8-17c8-4983-a52e-56878c8d4f72.dat"
    }
    ```
    2. The response is a command:command resource representing the command. Example response (abbreviated):
    ```
    {
    "version": "1.0",
    "command": {
        "type": "aa:import-asset-command",
        "lifecycle": "pending"
    },
    "_links": {
        "self": {
        "href": "https://..."
        }
    }
    }
    ```
5. Poll the command status (with a small delay of, for example, 200 milliseconds between calls) by making an HTTP GET call to the "self" link until "lifecycle" in "command" is either "finished" or "error". The result depends on the final value of the "lifecycle" property:
    1. “finished”: The export process was completed successfully. The response contains an embedded [loc:item](https://developer.avid.com/ctms/api/loc/linkrels/item.html) resource with the reference to the checked-in asset, including an embedded loc:referenced-object resource with information about the asset. Example (abbreviated):
    ```
    {
    "version": "1.0",
    "command": {
        "type": "pa:import-asset-command",
        "lifecycle": "finished"
    },
    "_embedded": {
        "loc:item": {
        "base": {
            "id": "/Catalogs/IPWS/060a2b340101010101010f0013-000000-55dd943eda0748bd-060e2b347f7f-2a80"
        },
        "common": {
            "name": "Some asset"
        },
        "_embedded": {
            "loc:referenced-object": {
            "base": {
                "id": "060a2b340101010101010f0013-000000-55dd943eda0748bd-060e2b347f7f-2a80",
                "type": "masterclip"
            },
            "common": {
                "name": "Some asset"
            }
            }
        }
        }
    }
    }
    ```
    2. “error”: The call failed. The response contains a property "error" within the "command" property with error details. See command:command for details.

> The pa:upload-file and pa:import-asset-command links will be part of the release version of  Avid Production Management and will be documented on developer.avid.com at that point in time.

> See [SetHeadframe via CTMS]() if you want to set the headframe for the asset.

#### How to use this collection:
This collection involves the process of following the above steps, as provided in the summary, in your postman application.
Open your postman, import the collection "Check in AAF/CTMS Check in AAF.postman_collection.json", and follow the steps as given below:

###### Postman API Calls
(Hit Send on the "ROPC Login" API call to login in the system. View the project-level ReadMe to understand how it works.)

> **GET** 1_CTMS Registry information: avid.ctms.registry
- This GET call hits the service roots URL for CTMS registry, fetching the resources, systems and the links associated to the system.
- In the **Scripts** section: We check if the  Avid Production Management is avaialable with the registry. If yes, we fetch "[loc:item-by-id](https://developer.avid.com/ctms/api/loc/linkrels/item-by-id.html)" link present inside the "resources", and store the variable globally as selected_system_locItemByIdHref.

    <mark>🔶 At this step, you need to insert the appropriate **folder ID** in the environment variable named: folderIdInput</mark>

> **GET** 2_loc item by id
- Hitting the above fetched selected_system_locItemByIdHref, to get the location/folder structure details of the selected folder ID.
- In the **Scripts** section: 
    - We fetch the "pa:upload-file" link from the _links in the HAL output, and store it in selected_system_paUploadFileHref variable globally.
    - We also fetch "pa:import-asset-command" from the _links, and store it in selected_system_paImportAssetCommandHref variable globally.
Both of these links will be used in the upcoming steps.

> **PUT** 3 upload file
- In the **Headers** section : Put Content-Type as "application/octet-stream".
- In the **Body** section: Add your aaf file as a binary.
- From the Response, get the filename and keep it with you for the next step.

> **POST** 4 import asset command
- In the **Body** section: add the filename you retreived in the last step.
- In the **Scripts** section: We fetch the "self" link from "_links", that point to the long running command and we can poll the command status using this link.

> **GET** 5 poll command status
- Here we poll the status of the long running command that shows if the thumbnail has been set for the asset or not.

#### Precautions/Recommendations:
- Please **select and put** the right asset/masterclip IDs in the environment required for this example.