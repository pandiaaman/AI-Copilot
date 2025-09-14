# Documentation Title: Create Subclip

#### Summary:
The Interplay Web Services method CreateSubclip is used to create a subclip from a given masterclip. The subclip gets a new MOB ID. The method accepts the following parameters:

- MasterclipURI: (mandatory) The URI of the masterclip.
- The range for the subclip within the masterclip (mandatory):
    - StartingOffset: start frame of the subclip range within the masterclip.
    - StartingTimecode: start of the subclip range within the masterclip, given as a SMPTE timecode label.
    - Length: length of the range in frames.
    - Exactly one of StartingOffset and StartingTimecode must be used.
- SubclipPathURI: (mandatory) The URI of the target folder for the created subclip.
- Name: (mandatory) The name of the subclip.
- Attributes: (optional) attributes to set for the subclip.
- Headframe: (optional) the bytes of an image to use as headframe (or thumbnail) for the subclip.

## Creating a subclip of a masterclip in CTMS

###### Parameter:
- The MOB ID of the masterclip.
- The range in the masterclip to use for the sub clip, given as start frame and duration in frames.
- The ID of the target folder.
- Optional: the name of the subclip. If not given, the subclip will get a default name derived from the name of the masterclip.

###### Steps:
1. Use the cached CTMS Registry information or fetch it as shown in Using the CTMS API.
2. Find the link [aa:asset-by-id](https://developer.avid.com/ctms/api/aa/linkrels/asset-by-id.html) for the  Avid Production Management. The "href" is an  URI template.
    1. Set the URI template variable "id" to the ID of the masterclip and expand the URI template.
    2. Make an HTTP GET request to get the [aa:asset](https://developer.avid.com/ctms/api/aa/linkrels/asset.html) resource for the asset.
3. Make an HTTP POST request to the link aa:create-subclip with a JSON request body

    ```
    {
    "common": {
        "name": "My subclip"          // Name of the subclip, optional
    },
    "start": 10,                    // Start frame of the subclip within the masterclip.
    "duration": 30,                 // Duration of the subclip
    "location": "/Catalogs/IPWS/"   // ID of the target folder
    }
    ```
4. The response is a JSON object with two properties, "aa:asset" and "loc:item", both in the same format as the response for an item of a bulk call (see Bulk calls in CTMS for details, here abbreviated):
    ```
    {
    "aa:asset": {
        "success": true,
        "data": {
        "base": {
            "systemID": "E75274DF-BFE6-46CD-BA52-FB58CA0134F2",
            "systemType": "avid-pmplus",
            "id": "060a2b340101010101010f0013-000000-01eacf5d64ed0080-a2083662fe28-3bc5",
            "type": "subclip"
        },
        "common": {
            "name": "Created subclip",
            ...
        },
        "_links": { ... }
        }
    },
    "loc:item": {
        "success": true,
        "data": {
        "base": {
            "systemID": "E75274DF-BFE6-46CD-BA52-FB58CA0134F2",
            "systemType": "avid-pmplus",
            "id": "/Catalogs/IPWS//060a2b340101010101010f0013-000000-01eacf5d64ed0080-a2083662fe28-3bc5",
            "type": "folder-item"
        },
        "common": {
            "name": "Created subclip",
            ...
        },
        "_links": { ... },
        "_embedded": {
            "loc:referenced-object": { ... }
        }
        }
    }
    }
    ```

The property [aa:asset](https://developer.avid.com/ctms/api/aa/linkrels/asset.html) contains the information about the created asset. The format is the same as in the response for bulk calls with the sub properties:

1. success: true if the asset was created successfully, false if not.
2. data: in case of success, the property contains the [aa:asset](https://developer.avid.com/ctms/api/aa/linkrels/asset.html) resource of the created subclip, including the MOB ID in the property "id" in "base".
3. httpStatus, errorCode and errorMessage: in case of an error.

The property [loc:item](https://developer.avid.com/ctms/api/loc/linkrels/item.html) contains information about the created asset link in the target folder. The format is the same as above, only with the [loc:item](https://developer.avid.com/ctms/api/loc/linkrels/item.html) resource of the created subclip in the data property in case of success.

> You can use the link aa:update-asset in the returned [aa:asset](https://developer.avid.com/ctms/api/aa/linkrels/asset.html) resource to set common attributes and user attributes of the subclip. See "SetAttributes via CTMS" for details.

> You can use the link [aa:set-thumb-command](https://developer.avid.com/ctms/api/aa/linkrels/set-thumb-command.html) to set a thumbnail. See "SetHeadframe via CTMS" for details.

#### How to use this collection:
This collection involves the process of following the above steps, as provided in the summary, in your postman application.
Open your postman, import the collection "Subclips/CTMS Create Subclip.postman_collection.json", and follow the steps as given below:

###### Postman API Calls
(Hit Send on the "ROPC Login" API call to login in the system. View the project-level ReadMe to understand how it works.)

> **GET** 1_CTMS Registry information: avid.ctms.registry
- This GET call hits the service roots URL for CTMS registry, fetching the resources, systems and the links associated to the system.
- In the **Scripts** section: We check if the  Avid Production Management is avaialable with the registry. If yes, we fetch "[aa:asset-by-id](https://developer.avid.com/ctms/api/aa/linkrels/asset-by-id.html)" link present inside the "resources", and store the variable globally as selected_system_aaAssetByIdHref.

    <mark>🔶 At this step, you need to insert the appropriate **master clip ID** in the environment variable named: masterClipId</mark>

> **GET** 2_aa asset by id
- Hitting the above fetched selected_system_aaAssetByIdHref, to get the asset information by id.
- In the **Scripts** section: From the response, we fetch the "aa:create-subclip", which is used to create a subclip for the selected asset, and store it globally as selected_system_aaCreateSubclipHref.

> **POST** 3 create subclip
- Hitting the above selected_system_aaCreateSubclipHref URL, we create the subclip for the selected asset.
- In the **Body** section: We provide the subclip details, like the name, the start, duration and location where we need to store this subclip finally.

#### Precautions/Recommendations:
- Please **select and put** the right asset/masterclip IDs in the environment required for this example.