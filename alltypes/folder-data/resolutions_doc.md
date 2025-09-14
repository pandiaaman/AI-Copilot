# Documentation Title: Get Resolutions

#### Summary:
The Interplay Web Services method GetResolutions can be used for two purposes:

- Get the resolutions that are available for a list of masterclips.
    - A caller can get all known resolutions for each masterclip, or only the resolutions that are available online.
    - The method returns a summary of the resolutions for the masterclips and, optionally, the resolutions for each masterclip individually.
- Get the list of known resolutions for the  Avid Production Management workgroup.

## Get resolutions available for a masterclip in CTMS

###### Parameter:
- The MOB ID of the asset.

###### Steps:
1. Use the cached CTMS Registry information or fetch it as shown in Using the CTMS API.
2. Find the link [aa:asset-by-id](https://developer.avid.com/ctms/api/aa/linkrels/asset-by-id.html) for the  Avid Production Management. The "href" is an   URI template.
    1. Set the URI template variable "id" to the ID of the asset and expand the URI template.
    2. Make an HTTP GET request to get the [aa:asset](https://developer.avid.com/ctms/api/aa/linkrels/asset.html) resource for the asset
3. Make an HTTP GET request to the link pa:asset-medias and take the values of the property "format" in "media-items". Filter by the "online" property  if you want to get online resolutions only.

    Example: 

    ```
    {
    "base": {...},
    "common": {...},
    "media-items": [
        {
        "name": "060a2b340101010101010f0013-000000-e070a775d8eb00a5-241ed6ae5290-49f1",
        "track": "V1",
        "online": "true",
        "filePath": "//host/.../2024-03-07/202403010v0146ffe522.mxf",
        "type": "filemob",
        "essenceType": "NATIVE",
        "createdBy": "administrator",
        "format": "DV 25 420",
        "size": "7680"
        },
        {
        "name": "060a2b340101010101010f0013-000000-e170a775d8eb00a5-6ddaf1bbe9eb-b3a6",
        "track": "A1",
        "online": "true",
        "filePath": "//host/.../2024-03-07/202403010a0146ff5c9a.mxf",
        "type": "filemob",
        "essenceType": "NATIVE",
        "createdBy": "administrator",
        "format": "PCM",
        "size": "896"
        }
    ],
    "_links": {...}
    }
    ```
> In CTMS, you must query the resolutions one-by-one for each masterclip.


#### How to use this collection:
This collection involves the process of following the above steps, as provided in the summary, in your postman application.
Open your postman, import the collection "Resolutions/CTMS Get Resolutions.postman_collection.json", and follow the steps as given below:

###### Postman API Calls
(Hit Send on the "ROPC Login" API call to login in the system. View the project-level ReadMe to understand how it works.)

> **GET** 1_CTMS Registry information: avid.ctms.registry
- This GET call hits the service roots URL for CTMS registry, fetching the resources, systems and the links associated to the system.
- In the **Scripts** section: We check if the  Avid Production Management is avaialable with the registry. If yes, we fetch "[aa:asset-by-id](https://developer.avid.com/ctms/api/aa/linkrels/asset-by-id.html)" link present inside the "resources", and store the variable globally as selected_system_aaAssetByIdHref.

    <mark>🔶 At this step, you need to insert the appropriate **master clip ID** in the environment variable named: masterClipId</mark>

> **GET** 2_aa asset by id
- Hitting the above fetched selected_system_aaAssetByIdHref, to get the asset information by id.
- In the **Scripts** section: From the response, we fetch the "pa:asset-medias", which is used to fetch the asset media information that further contains resolutions, and store it globally as selected_system_paAssetMediasHref.

> **GET** 3_pa_asset_medias
- Hitting the above selected_system_paAssetMediasHref URL, fetch the resolutions associated to an asset, in this case, the master clip.

#### Precautions/Recommendations:
- Please **select and put** the right asset/masterclip IDs in the environment required for this example.

## Get resolutions for the  Avid Production Management workgroup in CTMS
>> **This function is not available in CTMS.**