# Documentation Title: Restrictions

## Add Restrictions in CTMS

#### Summary:
The Interplay Web Services method AddRestrictions adds restrictions to a masterclip. A restriction is set for a range of frames with a comment describing the restriction.

###### Parameter:
- The MOB ID of the masterclip.
- An array of restrictions. For each:
    - The start frame (zero-based).
    - The duration in frames.
    - A comment string.

###### Steps:
1. Use the cached CTMS Registry information or fetch it as shown in Using the CTMS API.
2. Find the link [aa:asset-by-id](https://developer.avid.com/ctms/api/aa/linkrels/asset-by-id.html) for the  Avid Production Management. The "href" is an  URI template.
    1. Set the URI template variable "id" to the ID of the masterclip and expand the URI template.
    2. Make an HTTP GET request to get the [aa:asset](https://developer.avid.com/ctms/api/aa/linkrels/asset.html) resource for the masterclip.
3. Call HTTP PATCH on the aa:update-time-based link with a JSON message body like this:

```
{
  "layers": [
    {
      "name": "restrictions",
      "segments": [
        {
          "id": null,
          "start": 10,
          "duration": 5,
          "attributes": [
            {
              "name": "comment",
              "value": "Access restricted"
            }
          ],
          "userName": "johndoe"
        }
      ]
    }
  ]
}
```

4. The response is a JSON with similar structure and in the same order for the segments where the id property is filled with the generated restriction ID.
The request body above contains a layer named "restrictions". Each segment of this layer represents one restriction. It has the following properties:

| Segment property  | Description | 
| ------------- |:-------------:|
| id      | The restriction ID. Should be null to create a new restriction. If you use the ID of an existing restriction, the restriction is updated.     |
| start      | The start of the restriction (in frames). Same as InFrameNumber in IPWS.     |
| duration      | The duration of the restriction (in frames). Same as OutFrameNumber - InFrameNumber + 1 in IPWS.     |
| attributes      | Contains an attribute named “comment” with the comment for the segment. Via CTMS, you can also set the “color” attribute of the restriction.     |
| userName      | The username for the segment. The value must be given!     |

#### How to use this collection:
This collection involves the process of following the above steps, as provided in the summary, in your postman application.
Open your postman, import the collection "Restrictions/CTMS Add Restrictions.postman_collection.json", and follow the steps as given below:

###### Postman API Calls
(Hit Send on the "ROPC Login" API call to login in the system. View the project-level ReadMe to understand how it works.)

> **GET** 1_CTMS Registry information: avid.ctms.registry
- This GET call hits the service roots URL for CTMS registry, fetching the resources, systems and the links associated to the system.
- In the **Scripts** section: We check if the  Avid Production Management is avaialable with the registry. If yes, we fetch "[aa:asset-by-id](https://developer.avid.com/ctms/api/aa/linkrels/asset-by-id.html)" link present inside the "resources", and store the variable globally as selected_system_aaAssetByIdHref.

    <mark>🔶 At this step, you need to insert the appropriate **master clip ID** in the environment variable named: masterClipId</mark>

> **GET** 2_aa asset by id
- Hitting the above fetched selected_system_aaAssetByIdHref, to get the asset by id.
- In the **Scripts** section: From the response, we fetch the "aa:update-time-based", which is used to get time based referernce for the given asset, that can be then used to add a restriction, and store it globally as selected_system_aaUpdateTimeBased.

> **PATCH** 3 update time based
- Hitting the above selected_system_aaUpdateTimeBased URL, to set the asset restrictions.
- In the **Body** section: Add request body with the "layers" and name as restrictions to add restrictions for the given asset by hitting the PATCH request.

#### Precautions/Recommendations:
- Please **select and put** the right asset/masterclip IDs in the environment required for this example.

***
## Get Restrictions

#### Summary:
The Interplay Web Services method GetRestrictions returns time ranges of an asset that have usage restrictions.

> In CTMS, you must query the restrictions one-by-one for each masterclip. There is no bulk call for that function.

###### Parameters
- The MOB ID of the asset.

###### Steps
1. Use the cached CTMS Registry information or fetch it as shown in Using the CTMS API.
2. Find the link [aa:asset-by-id](https://developer.avid.com/ctms/api/aa/linkrels/asset-by-id.html) for the  Avid Production Management. The "href" is an   URI template.
    1. Set the URI template variable "id" to the ID of the asset and expand the URI template.
    2. Add the query parameters "?embed=time-based&layers=restrictions".
    3. Make an HTTP GET request to get the [aa:asset](https://developer.avid.com/ctms/api/aa/linkrels/asset.html) resource for the asset with an embedded aa:time-based resource with a layer "restrictions" that contains an array of segments with the restrictions of the asset.
    
    ```
    {
    "assetDuration": 217,
    "editRate": "24000/1001",
    "dropFrame": false,
    "offsetToAssetStart": 0,
    "videoStartTC": "18:17:29:02",
    "_links": { }
    "layers": [
        {
        "name": "restrictions",
        "segments": [
            {
            "id": "060a2b340101010101010f0013-000000-c39522ac781a4136-bb1dea7ebcf1-ac77",
            "start": 10,
            "duration": 6,
            "attributes": [
                {
                "name": "comment",
                "value": "Use of swear words"
                },
                {
                "name": "color",
                "value": "WHITE"
                },
                {
                "name": "modified",
                "value": "2024-04-30T14:25:27Z"
                }
            ],
            "userName": "johndoe"
            }
        ]
        }
    ]
    }
    ```
 
#### Mapping of IPWS properties to CTMS properties

| IPWS property  | CTMS property | 
| ------------- |:-------------:|
| Comment      | Value of the attribute with name “comment”     |
| InFrameNumber      | **start**: Start frame for the restriction    |
| OutFrameNumber      | **duration**: The duration of the restriction in frames. The last frame of the restriction can be calculated like this: **start + duration - 1**    |
| Username      | **userName**: Login name of the user that created the restriction.    |
| < not available>      | CTMS returns three additional properties: **“id”**: the ID of the restriction. Attribute **“color”**: a restriction color that can be set and displayed in Interplay Access. Attribute **“modified”**: the last modification time of the restriction.     |

#### How to use this collection:
This collection involves the process of following the above steps, as provided in the summary, in your postman application.
Open your postman, import the collection "Restrictions/CTMS Get Restrictions.postman_collection.json", and follow the steps as given below.

###### Postman API Calls
(Hit Send on the "ROPC Login" API call to login in the system. View the project-level ReadMe to understand how it works.)

> **GET** 1_CTMS Registry information: avid.ctms.registry
- This GET call hits the service roots URL for CTMS registry, fetching the resources, systems and the links associated to the system.
- In the **Scripts** section: We check if the  Avid Production Management is avaialable with the registry. If yes, we fetch "[aa:asset-by-id](https://developer.avid.com/ctms/api/aa/linkrels/asset-by-id.html)" link present inside the "resources", and store the variable globally as selected_system_aaAssetByIdHref.

    <mark>🔶 At this step, you need to insert the appropriate **master clip ID** in the environment variable named: masterClipId</mark>

> **GET** 2_aa asset by id
- Hitting the above fetched selected_system_aaAssetByIdHref, to get the asset by id.
- In the **Params** section: Enter the key value pairs as below:
    - embed: time-based
    - layers: restrictions

This will fetch you the restrictions associated to the given asset in the response.

#### Precautions/Recommendations:
- Please **select and put** the right asset/masterclip IDs in the environment required for this example.
