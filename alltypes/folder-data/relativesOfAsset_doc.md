# Documentation Title: Relatives of an Asset

#### Summary:
The Interplay Web Services method FindRelatives returns assets that are related to a given asset. For example, the relatives of a masterclip are the sequences that use the masterclip, and the subclips that have been created from it. The response also contains attributes for each of the related assets. 

## Find related assets in CTMS

###### Parameter:
- The MOB ID of the asset.
- Optional: a list of attributes to get for each related asset.

###### Steps:
1. Use the cached CTMS Registry information or fetch it as shown in Using the CTMS API.
2. Find the link [aa:asset-by-id](https://developer.avid.com/ctms/api/aa/linkrels/asset-by-id.html) for the  Avid Production Management. The "href" is an   URI template.
    1. Set the URI template variable "id" to the ID of the asset and expand the URI template.
    2. Make an HTTP GET request to get the [aa:asset](https://developer.avid.com/ctms/api/aa/linkrels/asset.html) resource for the asset.
3. Call HTTP GET on the relations:relations link. The response is a relations:relations resource containing the first page of the list of related assets.
4. Call HTTP GET on the "next" link to get the next page of related assets as long as the "next" link is present. Each page contains the paging information and an array of related entities (here, for example, with a page size of 1):

    ```
    {
    "paging": {
        "limit": 1,
        "offset": 0,
        "elements": 1,
        "totalElements": 2
    },
    "_links": {
        "self": {
        "href": "https://..."
        },
        "first": {
        "href": "https://..."
        },
        "next": {
        "href": "https://..."
        },
        "relations:relation": [
        {
            "href": "https://..."
        }
        ]
    },
    "_embedded": {
        "relations:relation": [
        {
            "relationType": "masterclip.forward",
            "relatedEntity": {
            "id": "060a2b340101010101010f0013-000000-00003d0f311a40e5-060e2b347f7f-2a80",
            "kind": "aa",
            "type": "masterclip"
            },
            "labels": {
            "en": "Master Clip Relatives"
            },
            "_links": {
            "self": {
                "href": "https://..."
            },
            "relations:related-entity": {
                "href": "https://..."
            },
            "relations:relation-type": {
                "href": "https://..."
            }
            }
        }
        ]
    }
    }
    ```
5. The properties "relatedEntity.id" and "relatedEntity.type" of the embedded relations:relation resources from all pages contain the IDs and types of the related assets.

If you need attributes for the related assets:

1. Find the link [aa:asset-by-id](https://developer.avid.com/ctms/api/aa/linkrels/asset-by-id.html)-bulk in the CTMS Registry for the system ID of the  Avid Production Management.
2. In batches of about 20 asset IDs: Use HTTP POST on the "href" of the [aa:asset-by-id](https://developer.avid.com/ctms/api/aa/linkrels/asset-by-id.html)-bulk link with an array of asset IDs as body:
```
[
  "060a2b340101010101010f0013-000000-00003d0f311a40e5-060e2b347f7f-2a80"
]
```
3. This returns a bulk response with an array in the same order as in the request body. For each requested asset, you get back either "success": false and error information, or "success": true and an [aa:asset](https://developer.avid.com/ctms/api/aa/linkrels/asset.html) resource with common attributes and status values in the "data" property. See Bulk Calls for details.
4. If you want additional attributes, use the URL query parameters "?embed=attributes&attributes=X,Y,Z" to get an embedded [aa:attributes](https://developer.avid.com/ctms/api/aa/linkrels/attributes.html) resource with the additional attributes X, Y, and Z. Without the "attributes" query parameter, you get back all attributes.

Evaluate the attributes in the same way as for the method GetAttributes.

#### How to use this collection:
This collection involves the process of following the above steps, as provided in the summary, in your postman application.
Open your postman, import the collection "Relatives of Asset/CTMS Find Relatives or related assets.postman_collection.json", and follow the steps as given below:

###### Postman API Calls
(Hit Send on the "ROPC Login" API call to login in the system. View the project-level ReadMe to understand how it works.)

> **GET** 1_CTMS Registry information: avid.ctms.registry
- This GET call hits the service roots URL for CTMS registry, fetching the resources, systems and the links associated to the system.
- In the **Scripts** section: We check if the  Avid Production Management is avaialable with the registry. If yes, we fetch "[aa:asset-by-id](https://developer.avid.com/ctms/api/aa/linkrels/asset-by-id.html)" link present inside the "resources", and store the variable globally as selected_system_aaAssetByIdHref.

    <mark>🔶 At this step, you need to insert the appropriate **asset ID** in the environment variable named: assetMobId</mark>

> **GET** 2_aa asset by id
- Hitting the above fetched selected_system_aaAssetByIdHref, to get the asset information by id.
- In the **Scripts** section: From the response, we fetch the "relations:relations", which is used to fetch the related assets to the given asset, and store it globally as selected_system_relationsRelationsHref.

> **GET** 3 get related assets
- Hitting the above selected_system_relationsRelationsHref URL, to fetch all the relations to the given asset.

#### Precautions/Recommendations:
- Please **select and put** the right asset/masterclip IDs in the environment required for this example.