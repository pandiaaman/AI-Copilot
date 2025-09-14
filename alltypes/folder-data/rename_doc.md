# Documentation Title: Rename

## Rename folder or an asset in CTMS

#### Summary:
The Interplay Web Services method Rename changes the name of an asset or a folder.

### Rename Folder

###### Parameter:
- The ID of the folder, consisting of the path with leading and trailing slashes. Example: "/Projects/Example/". 
- The new name.

###### Steps:
1. Use the cached CTMS Registry information or fetch it as shown in Using the CTMS API. 
2. Find the link loc:item-by-id for the  Avid Production Management. The "href" is an RFC-6570 URI template. 
   1. Set the URI template variable "id" to the ID of the folder and expand the URI template. 
   2. Make an HTTP GET request to get the loc:item resource of the folder.
3. Find the link loc:update-item.
   1. Make an HTTP PATCH request to the link with a loc:item resource that sets the common attribute "name" as request body.

Example:
```
{
"common": {
"name": "New name"
}
}
```

### Rename Asset

###### Parameter:
- The MOB ID of the asset 
- The new name.

###### Steps:
1. Use the cached CTMS Registry information or fetch it as shown in Using the CTMS API.
2. Find the link aa:update-asset-by-id for the  Avid Production Management. The "href" is an RFC-6570  URI template. 
   1. Set the URI template variable "id" to the ID of the masterclip and expand the URI template.
   2. Make an HTTP PATCH request with an aa:asset resource. Set the common attribute "name" to the new name. Example:

Example:
```
{
"common": {
"name": "New name"
}
}
```

#### How to use this collection:
This collection involves the process of following the above steps, as provided in the summary, in your postman application.
Open your postman, import the collection "Rename\CTMS Rename Folder-Asset.postman_collection.json", and follow the steps as given below:

###### Postman API Calls
(Hit Send on the "ROPC Login" API call get logged in the system. View the project-level ReadMe to understand how it works.)

> **GET** 1_CTMS Registry information: avid.ctms.registry
- This GET call hits the service roots URL for CTMS registry, fetching the resources, systems and the links associated to the system.
- In the **Scripts** section: 
  a. We check if the  Avid Production Management is available with the registry. If yes, we fetch "[loc:item-by-id](https://developer.avid.com/ctms/api/loc/linkrels/item-by-id.html)" link present inside the "resources" for "selected_system" systemType, and store the variable globally as "selected_system_locItemByIdHref".
  Here we also replace "id" parameter in the url with user input "folder_path".
  b. We check if the  Avid Production Management is available with the registry. If yes, we fetch "[aa:update-asset-by-id]"(https://developer.avid.com/ctms/api/aa/linkrels/update-asset-by-id.html)" link present inside the "resources" for "selected_system" systemType, and store the variable globally as "selected_system_updateAssetByIdHref".
  Here we also replace "id" parameter in the url with the ID of the masterclip.

    <mark>🔶 At this step, you need to insert the appropriate **folder_path** and **asset_id** in the environment variable.</mark>

> **Get** 2_loc:item-by-id -> update-item
- Hitting the above fetched 'selected_system_locItemByIdHref', to get ["loc:update-item"] resource for a folder.
- In the **Scripts** section: From the response, we fetch the "["loc:update-item"]", which will be used to rename a given folder, and store it globally as "selected_system_updateItemByIdHref".

> **PATCH** 3_Rename Folder
- Hitting the above "selected_system_updateItemByIdHref" URL, to update the name of a given input folder.
- In the **Body** section: Add request body with the common attribute "name" field to add new name for the folder to be renamed.
  The response contains a modified loc:item resource with a new ID  in the sub property "id" of property "base".

> **PATCH** 4_Rename Asset
- Hitting the above "selected_system_updateAssetByIdHref" URL fetched in step 1, to update the name of an asset for a given assetId.
- In the **Body** section: Add request body with the common attribute "name" field to add new name for an asset to be renamed.
  The response contains a modified loc:item resource with a new name in the sub property "name" of property "common".

#### Precautions/Recommendations:
- Please select and put the right **folder_path** and **asset_id** in the environment required for this example.