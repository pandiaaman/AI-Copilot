# Documentation Title: Attributes

## Get attributes of assets in CTMS

#### Summary:
The Interplay Web Services method GetAttributes returns user and system attributes for assets and folders. 

###### Parameter:
- The MOB ID of the asset.
- Optional: a list of attributes to request.

###### Steps:
1. Use the cached CTMS Registry information or fetch it as shown in Using the CTMS API.
2. Find the link aa:asset-by-id for the  Avid Production Management. The "href" is an   URI template.
    1. Set the URI template variable "id" to the ID of the masterclip and expand the URI template.
    2. Add the query parameter "embed=attributes".
    3. Optional: add the query parameter "attributes=a,b,c" with a comma-separated list of attributes to request. If not given, a default set of attributes is returned.
    4. Make an HTTP GET request to get the aa:asset resource with an embedded aa:attributes resource.
3. Evaluate the "common" property of the aa:asset resource and the "attributes" property of the aa:attributes resource. See below to see how to map IPWS attributes to CTMS attributes.

> You can also use the link aa:asset-by-id-bulk to query multiple assets with a single bulk call. Avid recommends keeping the number of assets per request small (<= 20).

#### How to use this collection:
This collection involves the process of following the above steps, as provided in the summary, in your postman application.
Open your postman, import the collection "Attributes/CTMS Get Attributes of Assets User Input.postman_collection.json", and follow the steps as given below:

###### Postman API Calls
(Hit Send on the "ROPC Login" API call to login in the system. View the project-level ReadMe to understand how it works.)

> **GET** 1_CTMS Registry information: avid.ctms.registry
- This GET call hits the service roots URL for CTMS registry, fetching the resources, systems and the links associated to the system.
- In the **Scripts** section: We check if the  Avid Production Management is avaialable with the registry. If yes, we fetch "[aa:asset-by-id](https://developer.avid.com/ctms/api/aa/linkrels/asset-by-id.html)" link present inside the "resources", and store the variable globally as selected_system_aaAssetByIdHref.

    <mark>🔶 At this step, you need to insert the appropriate **asset Id** in the environment variable named: assetId</mark>

> **GET** 2_asset by id
- Hitting the above fetched selected_system_aaAssetByIdHref, to get the details of the given asset.
- In the **Scripts** section: 
    - We fetch aa:asset link's href, present inside ["_embedded"]["aa:attributes"]["_links"], and store it globally as selected_system_aaAssetHref.
    - We fetch aa:attributes link's href, present inside ["_links"], and store it globally as selected_system_aaAttributesHref.

> **GET** 3.1_check attributes at aa:asset href: common property
- Hitting the above selected_system_aaAssetHref command, to verify the attributes output associated to the given asset as shown above in summary.

> **GET** 3.2_check attributes at aa:attributes href: attributes property
- Hitting the above selected_system_aaAttributesHref command, to verify the similar output in the attributes section of the output.


#### Precautions/Recommendations:
- Please **select and put** the right asset/masterclip IDs in the environment required for this example.

***

## Get attributes of a folder

###### Parameters:
- The ID of the folder, consisting of the path with leading and trailing slashes. Example: "/Projects/Example/".
- Optional: a list of attributes to request.

###### Steps:
1. Query the information from the CTMS Registry.
2. Find the link loc:item-by-id for the  Avid Production Management. The "href" is an  URI template.
    1. Set the URI template variable "id" to the ID of the folder and expand the URI template.
    2. Add query parameter "?attributes=*" to get all attributes, or "?attributes=a,b,c" to get a specific list of attributes.
    3. Make an HTTP GET request to get the loc:item resource of the folder.
3. Evaluate the properties "common" and "attributes".

#### How to use this collection:
This collection involves the process of following the above steps, as provided in the summary, in your postman application.
Open your postman, import the collection "Attributes/CTMS Get Attributes of Folder User Input.postman_collection.json", and follow the steps as given below:

###### Postman API Calls
(Hit Send on the "ROPC Login" API call to login in the system. View the project-level ReadMe to understand how it works.)

> **GET** 1_CTMS Registry information: avid.ctms.registry
- This GET call hits the service roots URL for CTMS registry, fetching the resources, systems and the links associated to the system.
- In the **Scripts** section: We check if the  Avid Production Management is avaialable with the registry. If yes, we fetch "[loc:item-by-id](https://developer.avid.com/ctms/api/loc/linkrels/item-by-id.html)" link present inside the "resources", and store the variable globally as selected_system_locItemByIdHref.

    <mark>🔶 At this step, you need to insert the appropriate **folder Id** in the environment variable named: folderIdInput</mark>

> **GET** 2_loc item by id for the folder
- In the **Query Params** section: Add key as  `attributes` and value as `*`.
- Hitting the above fetched selected_system_locItemByIdHref, to get the folder structure details of the given folder id.
- In the **Scripts** section: We fetch the "[aa:attributes](https://developer.avid.com/ctms/api/aa/linkrels/attributes.html)" link present inside the _links, and store it globally as selected_system_aaAttributesHref.

> **GET** 3_check attributes at aa:attributes href: attributes property
- Hitting the above fetched selected_system_aaAttributesHref, to get the attributes property of the given folder.

#### Precautions/Recommendations:
- Please **select and put** the right asset/folder IDs in the environment required for this example.

***

## Set attributes of assets in CTMS
- The Interplay Web Services method SetAttributes updates user and system attributes for assets and folders. 

###### Parameters:
- The MOB ID of the asset.
- An array of attributes to update.

> Avid recommends updating the attributes via an embedded aa:attributes resource as shown below. You can update a few common asset attributes directly but there are tight restrictions for that.

###### Steps:
1. Use the cached CTMS Registry information or fetch it as shown in Using the CTMS API.
2. Find the link aa:update-asset-by-id for the  Avid Production Management. The "href" is an   URI template.
    1. Set the URI template variable "id" to the ID of the masterclip and expand the URI template.
    2. Make an HTTP PATCH request with an aa:asset resource with an embedded aa:attributes resource with the attributes to set as request body. See below for the mapping between IPWS and CTMS. Example:

    ```
    {
    "_embedded": {
        "aa:attributes": {
        "attributes": [
            {
            "name": "com.avid.workgroup.Property.User.IPWSTest",
            "value": "The weather is beautiful outside."
            },
            {
            "name": "Comments",
            "value": "Weather report"
            }
        ]
        }
    }
    }
    ```
#### How to use this collection:
This collection involves the process of following the above steps, as provided in the summary, in your postman application.
Open your postman, import the collection "Attributes/CTMS Set Attributes of an Asset.postman_collection.json", and follow the steps as given below:

###### Postman API Calls
(Hit Send on the "ROPC Login" API call to login in the system. View the project-level ReadMe to understand how it works.)

> **GET** 1_CTMS Registry information: avid.ctms.registry
- This GET call hits the service roots URL for CTMS registry, fetching the resources, systems and the links associated to the system.
- In the **Scripts** section: We check if the  Avid Production Management is avaialable with the registry. If yes, we fetch "[aa:update-asset-by-id](https://developer.avid.com/ctms/api/aa/linkrels/update-asset-by-id.html)" link present inside the "resources", and store the variable globally as selected_system_aaUpdateAssetByIdHref.

    <mark>🔶 At this step, you need to insert the appropriate **asset Id** in the environment variable named: masterClipId</mark>

> **PATCH** 2_Update Asset by ID
- In the **Body** section, add the JSON for embedded attributes, as shown above in the summary tab.
- Hitting the above fetched selected_system_aaUpdateAssetByIdHref, to update the given asset ID.

#### Precautions/Recommendations:
- Please **select and put** the right asset/folder IDs in the environment required for this example.
