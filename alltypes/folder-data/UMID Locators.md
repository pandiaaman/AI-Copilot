# Documentation Title: UMID Locators

## Add and update markers in CTMS

#### Summary:
The Interplay Web Services method SaveUMIDLocators adds and updates markers (also known as "locators") on an asset. A marker is a marked position on a track of the timeline with a comment and a color.

###### Parameter:
- The MOB ID of the asset. 
- Array of markers to add or update.
  - To update a marker, you must pass in the ID of the marker.
  - To add a marker, omit the ID in the request or set it to null.

###### Steps:
1. Use the cached CTMS Registry information or fetch it as shown in Using the CTMS API.
2. Find the link aa:asset-by-id for the  Avid Production Management. The "href" is an RFC-6570  URI template.
   1. Set the URI template variable "id" to the ID of the asset and expand the URI template.
   2. Make an HTTP GET request to get the aa:asset resource for the asset.
3. Call HTTP PATCH on the aa:update-time-based link with a request body with the markers to add and update. See below for details and an example. The call returns a similar structure as in the request body, with the created and added segments in the same order but with the new ID of the created segments.

Example request body:
```
{
  "layers": [
    {
      "name": "V1",
      "segments": [
        {
          "start": 2924,
          "duration": 1,
          "attributes": [
            {
              "name": "comment",
              "value": "Lionel Messi scores a goal"
            },
            {
              "name": "color",
              "value": "Blue"
            }
          ],
          "userName": "janesmith"
        },
        {
          "id": "060a2b340101010101010f0013-000000-b238acb69d8e412b-9a0d648212d4-cae4",
          "start": 3724,
          "duration": 1,
          "attributes": [
            {
              "name": "comment",
              "value": "Substitution: Andrés Iniesta for Lionel Messi"
            },
            {
              "name": "color",
              "value": "Black"
            }
          ],
          "userName": "janesmith"
        }
      ]
    }
  ]
}
 ```
> The request body is an aa:time-based resource. It contains a property "layers" with an array of layers. In  Avid Production Management, the "name" of the layer is the name of the track ("V1", "A1", "A2", ... ) for the markers. The property "segments" contains the markers in the form of segments.

A marker is a segment with the following properties:

| Segment property  |                                                   Description                                                    | 
| ------------- |:----------------------------------------------------------------------------------------------------------------:|
| id      |      The segment ID. SSet it to an existing marker ID to update the marker, or to null to add a new marker.      |
| start      |               The position of the marker. The value is a zero-based frame number within the video.               |
| duration      |                                   Always 1. Markers are set on a single frame.                                   |
| attributes      | Array of attributes to set for the marker: "comment": the text of the marker , "color": the color of the marker. |
| userName      |       The login name of the user that created a marker. The property is mandatory and must be set for  Avid Production Management.       |


#### How to use this collection:
This collection involves the process of following the above steps, as provided in the summary, in your postman application.
Open your postman, import the collection "UMID Locators\CTMS Add-Update Markers.postman_collection.json", and follow the steps as given below:

###### Postman API Calls
(Hit Send on the "ROPC Login" API call to login in the system. View the project-level ReadMe to understand how it works.)

> **GET** 1_avid.ctms.registry -> getServiceRoots (set assetById from global var asset_id)
- This GET call hits the service roots URL for CTMS registry, fetching the resources, systems and the links associated to the system.
- In the **Scripts** section: We check if the  Avid Production Management is available with the registry. If yes, we fetch "[aa:asset-by-id](https://developer.avid.com/ctms/api/aa/linkrels/asset-by-id.html)" link present inside the "resources", and store the variable globally as "selected_system_assetByIdHref".
  Here we also replace "id" parameter in the url with user input "asset_id".

  <mark>🔶 At this step, you need to insert the appropriate **asset_id** in the environment variable. </mark>

> **Get** 2_asset-by-id to update-time-based
- Hitting the above fetched "selected_system_assetByIdHref" url to get the link relation for "[aa:update-time-based]". Here we need to pass embed='time-based' in query param.
- In the **Scripts** section: From the response, we fetch the "[aa:update-time-based]", and store the variable globally as "selected_system_updateTimeBasedHref".

> **PATCH** 3_Add/Update Markers
- Hitting the above selected_system_updateTimeBasedHref URL, to add/update the markers on a layer in a given asset.
- In the **Body** section: Add request body with the layer name, segment id and segment attributes to be updated. If segmentId is not passed, then a new segment/marker with new segmentId is created under same layer.

Response contains a similar structure as in the request body, with the created and added segments in the same order but with the new ID of the created segments.

#### Precautions/Recommendations:
- Please **select and put** the right **asset_id** in the environment required for this example.

******

## Get markers in CTMS

#### Summary:
The Interplay Web Services method GetUMIDLocators returns the markers (also known as "locators") of an asset. A marker is a marked position on a track of the timeline with a comment and a color.

###### Parameter:
- The MOB ID of the asset.

###### Steps
1. Use the cached CTMS Registry information or fetch it as shown in Using the CTMS API.
2. Find the link aa:asset-by-id for the  Avid Production Management. The "href" is an RFC-6570  URI template.
    1. Set the URI template variable "id" to the ID of the asset and expand the URI template.
    2. Add the query parameter "?embed=time-based".
    3. Make an HTTP GET request to get the aa:asset resource for the asset with an embedded aa:time-based resource.

Example (abbreviated):
```

{
  "editRate": "24000/1001",
  "dropFrame": false,
  "offsetToAssetStart": 0,
  "videoStartTC": "18:17:29:02",
  "_links": { ... },
  "layers": [
    {
      "name": "V1",
      "segments": [
        {
          "id": "060a2b340101010101010f0013-000000-b238acb69d8e412b-9a0d648212d4-cae4",
          "start": 45,
          "duration": 1,
          "attributes": [
            {
              "name": "color",
              "value": "Green"
            },
            {
              "name": "comment",
              "value": "test comment 2: 2024-04-30 10:10:16.291"
            }
          ],
          "userName": "svcqa"
        }
      ]
    }
  ]
}
```
The resource may also contain the layer "restrictions" with restrictions on the asset. This layer can be ignored here.

#### How to use this collection:
This collection involves the process of following the above steps, as provided in the summary, in your postman application.
Open your postman, import the collection "UMID Locators\CTMS Get Markers.postman_collection.json", and follow the steps as given below.

###### Postman API Calls
(Hit Send on the "ROPC Login" API call to login in the system. View the project's ReadMe to understand how it works.)

> **GET** 1_avid.ctms.registry -> getServiceRoots (set assetById from global var asset_id)
- This GET call hits the service roots URL for CTMS registry, fetching the resources, systems and the links associated to the system.
- In the **Scripts** section: We check if the  Avid Production Management is available with the registry. If yes, we fetch "[aa:asset-by-id](https://developer.avid.com/ctms/api/aa/linkrels/asset-by-id.html)" link present inside the "resources", and store the variable globally as "selected_system_assetByIdHref".
  Here we also replace "id" parameter in the url with user input "asset_id".

  <mark>🔶 At this step, you need to insert the appropriate **asset_id** in the environment variable. </mark>

> **Get** 2_asset-by-id -> aa:time-based
- Hitting the above fetched "selected_system_assetByIdHref" url to get the link relation for "[aa:time-based]". Here we need to pass embed='time-based' in query param.
- In the **Scripts** section: From the response, we fetch the "[aa:time-based]", and store the variable globally as "selected_system_timeBasedHref".

> **GET** 3_Get Markers
- Hitting the above "selected_system_timeBasedHref" URL, to get all markers on a layer V1 on a given asset.

Response contains the layers with names like "V1", "V2", "A1", "A2" for each track of the asset that has markers. The property "segments" contains the information about the markers on each track.

#### Precautions/Recommendations:
- Please **select and put** the right **asset_id** in the environment required for this example.

******

## Remove Markers in CTMS

#### Summary:
The Interplay Web Services method RemoveUMIDLocators removes markers (also known as "locators") from an asset. A marker is a marked position on a track of the timeline with a comment and a color.

###### Parameter:
- The MOB ID of the asset.
- An array of marker IDs.

###### Steps

1. Use the cached CTMS Registry information or fetch it as shown in Using the CTMS API.
2. Find the link aa:asset-by-id for the  Avid Production Management. The "href" is an RFC-6570  URI template. 
   1. Set the URI template variable "id" to the ID of the asset and expand the URI template. 
   2. Make an HTTP GET request to get the aa:asset resource for the asset.
3. Find the aa:delete-time-based link in the aa:asset resource.
   1. Add query parameter "segmentids" with a comma-separated list of marker IDs you want to delete. 
   2. Call HTTP DELETE on the resulting URI to delete the segments with the given IDs in all layers.


#### How to use this collection:
This collection involves the process of following the above steps, as provided in the summary, in your postman application.
Open your postman, import the collection "UMID Locators\CTMS Remove UMID Locators.postman_collection.json" and follow the steps as given below.

###### Postman API Calls
(Hit Send on the "ROPC Login" API call to get logged in the system. View the project's ReadMe to understand how it works.)

> **GET** 1_avid.ctms.registry -> getServiceRoots (set assetById from global var asset_id)
- This GET call hits the service roots URL for CTMS registry, fetching the resources, systems and the links associated to the system.
- In the **Scripts** section: We check if the  Avid Production Management is available with the registry. If yes, we fetch "[aa:asset-by-id](https://developer.avid.com/ctms/api/aa/linkrels/asset-by-id.html)" link present inside the "resources", and store the variable globally as "selected_system_assetByIdHref".
  Here we also replace "id" parameter in the url with user input "asset_id".

  <mark>🔶 At this step, you need to insert the appropriate **asset_id** in the environment variable. </mark>

> **Get** 2_asset-by-id -> delete-time-based
- Hitting the above fetched "selected_system_assetByIdHref" url to get the link relation for "[aa:delete-time-based]". Here we need to pass embed='time-based' in query param.
- In the **Scripts** section: From the response, we fetch the "[aa:delete-time-based]", and store the variable globally as "selected_system_delete-time-based".

> **DELETE** 3_Delete Markers
- Hitting the above "selected_system_delete-time-based" URL, to delete the segments(markers) with the given IDs in all layers(tracks).
- Add query parameter "segmentids" with a comma-separated list of marker IDs you want to delete.

  <mark>🔶 At this step, you need to be careful about inserting  the appropriate **segmentids** in the parameter. If **segmentids** is passed as null or not passed, it will delete all the markers and restrictions on given asset.</mark>

```
Markers in MediaCentral | Production Management and MediaCentral |  Avid Production Management have unique IDs across all layers of time-based information. That's why it is sufficient to filter by segment IDs, meaning that the segments with the given IDs are deleted from all layers. For other products like, for example, MediaCentral | Asset Management, the segment IDs are only unique within a layer, but not across layers. A different segment in a different layer could have the same ID.
In that case you must combine the "segmentids" query parameter with the "layers" query parameter to identify a specific segment in a specific layer. **
```

#### Precautions/Recommendations:
- Please **select and put** the right **asset_id** in the environment required for this example.
- Make sure that you always provide the query parameter **segmentids** with a non-empty list of marker IDs! The query parameters for the aa:delete-time-based link work like a filter for the segments to be deleted. 
  **If you omit or mistype the query parameter, you will delete all markers and restrictions.**