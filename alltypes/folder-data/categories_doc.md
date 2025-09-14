# Documentation Title: Categories

## Set categories for an asset in CTMS

#### Summary:
The Interplay Web Services method SetCategories sets the categories for assets and folders. 
> The list of available categories is pre-configured in the MediaCentral |  Avid Production Management. See "Get categories via CTMS" to learn how to query the list of configured categories.
> CTMS replaces the categories of the asset with the given array of categories. The IPWS method works differently and accepts an incremental update with categories to add and to remove. If you want to replace that semantic, you must first get the current categories, add or remove categories in the list, and then use the CTMS link below to replace the categories with the resulting list.

###### Parameter:
- The MOB ID of the asset.
- An array of categories.

###### Steps:
1. Use the cached CTMS Registry information or fetch it as shown in Using the CTMS API.
2. Find the link [aa:update-asset-by-id](https://developer.avid.com/ctms/api/aa/linkrels/update-asset-by-id.html) for the  Avid Production Management. The "href" is an   URI template.
    1. Set the URI template variable "id" to the ID of the masterclip and expand the URI template.
    2. Make an HTTP PATCH request with an [aa:asset](https://developer.avid.com/ctms/api/aa/linkrels/asset.html) resource with an embedded [aa:attributes](https://developer.avid.com/ctms/api/aa/linkrels/attributes.html) resource with the attribute "com.avid.workgroup.Property.Category" in the request body. The value of the attribute is an array of entries, each with an increasing row number in the property "index", and the category to set in the property "value".

    ```
    {
    "_embedded": {
        "aa:attributes": {
        "attributes": [
            {
            "name": "com.avid.workgroup.Property.Category",
            "value": [
                {
                "index": 0,
                "value": "category1"
                },
                {
                "index": 1,
                "value": "category2"
                }
            ]
            }
        ]
        }
    }
    }
    ```

#### How to use this collection:
This collection involves the process of following the above steps, as provided in the summary, in your postman application.
Open your postman, import the collection "Categories/CTMS Set Categories of an Asset.postman_collection.json", and follow the steps as given below:

###### Postman API Calls
(Hit Send on the "ROPC Login" API call to login in the system. View the project-level ReadMe to understand how it works.)

> **GET** 1_CTMS Registry information: avid.ctms.registry
- This GET call hits the service roots URL for CTMS registry, fetching the resources, systems and the links associated to the system.
- In the **Scripts** section: We check if the  Avid Production Management is avaialable with the registry. If yes, we fetch "[aa:update-asset-by-id](https://developer.avid.com/ctms/api/aa/linkrels/update-asset-by-id.html)" link present inside the "resources", and store the variable globally as selected_system_aaUpdateAssetByIdHref.

    <mark>🔶 At this step, you need to insert the appropriate **master clip ID** in the environment variable named: masterClipId</mark>

> **PATCH** 2_update aa asset by id
- Hitting the above fetched selected_system_aaUpdateAssetByIdHref, to get the response associated to the asset, showing the associated categories.
- In the **Body** section: Add the request body, as mentioned above in the summary tab. 
    
    <mark>Please make sure, that you have set the categories "category1", "category2" etc. in your system before running this.</mark>


#### Precautions/Recommendations:
- Please **select and put** the right asset/masterclip IDs in the environment required for this example.
- The categories must be set beforehand, otherwise, the system will throw an error if unknown values of categories is sent in the request body.

***

## Get categories for an asset in CTMS

The Interplay Web Services method GetCategories can be used for two purposes:

- Get the list of categories that are configured for the  Avid Production Management.
- Get the categories that are assigned to a concrete asset or folder.

### Get configured categories for the  Avid Production Management in CTMS

###### Steps:
1. Use the cached CTMS Registry information or fetch it as shown in Using the CTMS API.
2. Find the link [taxonomies:taxonomy-by-taxonomyid](https://developer.avid.com/ctms/api/taxonomies/linkrels/taxonomy-by-taxonomyid.html) for the  Avid Production Management. The "href" is an   URI template.
    1. Set the URI template variable "taxonomyid" to “com.avid.workgroup.Property.Category” and expand the URI template.
    2. Make an HTTP GET request to get the [taxonomies:taxonomy](https://developer.avid.com/ctms/api/taxonomies/linkrels/taxonomy.html) resource of the taxonomy that contains the configured categories.
3. Find the link [taxonomies:entries](https://developer.avid.com/ctms/api/taxonomies/linkrels/entries.html) and make an HTTP GET request to get a taxonomy:entries resource with the first page of entries in the form of an embedded array of taxonomies:entry resources. The resource uses paging to limit the message size. Example:

    ```
    {
    "paging": {
        "limit": 25,
        "offset": 0,
        "elements": 2,
        "totalElements": 2
    },
    "_links": { ... },
    "_embedded": {
        "taxonomies:entry": [
        {
            "id": "category1",
            "labels": {
            "en": "category1"
            },
            "_links": { ... }
        },
        {
            "id": "category2",
            "labels": {
            "en": "category2"
            },
            "_links": { ... }
        }
        ]
    }
    }
    ```
4. Repeat as long as a "next" link exists: make an HTTP GET request to the "next" link to get a taxonomy:entries resource with the next page of entries.

#### How to use this collection:
This collection involves the process of following the above steps, as provided in the summary, in your postman application.
Open your postman, import the collection "Categories/CTMS Get Categories of a System.postman_collection.json", and follow the steps as given below:

###### Postman API Calls
(Hit Send on the "ROPC Login" API call to login in the system. View the project-level ReadMe to understand how it works.)

> **GET** 1_CTMS Registry information: avid.ctms.registry
- This GET call hits the service roots URL for CTMS registry, fetching the resources, systems and the links associated to the system.
- In the **Scripts** section: We check if the  Avid Production Management is avaialable with the registry. If yes, we fetch "[taxonomies:taxonomy-by-taxonomyid](https://developer.avid.com/ctms/api/taxonomies/linkrels/taxonomy-by-taxonomyid.html)" link present inside the "resources", and store the variable globally as selected_system_taxonomyByTaxonomyIdHref.

> **GET** 2_taxonomy by taxonomyid
- Hitting the above fetched selected_system_taxonomyByTaxonomyIdHref, to get the taxonomies for the given ID:"com.avid.workgroup.Property.Category".
- In the **Scripts** section: We fetch the "[taxonomies:entries](https://developer.avid.com/ctms/api/taxonomies/linkrels/entries.html)" link present inside the _links, and store it globally as selected_system_taxonomyEntriesHref, showing the list of taxonomy enteries for the given system. 

> **GET** 3 taxonomy enteries
- Hitting the above fetched selected_system_taxonomyEntriesHref, to get the taxonomy enteries for the system.

#### Precautions/Recommendations:
- Please **select and put** the right asset/masterclip IDs in the environment required for this example.

***

### Get categories of an asset in CTMS

###### Parameters:
- The MOB ID of the asset.

###### Steps:
1. Use the cached CTMS Registry information or fetch it as shown in Using the CTMS API.
2. Find the link [aa:asset-by-id](https://developer.avid.com/ctms/api/aa/linkrels/asset-by-id.html) for the  Avid Production Management. The "href" is an   URI template.
    1. Set the URI template variable "id" to the ID of the masterclip and expand the URI template.
    2. Add the query parameters "embed=attributes&attributes=com.avid.workgroup.Property.Category".
    3. Make an HTTP GET request to get the [aa:asset](https://developer.avid.com/ctms/api/aa/linkrels/asset.html) resource with an embedded [aa:attributes](https://developer.avid.com/ctms/api/aa/linkrels/attributes.html) resource.
3. Find the attribute "com.avid.workgroup.Property.Category" in the "attributes" property of the embedded [aa:attributes](https://developer.avid.com/ctms/api/aa/linkrels/attributes.html) resource. The property "value" contains the ID and label of the category. Example:

    ```
    {
    "base": {...},
    "common": {...},
    "_links": {...},
    "_embedded": {
        "aa:attributes": {
        "attributes": [
            {
            "name": "com.avid.workgroup.Property.Category",
            "value": [
                {
                "index": 0,
                "value": "category1"
                },
                {
                "index": 1,
                "value": "category2"
                }
            ],
            "type": "multi-value list",
            "taxonomyid ": "com.avid.workgroup.Property.Category"
            }
        ],
        "_links": {...}
        }
    }
    }
    ```
> You can also use the link [aa:asset-by-id](https://developer.avid.com/ctms/api/aa/linkrels/asset-by-id.html)-bulk in step 2 to query multiple assets with a single bulk call. Avid recommends to keep the number of assets per request small (<= 20).

#### How to use this collection:
This collection involves the process of following the above steps, as provided in the summary, in your postman application.
Open your postman, import the collection "Categories/CTMS Get Categories of an Asset.postman_collection.json", and follow the steps as given below:

###### Postman API Calls
(Hit Send on the "ROPC Login" API call to login in the system. View the project-level ReadMe to understand how it works.)

> **GET** 1_CTMS Registry information: avid.ctms.registry
- This GET call hits the service roots URL for CTMS registry, fetching the resources, systems and the links associated to the system.
- In the **Scripts** section: We check if the  Avid Production Management is avaialable with the registry. If yes, we fetch "[aa:update-asset-by-id](https://developer.avid.com/ctms/api/aa/linkrels/update-asset-by-id.html)" link present inside the "resources", and store the variable globally as selected_system_aaUpdateAssetByIdHref.

    <mark>🔶 At this step, you need to insert the appropriate **master clip ID** in the environment variable named: masterClipId</mark>

> **GET** 2_aa asset by id
- Hitting the above fetched selected_system_aaUpdateAssetByIdHref, to get the asset information for the given asset ID.
- In the **Params** section: We add the query parameters as (i) key as embed, value as attributes, and (ii) key as attributes, value as com.avid.workgroup.Property.Category. The query parameter overall should look like: ?embed=attributes&attributes=com.avid.workgroup.Property.Category  

#### Precautions/Recommendations:
- Please **select and put** the right asset/masterclip IDs in the environment required for this example.

***

### Get categories of a folder

###### Parameters:
- The ID of the folder, consisting of the path with leading and trailing slashes. Example: "/Projects/Example/".

###### Steps:
1. Query the information from the CTMS Registry.
2. Find the link [loc:item-by-id](https://developer.avid.com/ctms/api/loc/linkrels/item-by-id.html) for the  Avid Production Management. The "href" is an  URI template.
    1. Set the URI template variable "id" to the ID of the folder and expand the URI template.
    2. Add query parameter "attributes=com.avid.workgroup.Property.Category".
    3. Make an HTTP GET request to get the [loc:item](https://developer.avid.com/ctms/api/loc/linkrels/item.html) resource of the folder.
3. Find the attribute "com.avid.workgroup.Property.Category" in the property "attributes". The structure of the attribute is the same as above for assets.

#### How to use this collection:
This collection involves the process of following the above steps, as provided in the summary, in your postman application.
Open your postman, import the collection "Categories/CTMS Get Categories of a Folder.postman_collection.json", and follow the steps as given below:

###### Postman API Calls
(Hit Send on the "ROPC Login" API call to login in the system. View the project-level ReadMe to understand how it works.)

> **GET** 1_CTMS Registry information: avid.ctms.registry
- This GET call hits the service roots URL for CTMS registry, fetching the resources, systems and the links associated to the system.
- In the **Scripts** section: We check if the  Avid Production Management is avaialable with the registry. If yes, we fetch "[loc:item-by-id](https://developer.avid.com/ctms/api/loc/linkrels/item-by-id.html)" link present inside the "resources", and store the variable globally as selected_system_locItemByIdHref.

    <mark>🔶 At this step, you need to insert the appropriate **folder ID** in the environment variable named: folderIdInput</mark>

> **GET** 2_loc item by id
- Hitting the above fetched selected_system_locItemByIdHref, to get the folder structure information for the given folder ID.
- In the **Params** section: We add the query parameters as (i) key as attributes, value as com.avid.workgroup.Property.Category. The query parameter overall should look like: ?attributes=com.avid.workgroup.Property.Category  

#### Precautions/Recommendations:
- Please **select and put** the right folder IDs in the environment required for this example.