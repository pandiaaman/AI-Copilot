# Documentation Title: Get File Details

## Get file details for a masterclip in CTMS

#### Summary:
The Interplay Web Services method GetFileDetails returns information about the media files used by a masterclip.

###### Parameter:
- The MOB ID of the masterclip.

###### Steps:
1. Use the cached CTMS Registry information or fetch it as shown in Using the CTMS API.
2. Find the link aa:asset-by-id for the  Avid Production Management. The "href" is a URI template.
   1. Set the URI template variable "id" to the ID of the asset and expand the URI template.
   2. Make an HTTP GET request to get the aa:asset resource for the asset
3. Make an HTTP GET request to the pa:asset-medias link to get the information about the files used by the masterclip in the property "media-items". 

 Example response (abbreviated):
```
   {
   "media-items": [
   {
   "name": "060a2b340101010101010f0013-000000-9a855fb4b5e900a5-5d76f1bbe9eb-b3a6",
   "track": "A1",
   "online": "true",
   "filePath": "//somehost/.../2013060413a018c27d65.mxf",
   "type": "filemob",
   "essenceType": "NATIVE",
   "createdBy": "Administrator",
   "format": "PCM",
   "size": "2816"
   },
   {
   "name": "060a2b340101010101010f0013-000000-9b855fb4b5e900a5-eaaddb3c870c-3e99",
   "track": "A2",
   "online": "true",
   "filePath": "//somehost/.../2013060413a028c26f7f.mxf",
   "type": "filemob",
   "essenceType": "NATIVE",
   "createdBy": "Administrator",
   "format": "PCM",
   "size": "2816"
   },
   {
   "name": "060a2b340101010101010f0013-000000-9a855fb4b5e900a5-8be8d6ae5290-49f1",
   "track": "V1",
   "online": "true",
   "filePath": "//somehost/.../2013060413v018c21529.mxf",
   "type": "filemob",
   "essenceType": "NATIVE",
   "createdBy": "Administrator",
   "format": "XDCAM-HD 50mbps 1080p 25",
   "size": "141824"
   }
   ]
   }
```

#### How to use this collection:
This collection involves the process of following the above steps, as provided in the summary, in your postman application.
Open your postman, import the collection "Get File Details\CTMS Get File Details.postman_collection.json", and follow the steps as given below:

###### Postman API Calls
(Hit Send on the "ROPC Login" API call to get logged in the system. View the project-level ReadMe to understand how it works.)

> **GET** 1_avid.ctms.registry -> getServiceRoots -> set assetById from global var master_clip_id
- This GET call hits the service roots URL for CTMS registry, fetching the resources, systems and the links associated to the system.
- In the **Scripts** section: We check if the  Avid Production Management is available with the registry. If yes, we fetch "[aa:asset-by-id]"(https://developer.avid.com/ctms/api/aa/linkrels/asset-by-id.html)" link present inside the "resources" for 'selected_system' systemType, and store the variable globally as "selected_system_assetByIdHref".
  Here we also replace "id" parameter in the url with the ID of the masterclip.

    <mark>🔶 At this step, you need to insert the appropriate **master_clip_id** in the environment variable.</mark>

> **Get** 2_asset-by-id -> asset-medias
- Hitting the above fetched 'selected_system_assetByIdHref', to get asset medias link relation for the given asset.
- In the **Scripts** section: From the response, we fetch the "[pa:asset-medias]" href, which will be used to get the information about the files used by the masterclip in the property "media-items", and store it globally as "selected_system_assetmedias".

> **GET** 3_asset-medias -> media-items
- Hitting the above "selected_system_assetmedias" URL to get the asset media information.
  The response contains information about the files used by the masterclip in the property "media-items".


#### Precautions/Recommendations:
- Please **select and put** the right **master_clip_id** in the environment required for this example.