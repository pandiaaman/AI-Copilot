# Documentation Title: Get Resolutions

#### Summary:
The Interplay Web Services method CreateShotlist is used to create a simple cuts-only shotlist. The method accepts the following parameters:

- ShotlistName: The name of the created shotlist.
- DestinationFolderURI: The URI of the target folder for the shotlist.
- StartTimecode: The  SMPTE timecode of the start of the timeline.
- ShotlistMobID: The MOB ID for the created shotlist. If not given, the service will assign a new MOB ID.
- ShotlistElements: the elements to be put on the timeline of the shotlist. Each element consists of:
    - InterplayURI: the URI of a masterclip or subclip used for the element.
    - A range within the masterclip or subclip:
        - InTimecode: in-point in SMPTE timecode format.
        - OutTimecode: out-point in SMPTE timecode format.
        - Duration: duration of the element.
        - Only one of OutTimecode or Duration should be given.
    - Locators: locators to set, relative to the start of the range.
- Attributes: attributes to set for the shotlist.
- Locators: locators to set, relative to the start of the shotlist timeline.

> All masterclips and subclips used in the shotlist must have the same framerate.

- Locators have the following properties:

    - The position of the locator is defined by one of two properties:
        - FrameNumber: frame number, either relative to the start of the shotlist (for the top-level locators), or relative to the start of the element range (for the locators in an element).
        - Timecode: SMPTE timecode for the position of the locator, either on the shotlist timeline (for the top-level locators), or on the masterclip or subclip timeline (for the locators in an element).
    - Comment: comment on the locator.
    - Color: color of the locator.
    - Username: creator of the locator.
All locators are set on the V1 track of the shotlist.

## Creating a shotlist in CTMS

###### Parameter:
- The ID of the target folder.
- An XMD document with:
    - The name of the shotlist.
    - Optional: the start timecode for the shotlist in SMPTE format (HH:MM:SS:FF).
    - The elements on the timeline. Each element consists of:
        - The asset ID of a masterclip or subclip
        - The range given as in and out points.
        - An optional comment for the element.
    - See below for detailed information about creating an XMD document.

###### Steps:
1. Use the cached CTMS Registry information or fetch it as shown in Using the CTMS API.
2. Find the link aa:assets for the  Avid Production Management and call HTTP GET on it.
3. Make an HTTP POST request to the link aa:create-xmd-timeline.
    1. Set the query parameter "type" to "shotlist".
    2. Set the query parameter "location" to the ID of the target folder.
    3. Example (with proper URL encoding for the slashes in the folder ID): ?type=shotlist&location=%2FProjects%2FSomeFolder%2F
    4. The request body is the XMD document for the shotlist. See below for details and an example.

The response is a JSON object with two properties, "aa:asset" and "loc:item", both in the same format as the response for an item of a bulk call (see Bulk calls in CTMS for details, here abbreviated):

    Example: 

    ```
    {
    "aa:asset": {
        "success": true,
        "data": {
        "base": {
            "systemID": "E75274DF-BFE6-46CD-BA52-FB58CA0134F2",
            "systemType": "avid-pmplus",
            "id": "060a2b340101010101010f0013-000000-0b312000082d00ac-060e2b347f7f-d080",
            "type": "sequence"
        },
        "common": {
            "name": "New shotlist",
            ...
        },
        "_links": { ... }
        }
    },
    "loc:item": {
        "success": true,
        "data": {
        "base": {
            "systemID": "E75274DF-BFE6-46CD-BA52-FB58CA0134F2",
            "systemType": "avid-pmplus",
            "id": "/Catalogs/IPWS//060a2b340101010101010f0013-000000-0b312000082d00ac-060e2b347f7f-d080",
            "type": "folder-item"
        },
        "common": {
            "name": "New shotlist",
            ...
        },
        "_links": { ... },
        "_embedded": {
            "loc:referenced-object": { ... }
        }
        }
    }
    }
    ```

The property [aa:asset](https://developer.avid.com/ctms/api/aa/linkrels/asset.html) contains the information about the created sequence. The format is the same as in the response for bulk calls with the sub properties:

1. success: true if the sequence was created successfully, false if not.
2. data: in case of success, the property contains the [aa:asset](https://developer.avid.com/ctms/api/aa/linkrels/asset.html) resource of the created subclip, including the MOB ID in the property "id" in "base".
3. httpStatus, errorCode and errorMessage: in case of an error.

The property [loc:item](https://developer.avid.com/ctms/api/loc/linkrels/item.html) contains information about the created asset link in the target folder. The format is the same as above, only with the [loc:item](https://developer.avid.com/ctms/api/loc/linkrels/item.html) resource of the created sequence in the data property in case of success.

> You can use the link aa:update-asset in the returned [aa:asset](https://developer.avid.com/ctms/api/aa/linkrels/asset.html) resource to set common attributes and user attributes of the duplicated asset. See "SetAttributes via CTMS" for examples.

> You can use the link aa:update-time-based in the returned [aa:asset](https://developer.avid.com/ctms/api/aa/linkrels/asset.html) resource to set markers. See "SaveUMIDLocators via CTMS" for details. The marker positions in CTMS are positions on the sequence timeline. The locators in the elements in the IPWS call must be re-calculated to the corresponding positions in the shotlist timeline.

## Creating an XMD document for a simple shotlist
The XMD document must be in the format as shown in this example:

```
{
  "timeline": {
    "version": 4,
    // Name of the shotlist:
    "name": "My new shotlist",
    // Start timecode of the shotlist:
    "stampTimecode": "01:00:00:00",
    "tracks": [
      {
        "segments": [
          {
            "mob": {
              // asset ID of referenced masterclip or subclip
              "id": "060a2b340101010101010f0013-000000-6dda7dad08c24cfd-b581d7f05b5b-51fb"
            },
            "position": {
              "trackIn": -1,
              "trackOut": -1,
              // in and out point of the segment in the masterclip or subclip 
              "in": 5,
              "out": 12
            },
            // comment or title of the segment
            "name": "The referenced master clip."
          },
          ...   // more segments in the shotlist
        ]
      }
    ]
  }
}
```

###### In and out points for segments

In CTMS, the segment ranges use frame numbers instead of SMPTE timecodes as in IPWS.

For segments that reference a masterclip, you can calculate the frame numbers like this:
1. Use [aa:asset-by-id](https://developer.avid.com/ctms/api/aa/linkrels/asset-by-id.html) in the CTMS Registry to query the [aa:asset](https://developer.avid.com/ctms/api/aa/linkrels/asset.html) resource for the masterclip.
2. Calculate the difference between the in or out points to the value of the common attribute "startTC".

For subclips, you must re-calculate the in and out points to the original masterclip:
1. Use [aa:asset-by-id](https://developer.avid.com/ctms/api/aa/linkrels/asset-by-id.html) in the CTMS Registry to query the [aa:asset](https://developer.avid.com/ctms/api/aa/linkrels/asset.html) resource for the subclip.
2. Call GET on relations:relations with query parameter "?relationtypes=masterclip.forward to find the ID of the masterclip from which the subclip was created. The result is a relations:relations resource that should contain only a single embedded relation:

```
{
  "_embedded": {
    "relations:relation": [
      {
        "relationType": "masterclip.forward",
        "relatedEntity": {
          "id": "060a2b340101010101010f0013-000000-6dda7dad08c24cfd-b581d7f05b5b-51fb",
          "kind": "aa",
          "type": "masterclip"
        },
        "_links": {
          "relations:related-entity": {
            "href": "https://..."
          }
        }
      }
    ]
  }
}
```

3. Call GET on the link relations:related-entity to get the [aa:asset](https://developer.avid.com/ctms/api/aa/linkrels/asset.html) resource of the original masterclip.
4. Calculate the difference between the in or out points to the value of the common attribute "startTC" of the masterclip.

#### How to use this collection:
This collection involves the process of following the above steps, as provided in the summary, in your postman application.
Open your postman, import the collection "Shotlist/CTMS Create Shotlist.postman_collection.json", and follow the steps as given below:

###### Postman API Calls
(Hit Send on the "ROPC Login" API call to login in the system. View the project-level ReadMe to understand how it works.)

> **GET** 1_CTMS Registry information: avid.ctms.registry
- This GET call hits the service roots URL for CTMS registry, fetching the resources, systems and the links associated to the system.
- In the **Scripts** section: We check if the  Avid Production Management is avaialable with the registry. If yes, we fetch "aa:assets" link present inside the "resources", and store the variable globally as selected_system_aaAssetsHref.

> **GET** 2_aa assets
- Hitting the above fetched selected_system_aaAssetsHref, to get the assets information for the system.
- In the **Scripts** section: From the response, we fetch the "aa:create-xmd-timeline", which is used to create the xmd timeline for creation of shotlist, and store it globally as selected_system_aaCreateXmdTimelineHref.

> **POST** 3 create xmd timeline
- Hitting the above selected_system_aaCreateXmdTimelineHref URL, fetch the resolutions associated to an asset, in this case, the master clip.
- In the **Body** section: Add the request body with "timeline" as mentioned above in the summary tab. Make the POST call to create the shotlist.

#### Precautions/Recommendations:
- Please **select and put** the right asset/masterclip IDs in the environment required for this example.