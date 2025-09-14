# Documentation Title: Headframe/Thumbnails

## Set HeadFrame/Thumbnails

#### Summary:
The Interplay Web Services method SetHeadframe sets the headframe (or "thumbnail") image for an asset.

###### Parameter:
- The MOB ID of the asset.
- The binary image.

###### Steps:
1. Use the cached CTMS Registry information or fetch it as shown in Using the CTMS API.
2. Find the link [aa:asset-by-id](https://developer.avid.com/ctms/api/aa/linkrels/asset-by-id.html) for the  Avid Production Management. The "href" is an   URI template.
    1. Set the URI template variable "id" to the ID of the asset and expand the URI template.
    2. Make an HTTP GET request to get the [aa:asset](https://developer.avid.com/ctms/api/aa/linkrels/asset.html) resource for the asset.
3. Find the [aa:set-thumb-command](https://developer.avid.com/ctms/api/aa/linkrels/set-thumb-command.html) link.
    1. Send the byte array of the image in the request body.
    2. Set the HTTP header “Content-Type: image/jpeg”
    3. Make an HTTP POST call to the link to start a long-running command that sets the thumbnail. The response is a command:command resource representing the long-running command. Example response (abbreviated):

```
{
  "version": "1.0",
  "command": {
    "lifecycle": "pending"
  },
  "_links": {
    "self": {
      "href": "https://..."
    }
  }
}
```

4. Poll the command status (with a small delay of, for example, 200 milliseconds between calls) by making an HTTP GET call to the "self" link until "lifecycle" in "command" is either "finished" or "error".
5. The result depends on the final value of the "lifecycle" property:
    1. “finished”: The thumbnail has been set successfully.
    2. “error”: The call failed. The response contains a property "error" within the "command" property with error details. See command:command for details.


#### How to use this collection:
This collection involves the process of following the above steps, as provided in the summary, in your postman application.
Open your postman, import the collection "HeadFrames or Thumbnails/CTMS Set Headframe.postman_collection.json", and follow the steps as given below:

###### Postman API Calls
(Hit Send on the "ROPC Login" API call to login in the system. View the project-level ReadMe to understand how it works.)

> **GET** 1_CTMS Registry information: avid.ctms.registry
- This GET call hits the service roots URL for CTMS registry, fetching the resources, systems and the links associated to the system.
- In the **Scripts** section: We check if the  Avid Production Management is avaialable with the registry. If yes, we fetch "[aa:asset-by-id](https://developer.avid.com/ctms/api/aa/linkrels/asset-by-id.html)" link present inside the "resources", and store the variable globally as selected_system_aaAssetByIdHref.

    <mark>🔶 At this step, you need to insert the appropriate **master clip ID** in the environment variable named: masterClipId</mark>

> **GET** 2_aa asset by id
- Hitting the above fetched selected_system_aaAssetByIdHref, to get the asset by id.
- In the **Scripts** section: From the response, we fetch the "[aa:set-thumb-command](https://developer.avid.com/ctms/api/aa/linkrels/set-thumb-command.html)", which is used to set the thumbnail information for the given asset, and store it globally as selected_system_aaSetThumbCommandHref.

> **POST** 3 set a thumbnail
- Hitting the above selected_system_aaSetThumbCommandHref URL, to set the thumbnail information.
- In the **Body** section: Select 'binary' as the input and select the thumbnail image of your choice. You can choose the file present in the /extras/ folder as well.
- The response starts a long running command that sets the thumbnail, with lifecyle initially as pending, and once completed, turns to finished.
- In the **Scripts** section: We fetch the "self" link from "_links", that point to the long running command and we can poll the command status using this link.

> **GET** 4 poll command status (pending/finished)
- Here we poll the status of the long running command that shows if the thumbnail has been set for the asset or not.


#### Precautions/Recommendations:
- Please **select and put** the right asset/masterclip IDs in the environment required for this example.
- Please update the image or choose a new one in case, you get an error saying "INTERNAL SERVER ERROR".
- Feel free to play around with the image you can use as the thumbnail at step 3.

***
## Get HeadFrame/Thumbnails

#### Summary:
> The Interplay Web Services method GetHeadframe returns a headframe (or "thumbnail") image for an asset.

###### Parameters
- The MOB ID of the asset.

###### Steps
1. Use the cached CTMS Registry information or fetch it as shown in Using the CTMS API.
2. Find the link [aa:asset-by-id](https://developer.avid.com/ctms/api/aa/linkrels/asset-by-id.html) for the  Avid Production Management. The "href" is an   URI template.
    1. Set the URI template variable "id" to the ID of the asset and expand the URI template.
    2. Add the query parameter "embed=thumb".
    3. Optional: add the query parameters "thumbnailWidth" and "thumbnailHeight" to request the image in a specific resolution. See below for details.
    4. Make an HTTP GET request to get the [aa:asset](https://developer.avid.com/ctms/api/aa/linkrels/asset.html) resource for the asset with an embedded [aa:thumb](https://developer.avid.com/ctms/api/aa/linkrels/thumb.html) resource. The property "thumbnail" has either the URL of the thumbnail image as value, or null to indicate that the asset has no thumbnail. Example:

    ```
    {
    "base": { ... },
    "common": { ... },
    "_embedded": {
        "[aa:thumb](https://developer.avid.com/ctms/api/aa/linkrels/thumb.html)": {
        "thumbnail": "https://...",
        "_links": {
        }
        }
    }
    }
    ```
3. If "thumbnail" is not null, call HTTP GET on the URL to get the image.

> CTMS returns the image for a  Avid Production Management asset by default as a JPEG image scaled to a configured default resolution. You can use the query parameters **"thumbnailWidth"** and **"thumbnailHeight"** to request the image in a specific size. CTMS will return an image of at most the given size but may also return a smaller image. 

#### How to use this collection:
This collection involves the process of following the above steps, as provided in the summary, in your postman application.
Open your postman, import the collection "HeadFrames or Thumbnails/CTMS Get Headframe.postman_collection.json", and follow the steps as given below.

###### Postman API Calls
(Hit Send on the "ROPC Login" API call to login in the system. View the project-level ReadMe to understand how it works.)

> **GET** 1_CTMS Registry information: avid.ctms.registry
- This GET call hits the service roots URL for CTMS registry, fetching the resources, systems and the links associated to the system.
- In the **Scripts** section: We check if the  Avid Production Management is avaialable with the registry. If yes, we fetch "[aa:asset-by-id](https://developer.avid.com/ctms/api/aa/linkrels/asset-by-id.html)" link present inside the "resources", and store the variable globally as selected_system_aaAssetByIdHref.

    <mark>🔶 At this step, you need to insert the appropriate **master clip ID** in the environment variable named: masterClipId</mark>

> **GET** 2_aa asset by id
- Hitting the above fetched selected_system_aaAssetByIdHref, to get the asset by id.
- In the **Scripts** section: From the response, we fetch the "[aa:thumb](https://developer.avid.com/ctms/api/aa/linkrels/thumb.html)", which is used to get the thumbnail information for the given asset, and store it globally as selected_system_thumbnailHref.

> **GET** 3 get a thumbnail
- Hitting this URL will load the thumbnail image for the  Avid Production Management asset.

#### Precautions/Recommendations:
- Please **select and put** the right asset/masterclip IDs in the environment required for this example.
