# Documentation Title: References To An Asset (FindLinks in IPWS)

#### Summary:
The Interplay Web Services method FindLinks returns all references to a given asset in the entire folder structure.

## Get all references to an asset in CTMS

###### Parameter:
- The MOB ID of the asset.

###### Steps:
1. Use the cached CTMS Registry information or fetch it as shown in Using the CTMS API.
2. Find the link [aa:asset-by-id](https://developer.avid.com/ctms/api/aa/linkrels/asset-by-id.html) for the  Avid Production Management. The "href" is an   URI template.
    1. Set the URI template variable "id" to the ID of the asset and expand the URI template.
    2. Make an HTTP GET request to get the [aa:asset](https://developer.avid.com/ctms/api/aa/linkrels/asset.html) resource for the asset
3. Make an HTTP GET request to the [loc:referencing-items](https://developer.avid.com/ctms/api/loc/linkrels/referencing-items.html)  link to get a [loc:referencing-items](https://developer.avid.com/ctms/api/loc/resources/referencing-items.html)  resource with an embedded array of [loc:item](https://developer.avid.com/ctms/api/loc/linkrels/item.html) resources with all references to the asset in the entire folder hierarchy. The IDs of the references can be found in the property "id" in "base". Example response (abbreviated):

    ```
    {
    "_embedded": {
        "loc:item": [
        {
            "base": {
            "id": "/Catalogs/IPWS/Example/060a2b340101010101010f0013-000000-6dda7dad08c24cfd-b581d7f05b5b-51fb",
            "type": "folder-item",
            "systemType": "avid-pmplus",
            "systemID": "DD481E2E-260B-4684-9D25-44C774E3F782"
            }
        },
        {
            "base": {
            "id": "/Catalogs/JaneSmith/060a2b340101010101010f0013-000000-6dda7dad08c24cfd-b581d7f05b5b-51fb",
            "type": "folder-item",
            "systemType": "avid-pmplus",
            "systemID": "DD481E2E-260B-4684-9D25-44C774E3F782"
            }
        }
        ]
    }
    }
    ```

#### How to use this collection:
This collection involves the process of following the above steps, as provided in the summary, in your postman application.
Open your postman, import the collection "References to an Asset (FindLinks)/CTMS Find Links or References to an Asset.postman_collection.json", and follow the steps as given below:

###### Postman API Calls
(Hit Send on the "ROPC Login" API call to login in the system. View the project-level ReadMe to understand how it works.)

> **GET** 1_CTMS Registry information: avid.ctms.registry
- This GET call hits the service roots URL for CTMS registry, fetching the resources, systems and the links associated to the system.
- In the **Scripts** section: We check if the  Avid Production Management is avaialable with the registry. If yes, we fetch "[aa:asset-by-id](https://developer.avid.com/ctms/api/aa/linkrels/asset-by-id.html)" link present inside the "resources", and store the variable globally as selected_system_aaAssetByIdHref.

    <mark>🔶 At this step, you need to insert the appropriate **asset ID** in the environment variable called, assetMobId.</mark>

> **GET** 2_aa asset by id
- Hitting the above fetched selected_system_aaAssetByIdHref, to get the asset by id in the system.
- In the **Scripts** section: From the response, we fetch the "[loc:referencing-items](https://developer.avid.com/ctms/api/loc/linkrels/referencing-items.html) ", which is used to get the link to get all the references of an asset or links to that asset, and store it globally as selected_system_locReferencingItemsHref.

> **POST** 3 get references/links to an asset
- Hitting the above selected_system_locReferencingItemsHref URL, to fetch all the associated links of that asset.

#### Precautions/Recommendations:
- Please **select and put** the right asset/masterclip IDs in the environment required for this example.