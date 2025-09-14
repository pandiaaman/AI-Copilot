# Documentation Title: References To An Asset (FindLinks in IPWS)

#### Summary:
The Interplay Web Services method Search is used to search for assets. The method accepts a search request with the following properties:
- **InterplayPathURI (mandatory)**: The folder in which to search for assets.
- **SearchGroup**: The search criteria. See below for details.
- **ReturnAttributes**: a list of attributes to return for each matching asset. If not given, a default set of attributes is returned.
- **MaxResults**: the maximum number of results to return. If not given, all results are returned.

> In MediaCentral | Production Management, the SearchGroup parameter allowed for a very fine-granular search with a logical combination with AND, OR, and NOT over conditions on almost all attributes, on categories, on resolutions, and on usage of assets. In  Avid Production Management, the search functionality is optimized for performance and supports only conditions for the most frequently used attributes and properties. 

The search in Interplay Web Services always returns all references to the matching assets in the given folder and all its sub folders. If a matching asset is in two sub folders, then the result will contain the asset twice, one entry for each of the two sub folders.

In CTMS, there are two different search methods:
    - `pa:advanced-asset-search`: returns a list of matching assets (masterclips, sequences, sub clips, and so on) in and below the given folder, but without a direct reference to the folder. In CTMS terms, it returns [aa:asset](https://developer.avid.com/ctms/api/aa/linkrels/asset.html) resources. If a matching asset is in two sub folders, it's returned only once in the result set.
    - `pa:advanced-item-search`: returns a list of asset links in folders. In CTMS terms, it returns [loc:item](https://developer.avid.com/ctms/api/loc/linkrels/item.html) resources. If a matching asset is in two sub folders, the caller can decide with a parameter (oneLinkOnly) if both asset links are returned or only one of them.


## Search request in CTMS

The request body is almost the same for pa:advanced-asset-search and pa:advanced-item-search. Example:

    ```
    {
    "version": "1.0",
    "folder": "/Catalogs/Example",
    "text": "Michael Jordon",
    "type": [ "masterclip", "sequence" ],
    "categories": [ "news", "sports" ],
    "categoriesMode": "anyof",
    "resolution": "PCM",
    "inUse": true,
    "from": "2025-03-06T14:00:00+01:00",
    "to": "2025-03-26T14:33:00+01:00",
    "timeMode": "modified",
    "videoId": "1234",
    "videoIdMode": "exact",
    "multiLink": true,
    "attributes": [
        "com.avid.workgroup.Property.System.FPS",
        "com.avid.workgroup.Property.System.Tracks"
    ],
    "oneLinkOnly": true
    }
    ```
    Properties of a search request:
    
| Property  | Mandatory | Description |
| ------------- |:-------------:|:-----------|
| version      | mandatory     |Version of the search request format. Currently always "1.0".
| folder     | mandatory     |The folder to search in. The method finds assets in the given folder and all its sub folders that the caller can access.
| text      | optional     |Search text. If given, matches only assets that contain the text in the name or comment of the asset.
| type      | optional     |Array of asset types to return. Possible values: "masterclip", "sequence", "subclip", "group", "motioneffect", "effect", "renderedeffect", "stereomasterclip" and "stereosubclip".
| categories and categoriesMode      | optional     |categories is an array of categories to search for. The search behavior depends on the value of categoriesMode: 1. anyof: matches if an asset has any of the given categories. This is the default if categoriesMode is not given. 2. equality: matches if an asset has exactly the given categories and none more. 3. include: matches if an asset has all the given categories and maybe additional ones.
| resolution      | optional     |Resolution to search for. If given, matches only assets that have a track with the given resolution.
| inUse      | optional     |Boolean flag. If given, returns only asset that are used by other assets (inUse=true) or that are not used by other assets (inUse=false).
| from, to and timeMode      | optional     |Defines a time range for the search: 1. timeMode: defines if the time range applies to the creation time (timeMode="created") or the modification time (timeMode="modified"). Default is "created". 2. from: defines the start of the time range. 3. to: defines the end of the time range.
| videoId and videoIdMode      | optional     |Searches for assets that match the given videoId. The videoIdMode defines the behavior: 1. exact: the Video ID must be exactly the given string. 2. contains: the Video ID must contain the given string.
| multiLink      | optional     |Boolean flag. If given, returns only assets that are in more than one folder (multiLink=true), or only assets that are only in a single folder (multiLink=false).
| oneLinkOnly      | optional     |Boolean flag, only for pa:advanced-item-search. It defines the result for matching assets that are linked in multiple folders: 1. false: returns all links, including multiple links to the same asset in different folders. 2. true: returns exactly one link for each returned asset.
| attributes      | optional     |A list of attributes to return for each asset. If not given, the result contains the values of all attributes.

## Search for assets in CTMS

Searches for assets in the given folder and its sub folders that match the given conditions. The result is a HAL resource with embedded [aa:asset](https://developer.avid.com/ctms/api/aa/linkrels/asset.html) links.

###### Steps:
1.  Use the cached CTMS Registry information or fetch it as shown in Using the CTMS API.
2. Find the link search:searches for the  Avid Production Management and call HTTP GET on it.
3. Make an HTTP POST request to the link pa:advanced-asset-search:
    - The request body is a search request as documented above.
    - Optionally, you can set the URI query parameter limit to define a maximum number of results. In any way, the service imposes a maximum number of returned assets to avoid overloading the system.

The response is a HAL resource with:
    - `An optional boolean property more-results`. It is returned with value "true" if there are more search results than requested with limit or more than the service allows as a maximum number of results.
    - `An embedded list of [aa:asset](https://developer.avid.com/ctms/api/aa/linkrels/asset.html) resources` with the matching assets.
        - Each may contain an embedded [aa:attributes](https://developer.avid.com/ctms/api/aa/linkrels/attributes.html) resource with either the requested attributes (via the property attributes in the search request) or a default list of attributes.

Example response with one asset (query parameter ?limit=1), abbreviated:

    ```
    {
    "more-results": true,
    "_links": { ... },
    "_embedded": {
        "aa:asset": [
        {
            "base": {
            "systemID": "E75274DF-BFE6-46CD-BA52-FB58CA0134F2",
            "systemType": "avid-pmplus",
            "id": "060a2b340101010101010f0013-000000-1330fb24616e411c-8748d585a9ff-48bd",
            "type": "masterclip"
            },
            "common": {
            "name": "My test asset",
            ...
            },
            "_links": { ... },
            "_embedded": {
            "aa:attributes": {
                "editRate": "25/1",
                "dropFrame": false,
                "attributes": [
                {
                    "name": "com.avid.workgroup.Property.System.Tracks",
                    "value": "V1 A1-2",
                    "type": "string",
                    "value-labels": {
                    "en": "V1 A1-2"
                    }
                }
                ],
                "_links": { ... }
            }
            }
        }
        ]
    }
    }
    ```
#### How to use this collection:
This collection involves the process of following the above steps, as provided in the summary, in your postman application.
Open your postman, import the collection "Search/CTMS Search Asset.postman_collection.json", and follow the steps as given below:

###### Postman API Calls
(Hit Send on the "ROPC Login" API call to login in the system. View the project-level ReadMe to understand how it works.)

> **GET** 1_CTMS Registry information: avid.ctms.registry
- This GET call hits the service roots URL for CTMS registry, fetching the resources, systems and the links associated to the system.
- In the **Scripts** section: We check if the  Avid Production Management is avaialable with the registry. If yes, we fetch "search:searches" link present inside the "resources", and store the variable globally as selected_system_searchSearchesHref.

> **GET** 2 search searches
- Hitting the above fetched selected_system_searchSearchesHref, to get the search link for the given system.
- In the **Scripts** section: From the response, we fetch the "pa:advanced-asset-search", which is used to get the link to search an asset in the system, and store it globally as selected_system_paAdvancedAssetSearchHref.

> **POST** 3 advanced asset search
- Hitting the above selected_system_paAdvancedAssetSearchHref URL, to fetch result of the search URL.

    <mark>🔶 At this step, you need to insert the appropriate **folder, text, type etc.** in the request body.</mark>

#### Precautions/Recommendations:
- Please **select and put** the right asset/masterclip IDs in the environment required for this example.


***
## Search for asset links in CTMS

Searches for asset links in the given folder and its sub folders that match the given conditions. The result is a HAL resource with embedded [loc:item](https://developer.avid.com/ctms/api/loc/linkrels/item.html) links, which again contain embedded loc:referenced-object links with information about the assets.

###### Steps:
1. Use the cached CTMS Registry information or fetch it as shown in Using the CTMS API.
2. Find the link search:searches for the  Avid Production Management and call HTTP GET on it.
3. Make an HTTP POST request to the link pa:advanced-item-search:
    - The request body is a search request as documented above.
    - Optionally, you can set the URI query parameter limit to define a maximum number of results. In any way, the service imposes a maximum number of returned asset links to avoid overloading the system. 

The response is a HAL resource with:

- An optional boolean property more-results. It is returned with value "true" if there are more search results than requested with limit or more than the service allows as a maximum number of results.
- An embedded list of [loc:item](https://developer.avid.com/ctms/api/loc/linkrels/item.html) resources with the matching asset links.
    - Each contains an embedded loc:referenced-object resource, which has the exact same structure as an  [aa:asset](https://developer.avid.com/ctms/api/aa/linkrels/asset.html) resource, with information about the asset.
        - Each of those again may contain an embedded [aa:attributes](https://developer.avid.com/ctms/api/aa/linkrels/attributes.html) resource with either the requested attributes (via the property attributes in the search request) or a default list of attributes. 

Example with one asset, abbreviated:

    ```
    {
    "more-results": true,
    "_links": { ... },
    "_embedded": {
        "loc:item": [
        {
            "base": {
            "systemID": "E75274DF-BFE6-46CD-BA52-FB58CA0134F2",
            "systemType": "avid-pmplus",
            "id": "/Projects/Example/060a2b340101010101010f0013-000000-1330fb24616e411c-8748d585a9ff-48bd",
            "type": "folder-item"
            },
            "common": {
            "name": "My test asset",
            ...
            },
            "_links": { ... },
            "_embedded": {
            "loc:referenced-object": {
                "base": {
                "systemID": "E75274DF-BFE6-46CD-BA52-FB58CA0134F2",
                "systemType": "avid-pmplus",
                "id": "060a2b340101010101010f0013-000000-1330fb24616e411c-8748d585a9ff-48bd",
                "type": "masterclip"
                },
                "common": {
                "name": "My test asset",
                ...
                },
                "_links": { ... },
                "_embedded": {
                "aa:attributes": {
                    "editRate": "25/1",
                    "dropFrame": false,
                    "attributes": [
                    {
                        "name": "com.avid.workgroup.Property.System.Tracks",
                        "value": "V1 A1-2",
                        "type": "string",
                        "value-labels": {
                        "en": "V1 A1-2"
                        }
                    }
                    ],
                    "_links": { ... }
                }
                }
            }
            }
        }
        ]
    }
    }
    ```

#### How to use this collection:
This collection involves the process of following the above steps, as provided in the summary, in your postman application.
Open your postman, import the collection "Search/CTMS Search for Asset Link.postman_collection.json", and follow the steps as given below:

###### Postman API Calls
(Hit Send on the "ROPC Login" API call to login in the system. View the project-level ReadMe to understand how it works.)

> **GET** 1_CTMS Registry information: avid.ctms.registry
- This GET call hits the service roots URL for CTMS registry, fetching the resources, systems and the links associated to the system.
- In the **Scripts** section: We check if the  Avid Production Management is avaialable with the registry. If yes, we fetch "search:searches" link present inside the "resources", and store the variable globally as selected_system_searchSearchesHref.

> **GET** 2 search searches
- Hitting the above fetched selected_system_searchSearchesHref, to get the search link for the given system.
- In the **Scripts** section: From the response, we fetch the "pa:advanced-item-search", which is used to get the link to search an asset in the system, and store it globally as selected_system_paAdvancedItemSearchHref.

> **POST** 3 advanced item search
- Hitting the above selected_system_paAdvancedAssetSearchHref URL, to fetch result of the search URL.

    <mark>🔶 At this step, you need to insert the appropriate **folder, text, type etc.** in the request body.</mark>

#### Precautions/Recommendations:
- Please **select and put** the right asset/masterclip IDs in the environment required for this example.