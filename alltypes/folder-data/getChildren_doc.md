# Documentation Title: Get Children

## Getting the folder content in CTMS

#### Summary:
The Interplay Web Services method GetChildren returns the content of a folder. There are a number of parameters for this function:
* IncludeMOBs: defines if Avid assets are returned or not. Default: true.
* IncludeFolders: defines if folders are returned or not. Default: true.
* IncludeRefAssets: defines if referenced assets are returned or not. Default: false. If you store, for example, a sequence in a folder, then the masterclips that are used in the sequence are also added silently as "referenced assets" to the folder.
* ReturnAttributes: defines attributes to return for each item in the folder. If not given, a default set of attributes are returned.
* Filter: regular expression filter on the names of items.

###### Parameter:
- The ID of the folder, consisting of the path with leading and trailing slashes. Example: "/Projects/Example/". 
- Optional: a list of attributes to get.
- Optional: a filter for the items to return.

###### Steps:

1. Use the cached CTMS Registry information or fetch it as shown in Using the CTMS API.
2. Find the link [loc:item-by-id](https://developer.avid.com/ctms/api/loc/linkrels/item-by-id.html) for the  Avid Production Management. The "href" is an RFC-6570  URI template.
   1. Set the URI template variable "id" to the ID of the folder and expand the URI template. 
   2. Add the query parameter "attributes=*" to get all attributes, or "attributes=a,b,c" to get a specific list of attributes.
   3. Add the query parameter "filter" to control which items to return. The value is a comma-separated list of the following values:
        - item-type-folder: return folders.
        - item-type-asset: return assets.
        - item-type-referenced-asset: return referenced assets. 
      If filter is not given, the method returns folders and asset, similar to "filter=item-type-folder,item-type-asset". 
   4. Make an HTTP GET call on the resulting URI. The result is the loc:item resource for the requested folder with an embedded loc:collection resource having an embedded list with the first page of loc:item resources for the items in the folder. See below for an example.
3. The [loc:collection](https://developer.avid.com/ctms/api/loc/resources/collection.html) resource uses paging. To get all items, find the "next" link in it. As long as the "next" link exists, add the same query parameters as above and use HTTP GET to get the next page.

<mark> CTMS doesn't support a regular expression as filter for items to return. You must apply the filter on the client side. </mark>


### Structure of the loc:item response

The result of step 2.4 above has the following structure:

* base, common, and attributes: information for the requested folder.
* _embedded 
     * loc:collection: the collection of items in the folder
       * paging: information about the items that are returned by this call, and the total number of items in the folder
       * _links: HAL links of the collection
            * next: link to the next page of results. Only present if there are more pages.
       * _embedded:
            * loc:item: embedded array of loc:item resources for the items in the collection. This can be either sub folders or assets that are in the requested folder. 
                * base: ID of the item in the folder
                * common: common attributes like display name for the item.
                * attributes (only for sub folders): user and system attributes of the sub folder
                * _links: links of the loc:item. If it contains a loc:collection link, the item is a folder.
                * _embedded (only for assets)
                    * loc:referenced-object: the aa:asset resource of the asset in the folder
                        * base: ID of the asset
                        * common: common attributes like display name for the asset
                        * _embedded
                            * aa:attributes: user and system attributes for an asset.
                          
When following the "next" link of the collection, the structure is the same as the one for the embedded loc:collection resource above.

Abbreviated example for the result with a first page with two items, an asset and a sub folder:

```
{
"base": {...},
"common": {...},
"_links": {...},
"_embedded": {
"loc:collection": {
"paging": {
"limit": 2,
"offset": 0,
"elements": 2,
"totalElements": 7
},
"_links": {
"next": {
"href": "https://..."
},
...
},
"_embedded": {
"loc:item": [
{
"base": {
"systemID": "E75274DF-BFE6-46CD-BA52-FB58CA0134F2",
"systemType": "avid-pmplus",
"id": "/Catalogs/IPWS/060a2b340101010101010f0013-000000-00c5dfe08ab0de80-060e2b347f7f-2a80",
"type": "folder-item"
},
"common": {
"creator": "svceditor",
"created": "2017-03-16T16:01:14Z",
"name": "Example asset"
},
"_links": {...},
"_embedded": {
"loc:referenced-object": {
"base": {
"systemID": "E75274DF-BFE6-46CD-BA52-FB58CA0134F2",
"systemType": "avid-pmplus",
"id": "060a2b340101010101010f0013-000000-00c5dfe08ab0de80-060e2b347f7f-2a80",
"type": "masterclip"
},
"common": {
"creator": "svceditor",
"created": "2017-03-16T16:01:14Z",
"name": "Example asset"
},
"_links": {...},
"_embedded": {
"aa:attributes": {
"attributes": [
{
"name": "com.avid.workgroup.Property.System.Format",
"value": "1080i/50",
"type": "string"
}
],
"_links": {...}
}
}
}
}
},
{
"base": {
"systemID": "E75274DF-BFE6-46CD-BA52-FB58CA0134F2",
"systemType": "avid-pmplus",
"id": "/Catalogs/IPWS/A sub folder/",
"type": "folder"
},
"common": {
"path": "/Catalogs/IPWS/A sub folder/",
"creator": "svcadmin",
"created": "2024-04-16T13:01:42.204Z",
"name": "A sub folder",
"modified": "2024-04-16T13:01:42.204Z"
},
"attributes": [
{
"name": "Created By",
"value": "svcadmin",
"type": "string"
}
],
"_links": {...}
}
]
}
}
}
}

```

#### How to use this collection:
This collection involves the process of following the above steps, as provided in the summary, in your postman application.
Open your postman, import the collection "Get Children\ Avid Production Management CTMS-Get Children.postman_collection.json", and follow the steps as given below:

###### Postman API Calls
(Hit Send on the "ROPC Login" API call get logged in the system. View the project-level ReadMe to understand how it works.)

> **GET** 1_avid.ctms.registry -> getServiceRoots -> set locItemById from global folderID
- This GET call hits the service roots URL for CTMS registry, fetching the resources, systems and the links associated to the system.
- In the **Scripts** section, we check if the  Avid Production Management is available with the registry. If yes, we fetch "[loc:item-by-id](https://developer.avid.com/ctms/api/loc/linkrels/item-by-id.html)" link present inside the "resources" for "avid-pmplus" systemType, and store the variable globally as **selected_system_locItemByIdHref**.
  Here we also replace "id" parameter in the url with user input "folder_path".

    <mark>🔶 At this step, you need to insert the appropriate **folder_path** in the environment variable.</mark>

> **Get** 2.1_Get Loc:item by ID(w/o filter)
- Hitting the above fetched **selected_system_locItemByIdHref**, to get ["loc:item"] resource for a folder.
  The result is the loc:item resource for the requested folder with an embedded loc:collection resource having an embedded list with the first page of loc:item resources for the items in the folder.

> **Get** 2.2_Get Loc:items by ID(with attr)
- Hitting the above **selected_system_locItemByIdHref** URL with **attributes** as a query parameter.
- Here we pass **attributes** as a query parameter. e.g, "attributes = Name,SMOT"
  The result is the loc:item resource for the requested folder with an embedded loc:collection resource with selected list of attributes in the "attributes" array.

> **Get** 2.3_Get Loc:items by ID(with filter)
- Hitting the above "selected_system_locItemByIdHref" URL with **filter** as a query parameter.
- Here we pass **filter** as a query parameter to control which items to return. Below are values we can pass in a filter.
**   filter = item-type-folder (return folders) **
**   filter = item-type-asset  (return assets)  **
**   filter = item-type-referenced-asset (return referenced assets) **

The result is the filtered loc:item resource for the requested folder with an embedded loc:collection resource having an embedded list with the first page of loc:item resources for the items(children) in the folder.

#### Precautions/Recommendations:
- Please select and put the right **folder_path** in the environment required for this example.